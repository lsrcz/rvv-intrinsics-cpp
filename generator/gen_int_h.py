from typing import Callable

from codegen import func, header, main, ops
from codegen.param_list import function
from codegen.typing import base, misc, vl, vreg


def binary_widening_op(
    inst: str, arg_variant: str, signed: bool
) -> Callable[[str], func.Function]:
    assert arg_variant in ["vx", "wx", "vv", "wv"]

    def ret_type(
        vreg_type: vreg.ParamVRegType, _ratio: misc.ParamSizeTValue
    ) -> vreg.VRegType:
        if arg_variant in ["wx", "wv"]:
            return vreg_type
        return vreg.widen(vreg_type)

    def arg2(vreg_type: vreg.ParamVRegType) -> base.Type:
        match arg_variant:
            case "vx":
                return vreg.get_elem(vreg_type)
            case "vv":
                return vreg_type
            case "wx":
                return vreg.get_elem(vreg.narrow(vreg_type))
            case "wv":
                return vreg.narrow(vreg_type)
            case _:
                assert False

    return func.template_vreg_ratio(
        ret_type,
        inst + ("" if signed else "u"),
        lambda variant, vreg_type, ratio: func.vreg_ratio_param_list(
            ret_type(vreg_type, ratio),
            ratio,
            variant,
            [
                vreg_type,
                arg2(vreg_type),
                vl.vl(ratio),
            ],
            ["vs2", "vs1" if arg_variant in ["vv", "wv"] else "rs1", "vl"],
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}"
                + ("_" if signed else "u_")
                + arg_variant
                + func.rvv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
            "signed" if signed else "unsigned",
            vreg_type,
            ratio,
            widening=arg_variant in ["vv", "vx"],
            narrowing=arg_variant in ["wv", "wx"],
        ),
    )


def widening_vx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return binary_widening_op(inst, "vx", signed)


def widening_wx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return binary_widening_op(inst, "wx", signed)


def widening_vv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return binary_widening_op(inst, "vv", signed)


def widening_wv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return binary_widening_op(inst, "wv", signed)


def widening_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg.widen(vreg_type),
        inst + ("" if signed else "u"),
        lambda variant, vreg_type, ratio: func.vreg_ratio_param_list(
            vreg.widen(vreg_type),
            ratio,
            variant,
            [vreg_type, vl.vl(ratio)],
            ["vs2", "vl"],
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}"
                + ("" if signed else "u")
                + "_x"
                + func.rvv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
            "signed" if signed else "unsigned", vreg_type, ratio, widening=True
        ),
    )


def narrowing_shift_op(
    inst: str, *, arg_variant: str
) -> Callable[[str], func.Function]:
    assert inst in ["vnsra", "vnsrl"]
    assert arg_variant in ["wv", "wx"]

    def function_param_list(
        variant: str, vreg_type: vreg.ParamVRegType, ratio: misc.ParamSizeTValue
    ) -> function.FunctionTypedParamList:
        def arg2_type(vreg_type: vreg.ParamVRegType) -> base.Type:
            match arg_variant:
                case "wv":
                    if inst == "vnsra":
                        return vreg.narrow(vreg.to_unsigned(vreg_type))
                    else:
                        return vreg.narrow(vreg_type)
                case "wx":
                    return misc.size_t
                case _:
                    assert False

        arg2_name = "vs1" if arg_variant in ["wv"] else "rs1"

        return func.vreg_ratio_param_list(
            vreg.narrow(vreg_type),
            ratio,
            variant,
            [vreg_type, arg2_type(vreg_type), vl.vl(ratio)],
            ["vs2", arg2_name, "vl"],
        )

    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg.narrow(vreg_type),
        inst,
        function_param_list,
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}" + func.rvv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
            "signed" if inst == "vnsra" else "unsigned",
            vreg_type,
            ratio,
            narrowing=True,
        ),
    )


def extending_op(
    inst: str, signed: bool
) -> Callable[[str, int], func.Function]:
    def inner(variant: str, n: int) -> func.Function:
        return func.template_vreg_ratio(
            lambda vreg_type, ratio: vreg.widen_n(n, vreg_type),
            f"{inst}{n}",
            lambda variant, vreg_type, ratio: func.vreg_ratio_param_list(
                vreg.widen_n(n, vreg_type),
                ratio,
                variant,
                [vreg_type, vl.vl(ratio)],
                ["vs2", "vl"],
            ),
            lambda variant, elem_type, ratio, param_list: (
                "  return "
                + func.apply_function(
                    f"__riscv_{inst}"
                    + f"_vf{n}"
                    + func.rvv_postfix(variant, overloaded=True),
                    param_list,
                )
                + ";"
            ),
            require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
                "signed" if signed else "unsigned", vreg_type, ratio, widening=n
            ),
        )(variant)

    return inner


def vncvt(variant: str) -> func.Function:
    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg.narrow(vreg_type),
        "vncvt",
        lambda variant, vreg_type, ratio: func.vreg_ratio_param_list(
            vreg.narrow(vreg_type),
            ratio,
            variant,
            [vreg_type, vl.vl(ratio)],
            ["vs2", "vl"],
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                "__riscv_vncvt_x" + func.rvv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
            "int", vreg_type, ratio, narrowing=True
        ),
    )(variant)


def simple_vx_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, allowed_type_category, "vx")


def simple_vv_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, allowed_type_category, "vv")


def vx_shifting_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(
        inst, allowed_type_category, "vx", op_variant="shifting"
    )


def vv_shifting_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(
        inst, allowed_type_category, "vv", op_variant="shifting"
    )


def vx_comparing_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(
        inst + ("u" if allowed_type_category == "unsigned" else ""),
        allowed_type_category,
        arg_variant="vx",
        op_variant="comparing",
    )


def vv_comparing_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(
        inst + ("u" if allowed_type_category == "unsigned" else ""),
        allowed_type_category,
        "vv",
        op_variant="comparing",
    )


def add_sub_carry_vvm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, "int", "vv", op_variant="use_carry")


def add_sub_carry_vxm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, "int", "vx", op_variant="use_carry")


def carry_out_vvm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, "int", "vv", op_variant="use_and_produce_carry")


def carry_out_vxm_op(inst: str) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, "int", "vx", op_variant="use_and_produce_carry")


def carry_out_vv_op(inst: str) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, "int", "vv", op_variant="produce_carry")


def carry_out_vx_op(inst: str) -> Callable[[str], func.Function]:
    return ops.binary_op(inst, "int", "vx", op_variant="produce_carry")


def vx_min_max_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(
        inst + ("u" if allowed_type_category == "unsigned" else ""),
        allowed_type_category,
        "vx",
    )


def vv_min_max_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op(
        inst + ("u" if allowed_type_category == "unsigned" else ""),
        allowed_type_category,
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


def carrying_part(
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
                        header.WithVariants(
                            ops.binary_op("vrsub", "int", "vx")
                        ),
                        header.WithVariants(ops.unary_op("vneg", "int")),
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
                            extending_op("vsext", True), [2, 4, 8]
                        ),
                        header.CrossProduct.variant(
                            extending_op("vzext", False), [2, 4, 8]
                        ),
                        "// 3.5. Vector Integer Add-with-Carry and Subtract-with-Borrow Intrinsics",
                        header.CrossProduct(
                            carrying_part,
                            ["vadc", "vsbc"],
                            [add_sub_carry_vvm_op, add_sub_carry_vxm_op],
                            allowed_variants={"", "tu"},
                        ),
                        header.CrossProduct(
                            carrying_part,
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
                        header.WithVariants(ops.unary_op("vnot", "int")),
                        "// 3.8. Vector Single-Width Bit Shift Intrinsics",
                        header.CrossProduct(
                            bin_part,
                            ["vsll", "vsra"],
                            ["signed"],
                            [vv_shifting_op, vx_shifting_op],
                        ),
                        header.CrossProduct(
                            bin_part,
                            ["vsll", "vsrl"],
                            ["unsigned"],
                            [vv_shifting_op, vx_shifting_op],
                        ),
                        "// 3.9. Vector Narrowing Integer Right Shift Intrinsics",
                        header.WithVariants(
                            narrowing_shift_op("vnsra", arg_variant="wv")
                        ),
                        header.WithVariants(
                            narrowing_shift_op("vnsra", arg_variant="wx")
                        ),
                        header.WithVariants(
                            narrowing_shift_op("vnsrl", arg_variant="wv")
                        ),
                        header.WithVariants(
                            narrowing_shift_op("vnsrl", arg_variant="wx")
                        ),
                        "// 3.10. Vector Integer Narrowing Intrinsics",
                        header.WithVariants(vncvt),
                        "// 3.11. Vector Integer Compare Intrinsics",
                        header.CrossProduct(
                            bin_part,
                            ["vmseq", "vmsne"],
                            ["int"],
                            [vv_comparing_op, vx_comparing_op],
                        ),
                        header.CrossProduct(
                            bin_part,
                            ["vmslt", "vmsle", "vmsgt", "vmsge"],
                            ["signed", "unsigned"],
                            [vv_comparing_op, vx_comparing_op],
                        ),
                        "// 3.12. Vector Integer Compare Intrinsics",
                        header.CrossProduct(
                            bin_part,
                            ["vmax", "vmin"],
                            ["signed", "unsigned"],
                            [
                                vv_min_max_op,
                                vx_min_max_op,
                            ],
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_int_header)
