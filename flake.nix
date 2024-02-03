{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachSystem [
      flake-utils.lib.system.x86_64-linux
      flake-utils.lib.system.riscv64-linux
    ]
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
          cross = import nixpkgs {
            inherit system;
            crossSystem = { config = flake-utils.lib.system.riscv64-linux; };
          };
          isCross = system != flake-utils.lib.system.riscv64-linux;
          riscv_gtest = if isCross then cross.gtest else pkgs.gtest;
          riscv_gcc = if isCross then cross.buildPackages.gcc13 else pkgs.gcc13;
          riscv_llvm =
            if isCross
            then cross.buildPackages.llvmPackages_17
            else pkgs.llvmPackages_17;

          buildDependencies = [
            riscv_gcc
            riscv_gtest
            pkgs.cmake
            pkgs.ninja
            pkgs.python311
            pkgs.cmake-format
          ];
        in
        {
          formatter = pkgs.nixpkgs-fmt;
          devShell = pkgs.mkShell rec {
            buildInputs = [
              riscv_llvm.clang
              riscv_llvm.bintools
              riscv_gcc
              pkgs.clang-tools_17
              pkgs.cpplint
            ] ++ buildDependencies;
          };
          packages.default = riscv_gcc.stdenv.mkDerivation rec {
            pname =
              if isCross
              then "rvv-intrinsic-cpp-riscv64-linux"
              else "rvv-intrinsic-cpp";
            version = "0.1.0";
            src = ./.;

            nativeBuildInputs = buildDependencies;
          };
        }
      );
}
