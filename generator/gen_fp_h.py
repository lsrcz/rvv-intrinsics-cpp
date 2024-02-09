from codegen import header, main, ops


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
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_fp_header)
