from typing import Callable

from codegen import func, header, main, ops


def simple_vx_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", "vx")


def simple_vv_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", "vv")


def simple_v_op(
    inst: str, allowed_type_category: str
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", "v", names=["vs"])


def widening_vx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_vx"),
        "signed" if signed else "unsigned",
        "w",
        "vx",
    )


def widening_wx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_wx"),
        "signed" if signed else "unsigned",
        "v",
        "vy",
    )


def widening_vv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_vv"),
        "signed" if signed else "unsigned",
        "w",
        "vv",
    )


def widening_wv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_wv"),
        "signed" if signed else "unsigned",
        "v",
        "vn",
    )


def widening_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    inst_with_sign = inst + ("" if signed else "u")
    return ops.op(
        (inst_with_sign, f"__riscv_{inst_with_sign}_x"),
        "signed" if signed else "unsigned",
        "w",
        "v",
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
            (f"{inst}{n}", f"__riscv_{inst}_vf{n}"), sign, f"{n}", "v"
        )(variant)

    return inner


def add_sub_carry_vvm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "v", "vvm")


def add_sub_carry_vxm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "v", "vxm")


def carry_out_vvm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", "vvm")


def carry_out_vxm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", "vxm")


def carry_out_vv_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", "vv")


def carry_out_vx_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(inst, "int", "m", "vx")


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
    return ops.op(inst, shifting_type_category(inst), "v", "vs")


def shifting_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, shifting_type_category(inst), "v", "vu")


def narrowing_shift_wv_op(inst: str) -> Callable[[str], func.Function]:
    assert inst in ["vnsra", "vnsrl"]
    return ops.op(
        inst,
        "unsigned" if inst == "vnsrl" else "signed",
        "n",
        "vz" if inst == "vnsra" else "vn",
    )


def narrowing_shift_wx_op(inst: str) -> Callable[[str], func.Function]:
    assert inst in ["vnsra", "vnsrl"]
    return ops.op(inst, "unsigned" if inst == "vnsrl" else "signed", "n", "vs")


def vncvt(variant: str) -> func.Function:
    return ops.op(("vncvt", "__riscv_vncvt_x"), "int", "n", "v")(variant)


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
        "vx",
    )


def comparing_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        comparing_type_category(inst),
        "m",
        "vv",
    )


def vx_min_max_op(
    inst: str,
) -> Callable[[str], func.Function]:
    assert inst in ["vmax", "vmin", "vmaxu", "vminu"]
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "v",
        "vx",
    )


def vv_min_max_op(
    inst: str,
) -> Callable[[str], func.Function]:
    assert inst in ["vmax", "vmin", "vmaxu", "vminu"]
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "v",
        "vv",
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
                            ops.op("vneg", "int", "v", "v", names=["vs"])
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
                                vv_min_max_op,
                                vx_min_max_op,
                            ],
                        ),
                        "// 3.13. Vector Single-Width Integer Multiply Intrinsics",
                        header.WithVariants(simple_vv_op("vmul", "int")),
                        header.WithVariants(simple_vx_op("vmul", "int")),
                        header.WithVariants(
                            ops.op("vmulh", "signed", "v", "vv")
                        ),
                        header.WithVariants(
                            ops.op("vmulh", "signed", "v", "vx")
                        ),
                        header.WithVariants(
                            ops.op("vmulhu", "unsigned", "v", "vv")
                        ),
                        header.WithVariants(
                            ops.op("vmulhu", "unsigned", "v", "vx")
                        ),
                        header.WithVariants(
                            ops.op("vmulhsu", "signed", "v", "vu")
                        ),
                        header.WithVariants(
                            ops.op("vmulhsu", "signed", "v", "va")
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_int_header)
