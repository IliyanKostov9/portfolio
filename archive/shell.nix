{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  packages = with pkgs; [
    python311
    pdm
    zsh
  ];

  runScript = "zsh";
  shellHook = ''
    export PYTHONPATH="$(pwd):$(pwd)/src/apps"
    source .venv/bin/activate
  '';
}
