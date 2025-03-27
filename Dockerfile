FROM nixos/nix

RUN nix-channel --add https://nixos.org/channels/nixpkgs-unstable nixpkgs && \
    nix-channel --update

RUN nix-env -iA nixpkgs.python3 nixpkgs.poetry
RUN nix-env -iA nixpkgs.dafny nixpkgs.gawk nixpkgs.ps nixpkgs.findutils

ENTRYPOINT [ "/bin/sh" ]
