# flake for building the latex document
# thx to
# https://flyx.org/nix-flakes-latex/
{
  description = "NT Project Homework Fitting";
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-21.05;
    flake-utils.url = github:numtide/flake-utils;
  };
  outputs = { self, nixpkgs, flake-utils }:
    with flake-utils.lib; eachSystem allSystems (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      tex = pkgs.texlive.combine {
          inherit (pkgs.texlive) scheme-full latex-bin latexmk;
      };
    in rec {
      packages = {
        document = pkgs.stdenvNoCC.mkDerivation rec {
          name = "latex-doc-ntproj-hw2-fitting";
          src = self;
          buildInputs = [
            pkgs.coreutils
            tex
          ];
          phases = ["unpackPhase" "buildPhase" "installPhase"];
          buildPhase = ''
            export PATH="${pkgs.lib.makeBinPath buildInputs}";
            mkdir -p .cache/texmf-var
	    cp preamble.tex .cache/texmf-var/preamble.tex
	    cp colors.tex .cache/texmf-var/
	    cp sources.bib .cache/texmf-var/
	    cp software.bib .cache/texmf-var/
            env TEXMFHOME=.cache TEXMFVAR=.cache/texmf-var \
              latexmk -interaction=nonstopmode -pdf -lualatex \
              2-fitting.tex
          '';
          installPhase = ''
            mkdir -p $out
            cp 2-fitting.pdf $out/
          '';
        };
      };
      defaultPackage = packages.document;
    });
}
