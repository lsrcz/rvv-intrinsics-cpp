from codegen import header, ops, main

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
                        header.WithVariants(ops.vi_op("vadd", "int")),
                        header.WithVariants(ops.vv_op("vadd", "int")),
                        header.WithVariants(ops.vi_op("vsub", "int")),
                        header.WithVariants(ops.vv_op("vsub", "int")),
                        header.WithVariants(ops.vi_op("vrsub", "int")),
                        header.WithVariants(ops.v_op("vneg", "int")),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_int_header)
