{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  buildInputs = [
    (pkgs.buildFHSUserEnv {
      name = "pipzone";
      targetPkgs = pkgs: (with pkgs; [
        python311
        pdm
        zsh
      ]);
      runScript = "zsh";
      initHook = ''
        echo "Setting up environment..."
      '';
    })
  ];
}
