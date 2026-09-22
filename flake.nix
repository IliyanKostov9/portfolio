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

        devenv.shells.dev = {
          cachix = {
            pull = ["iliyankostov9-portfolio-dev"];
            push = "iliyankostov9-portfolio-dev";
          };

          languages.python = {
            enable = true;
            version = "3.14.3";
            venv.enable = true;
            uv = {
              enable = true;
              sync = {
                enable = true;
                groups = ["dev" "test"];
              };
            };
          };

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
          };

          enterShell = ''
            export PYTHONPATH="$(pwd)/src"
          '';

          enterTest = ''
            set -e
            python3 -Wa ./src/manage.py test portfolio.tests apps.resume.tests apps.blogs.tests -v 3
            echo "Now checking migrations..."
            python3 src/manage.py check --deploy
            python3 src/manage.py lintmigrations
          '';
        };

        devenv.shells.infra = {
          cachix = {
            pull = ["iliyankostov9-portfolio-infra"];
            push = "iliyankostov9-portfolio-infra";
          };

          languages.terraform = {
            enable = true;
            lsp.enable = true;
            version = "1.9.8";
          };
        };

        devenv.shells.latex = {
          packages = with pkgs; [
            age
            gettext # NOTE: Needed for django-admin compilemessages
            (texlive.combine
              {
                inherit (texlive) scheme-full;
              })
            zathura # NOTE: pdf viewer for Latex
          ];

          git-hooks.hooks.latexindent.enable = true;
        };
      };
    };
}
