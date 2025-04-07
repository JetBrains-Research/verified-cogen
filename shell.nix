{
  system ? builtins.currentSystem,
  pkgs ? import <nixpkgs> { inherit system; },
}:
pkgs.mkShell {
  packages = [
    pkgs.poetry
    pkgs.dafny

    pkgs.rustc
    pkgs.cargo
    pkgs.clippy
    pkgs.rust-analyzer
    pkgs.rustfmt
  ];

  shellHook = ''
    poetry sync
    source .venv/bin/activate
  '';
}
