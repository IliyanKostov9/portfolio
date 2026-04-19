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
    nixpkgs-terraform.url = "github:stackbuilders/nixpkgs-terraform";
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
        # NOTE: Unfree packages
        _module.args.pkgs = import inputs.nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        devenv.shells.default = {
          languages = {
            python = {
              enable = true;
              version = "3.14.3";
              uv = {
                enable = true;
                sync.enable = true;
              };
            };
            terraform = {
              enable = true;
              lsp.enable = true;
              version = "1.9.8";
            };
          };

          packages = with pkgs; [
            sops
            gettext # NOTE: Needed for django-admin compilemessages
            (texlive.combine
              {
                inherit (texlive) scheme-full;
              })
            zathura # NOTE: pdf viewer for Latex
          ];

          git-hooks.hooks = {
            # Common
            commitizen.enable = true;

            actionlint = {
              enable = false;
              excludes = ["docker-publish.yaml"];
            };

            # Python specific
            black.enable = true;
            flake8.enable = true;
            autoflake = {
              enable = true;
              description = "Used to remove unused imports & vars";
            };

            # NOTE: breakes ninja templates
            prettier.enable = false;
            latexindent.enable = true;
          };

          env = {
            PORTFOLIO_ENV = "dev";
            PORTFOLIO_HOST = "localhost";
            PORTFOLIO_SECRET_KEY = "django-insecure-8uyy0d7vvcll=*i_@b4_8tm$ehr58-+=7)82s3q$uhxok^$bim";
          };

          enterShell = ''
            export PYTHONPATH="$(pwd)/src"

            if ! [[ -d ".devenv/state/venv" ]]; then
              uv venv
              uv test --group test
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
