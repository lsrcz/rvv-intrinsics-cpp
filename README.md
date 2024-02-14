# RISC-V Vector Intrinsics in C++

This small library provides a set of overloaded functions for the RISC-V Vector
intrinsics. Due to the limitation of the C language, some of the RISC-V Vector intrinsics could not be overloaded and do not have a simplified, EEW/EMUL-omitted interface. This library uses C++ to provide a cleaner interface and tries to use concepts to simplify the error messages.


## Basic types

- Application vector length (AVL): `rvv::vl_t<ratio>`. `ratio` is the ratio of
  EEW and EMUL. For example, if you have a EEW of 32 (`float`, `uint32_t`,
  `uint64_t`), and you are using EMUL=1/2, then you should use `rvv::vl_t<64>`.
- Mask type: `vmask_t<ratio>`.
- Register type: `vreg_t<type, ratio>`. For example, if you are using the type
  `vint32mf2_t` in the C API, then you should use `vreg_t<int32_t, 64>` with
  this library.

The rationale to use `ratio` rather than the pair of the data type and the EMUL
is that the `ratio` determines how many elements are there in the register type,
regardless of the element types. This won't be changed when you widen or narrow
the elements, and feeding the `vl` to the operations operating on the registers
with the same `ratio` will not yield surprising behaviors.

For example, in the following code:

```C
// Assuming data{n} is int{n}_t*
size_t vl = __riscv_vsetvlmax_e8m4();
// The actual vector length could be smaller than the application vector length
// provided by the vsetvl call.
vint8m1_t reg0 = __riscv_vle8_v_i8m1(data8, vl);
vint8m2_t reg1 = __riscv_vle8_v_i8m2(data8, vl);
// The actual vector length are guaranteed to be the same the application vector
// length provided by the vsetvl call.
vint8m4_t reg2 = __riscv_vle8_v_i8m4(data8, vl);
vint16m8_t reg3 = __riscv_vle16_v_i16m8(data16, vl);
```

The actual `vl` used by the first two load intrinsics may be different from the
`vl` produced by the `vsetvl` as they have a larger EMUL/EEW ratio, meaning that
their registers could hold fewer elements. The actual `vl` used by the last two
load intrinsics are guaranteed to be the same as the result of `vsetvl`.

In our library, the code could be written as:
```C++
// Assuming data{n} is int{n}_t*
auto vl = rvv::vsetvlmax<2>();
// The compiler will deduce that the reg2 should have the type vreg_t<int8_t, 2>,
// aka. vint8m4_t
auto reg2 = rvv::vle(data8, vl);
// vint16m8_t
auto reg3 = rvv::vle(data16, vl);
// 16 isn't a valid LMUL value, so this won't compile.
auto reg_do_not_compile = rvv::vle(data32, vl);
```

## Building
Required prerequites: Python 3 (Only tested with 3.11+). Clang 17+ or GCC thunk
(The library is built with RVV v1.0.x, which is not supported by older
compilers).

Optional dependencies: pytest, gtest (required for the test suites),
clang-format (format the generated headers).

```bash
mkdir build
cd build
cmake -G Ninja -D CMAKE_INSTALL_PREFIX=<The installation folder> ..
ninja && ninja install
```

## TODO list
- [ ] Finish the section 9 in https://github.com/riscv-non-isa/rvv-intrinsic-doc.
