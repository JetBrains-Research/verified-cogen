{
  inputs = {
    flakelight.url = "github:nix-community/flakelight";
  };
  outputs = { flakelight, ... }@inputs:
    flakelight ./. {
      inherit inputs;

      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      devShell.packages = pkgs: with pkgs; [
        poetry
        dafny
      ];
      formatter = pkgs: with pkgs; [ nixpkgs-fmt ];
    };
}
