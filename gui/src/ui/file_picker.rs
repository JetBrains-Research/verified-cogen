use std::ffi::OsString;

use eframe::egui::Ui;

use crate::{AppState, FileMode};

impl AppState {
    pub(crate) fn file_picker(&mut self, ui: &mut Ui) {
        ui.label("File mode: ");
        if !self.settings.incremental_run
            && ui
                .radio_value(
                    &mut self.settings.file_mode,
                    FileMode::SingleFile,
                    "Single file",
                )
                .clicked()
        {
            self.settings.incremental_run = false;
            self.files = None;
        }
        if ui
            .radio_value(
                &mut self.settings.file_mode,
                FileMode::Directory,
                "Directory",
            )
            .clicked()
        {
            self.code = None;
        }

        if ui.button("Open").clicked() {
            match self.settings.file_mode {
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
                        let do_filter = self.settings.do_filter;
                        let filter_by_ext: OsString = self.settings.filter_by_ext.clone().into();
                        self.files = {
                            let mut files: Vec<_> = std::fs::read_dir(&dir)
                                .expect("Failed to read directory content")
                                .filter_map(|entry| {
                                    let path =
                                        entry.expect("Failed to read directory entry").path();
                                    if do_filter
                                        && path.extension().map_or(true, |ext| ext != filter_by_ext)
                                    {
                                        return None;
                                    }
                                    let s = path.to_string_lossy().to_string();
                                    let is_hidden = path
                                        .file_name()
                                        .map(|name| name.to_string_lossy().starts_with('.'))
                                        .unwrap_or(true);
                                    (!is_hidden).then_some(s)
                                })
                                .collect();
                            files.sort();
                            Some(files)
                        };
                        self.path = Some(dir);
                    }
                }
            }
        }
    }
}
