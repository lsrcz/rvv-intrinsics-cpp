from typing import Callable
from codegen import header, main, ops, func


def widening_vf_op(
    inst: str, need_suffix: bool = True
) -> Callable[[str], func.Function]:
    return ops.op(
        (inst, f"__riscv_{inst}_vf") if need_suffix else inst,
        "fp",
        "w",
        ["v", "e"],
    )


def widening_vf_no_suffix_op(inst: str) -> Callable[[str], func.Function]:
    return widening_vf_op(inst, False)


def widening_wf_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(
        (inst, f"__riscv_{inst}_wf"),
        "fp",
        "v",
        ["v", "en"],
    )


def widening_vv_op(
    inst: str, need_suffix: bool = True
) -> Callable[[str], func.Function]:
    return ops.op(
        (inst, f"__riscv_{inst}_vv") if need_suffix else inst,
        "fp",
        "w",
        ["v", "v"],
    )


def widening_vv_no_suffix_op(inst: str) -> Callable[[str], func.Function]:
    return widening_vv_op(inst, False)


def widening_wv_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(
        (inst, f"__riscv_{inst}_wv"),
        "fp",
        "v",
        ["v", "n"],
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
                            ops.bin_part,
                            ["vfadd", "vfsub"],
                            ["fp"],
                            [ops.simple_vx_op, ops.simple_vv_op],
                        ),
                        header.WithVariants(ops.simple_vx_op("vfrsub", "fp")),
                        header.WithVariants(
                            ops.op("vfneg", "fp", "v", ["v"], names=["vs"])
                        ),
                        "// 5.2. Vector Widening Floating-Point Add/Subtract Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vfwadd", "vfwsub"],
                            [
                                widening_vv_op,
                                widening_vf_op,
                                widening_wv_op,
                                widening_wf_op,
                            ],
                        ),
                        "// 5.3. Vector Single-Width Floating-Point Multiply/Divide Intrinsics",
                        header.CrossProduct(
                            ops.bin_part,
                            ["vfmul", "vfdiv"],
                            ["fp"],
                            [ops.simple_vx_op, ops.simple_vv_op],
                        ),
                        header.WithVariants(ops.simple_vx_op("vfrdiv", "fp")),
                        "// 5.4. Vector Widening Floating-Point Multiply Intrinsics",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vfwmul"],
                            [
                                widening_vv_no_suffix_op,
                                widening_vf_no_suffix_op,
                            ],
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
                            [ops.fma_vv_op, ops.fma_vx_op],
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
                            [ops.widening_fma_vv_op, ops.widening_fma_vx_op],
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_fp_header)
