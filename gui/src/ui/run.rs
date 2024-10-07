use std::{collections::HashMap, fs::File, io::Read, path::PathBuf, sync::Arc};

use eframe::egui::{TextEdit, Ui};

use crate::{
    helpers::{basename, extension, run_on_directory, run_on_file},
    AppState, FileMode, APP_DIRS,
};

impl AppState {
    pub(crate) fn runner(&mut self, ui: &mut Ui) {
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
        if matches!(self.settings.file_mode, FileMode::Directory) {
            ui.horizontal(|ui| {
                ui.checkbox(&mut self.settings.do_filter, "Filter by extension");
                ui.add_space(5.0);
                ui.add(
                    TextEdit::singleline(&mut self.settings.filter_by_ext)
                        .hint_text("enter the extension here")
                        .interactive(self.settings.do_filter),
                );
            });
        }
    }

    pub(crate) fn run(&mut self) {
        let running = Arc::clone(&self.running);
        let output = Arc::clone(&self.output);
        let last_verified_code = Arc::clone(&self.last_verified_code);
        let last_verified_ext = Arc::clone(&self.last_verified_extension);
        let incremental_run = self.settings.incremental_run;
        let file_count = Arc::clone(&self.file_count);
        let cnt = self.files.as_ref().map(|f| f.len());
        let run_results = Arc::clone(&self.run_results);

        let settings = self.settings.clone();
        let file_mode = self.settings.file_mode.clone();
        let path = self.path.clone();
        let log = Arc::clone(&self.log);

        _ = std::thread::spawn(move || {
            let _path = path.clone();
            let result = std::panic::catch_unwind(|| {
                running.store(true, std::sync::atomic::Ordering::SeqCst);
                if let Ok(mut output) = output.write() {
                    *output = None;
                }
                if let Ok(mut results) = run_results.write() {
                    *results = None;
                }
                let log_dir = APP_DIRS.cache_dir().join("log");
                _ = File::create(log_dir.join("llm.log")).expect("Failed to clean log file");
                match file_mode {
                    FileMode::SingleFile => {
                        if let Some(path) = _path {
                            let extension = extension(&path);
                            if let Some(path) = path.to_str() {
                                let py_output = run_on_file(path, &settings);
                                if let Ok(mut output) = output.write() {
                                    *output = Some(py_output);
                                }

                                let llm_generated_path =
                                    settings.bench_type.llm_generated_path(path);
                                let llm_code = std::fs::read_to_string(llm_generated_path).ok();
                                if let Ok(mut last_verified_code) = last_verified_code.write() {
                                    *last_verified_code = llm_code;
                                }

                                if let Ok(mut last_verified_extension) = last_verified_ext.write() {
                                    *last_verified_extension = Some(String::from(extension));
                                }
                            }
                        }
                    }
                    FileMode::Directory => {
                        if let Ok(mut last_verified_code) = last_verified_code.write() {
                            *last_verified_code = None;
                        }

                        if let Ok(mut last_verified_extension) = last_verified_ext.write() {
                            *last_verified_extension = None;
                        }

                        if let Some(directory) = _path {
                            if let Some(directory) = directory.to_str() {
                                let py_output = run_on_directory(directory, &settings);
                                if let Ok(mut output) = output.write() {
                                    *output = Some(py_output);
                                }

                                let mut results_contents = String::new();
                                let name = basename(directory);

                                let results_path = match incremental_run {
                                    true => {
                                        PathBuf::from("results").join(format!("tries_{name}.json"))
                                    }
                                    false => APP_DIRS.cache_dir().join("total_cnt.json"),
                                };

                                File::open(results_path)
                                    .expect("results are not where they should be")
                                    .read_to_string(&mut results_contents)
                                    .expect("failed read");

                                if let Ok(mut results) = run_results.write() {
                                    *results = Some({
                                        let result: HashMap<String, f64> =
                                            serde_json::from_str(&results_contents)
                                                .expect("results must contain a valid json");

                                        result.into_iter().filter(|(_, v)| *v != -1.0).collect()
                                    });
                                    file_count.store(
                                        cnt.expect("should be dir"),
                                        std::sync::atomic::Ordering::SeqCst,
                                    );
                                }
                            }
                        }
                    }
                }
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
            if let Err(err) = result {
                if let Ok(mut output) = output.write() {
                    *output = Some((String::from("Error"), format!("{:?}", err)));
                }
            }
            running.store(false, std::sync::atomic::Ordering::SeqCst);
        });

        let running = Arc::clone(&self.running);
        let log = Arc::clone(&self.log);
        _ = std::thread::spawn(move || {
            let log_file = APP_DIRS.cache_dir().join("log").join("llm.log");
            while running.load(std::sync::atomic::Ordering::SeqCst) {
                let log_output = std::fs::read_to_string(&log_file).unwrap_or_default();
                if let Ok(mut log) = log.write() {
                    *log = Some(log_output);
                }
                std::thread::sleep(std::time::Duration::from_millis(100));
            }
        });
    }
}
