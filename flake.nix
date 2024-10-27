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
          languages.python.uv.enable = true;
          languages.python.uv.sync.enable = true;

          packages = with pkgs; [
            zsh
          ];

          enterShell = ''
            export PYTHONPATH="$(pwd):$(pwd)/src/apps:$(pwd)"

            if ! [[ -d ".venv" ]]; then
              uv venv
              source .devenv/state/venv/bin/activate
              uv pip sync
            elif [[ -d "pyproject.toml" ]]; then
              source .devenv/state/venv/bin/activate
              uv pip sync
            else
              source .devenv/state/venv/bin/activate
            fi
          '';
        };
      };
    };
}
