{
  inputs = {
    flakelight.url = "github:nix-community/flakelight";
  };
  outputs = { flakelight, ... }@inputs:
    flakelight ./. {
      inherit inputs;

      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      devShell = pkgs: {
        packages = pkgs: (with pkgs; [
          poetry
          dafny
        ]) ++ (pkgs.lib.optionals pkgs.stdenv.isDarwin (with pkgs.darwin.apple_sdk.frameworks; [
          AppKit
          pkgs.libiconv
        ]));
      };
      formatter = pkgs: pkgs.nixpkgs-fmt;
    };
}
