use eframe::egui::{self, Ui};

use crate::helpers::integer_edit_field;
use crate::{AppState, BenchMode, FileMode, LLMProfile};

impl AppState {
    pub(crate) fn settings_ui(&mut self, ui: &mut Ui) {
        ui.vertical(|ui| {
            self.verifier_details(ui);
            ui.separator();

            ui.heading("Settings:");

            egui::ComboBox::from_label("LLM Profile")
                .selected_text(format!("{}", self.settings.llm_profile))
                .show_ui(ui, |ui| {
                    for profile in LLMProfile::all() {
                        ui.selectable_value(
                            &mut self.settings.llm_profile,
                            profile,
                            format!("{}", profile),
                        );
                    }
                });

            ui.separator();

            if ui
                .checkbox(
                    &mut self.settings.incremental_run,
                    "Incremental run (experimental validating mode)",
                )
                .clicked()
                && self.settings.incremental_run
            {
                _ = self.code.take();
                self.settings.file_mode = FileMode::Directory;
            }
            ui.add_space(2.0);
            if !self.settings.incremental_run {
                ui.horizontal(|ui| {
                    ui.label("Bench mode:");
                    egui::ComboBox::from_id_source("bench-mode-select")
                        .selected_text(format!("{}", self.settings.bench_type.name()))
                        .show_ui(ui, |ui| {
                            for mode in BenchMode::all() {
                                ui.selectable_value(
                                    &mut self.settings.bench_type,
                                    *mode,
                                    mode.name(),
                                );
                            }
                        });
                });
            }

            ui.separator();
            ui.horizontal(|ui| {
                let max_rect = ui.max_rect();
                let is_dir_mode = matches!(self.settings.file_mode, FileMode::Directory);
                let div = match (self.settings.incremental_run, is_dir_mode) {
                    (true, _) => 1.5,
                    (false, true) => 5.0,
                    (false, false) => 3.0,
                };
                let size = [max_rect.width() / div, max_rect.height()];
                ui.label("Tries: ");
                integer_edit_field(ui, "Tries", &mut self.settings.tries, size);

                if !self.settings.incremental_run {
                    ui.label("Retries: ");
                    integer_edit_field(ui, "Retries", &mut self.settings.retries, size);
                }

                if !self.settings.incremental_run && is_dir_mode {
                    ui.label("Runs: ");
                    integer_edit_field(ui, "Retries", &mut self.settings.runs, size);
                }
            });
        });
    }
}
