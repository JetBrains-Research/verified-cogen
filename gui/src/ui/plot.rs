use eframe::egui::Ui;
use egui_plot::{uniform_grid_spacer, Line, Plot};

use crate::{AppState, RunResults};

impl AppState {
    pub fn plot(&self, results: &RunResults, file_cnt: usize, ui: &mut Ui) {
        let tries: Vec<_> = results.values().copied().collect();
        let max_tries = *tries
            .iter()
            .max_by(|a, b| a.total_cmp(b))
            .expect("results should contain at least one file");
        let mut cnt = vec![0; max_tries.ceil() as usize + 1];
        for t in tries {
            cnt[t.ceil() as usize] += 1;
        }
        let percent = cnt
            .into_iter()
            .enumerate()
            .scan(0, |state, (i, x)| {
                *state += x;
                Some([i as f64, *state as f64 / file_cnt as f64 * 100.0])
            })
            .collect::<Vec<_>>();

        Plot::new("results_plot")
            .x_grid_spacer(uniform_grid_spacer(|_| [5.0, 1.0, 1.0]))
            // .view_aspect(1.0)
            .show(ui, |plot_ui| plot_ui.line(Line::new(percent)));
    }
}
