use eframe::egui::{self, Ui};

use crate::{
    helpers::{basename, extension, paint_code},
    AppState, FileMode,
};

impl AppState {
    pub(crate) fn display(&mut self, ui: &mut Ui) {
        if self.settings.file_mode == FileMode::SingleFile {
            if let Some(code) = self.code.as_ref() {
                let path = self.path.as_ref().expect("Code and path should be in sync");
                egui::ScrollArea::vertical().show(ui, |ui| {
                    paint_code(ui, code, extension(path));
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

                        if !self.settings.incremental_run && ui.button("Open").clicked() {
                            self.code = Some(
                                std::fs::read_to_string(file).expect("Failed to read file content"),
                            );
                            self.path = Some(file.into());
                            self.settings.file_mode = FileMode::SingleFile;
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
}
