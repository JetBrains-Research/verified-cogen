use eframe::egui::{self, Separator, Ui};

use crate::{helpers::paint_code, AppState, FileMode};

impl AppState {
    pub(crate) fn output_ui(&mut self, ui: &mut Ui, panel_height: f32) {
        let output_width = ui.available_width();
        let mut part = match self.settings.file_mode {
            FileMode::SingleFile => 4.0,
            FileMode::Directory => 2.0,
        };

        ui.horizontal(|ui| {
            ui.set_height(panel_height);
            ui.add(Separator::default().vertical().grow(panel_height));

            ui.vertical(|ui| {
                if let Ok(run_results) = self.run_results.read() {
                    part += 1.0;
                    if let Some(results) = run_results.as_ref() {
                        let cnt = self.file_count.load(std::sync::atomic::Ordering::SeqCst);
                        ui.push_id("plot", |ui| {
                            ui.set_max_height(panel_height / part);
                            self.plot(results, cnt, ui);
                        });
                    }
                }

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
                            if let Ok(ext) = self.last_verified_extension.read() {
                                if let Some(code) = code.as_ref() {
                                    if let Some(ext) = ext.as_ref() {
                                        ui.separator();
                                        ui.heading("Last verified code:");
                                        ui.push_id("llm-code", |ui| {
                                            egui::ScrollArea::vertical().show(ui, |ui| {
                                                ui.set_min_width(output_width);
                                                paint_code(ui, code, ext);
                                            });
                                        });
                                    }
                                }
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
