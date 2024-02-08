from typing import Callable

from codegen import func, header, main, ops


def simple_vx_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", ["v", "x"])


def simple_vv_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", ["v", "v"])


def simple_v_op(
    inst: str, allowed_type_category: str
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", ["v"], names=["vs"])


def widening_vx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_vx"),
        "signed" if signed else "unsigned",
        "w",
        ["v", "x"],
    )


def widening_wx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_wx"),
        "signed" if signed else "unsigned",
        "v",
        ["v", "en"],
    )


def widening_vv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_vv"),
        "signed" if signed else "unsigned",
        "w",
        ["v", "v"],
    )


def widening_wv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_wv"),
        "signed" if signed else "unsigned",
        "v",
        ["v", "n"],
    )


def widening_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_x"),
        "signed" if signed else "unsigned",
        "w",
        ["v"],
    )


def extending_op(inst: str) -> Callable[[str, int], func.Function]:
    assert inst in ["vsext", "vzext"]
    if inst == "vsext":
        sign = "signed"
    else:
        sign = "unsigned"

    def inner(variant: str, n: int) -> func.Function:
        assert n in [2, 4, 8]
        return ops.op(
            (f"{inst}{n}", f"__riscv_{inst}_vf{n}"), sign, f"{n}", ["v"]
        )(variant)

    return inner


def add_sub_carry_vvm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "v", ["v", "v", "m"])


def add_sub_carry_vxm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "v", ["v", "x", "m"])


def carry_out_vvm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "v", "m"])


def carry_out_vxm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "x", "m"])


def carry_out_vv_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "v"])


def carry_out_vx_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "x"])


def shifting_type_category(inst: str) -> str:
    match inst:
        case "vsll":
            return "int"
        case "vsra":
            return "signed"
        case "vsrl":
            return "unsigned"
        case _:
            raise ValueError(f"Unknown instruction: {inst}")


def shifting_vx_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, shifting_type_category(inst), "v", ["v", "size"])


def shifting_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, shifting_type_category(inst), "v", ["v", "u"])


def narrowing_shift_wv_op(inst: str) -> Callable[[str], func.Function]:
    assert inst in ["vnsra", "vnsrl"]
    return ops.op(
        inst,
        "unsigned" if inst == "vnsrl" else "signed",
        "n",
        ["v", "nu"] if inst == "vnsra" else ["v", "n"],
    )


def narrowing_shift_wx_op(inst: str) -> Callable[[str], func.Function]:
    assert inst in ["vnsra", "vnsrl"]
    return ops.op(
        inst, "unsigned" if inst == "vnsrl" else "signed", "n", ["v", "size"]
    )


def vncvt(variant: str) -> func.Function:
    return ops.op(("vncvt", "__riscv_vncvt_x"), "int", "n", ["v"])(variant)


def comparing_type_category(inst: str) -> str:
    match inst:
        case "vmseq" | "vmsne":
            return "int"
        case "vmslt" | "vmsle" | "vmsgt" | "vmsge":
            return "signed"
        case "vmsltu" | "vmsleu" | "vmsgtu" | "vmsgeu":
            return "unsigned"
        case _:
            raise ValueError(f"Unknown instruction: {inst}")


def comparing_vx_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        comparing_type_category(inst),
        "m",
        ["v", "x"],
    )


def comparing_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        comparing_type_category(inst),
        "m",
        ["v", "v"],
    )


def sign_aware_vx_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "v",
        ["v", "x"],
    )


def sign_aware_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "v",
        ["v", "v"],
    )


def fma_vx_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst, "int", "v", ["x", "v"], names=["rs1", "vs2"], have_dest_arg=True
    )


def fma_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst, "int", "v", ["v", "v"], names=["vs1", "vs2"], have_dest_arg=True
    )


def bin_part(
    op: str,
    allowed_type_category: str,
    f: Callable[[str, str], Callable[[str], func.Function]],
) -> header.HeaderPart:
    return header.WithVariants(f(op, allowed_type_category))


def widening_part(
    op: str,
    signed: bool,
    f: Callable[[str, bool], Callable[[str], func.Function]],
) -> header.HeaderPart:
    return header.WithVariants(f(op, signed))


def inferred_type_part(
    op: str,
    f: Callable[[str], Callable[[str], func.Function]],
) -> header.HeaderPart:
    return header.WithVariants(f(op))


rvv_int_header = header.Header(
    [
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 3. Vector Integer Arithmetic Intrinsics",
                        "// 3.1. Vector Single-Width Integer Add and Substract Intrinsics",
                        header.CrossProduct(
                            bin_part,
                            ["vadd", "vsub"],
                            ["int"],
                            [simple_vx_op, simple_vv_op],
                        ),
                        header.WithVariants(simple_vx_op("vrsub", "int")),
                        header.WithVariants(
                            ops.op("vneg", "int", "v", ["v"], names=["vs"])
                        ),
                        "// 3.2. Vector Widening Integer Add/Subtract Intrinsics",
                        header.CrossProduct(
                            widening_part,
                            ["vwadd", "vwsub"],
                            [True, False],
                            [
                                widening_vv_op,
                                widening_vx_op,
                                widening_wv_op,
                                widening_wx_op,
                            ],
                        ),
                        "// 3.3. Vector Integer Widening Intrinsics",
                        header.WithVariants(widening_op("vwcvt", True)),
                        header.WithVariants(widening_op("vwcvt", False)),
                        "// 3.4. Vector Integer Extension Intrinsics",
                        header.CrossProduct.variant(
                            extending_op("vsext"), [2, 4, 8]
                        ),
                        header.CrossProduct.variant(
                            extending_op("vzext"), [2, 4, 8]
                        ),
                        "// 3.5. Vector Integer Add-with-Carry and Subtract-with-Borrow Intrinsics",
                        header.CrossProduct(
                            inferred_type_part,
                            ["vadc", "vsbc"],
                            [add_sub_carry_vvm_op, add_sub_carry_vxm_op],
                            allowed_variants={"", "tu"},
                        ),
                        header.CrossProduct(
                            inferred_type_part,
                            ["vmadc", "vmsbc"],
                            [
                                carry_out_vvm_op,
                                carry_out_vxm_op,
                                carry_out_vv_op,
                                carry_out_vx_op,
                            ],
                            allowed_variants={""},
                        ),
                        "// 3.6. Vector Bitwise Binary Logical Intrinsics",
                        header.CrossProduct(
                            bin_part,
                            ["vand", "vor", "vxor"],
                            ["int"],
                            [simple_vx_op, simple_vv_op],
                        ),
                        "// 3.7. Vector Bitwise Unary Logical Intrinsics",
                        header.WithVariants(simple_v_op("vnot", "int")),
                        "// 3.8. Vector Single-Width Bit Shift Intrinsics",
                        header.CrossProduct(
                            inferred_type_part,
                            ["vsll", "vsra", "vsrl"],
                            [shifting_vv_op, shifting_vx_op],
                        ),
                        "// 3.9. Vector Narrowing Integer Right Shift Intrinsics",
                        header.CrossProduct(
                            inferred_type_part,
                            ["vnsra", "vnsrl"],
                            [narrowing_shift_wv_op, narrowing_shift_wx_op],
                        ),
                        "// 3.10. Vector Integer Narrowing Intrinsics",
                        header.WithVariants(vncvt),
                        "// 3.11. Vector Integer Compare Intrinsics",
                        header.CrossProduct(
                            inferred_type_part,
                            [
                                "vmseq",
                                "vmsne",
                                "vmslt",
                                "vmsle",
                                "vmsgt",
                                "vmsge",
                                "vmsltu",
                                "vmsleu",
                                "vmsgtu",
                                "vmsgeu",
                            ],
                            [comparing_vv_op, comparing_vx_op],
                        ),
                        "// 3.12. Vector Integer Compare Intrinsics",
                        header.CrossProduct(
                            inferred_type_part,
                            ["vmax", "vmin", "vmaxu", "vminu"],
                            [
                                sign_aware_vv_op,
                                sign_aware_vx_op,
                            ],
                        ),
                        "// 3.13. Vector Single-Width Integer Multiply Intrinsics",
                        header.WithVariants(simple_vv_op("vmul", "int")),
                        header.WithVariants(simple_vx_op("vmul", "int")),
                        header.CrossProduct(
                            inferred_type_part,
                            ["vmulh", "vmulhu"],
                            [sign_aware_vv_op, sign_aware_vx_op],
                        ),
                        header.WithVariants(
                            ops.op("vmulhsu", "signed", "v", ["v", "u"])
                        ),
                        header.WithVariants(
                            ops.op("vmulhsu", "signed", "v", ["v", "eu"])
                        ),
                        "// 3.14. Vector Integer Divide Intrinsics",
                        header.CrossProduct(
                            inferred_type_part,
                            ["vdiv", "vdivu", "vrem", "vremu"],
                            [sign_aware_vv_op, sign_aware_vx_op],
                        ),
                        "// 3.15. Vector Widening Integer Multiply Intrinsics",
                        header.WithVariants(
                            ops.op("vwmul", "signed", "w", ["v", "v"])
                        ),
                        header.WithVariants(
                            ops.op("vwmul", "signed", "w", ["v", "x"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulu", "unsigned", "w", ["v", "v"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulu", "unsigned", "w", ["v", "x"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulsu", "signed", "w", ["v", "u"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulsu", "signed", "w", ["v", "eu"])
                        ),
                        "// 3.16. Vector Single-Width Integer Multiply-Add Intrinsics",
                        header.CrossProduct(
                            inferred_type_part,
                            ["vmacc", "vmadd", "vnmsac", "vnmsub"],
                            [fma_vv_op, fma_vx_op],
                        ),
                        "// 3.17. Vector Widening Integer Multiply-Add Intrinsics",
                        header.WithVariants(
                            ops.op(
                                "vwmacc",
                                "signed",
                                "w",
                                ["x", "v"],
                                have_dest_arg=True,
                            )
                        ),
                        header.WithVariants(
                            ops.op(
                                "vwmacc",
                                "signed",
                                "w",
                                ["v", "v"],
                                have_dest_arg=True,
                            )
                        ),
                        header.WithVariants(
                            ops.op(
                                "vwmaccu",
                                "unsigned",
                                "w",
                                ["x", "v"],
                                have_dest_arg=True,
                            )
                        ),
                        header.WithVariants(
                            ops.op(
                                "vwmaccu",
                                "unsigned",
                                "w",
                                ["v", "v"],
                                have_dest_arg=True,
                            )
                        ),
                        header.WithVariants(
                            ops.op(
                                "vwmaccsu",
                                "unsigned",
                                "ws",
                                ["es", "v"],
                                have_dest_arg=True,
                            )
                        ),
                        header.WithVariants(
                            ops.op(
                                "vwmaccsu",
                                "signed",
                                "w",
                                ["v", "u"],
                                have_dest_arg=True,
                            )
                        ),
                        header.WithVariants(
                            ops.op(
                                "vwmaccus",
                                "signed",
                                "w",
                                ["eu", "v"],
                                have_dest_arg=True,
                            )
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_int_header)
