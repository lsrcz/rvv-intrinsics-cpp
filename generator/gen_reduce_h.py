from typing import Callable
from codegen import header, main, ops, func


def reduce_vv_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "m1", ["v", "m1"])


def sign_aware_reduce_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "m1",
        ["v", "m1"],
    )


def widening_fp_reduce_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, "fp", "wm1", ["v", "wm1"])


def sign_aware_widening_reduce_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "wm1",
        ["v", "wm1"],
    )


rvv_reduce_header = header.Header(
    [
        header.Include("rvv/elem.h"),
        header.Include("rvv/conversion.h"),
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 6. Vector Reduction operations",
                        "// 6.1. Vector Single-Width Integer Reduction Intrinsics",
                        header.CrossProduct(
                            ops.bin_part,
                            ["vredsum", "vredand", "vredor", "vredxor"],
                            ["int"],
                            [reduce_vv_op],
                            allowed_variants={"", "m", "tu", "tum"},
                        ),
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vredmax", "vredmaxu", "vredmin", "vredminu"],
                            [sign_aware_reduce_vv_op],
                            allowed_variants={"", "m", "tu", "tum"},
                        ),
                        "// 6.2. Vector Widening Integer Reduction Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vwredsum", "vwredsumu"],
                            [sign_aware_widening_reduce_vv_op],
                            allowed_variants={"", "m", "tu", "tum"},
                        ),
                        "// 6.3. Vector Single-Width Floating-Point Reduction Intrinsics",
                        header.CrossProduct(
                            ops.bin_part,
                            ["vfredosum", "vfredusum", "vfredmax", "vfredmin"],
                            ["fp"],
                            [reduce_vv_op],
                            allowed_variants={"", "m", "tu", "tum"},
                        ),
                        "// 6.4. Vector Widening Floating-Point Reduction Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vfwredosum", "vfwredusum"],
                            [widening_fp_reduce_vv_op],
                            allowed_variants={"", "m", "tu", "tum"},
                        ),
                    ],
                )
            ],
        ),
    ]
)


if __name__ == "__main__":
    main.main(rvv_reduce_header)
