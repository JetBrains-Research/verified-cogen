use std::{
    path::Path,
    process::{Command, Output},
};

use eframe::egui::{self, TextEdit};

use crate::Settings;

pub fn basename(file: &str) -> &str {
    std::path::Path::new(file)
        .file_name()
        .expect("invalid file passed")
        .to_str()
        .expect("invalid file name")
}

pub fn extension(file: &Path) -> &str {
    file.extension()
        .expect("file should have an extension")
        .to_str()
        .expect("extension should be a valid string")
}

fn make_tries(tries: &str) -> String {
    if tries.is_empty() {
        String::from("1")
    } else {
        tries.to_string()
    }
}

fn make_retries(retries: &str) -> String {
    if retries.is_empty() {
        String::from("0")
    } else {
        retries.to_string()
    }
}

fn make_timeout(timeout: &str) -> String {
    if timeout.is_empty() {
        String::from("60")
    } else {
        timeout.to_string()
    }
}

fn make_runs(runs: &str) -> String {
    if runs.is_empty() {
        String::from("1")
    } else {
        runs.to_string()
    }
}

fn add_common_arguments<'a>(
    cmd: &'a mut Command,
    token: &str,
    settings: &Settings,
) -> &'a mut Command {
    cmd.args(["--verifier-command", &settings.verifier_command])
        .args(["--prompts-directory", &settings.prompts_directory])
        .args(["--insert-conditions-mode", "llm-single-step"])
        .args(["--llm-profile", settings.llm_profile.as_grazie()])
        .args(["--grazie-token", token])
        .args(["--bench-type", &settings.bench_type.to_string()])
        .args(["--tries", &make_tries(&settings.tries)])
        .args(["--retries", &make_retries(&settings.retries)])
        .args(["--verifier-timeout", &make_timeout(&settings.timeout)])
}

fn parse_output(output: Output) -> (String, String) {
    let stdout = String::from_utf8(output.stdout).expect("Failed to parse stdout");
    let stderr = String::from_utf8(output.stderr).expect("Failed to parse stderr");
    (stdout, stderr)
}

pub fn run_on_file(file: &str, settings: &Settings) -> (String, String) {
    log::info!("Running on file: {}", file);

    let output = add_common_arguments(
        &mut compose_command(settings),
        &settings.grazie_token,
        settings,
    )
    .args(["-i", file])
    .output()
    .expect("Failed to run python to add information");

    parse_output(output)
}

pub fn run_on_directory(directory: &str, settings: &Settings) -> (String, String) {
    log::info!("Running on directory: {}", directory);

    let output = add_common_arguments(
        &mut compose_command(settings),
        &settings.grazie_token,
        settings,
    )
    .args(["-d", directory])
    .args(["--runs", &make_runs(&settings.runs)])
    .output()
    .expect("Failed to run python to add information");

    parse_output(output)
}

fn compose_command(settings: &Settings) -> Command {
    if settings.use_poetry {
        let mut tmp = Command::new("poetry");
        tmp.args(["run", &settings.generate_command]);
        tmp
    } else {
        Command::new(&settings.generate_command)
    }
}

pub fn integer_edit_field(
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
