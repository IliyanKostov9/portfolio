{
  description = "Dev shell for portfolio";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.systems.follows = "nixpkgs";
    };
    devenv.url = "github:cachix/devenv";
    nixpkgs-python = {
      url = "github:cachix/nixpkgs-python";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ nixpkgs, flake-parts, devenv, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {

      imports = [
        inputs.devenv.flakeModule
      ];
      systems = nixpkgs.lib.systems.flakeExposed;

      perSystem = { config, self', inputs', pkgs, system, ... }: {

        devenv.shells.default = {
          languages.python.enable = true;
          languages.python.version = "3.11.9";

          packages = with pkgs; [
            pdm
          ];

          enterShell = ''
            export PYTHONPATH="$(pwd):$(pwd)/src/apps"

            if ! [[ -d ".venv" ]]; then
              pdm venv create --with venv
              pdm install
            elif [[ -d "pyproject.toml" ]]; then
              pdm init
            else
              pdm venv activate
            fi
          '';
        };
      };
    };
}
