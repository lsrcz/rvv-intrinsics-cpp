from typing import Callable

from codegen import func, header, main, ops


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
                        header.WithVariants(ops.vx_op("vadd", "int")),
                        header.WithVariants(ops.vv_op("vadd", "int")),
                        header.WithVariants(ops.vx_op("vsub", "int")),
                        header.WithVariants(ops.vv_op("vsub", "int")),
                        header.WithVariants(ops.vx_op("vrsub", "int")),
                        header.WithVariants(ops.v_op("vneg", "int")),
                        "// 3.2. Vector Widening Integer Add/Subtract Intrinsics",
                        header.CrossProduct(
                            widening_part,
                            ["vwadd", "vwsub"],
                            [True, False],
                            [
                                ops.widening_vv_op,
                                ops.widening_vx_op,
                                ops.widening_wv_op,
                                ops.widening_wx_op,
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
