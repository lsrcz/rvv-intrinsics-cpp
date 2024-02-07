from typing import Callable

from codegen import func, header, main, ops
from codegen.param_list import function
from codegen.typing import elem, vl, vreg


def widening_vx_or_wx_op(
    inst: str, is_vx: bool, signed: bool
) -> Callable[[str], func.Function]:
    return func.template_elem_ratio(
        lambda elem_type, ratio: vreg.ConcreteVRegType(
            elem_type=elem.WidenElemType(base_type=elem_type), ratio=ratio
        ),
        inst,
        lambda variant, elem_type, ratio: func.elem_ratio_extend_param_list(
            elem.WidenElemType(base_type=elem_type),
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=vreg.ConcreteVRegType(
                        elem_type=(
                            elem_type
                            if is_vx
                            else elem.WidenElemType(base_type=elem_type)
                        ),
                        ratio=ratio,
                    ),
                    name="vs2",
                ),
                function.TypedParam(type=elem_type, name="rs1"),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}"
                + ("" if signed else "u")
                + ("_vx" if is_vx else "_wx")
                + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda elem_type, ratio: ops.elem_require_clauses(
            "signed" if signed else "unsigned", elem_type, ratio, widening=True
        ),
    )


def widening_vv_or_wv_op(
    inst: str, is_vv: bool, signed: bool
) -> Callable[[str], func.Function]:
    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg.WidenVRegType(base_type=vreg_type),
        inst,
        lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
            vreg.WidenVRegType(base_type=vreg_type),
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=(
                        vreg_type
                        if is_vv
                        else vreg.WidenVRegType(base_type=vreg_type)
                    ),
                    name="vs2",
                ),
                function.TypedParam(type=vreg_type, name="vs1"),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}"
                + ("" if signed else "u")
                + ("_vv" if is_vv else "_wv")
                + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
            "signed" if signed else "unsigned", vreg_type, ratio, widening=True
        ),
    )


def widening_vx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vx_or_wx_op(inst, True, signed)


def widening_wx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vx_or_wx_op(inst, False, signed)


def widening_vv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vv_or_wv_op(inst, True, signed)


def widening_wv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vv_or_wv_op(inst, False, signed)


def widening_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg.WidenVRegType(base_type=vreg_type),
        inst,
        lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
            vreg.WidenVRegType(base_type=vreg_type),
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=vreg_type,
                    name="vs2",
                ),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}"
                + ("" if signed else "u")
                + "_x"
                + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
            "signed" if signed else "unsigned", vreg_type, ratio, widening=True
        ),
    )


def extending_op(
    inst: str, signed: bool
) -> Callable[[str, int], func.Function]:
    def inner(variant: str, n: int) -> func.Function:
        return func.template_vreg_ratio(
            lambda vreg_type, ratio: vreg.WidenNVRegType(
                n=n, base_type=vreg_type
            ),
            f"{inst}{n}",
            lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
                vreg.WidenNVRegType(n=n, base_type=vreg_type),
                ratio,
                variant,
                function.FunctionTypedParamList(
                    function.TypedParam(
                        type=vreg_type,
                        name="vs2",
                    ),
                    function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
                ),
            ),
            lambda variant, elem_type, ratio, param_list: (
                "  return "
                + func.apply_function(
                    f"__riscv_{inst}"
                    + f"_vf{n}"
                    + func.rv_postfix(variant, overloaded=True),
                    param_list,
                )
                + ";"
            ),
            require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
                "signed" if signed else "unsigned", vreg_type, ratio, widening=n
            ),
        )(variant)

    return inner


def vv_shifting_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op_template_on_vreg(
        inst, allowed_type_category, shifting=True
    )


def vx_shifting_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.binary_op_template_on_vreg(
        inst, allowed_type_category, shifting=True, shifting_scalar=True
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
                            [
                                ops.binary_op_template_on_vreg,
                                ops.binary_op_template_on_elem,
                            ],
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_elem("vrsub", "int")
                        ),
                        header.WithVariants(ops.v_op("vneg", "int")),
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
                        header.WithVariants(
                            ops.binary_op_template_on_elem(
                                "vadc", "int", with_carry=True
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_vreg(
                                "vadc", "int", with_carry=True
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_elem(
                                "vmadc",
                                "int",
                                with_carry=True,
                                return_carry=True,
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_vreg(
                                "vmadc",
                                "int",
                                with_carry=True,
                                return_carry=True,
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_elem(
                                "vsbc", "int", with_carry=True
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_vreg(
                                "vsbc", "int", with_carry=True
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_elem(
                                "vmsbc",
                                "int",
                                with_carry=True,
                                return_carry=True,
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        header.WithVariants(
                            ops.binary_op_template_on_vreg(
                                "vmsbc",
                                "int",
                                with_carry=True,
                                return_carry=True,
                            ),
                            allowed_variants={"", "tu"},
                        ),
                        "// 3.6. Vector Bitwise Binary Logical Intrinsics",
                        header.CrossProduct(
                            bin_part,
                            ["vand", "vor", "vxor"],
                            ["int"],
                            [
                                ops.binary_op_template_on_vreg,
                                ops.binary_op_template_on_elem,
                            ],
                        ),
                        "// 3.7. Vector Bitwise Unary Logical Intrinsics",
                        header.WithVariants(ops.v_op("vnot", "int")),
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
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_int_header)
