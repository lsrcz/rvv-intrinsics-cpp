from typing import Callable, Sequence
from codegen import func, func_obj, header, main, ops, constraints
from codegen.param_list import template, function
from codegen.typing import misc, vl, vreg


def with_variant(
    template_param_list: template.TemplateTypeParamList,
    name: str,
    call_operators: Sequence[Callable[[str], func.Function]],
    *,
    requires_clauses: Sequence[str] = tuple(),
) -> Callable[[str], func_obj.CallableClass]:
    def inner(variant: str) -> func_obj.CallableClass:
        assert variant in ["", "tu", "mu", "tumu"]
        all_call_operators = list(map(lambda op: op(variant), call_operators))
        if variant == "" or variant == "tu":
            all_call_operators += list(
                map(lambda op: op(variant + "m"), call_operators)
            )
        return func_obj.CallableClass(
            template_param_list,
            name,
            all_call_operators,
            requires_clauses=requires_clauses,
        )

    return inner


def fixed_body(
    variant: str,
    inst: str,
    param_list: function.FunctionTypedParamList,
) -> str:
    function_name = f"__riscv_{inst}" + func.rvv_postfix(
        variant, overloaded=True
    )
    augmented_param_list: Callable[[str], function.FunctionArgumentList] = (
        lambda vxrm: param_list[0:-1].forward
        + function.FunctionArgumentList(vxrm)
        + param_list[-1:].forward
    )
    function_application: Callable[[str], str] = (
        lambda vxrm: func.apply_function(
            function_name, augmented_param_list(vxrm)
        )
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
) -> Callable[[str], func_obj.CallableClass]:
    allowed_type_category = (
        "unsigned" if inst.endswith("u") or inst == "vssrl" else "signed"
    )
    vxrm = misc.param_vxrm("kVXRM")

    def dest_type(vreg_type: vreg.VRegType) -> vreg.VRegType:
        if inst in ["vnclip", "vnclipu"]:
            return vreg.narrow(vreg_type)
        return vreg_type

    def arg2_v_type(vreg_type: vreg.VRegType) -> vreg.VRegType:
        match inst:
            case "vssra":
                return vreg.to_unsigned(vreg_type)
            case "vnclip":
                return vreg.to_unsigned(vreg.narrow(vreg_type))
            case "vnclipu":
                return vreg.narrow(vreg_type)
            case _:
                return vreg_type

    return with_variant(
        template.TemplateTypeParamList(vxrm),
        inst,
        [
            func.template_vreg_ratio(
                lambda vreg_type, _: dest_type(vreg_type),
                "operator()",
                lambda variant, vreg_type, ratio: func.vreg_ratio_param_list(
                    dest_type(vreg_type),
                    ratio,
                    variant,
                    [
                        vreg_type,
                        arg2_v_type(vreg_type),
                        vl.vl(ratio),
                    ],
                    ["vs2", "vs1", "vl"],
                ),
                lambda variant, vreg_type, ratio, param_list: (
                    fixed_body(variant, inst, param_list)
                ),
                require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
                    allowed_type_category,
                    vreg_type,
                    ratio,
                    narrowing=inst in ["vnclip", "vnclipu"],
                ),
                modifier="const",
            ),
            func.template_vreg_ratio(
                lambda vreg_type, _: dest_type(vreg_type),
                "operator()",
                lambda variant, vreg_type, ratio: func.vreg_ratio_param_list(
                    dest_type(vreg_type),
                    ratio,
                    variant,
                    [
                        vreg_type,
                        (
                            misc.size_t
                            if inst in ["vssra", "vssrl", "vnclip", "vnclipu"]
                            else vreg.get_elem(vreg_type)
                        ),
                        vl.vl(ratio),
                    ],
                    ["vs2", "rs1", "vl"],
                ),
                lambda variant, vreg_type, ratio, param_list: (
                    fixed_body(variant, inst, param_list)
                ),
                require_clauses=lambda vreg_type, ratio: ops.vreg_require_clauses(
                    allowed_type_category,
                    vreg_type,
                    ratio,
                    narrowing=inst in ["vnclip", "vnclipu"],
                ),
                modifier="const",
            ),
        ],
        requires_clauses=[constraints.supported_vxrm(vxrm)],
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
                            [fixed_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 4.3. Vector Single-Width Fractional Multiply with Rounding and Saturation Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vsmul"],
                            [fixed_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 4.4. Vector Single-Width Scaling Shift Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vssra", "vssrl"],
                            [fixed_op],
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 4.5. Vector Narrowing Fixed-Point Clip Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vnclip", "vnclipu"],
                            [fixed_op],
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
