use std::{
    collections::HashMap,
    path::Path,
    process::{Command, Output},
};

use crate::Settings;

pub fn basename(file: &str) -> &str {
    std::path::Path::new(file)
        .file_name()
        .expect("invalid file passed")
        .to_str()
        .expect("invalid file name")
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

fn add_common_arguments(cmd: &mut Command, token: &str, settings: &Settings) {
    cmd.envs(get_python_venv(Path::new(".")))
        .arg("src/main.py")
        .args(["--insert-invariants-mode", "llm-single-step"])
        .args(["--llm-profile", "gpt-4o"])
        .args(["--grazie-token", token])
        .args(["--bench-type", &settings.bench_type.to_string()])
        .args(["--tries", &make_tries(&settings.tries)])
        .args(["--retries", &make_retries(&settings.retries)]);
}

fn parse_output(output: Output) -> (String, String) {
    let stdout = String::from_utf8(output.stdout).expect("Failed to parse stdout");
    let stderr = String::from_utf8(output.stderr).expect("Failed to parse stderr");
    (stdout, stderr)
}

pub fn run_on_file(file: &str, token: &str, settings: &Settings) -> (String, String) {
    log::info!("Running on file: {}", file);

    let mut command = Command::new("python");
    add_common_arguments(&mut command, token, settings);

    let output = command
        .args(["-i", file])
        .output()
        .expect("Failed to run python to add information");

    parse_output(output)
}

pub fn run_on_directory(directory: &str, token: &str, settings: &Settings) -> (String, String) {
    log::info!("Running on directory: {}", directory);

    let mut command = Command::new("python");
    add_common_arguments(&mut command, token, settings);

    let output = command
        .args(["-d", directory])
        .output()
        .expect("Failed to run python to add information");

    parse_output(output)
}

fn get_python_venv(venv_base_directory: &Path) -> HashMap<String, String> {
    let mut env = HashMap::new();
    let activate_path = ["venv", ".venv"]
        .into_iter()
        .find_map(|virtual_environment_name| {
            let path = venv_base_directory.join(virtual_environment_name);
            path.exists().then_some(path)
        });

    if let Some(path) = activate_path {
        env.insert(
            "VIRTUAL_ENV".to_string(),
            path.to_string_lossy().to_string(),
        );

        if let Err(err) = add_environment_path(&mut env, &path.join("bin")) {
            log::error!(
                "Failed to add virtual environment bin directory to PATH: {}",
                err
            );
        }
    }
    env
}

fn add_environment_path(env: &mut HashMap<String, String>, new_path: &Path) -> anyhow::Result<()> {
    use anyhow::Context as _;

    let mut env_paths = vec![new_path.to_path_buf()];
    if let Some(path) = env.get("PATH").or(std::env::var("PATH").ok().as_ref()) {
        let mut paths = std::env::split_paths(&path).collect::<Vec<_>>();
        env_paths.append(&mut paths);
    }

    let paths = std::env::join_paths(env_paths).context("failed to create PATH env variable")?;
    env.insert("PATH".to_string(), paths.to_string_lossy().to_string());

    Ok(())
}
