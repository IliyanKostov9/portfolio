{
  description = "Portfolio app";
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

  outputs = inputs @ {
    nixpkgs,
    flake-parts,
    devenv,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      imports = [
        inputs.devenv.flakeModule
      ];
      systems = nixpkgs.lib.systems.flakeExposed;

      perSystem = {
        config,
        self',
        inputs',
        pkgs,
        system,
        ...
      }: {
        devenv.shells.default = {
          languages.python = {
            enable = true;
            version = "3.11.9";
            uv = {
              enable = true;
              sync.enable = true;
            };
          };

          packages = with pkgs; [
            zsh
          ];

          git-hooks.hooks = {
            # Common
            commitizen.enable = true;

            actionlint = {
              enable = false;
              excludes = ["docker-publish.yaml"];
            };
            checkmake.enable = true;

            # Python specific
            black.enable = true;
            flake8.enable = true;
            autoflake = {
              enable = true;
              description = "Used to remove unused imports & vars";
            };

            # NOTE: breakes ninja templates
            prettier.enable = false;
          };

          env = {
            ENV = "dev";
            HOST = "localhost";
            SECRET_KEY = "django-insecure-8uyy0d7vvcll=*i_@b4_8tm$ehr58-+=7)82s3q$uhxok^$bim";
          };

          enterShell = ''
            export PYTHONPATH="$(pwd):$(pwd)/src/apps:$(pwd)"

            if ! [[ -d ".devenv/state/venv" ]]; then
              uv venv
              source .devenv/state/venv/bin/activate
            elif [[ -d "pyproject.toml" ]]; then
              source .devenv/state/venv/bin/activate
            else
              source .devenv/state/venv/bin/activate
            fi
          '';
        };
      };
    };
}
