from typing import Callable

from codegen import func, header, main, ops


def widening_vx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_vx"),
        "signed" if signed else "unsigned",
        "w",
        ["v", "e"],
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


def vvm_v_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "v", ["v", "v", "m"])


def vxm_v_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "v", ["v", "e", "m"])


def carry_out_vvm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "v", "m"])


def carry_out_vxm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "e", "m"])


def carry_out_vv_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "v"])


def carry_out_vx_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", ["v", "e"])


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


def widening_part(
    op: str,
    signed: bool,
    f: Callable[[str, bool], Callable[[str], func.Function]],
) -> header.HeaderPart:
    return header.WithVariants(f(op, signed))


rvv_int_header = header.Header(
    [
        header.Include("rvv/elem.h"),
        header.Include("rvv/conversion.h"),
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 3. Vector Integer Arithmetic Intrinsics",
                        "// 3.1. Vector Single-Width Integer Add and Substract Intrinsics",
                        header.CrossProduct(
                            ops.bin_part,
                            ["vadd", "vsub"],
                            ["int"],
                            [ops.simple_vx_op, ops.simple_vv_op],
                        ),
                        header.WithVariants(ops.simple_vx_op("vrsub", "int")),
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
                            ops.inferred_type_part,
                            ["vadc", "vsbc"],
                            [vvm_v_op, vxm_v_op],
                            allowed_variants={"", "tu"},
                        ),
                        header.CrossProduct(
                            ops.inferred_type_part,
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
                            ops.bin_part,
                            ["vand", "vor", "vxor"],
                            ["int"],
                            [ops.simple_vx_op, ops.simple_vv_op],
                        ),
                        "// 3.7. Vector Bitwise Unary Logical Intrinsics",
                        header.WithVariants(ops.simple_v_op("vnot", "int")),
                        "// 3.8. Vector Single-Width Bit Shift Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vsll", "vsra", "vsrl"],
                            [shifting_vv_op, shifting_vx_op],
                        ),
                        "// 3.9. Vector Narrowing Integer Right Shift Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vnsra", "vnsrl"],
                            [narrowing_shift_wv_op, narrowing_shift_wx_op],
                        ),
                        "// 3.10. Vector Integer Narrowing Intrinsics",
                        header.WithVariants(vncvt),
                        "// 3.11. Vector Integer Compare Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
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
                            [ops.comparing_vv_op, ops.comparing_vx_op],
                        ),
                        "// 3.12. Vector Integer Compare Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vmax", "vmin", "vmaxu", "vminu"],
                            [
                                ops.sign_aware_vv_op,
                                ops.sign_aware_vx_op,
                            ],
                        ),
                        "// 3.13. Vector Single-Width Integer Multiply Intrinsics",
                        header.WithVariants(ops.simple_vv_op("vmul", "int")),
                        header.WithVariants(ops.simple_vx_op("vmul", "int")),
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vmulh", "vmulhu"],
                            [ops.sign_aware_vv_op, ops.sign_aware_vx_op],
                        ),
                        header.WithVariants(
                            ops.op("vmulhsu", "signed", "v", ["v", "u"])
                        ),
                        header.WithVariants(
                            ops.op("vmulhsu", "signed", "v", ["v", "eu"])
                        ),
                        "// 3.14. Vector Integer Divide Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vdiv", "vdivu", "vrem", "vremu"],
                            [ops.sign_aware_vv_op, ops.sign_aware_vx_op],
                        ),
                        "// 3.15. Vector Widening Integer Multiply Intrinsics",
                        header.WithVariants(
                            ops.op("vwmul", "signed", "w", ["v", "v"])
                        ),
                        header.WithVariants(
                            ops.op("vwmul", "signed", "w", ["v", "e"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulu", "unsigned", "w", ["v", "v"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulu", "unsigned", "w", ["v", "e"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulsu", "signed", "w", ["v", "u"])
                        ),
                        header.WithVariants(
                            ops.op("vwmulsu", "signed", "w", ["v", "eu"])
                        ),
                        "// 3.16. Vector Single-Width Integer Multiply-Add Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vmacc", "vmadd", "vnmsac", "vnmsub"],
                            [ops.fma_vv_op, ops.fma_vx_op],
                        ),
                        "// 3.17. Vector Widening Integer Multiply-Add Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vwmacc", "vwmaccu", "vwmaccsu"],
                            [ops.widening_fma_vv_op],
                        ),
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vwmacc", "vwmaccu", "vwmaccsu", "vwmaccus"],
                            [ops.widening_fma_vx_op],
                        ),
                        "// 3.18. Vector Integer Merge Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vmerge"],
                            [vvm_v_op, vxm_v_op],
                            allowed_variants={"", "tu"},
                        ),
                        "// 3.19. Vector Integer Move Intrinsics",
                        header.WithVariants(
                            ops.op(
                                ("vmv", "__riscv_vmv_v"),
                                "int",
                                "v",
                                ["v"],
                                names=["vs1"],
                            ),
                            allowed_variants={"", "tu"},
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_int_header)
