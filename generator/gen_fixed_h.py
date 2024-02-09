from typing import Callable, Sequence

from codegen import constraints, func, func_obj, header, main, ops
from codegen.param_list import function, template
from codegen.typing import misc


def fixed_body(
    rvv_inst: str,
    param_list: function.FunctionTypedParamList,
) -> str:
    augmented_param_list: Callable[[str], function.FunctionArgumentList] = (
        lambda vxrm: param_list[0:-1].forward
        + function.FunctionArgumentList(vxrm)
        + param_list[-1:].forward
    )
    function_application: Callable[[str], str] = (
        lambda vxrm: func.apply_function(rvv_inst, augmented_param_list(vxrm))
    )
    return f"""  if constexpr (kVXRM == VXRM::kRNU) {{
    return {function_application("__RISCV_VXRM_RNU")};
  }} else if constexpr (kVXRM == VXRM::kRNE) {{
    return {function_application("__RISCV_VXRM_RNE")};
  }} else if constexpr (kVXRM == VXRM::kRDN) {{
    return {function_application("__RISCV_VXRM_RDN")};
  }} else if constexpr (kVXRM == VXRM::kROD) {{
    return {function_application("__RISCV_VXRM_ROD")};
  }}"""


def fixed_op(
    inst: str,
    allowed_type_category: str,
    type_specs: Sequence[ops.TypeSpec],
) -> Callable[[str], func_obj.CallableClass]:
    num = 2
    vxrm = misc.param_vxrm("kVXRM")

    template_param_list = template.TemplateTypeParamList(vxrm)
    requires_clauses = [constraints.supported_vxrm(vxrm)]
    return ops.callable_class_op(
        num,
        inst,
        allowed_type_category,
        template_param_list,
        type_specs,
        fixed_body,
        requires_clauses=requires_clauses,
    )


def fixed_arith_op(
    inst: str,
) -> Callable[[str], func_obj.CallableClass]:
    return fixed_op(
        inst,
        ("unsigned" if inst.endswith("u") or inst == "vssrl" else "signed"),
        [
            ("v", ["v", "v"]),
            ("v", ["v", "e"]),
        ],
    )


def fixed_nshift_op(
    inst: str,
) -> Callable[[str], func_obj.CallableClass]:
    return fixed_op(
        inst,
        ("unsigned" if inst == "vssrl" else "signed"),
        [
            ("v", ["v", "v" if inst == "vssrl" else "u"]),
            ("v", ["v", "size"]),
        ],
    )


def fixed_nclip_op(
    inst: str,
) -> Callable[[str], func_obj.CallableClass]:
    return fixed_op(
        inst,
        ("unsigned" if inst.endswith("u") else "signed"),
        [
            ("n", ["v", "n" if inst.endswith("u") else "nu"]),
            ("n", ["v", "size"]),
        ],
    )


rvv_fixed_header = header.Header(
    [
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 4. Vector Fixed-Point Arithmetic Intrinsics",
                        "// 4.1. Vector Single-Width Saturating Add and Subtract Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vsadd", "vssub", "vsaddu", "vssubu"],
                            [ops.sign_aware_vv_op, ops.sign_aware_vx_op],
                        ),
                        "// 4.2. Vector Single-Width Averaging Add and Subtract Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vaadd", "vaaddu", "vasub", "vasubu"],
                            [fixed_arith_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 4.3. Vector Single-Width Fractional Multiply with Rounding and Saturation Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vsmul"],
                            [fixed_arith_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 4.4. Vector Single-Width Scaling Shift Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vssra", "vssrl"],
                            [fixed_nshift_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 4.5. Vector Narrowing Fixed-Point Clip Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vnclip", "vnclipu"],
                            [fixed_nclip_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_fixed_header)
