from typing import Callable
from codegen import header, main, ops, func


def widening_vf_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(
        (inst, f"__riscv_{inst}_vf"),
        "fp",
        "w",
        ["v", "e"],
    )


def widening_wf_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(
        (inst, f"__riscv_{inst}_wf"),
        "fp",
        "v",
        ["v", "en"],
    )


def widening_vv_op(inst: str) -> Callable[[str], func.Function]:
    return ops.op(
        (inst, f"__riscv_{inst}_vv"),
        "fp",
        "w",
        ["v", "v"],
    )


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
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_fp_header)
