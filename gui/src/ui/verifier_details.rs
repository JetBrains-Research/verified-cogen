use eframe::egui::{TextEdit, Ui};

use crate::AppState;

impl AppState {
    pub(crate) fn verifier_details(&mut self, ui: &mut Ui) {
        ui.label("Prompts directory: ");
        ui.horizontal(|ui| {
            ui.add(
                TextEdit::singleline(&mut self.settings.prompts_directory)
                    .hint_text("Enter the prompts directory"),
            );
            if ui.button("Select").clicked() {
                if let Some(dir) = rfd::FileDialog::new().pick_folder() {
                    self.settings.prompts_directory = dir.to_string_lossy().to_string();
                }
            }
        });

        ui.columns(2, |cols| {
            let [left_ui, right_ui] = cols else { return };

            left_ui.vertical(|ui| {
                ui.label("Verifier command: ");
                ui.add(
                    TextEdit::singleline(&mut self.settings.verifier_command)
                        .hint_text("Enter the verifier command"),
                );
            });

            right_ui.vertical(|ui| {
                ui.label("Timeout: ");
                let mut tmp_value = self.settings.timeout.clone();
                ui.add(TextEdit::singleline(&mut tmp_value).hint_text("Enter the timeout"));
                if tmp_value.parse::<u8>().is_ok() || tmp_value.is_empty() {
                    self.settings.timeout = tmp_value;
                }
            });
        });

        ui.label("Generate code: ");
        ui.columns(2, |cols| {
            let [left_ui, right_ui] = cols else { return };

            left_ui.add(
                TextEdit::singleline(&mut self.settings.generate_command)
                    .hint_text("Enter the command to generate code"),
            );

            right_ui.checkbox(&mut self.settings.use_poetry, "Use poetry");
        });
    }
}
