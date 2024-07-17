{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  name = "amplify-gen2";
  buildInputs = with pkgs; [
    zsh
    nodejs_18
  ];
  runScript = "zsh";

  shellHook = ''
        SHELL=$(which zsh)
    	exec $SHELL
  '';
}
