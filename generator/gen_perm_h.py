from typing import Callable
from codegen.param_list import function
from codegen import constraints, header, main, func, ops
from codegen.typing import elem, misc, vreg


def s_x_move_part(
    inst_pair: tuple[str, str],
    elem_type: elem.RawElemType,
    ratio: misc.LitSizeTValue,
) -> header.WithVariants:
    return header.WithVariants(ops.v_scalar_move(inst_pair, elem_type, ratio))


def mv_reg_to_scalar(inst_pair: tuple[str, str]) -> func.Function:
    rvv_inst = inst_pair[1]
    inst = inst_pair[0]

    vreg_type = vreg.param("V")
    return func.Function(
        vreg.get_elem(vreg_type),
        inst,
        function.param_list([vreg_type], ["vs1"]),
        f"  return {rvv_inst}(vs1);",
        template_param_list=func.template.TemplateTypeParamList(vreg_type),
        require_clauses=[
            (
                constraints.supported_floating_point_vreg(vreg_type, True)
                if inst == "vfmv_f"
                else constraints.supported_integral_vreg(vreg_type)
            )
        ],
    )


def vslide1_op(inst: str) -> Callable[[str], func.Function]:
    allowed_type_category = "fp" if inst.startswith("vf") else "int"
    return ops.op(
        inst,
        allowed_type_category,
        "v",
        ["v", "e"],
    )


def vrgather_vv_op(variant: str) -> func.Function:
    return ops.op(
        "vrgather",
        "all",
        "v",
        ["v", "u"],
        extra_requires_clauses=lambda vreg_type, ratio: [
            constraints.does_not_have_width(vreg.get_elem(vreg_type), 16)
        ],
    )(variant)


def vrgather_ve_op(variant: str) -> func.Function:
    return ops.op(
        "vrgather",
        "all",
        "v",
        ["v", "size"],
        names=["vs2", "vs1"],
    )(variant)


def vrgather_ei16_op(variant: str) -> func.Function:
    return ops.op(
        ("vrgather", "__riscv_vrgatherei16"),
        "all",
        "v",
        ["v", "u16"],
        names=["vs2", "vs1"],
    )(variant)


def vcompress_op(variant: str) -> func.Function:
    return ops.op(
        "vcompress",
        "all",
        "v",
        ["v", "m"],
    )(variant)


rvv_perm_h = header.Header(
    [
        header.Include("rvv/elem.h"),
        header.Include("rvv/conversion.h"),
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 8. Vector Permutation Intrinsics",
                        "// 8.1. Integer and Floating-Point Scalar Move Intrinsics",
                        header.CrossProduct(
                            s_x_move_part,
                            [("vfmv_s", "__riscv_vfmv_s_f")],
                            elem.ALL_FLOAT_TYPES,
                            misc.ALL_RATIO,
                            allowed_variants={"", "tu"},
                        ),
                        header.CrossProduct(
                            s_x_move_part,
                            [("vmv_s", "__riscv_vmv_s_x")],
                            elem.ALL_INT_TYPES,
                            misc.ALL_RATIO,
                            allowed_variants={"", "tu"},
                        ),
                        header.CrossProduct(
                            mv_reg_to_scalar,
                            [
                                ("vfmv_f", "__riscv_vfmv_f"),
                                ("vmv_x", "__riscv_vmv_x"),
                            ],
                            allowed_variants={""},
                        ),
                        "// 8.2. Vector Slideup Intrinsics",
                        header.WithVariants(
                            ops.op(
                                "vslideup",
                                "all",
                                "v",
                                ["v", "size"],
                                have_dest_arg=True,
                            )
                        ),
                        "// 8.3. Vector Slidedown Intrinsics",
                        header.WithVariants(
                            ops.op(
                                "vslidedown",
                                "all",
                                "v",
                                ["v", "size"],
                            )
                        ),
                        "// 8.4. Vector Slide1up and Slide1down Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            [
                                "vslide1up",
                                "vslide1down",
                                "vfslide1up",
                                "vfslide1down",
                            ],
                            [vslide1_op],
                        ),
                        "// 8.5. Vector Register Gather Intrinsics",
                        header.CrossProduct(
                            header.WithVariants,
                            [vrgather_vv_op, vrgather_ve_op, vrgather_ei16_op],
                        ),
                        "// 8.6. Vector Compress Intrinsics",
                        header.WithVariants(
                            vcompress_op, allowed_variants={"", "tu"}
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_perm_h)
