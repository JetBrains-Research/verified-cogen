#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod helpers;
mod ui;

use eframe::egui::{self};
use std::{
    collections::HashMap,
    fmt::Display,
    fs::File,
    path::PathBuf,
    sync::{
        atomic::{AtomicBool, AtomicUsize},
        Arc, RwLock,
    },
};

use once_cell::sync::Lazy;
use serde::{Deserialize, Serialize};

use helpers::basename;

static APP_DIRS: Lazy<directories::ProjectDirs> = Lazy::new(|| {
    directories::ProjectDirs::from("", "", "verified-cogen").expect("Failed to get app directories")
});

fn should_restore() -> bool {
    std::env::var("NORESTORE").is_err()
}

fn main() -> eframe::Result {
    env_logger::init();
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([800.0, 720.0]),
        ..Default::default()
    };

    let log_dir = APP_DIRS.cache_dir().join("log");
    eprintln!("{log_dir:?}");

    if !log_dir.exists() {
        std::fs::create_dir_all(&log_dir).expect("Failed to create log directory");
    }
    _ = File::create(log_dir.join("llm.log")).expect("Failed to create log file");

    eframe::run_native(
        "Verified codegen",
        options,
        Box::new(|cc| {
            let settings = should_restore()
                .then(|| {
                    cc.storage.and_then(|storage| {
                        let settings = storage.get_string("settings_json")?;
                        serde_json::from_str(&settings).ok()
                    })
                })
                .flatten()
                .unwrap_or_default();
            let state = AppState {
                settings,
                ..Default::default()
            };
            Ok(Box::new(state))
        }),
    )
}

#[derive(Debug, Clone, PartialEq, Default, Serialize, Deserialize)]
enum FileMode {
    #[default]
    SingleFile,
    Directory,
}

#[derive(Debug, Clone, PartialEq, Default, Serialize, Deserialize)]
enum BenchMode {
    #[default]
    Invariants,
    Generic,
    Generate,
    Validating,
}

impl BenchMode {
    fn llm_generated_path(&self, path: &str) -> PathBuf {
        let name = match self {
            BenchMode::Invariants | BenchMode::Generic | BenchMode::Validating => {
                basename(path).to_string()
            }
            BenchMode::Generate => {
                let base = basename(path);
                base.chars()
                    .take(base.len() - 7)
                    .chain(".dfy".chars())
                    .collect::<String>()
            }
        };
        APP_DIRS.cache_dir().join("llm-generated").join(name)
    }
}

impl Display for BenchMode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            BenchMode::Invariants => write!(f, "invariants"),
            BenchMode::Generic => write!(f, "generic"),
            BenchMode::Generate => write!(f, "generate"),
            BenchMode::Validating => write!(f, "validating"),
        }
    }
}

type IncrementalRunResults = HashMap<String, usize>;

#[derive(Default)]
struct AppState {
    settings: Settings,
    path: Option<PathBuf>,
    code: Option<String>,
    files: Option<Vec<String>>,
    token_hovered: bool,
    running: Arc<AtomicBool>,
    last_verified_code: Arc<RwLock<Option<String>>>,
    last_verified_extension: Arc<RwLock<Option<String>>>,
    incremental_run_results: Arc<RwLock<Option<IncrementalRunResults>>>,
    incremental_file_count: Arc<AtomicUsize>,
    output: Arc<RwLock<Option<(String, String)>>>,
    log: Arc<RwLock<Option<String>>>,
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
enum LLMProfile {
    GPT4o,
    GPT4Turbo,
    Claude3Opus,
    Claude35Sonnet,
}

impl LLMProfile {
    fn as_grazie(&self) -> &str {
        match self {
            LLMProfile::GPT4o => "gpt-4o",
            LLMProfile::GPT4Turbo => "gpt-4-1106-preview",
            LLMProfile::Claude3Opus => "anthropic-claude-3-opus",
            LLMProfile::Claude35Sonnet => "anthropic-claude-3.5-sonnet",
        }
    }

    fn all() -> Vec<LLMProfile> {
        vec![
            LLMProfile::GPT4o,
            LLMProfile::GPT4Turbo,
            LLMProfile::Claude3Opus,
            LLMProfile::Claude35Sonnet,
        ]
    }
}

impl Display for LLMProfile {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LLMProfile::GPT4o => write!(f, "GPT-4o"),
            LLMProfile::GPT4Turbo => write!(f, "GPT-4 Turbo"),
            LLMProfile::Claude3Opus => write!(f, "Claude 3 Opus"),
            LLMProfile::Claude35Sonnet => write!(f, "Claude 3.5 Sonnet"),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Settings {
    grazie_token: String,
    llm_profile: LLMProfile,
    verifier_command: String,
    generate_command: String,
    use_poetry: bool,
    prompts_directory: String,
    tries: String,
    retries: String,
    bench_type: BenchMode,
    file_mode: FileMode,
    runs: String,
    timeout: String,
    do_filter: bool,
    filter_by_ext: String,
    incremental_run: bool,
}

impl Default for Settings {
    fn default() -> Self {
        Self {
            grazie_token: std::env::var("GRAZIE_JWT_TOKEN").unwrap_or_default(),
            llm_profile: LLMProfile::GPT4o,
            verifier_command: std::env::var("VERIFIER_COMMAND").unwrap_or_default(),
            generate_command: String::from("verified-cogen"),
            use_poetry: std::env::var("USE_POETRY").unwrap_or_default() == "1",
            prompts_directory: std::env::var("PROMPTS_DIRECTORY").unwrap_or_default(),
            tries: String::from("1"),
            retries: String::from("0"),
            bench_type: BenchMode::Invariants,
            file_mode: FileMode::SingleFile,
            runs: String::from("1"),
            timeout: String::from("60"),
            incremental_run: false,
            do_filter: false,
            filter_by_ext: String::new(),
        }
    }
}

impl eframe::App for AppState {
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

    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        let settings = serde_json::to_string(&self.settings).expect("Failed to serialize settings");
        storage.set_string("settings_json", settings);
    }
}
