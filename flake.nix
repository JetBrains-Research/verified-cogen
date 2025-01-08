{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flakelight = {
      url = "github:nix-community/flakelight";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs =
    { flakelight, ... }@inputs:
    flakelight ./. {
      inherit inputs;
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      devShell.packages = pkgs: [
        pkgs.poetry
        (pkgs.dafny.override {
          z3 = pkgs.z3.override {
            stdenv = pkgs.llvmPackages_16.stdenv;
          };
        })
      ];
      formatter = pkgs: pkgs.nixfmt-rfc-style;
    };
}
