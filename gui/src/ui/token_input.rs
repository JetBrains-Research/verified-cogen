use eframe::egui::{TextEdit, Ui};

use crate::AppState;

impl AppState {
    pub(crate) fn token_input(&mut self, ui: &mut Ui) {
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
    }
}
