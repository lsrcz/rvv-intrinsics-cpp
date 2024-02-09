from typing import Callable, Sequence

from codegen import func, header, main, ops, constraints, func_obj
from codegen.param_list import function, template
from codegen.typing import misc


def fp_body(rvv_inst: str, param_list: function.FunctionTypedParamList) -> str:
    augmented_param_list: Callable[[str], function.FunctionArgumentList] = (
        lambda frm: param_list[0:-1].forward
        + function.FunctionArgumentList(frm)
        + param_list[-1:].forward
    )
    function_application: Callable[[str], str] = (
        lambda frm: func.apply_function(rvv_inst, augmented_param_list(frm))
    )
    return f"""  if constexpr (kFRM == FRM::kImplicit) {{
    return {func.apply_function(rvv_inst, param_list)};
  }} if constexpr (kFRM == FRM::kRNE) {{
    return {function_application("__RISCV_FRM_RNE")};
  }} else if constexpr (kFRM == FRM::kRTZ) {{
    return {function_application("__RISCV_FRM_RTZ")};
  }} else if constexpr (kFRM == FRM::kRDN) {{
    return {function_application("__RISCV_FRM_RDN")};
  }} else if constexpr (kFRM == FRM::kRUP) {{
    return {function_application("__RISCV_FRM_RUP")};
  }} else if constexpr (kFRM == FRM::kRMM) {{
    return {function_application("__RISCV_FRM_RMM")};
  }}"""


def fp_op(
    inst: str | tuple[str, str] | tuple[str, Sequence[str]],
    type_specs: Sequence[ops.TypeSpec],
    *,
    have_dest_arg: bool = False,
) -> Callable[[str], func_obj.CallableClass]:
    num = len(type_specs)
    frm = misc.ParamFRMValue(typename="kFRM", default_value="FRM::kImplicit")

    template_param_list = template.TemplateTypeParamList(frm)
    requires_clauses = [constraints.supported_frm(frm)]
    return ops.callable_class_op(
        num,
        inst,
        "fp",
        template_param_list,
        type_specs,
        fp_body,
        requires_clauses=requires_clauses,
        have_dest_arg=have_dest_arg,
    )


def fp_vv_and_vx_op(
    inst: str,
) -> Callable[[str], func_obj.CallableClass]:
    return fp_op(
        inst,
        [
            ("v", ["v", "v"]),
            ("v", ["v", "e"]),
        ],
    )


def fp_vx_op(
    inst: str,
) -> Callable[[str], func_obj.CallableClass]:
    return fp_op(
        inst,
        [
            ("v", ["v", "e"]),
        ],
    )


def fp_v_op(
    inst: str,
) -> Callable[[str], func_obj.CallableClass]:
    return fp_op(
        inst,
        [
            ("v", ["v"]),
        ],
    )


def fp_widening_op(inst: str) -> Callable[[str], func_obj.CallableClass]:
    return fp_op(
        (
            inst,
            [
                f"__riscv_{inst}_vf",
                f"__riscv_{inst}_wf",
                f"__riscv_{inst}_vv",
                f"__riscv_{inst}_wv",
            ],
        ),
        [
            ("w", ["v", "e"]),
            ("v", ["v", "en"]),
            ("w", ["v", "v"]),
            ("v", ["v", "n"]),
        ],
    )


def fp_widening_vv_vf_op(inst: str) -> Callable[[str], func_obj.CallableClass]:
    return fp_op(
        inst,
        [
            ("w", ["v", "e"]),
            ("w", ["v", "v"]),
        ],
    )


def fp_fma_op(inst: str) -> Callable[[str], func_obj.CallableClass]:
    return fp_op(
        inst,
        [
            ("v", ["v", "v"]),
            ("v", ["e", "v"]),
        ],
        have_dest_arg=True,
    )


def fp_widening_fma_op(inst: str) -> Callable[[str], func_obj.CallableClass]:
    return fp_op(
        inst,
        [
            ("w", ["v", "v"]),
            ("w", ["e", "v"]),
        ],
        have_dest_arg=True,
    )


rvv_fp_header = header.Header(
    [
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 5. Vector Floating-Point Intrinsics",
                        "// 5.1. Vector Single-Width Floating-Point Add/Subtract Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vfadd", "vfsub"],
                            [fp_vv_and_vx_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        header.WithVariants(
                            fp_vx_op("vfrsub"),
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        header.WithVariants(
                            ops.op("vfneg", "fp", "v", ["v"], names=["vs"])
                        ),
                        "// 5.2. Vector Widening Floating-Point Add/Subtract Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vfwadd", "vfwsub"],
                            [fp_widening_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 5.3. Vector Single-Width Floating-Point Multiply/Divide Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vfmul", "vfdiv"],
                            [fp_vv_and_vx_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        header.WithVariants(
                            fp_vx_op("vfrdiv"),
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 5.4. Vector Widening Floating-Point Multiply Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vfwmul"],
                            [fp_widening_vv_vf_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 5.5. Vector Single-Width Floating-Point Fused Multiply-Add Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            [
                                "vfmacc",
                                "vfnmacc",
                                "vfmsac",
                                "vfnmsac",
                                "vfmadd",
                                "vfnmadd",
                                "vfmsub",
                                "vfnmsub",
                            ],
                            [fp_fma_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 5.6. Vector Widening Floating-Point Fused Multiply-Add Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            [
                                "vfwmacc",
                                "vfwnmacc",
                                "vfwmsac",
                                "vfwnmsac",
                            ],
                            [fp_widening_fma_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 5.7. Vector Floating-Point Square-Root Intrinsics",
                        header.WithVariants(
                            fp_v_op("vfsqrt"),
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 5.8. Vector Floating-Point Reciprocal Square-Root Estimate Intrinsics",
                        header.WithVariants(
                            ops.simple_v_op("vfrsqrt7", "fp"),
                        ),
                        header.WithVariants(
                            fp_v_op("vfrec7"),
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 5.9. Vector Floating-Point MIN/MAX Intrinsics",
                        header.CrossProduct(
                            ops.bin_part,
                            ["vfmax", "vfmin"],
                            ["fp"],
                            [ops.simple_vv_op, ops.simple_vx_op],
                        ),
                        "// 5.10. Vector Floating-Point Sign-Injection Intrinsics",
                        header.CrossProduct(
                            ops.bin_part,
                            ["vfsgnj", "vfsgnjn", "vfsgnjx"],
                            ["fp"],
                            [ops.simple_vv_op, ops.simple_vx_op],
                        ),
                        "// 5.11. Vector Floating-Point Absolute Value Intrinsics",
                        header.WithVariants(
                            ops.simple_v_op("vfabs", "fp"),
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_fp_header)
