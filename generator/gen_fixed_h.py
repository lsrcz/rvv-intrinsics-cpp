from codegen import header, main, ops

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
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_fixed_header)
