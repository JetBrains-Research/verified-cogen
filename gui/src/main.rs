#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod helpers;

use eframe::egui::{self, Separator, TextEdit, Ui};
use std::{
    fmt::Display,
    fs::File,
    path::PathBuf,
    sync::{atomic::AtomicBool, Arc, RwLock},
};

use helpers::{basename, run_on_directory, run_on_file};

fn main() -> eframe::Result {
    env_logger::init();
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([800.0, 720.0]),
        ..Default::default()
    };

    _ = File::create("log/llm.log").expect("Failed to create log file");

    eframe::run_native(
        "Verified codegen",
        options,
        Box::new(|_cc| Ok(Box::<App>::default())),
    )
}

#[derive(Debug, Clone, PartialEq, Default)]
enum FileMode {
    #[default]
    SingleFile,
    Directory,
}

#[derive(Debug, Clone, PartialEq, Default)]
enum BenchMode {
    #[default]
    Invariants,
    Preconditions,
}

impl Display for BenchMode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            BenchMode::Invariants => write!(f, "invariants"),
            BenchMode::Preconditions => write!(f, "preconditions"),
        }
    }
}

#[derive(Default)]
struct App {
    settings: Settings,
    file_mode: FileMode,
    path: Option<PathBuf>,
    code: Option<String>,
    files: Option<Vec<String>>,
    token_hovered: bool,
    running: Arc<AtomicBool>,
    last_verified_code: Arc<RwLock<Option<String>>>,
    output: Arc<RwLock<Option<(String, String)>>>,
    log: Arc<RwLock<Option<String>>>,
}

#[derive(Debug, Clone)]
struct Settings {
    grazie_token: String,
    verifier_command: String,
    prompts_directory: String,
    tries: String,
    retries: String,
    bench_type: BenchMode,
}

impl Default for Settings {
    fn default() -> Self {
        Self {
            grazie_token: std::env::var("GRAZIE_JWT_TOKEN").unwrap_or_default(),
            verifier_command: std::env::var("VERIFIER_COMMAND").unwrap_or_default(),
            prompts_directory: "llm/prompts".to_string(),
            tries: "1".to_string(),
            retries: "0".to_string(),
            bench_type: BenchMode::Invariants,
        }
    }
}

impl eframe::App for App {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            let panel_height = ui.max_rect().height();

            ui.columns(2, |columns| {
                let [left_ui, right_ui] = columns else {
                    return;
                };
                left_ui.vertical(|ui| {
                    self.token_input(ui);

                    ui.separator();
                    self.settings_ui(ui);

                    ui.separator();
                    self.runner(ui);

                    ui.separator();
                    self.display(ui);
                });

                self.output_ui(right_ui, panel_height);
            });
        });
    }
}

impl App {
    fn run(&mut self) {
        let running = Arc::clone(&self.running);
        let output = Arc::clone(&self.output);
        let last_verified_code = Arc::clone(&self.last_verified_code);

        let settings = self.settings.clone();
        let file_mode = self.file_mode.clone();
        let path = self.path.clone();
        let log = Arc::clone(&self.log);

        _ = std::thread::spawn(move || {
            running.store(true, std::sync::atomic::Ordering::SeqCst);
            if let Ok(mut output) = output.write() {
                *output = None;
            }
            File::create("log/llm.log").expect("Failed to clean log file");
            match file_mode {
                FileMode::SingleFile => {
                    if let Some(path) = path {
                        if let Some(path) = path.to_str() {
                            let py_output = run_on_file(path, &settings);
                            if let Ok(mut output) = output.write() {
                                *output = Some(py_output);
                            }

                            let llm_code = std::fs::read_to_string(format!(
                                "llm-generated/{}",
                                basename(path),
                            ))
                            .ok();
                            if let Ok(mut last_verified_code) = last_verified_code.write() {
                                *last_verified_code = llm_code;
                            }
                        }
                    }
                }
                FileMode::Directory => {
                    if let Some(directory) = path {
                        if let Some(directory) = directory.to_str() {
                            let py_output = run_on_directory(directory, &settings);
                            if let Ok(mut output) = output.write() {
                                *output = Some(py_output);
                            }

                            if let Ok(mut last_verified_code) = last_verified_code.write() {
                                *last_verified_code = None;
                            }
                        }
                    }
                }
            }
            running.store(false, std::sync::atomic::Ordering::SeqCst);
            if let Ok(mut log) = log.write() {
                if let Ok(mut output) = output.write() {
                    if let Some((_, stderr)) = output.as_mut() {
                        if let Some(log) = log.as_ref() {
                            *stderr += &format!("\nLog:\n{}", log)
                        }
                    }
                }
                *log = None;
            }
        });

        let running = Arc::clone(&self.running);
        let log = Arc::clone(&self.log);
        _ = std::thread::spawn(move || {
            while running.load(std::sync::atomic::Ordering::SeqCst) {
                let log_output = std::fs::read_to_string("log/llm.log").unwrap_or_default();
                if let Ok(mut log) = log.write() {
                    *log = Some(log_output);
                }
                std::thread::sleep(std::time::Duration::from_millis(100));
            }
        });
    }

    fn file_picker(&mut self, ui: &mut Ui) {
        ui.label("File mode: ");
        if ui
            .radio_value(&mut self.file_mode, FileMode::SingleFile, "Single file")
            .clicked()
        {
            self.files = None;
        }
        if ui
            .radio_value(&mut self.file_mode, FileMode::Directory, "Directory")
            .clicked()
        {
            self.code = None;
        }

        if ui.button("Open").clicked() {
            match self.file_mode {
                FileMode::SingleFile => {
                    if let Some(file) = rfd::FileDialog::new().pick_file() {
                        self.code = Some(
                            std::fs::read_to_string(&file).expect("Failed to read file content"),
                        );
                        self.path = Some(file);
                    }
                }
                FileMode::Directory => {
                    if let Some(dir) = rfd::FileDialog::new().pick_folder() {
                        self.files = Some(
                            std::fs::read_dir(&dir)
                                .expect("Failed to read directory content")
                                .map(|entry| {
                                    entry
                                        .expect("Failed to read directory entry")
                                        .path()
                                        .to_string_lossy()
                                        .to_string()
                                })
                                .collect(),
                        );
                        self.path = Some(dir);
                    }
                }
            }
        }
    }

    fn token_input(&mut self, ui: &mut Ui) {
        let label = ui.heading("Grazie and verifier: ");

        ui.label("Grazie token: ");
        ui.horizontal(|ui| {
            let token = ui
                .add(
                    TextEdit::singleline(&mut self.settings.grazie_token)
                        .hint_text("Enter your Grazie token")
                        .password(!self.token_hovered),
                )
                .labelled_by(label.id);
            self.token_hovered = token.hovered();
        });

        ui.columns(2, |cols| {
            let [left_ui, right_ui] = cols else { return };

            left_ui.vertical(|ui| {
                ui.label("Prompts directory: ");
                ui.add(
                    TextEdit::singleline(&mut self.settings.prompts_directory)
                        .hint_text("Enter the prompts directory")
                );
            });

            right_ui.vertical(|ui| {
                ui.label("Verifier command: ");
                ui.add(
                    TextEdit::singleline(&mut self.settings.verifier_command)
                        .hint_text("Enter the verifier command")
                );
            });
        });
    }

    fn runner(&mut self, ui: &mut Ui) {
        ui.horizontal(|ui| {
            self.file_picker(ui);

            let is_running = self.running.load(std::sync::atomic::Ordering::SeqCst);

            if ui.button("Run").clicked() && !is_running {
                self.run();
            }

            if is_running {
                ui.spinner();
            }
        });
    }

    fn settings_ui(&mut self, ui: &mut Ui) {
        fn integer_edit_field(
            ui: &mut egui::Ui,
            hint: &str,
            value: &mut String,
            size: [f32; 2],
        ) -> egui::Response {
            let mut tmp_value = value.clone();
            let res = ui.add_sized(size, TextEdit::singleline(&mut tmp_value).hint_text(hint));
            if tmp_value.parse::<u8>().is_ok() || tmp_value.is_empty() {
                *value = tmp_value;
            }
            res
        }

        ui.vertical(|ui| {
            ui.heading("Settings:");
            ui.horizontal(|ui| {
                ui.label("Bench mode: ");
                ui.radio_value(
                    &mut self.settings.bench_type,
                    BenchMode::Invariants,
                    "Invariants",
                );
                ui.radio_value(
                    &mut self.settings.bench_type,
                    BenchMode::Preconditions,
                    "Preconditions",
                );
            });
            ui.horizontal(|ui| {
                let max_rect = ui.max_rect();
                let size = [max_rect.width() / 3.0, max_rect.height()];
                ui.label("Tries: ");
                integer_edit_field(ui, "Tries", &mut self.settings.tries, size);

                ui.label("Retries: ");
                integer_edit_field(ui, "Retries", &mut self.settings.retries, size);
            });
        });
    }

    fn display(&mut self, ui: &mut Ui) {
        if self.file_mode == FileMode::SingleFile {
            if let Some(code) = self.code.as_ref() {
                egui::ScrollArea::vertical().show(ui, |ui| {
                    paint_code(ui, code);
                });
            } else {
                ui.label("No file selected");
            }
        } else if let Some(files) = self.files.as_mut() {
            let mut reset = false;

            egui::ScrollArea::vertical().show(ui, |ui| {
                ui.heading("Files");
                ui.separator();

                for file in files.iter() {
                    ui.horizontal(|ui| {
                        ui.label(basename(file));

                        if ui.button("Open").clicked() {
                            self.code = Some(
                                std::fs::read_to_string(file).expect("Failed to read file content"),
                            );
                            self.path = Some(file.into());
                            self.file_mode = FileMode::SingleFile;
                            reset = true;
                        }
                    });
                }
            });

            if reset {
                self.files = None;
            }
        } else {
            ui.label("No directory selected");
        }
    }

    fn output_ui(&mut self, ui: &mut Ui, panel_height: f32) {
        let output_width = ui.available_width();
        let part = match self.file_mode {
            FileMode::SingleFile => 4.0,
            FileMode::Directory => 2.0,
        };
        ui.horizontal(|ui| {
            ui.set_height(panel_height);
            ui.add(Separator::default().vertical().grow(panel_height));

            ui.vertical(|ui| {
                if let Ok(output) = self.output.read() {
                    if let Some(output) = output.as_ref() {
                        let (stdout, stderr) = &output;
                        ui.heading("Stdout:");
                        ui.push_id("stdout", |ui| {
                            ui.set_max_height(panel_height / part);
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                ui.set_min_width(output_width);
                                ui.monospace(stdout);
                            });
                        });

                        ui.separator();

                        ui.heading("Stderr:");
                        ui.push_id("stderr", |ui| {
                            ui.set_max_height(panel_height / part);
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                ui.set_min_width(output_width);
                                ui.monospace(stderr);
                            });
                        });

                        if let Ok(code) = self.last_verified_code.read() {
                            if let Some(code) = code.as_ref() {
                                ui.separator();
                                ui.heading("Last verified code:");
                                ui.push_id("llm-code", |ui| {
                                    egui::ScrollArea::vertical().show(ui, |ui| {
                                        ui.set_min_width(output_width);
                                        paint_code(ui, code);
                                    });
                                });
                            }
                        }
                    }
                }

                if let Ok(log) = self.log.read() {
                    if let Some(log) = log.as_ref() {
                        ui.heading("Log:");
                        ui.push_id("log", |ui| {
                            egui::ScrollArea::vertical().show(ui, |ui| {
                                ui.monospace(log);
                            });
                        });
                    }
                }
            });
        });
    }
}

fn paint_code(ui: &mut Ui, code: &str) {
    let theme = egui_extras::syntax_highlighting::CodeTheme::from_memory(ui.ctx());

    egui_extras::syntax_highlighting::code_view_ui(ui, &theme, code, "rs");
}
