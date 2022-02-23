{
  description = "gh-hosts";

  inputs = {
    # nixpkgs.url = "https://mirrors.tuna.tsinghua.edu.cn/nix-channels/nixpkgs-unstable/nixexprs.tar.xz";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      rec {
        packages = {
          my-pyenv = pkgs.python3.withPackages (
            ps: with ps; [
              (callPackage ./ping.nix { })
              aiohttp
            ]
          );
        };
        defaultPackage = packages.my-pyenv;

        devShell = packages.my-pyenv.env;

      }

    );

}
