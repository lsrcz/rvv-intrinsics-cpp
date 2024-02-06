from codegen import macro


def test_for_all_skip() -> None:
    assert (
        macro.for_all([1, 2, 3, 4], lambda x: str(x) if x % 2 == 0 else None)
        == "2\n4"
    )


def test_for_all_elem() -> None:
    assert (
        macro.for_all_elem(lambda x: x)
        == """uint8_t
uint16_t
uint32_t
uint64_t
int8_t
int16_t
int32_t
int64_t
float16_t
float32_t
float64_t"""
    )


def test_for_all_lmul() -> None:
    assert (
        macro.for_all_lmul(lambda x: x)
        == """LMul::kM8
LMul::kM4
LMul::kM2
LMul::kM1
LMul::kMF2
LMul::kMF4
LMul::kMF8"""
    )


def test_for_all_ratio() -> None:
    assert (
        macro.for_all_ratio(lambda x: x)
        == """1
2
4
8
16
32
64"""
    )


def test_for_all_elem_size() -> None:
    assert (
        macro.for_all_elem_size(lambda x: str(x))
        == """8
16
32
64"""
    )
