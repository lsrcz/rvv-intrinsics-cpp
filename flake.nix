{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    let
      package = { stdenv, gtest, cmake, ninja, python311, llvmPackages_17 }:
        llvmPackages_17.stdenv.mkDerivation {
          pname = "rvv-intrinsic-cpp";
          version = "0.1.0";
          src = ./.;

          nativeBuildInputs = [
            cmake
            ninja
            (python311.withPackages (ps: with ps; [ pytest ]))
          ];
          buildInputs = [
            gtest
          ];
        };
    in
    flake-utils.lib.eachSystem [
      flake-utils.lib.system.x86_64-linux
      flake-utils.lib.system.riscv64-linux
    ]
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
          cross = pkgs.pkgsCross.riscv64;
          isCross = system != flake-utils.lib.system.riscv64-linux;
          riscv_pkgs = if isCross then cross else pkgs;
          riscv_llvm =
            if isCross
            then cross.buildPackages.llvmPackages_17
            else pkgs.llvmPackages_17;
        in
        {
          formatter = pkgs.nixpkgs-fmt;
          devShell = pkgs.mkShell rec {
            buildInputs = [
              riscv_llvm.clang
              riscv_llvm.bintools
              riscv_pkgs.gtest
              pkgs.clang-tools_17
              pkgs.cpplint
              pkgs.cmake
              pkgs.ninja
              pkgs.cmake-format
              (pkgs.python311.withPackages (ps: with ps; [ pytest ]))
            ];
          };
          packages.default = riscv_pkgs.callPackage package { };
        }
      );
}
