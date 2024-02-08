// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_TYPE_TRAITS_H_
#define RVV_TYPE_TRAITS_H_

#include <rvv/config.h>
#include <stddef.h>
#include <stdint.h>

#include <type_traits>

namespace rvv {
template <typename E, typename... Es>
concept AnyOf = (... || std::is_same_v<E, Es>);

#if HAS_FLOAT16
template <typename E>
concept IsFloat16 = std::is_same_v<E, float16_t>;
#endif

template <typename E>
concept IsFloat32 = std::is_same_v<E, float>;

template <typename E>
concept IsFloat64 = std::is_same_v<E, double>;

template <typename E>
concept IsFloatingPoint =
#if HAS_FLOAT16
    IsFloat16<E> ||
#endif
    IsFloat32<E> || IsFloat64<E>;

template <typename E>
concept IsUnsigned = AnyOf<E, uint8_t, uint16_t, uint32_t, uint64_t>;

template <typename E>
concept IsSigned = AnyOf<E, int8_t, int16_t, int32_t, int64_t>;

template <typename E>
concept IsIntegral = IsSigned<E> || IsUnsigned<E>;

template <typename E, bool kNeedZvfh>
concept NeedUnsupportedZvfh =
#if HAS_ZVFH
    false;
#elif HAS_ZVFHMIN
    kNeedZvfh;
#elif HAS_FLOAT16
    std::is_same_v<E, _Float16>;
#else
    false;
#endif

template <typename E>
concept NeedUnsupportedZve32f =
#if HAS_ZVE32F
    false;
#else
    std::is_same_v<E, float>;
#endif

template <typename E>
concept NeedUnsupportedZve64d =
#if HAS_ZVE64D
    false;
#else
    std::is_same_v<E, double>;
#endif

template <typename E>
concept NeedUnsupportedZve64x =
#if HAS_ZVE64X
    false;
#else
    AnyOf<E, int64_t, uint64_t>;
#endif

template <typename E>
concept SupportedIntegralElement = !NeedUnsupportedZve64x<E> && IsIntegral<E>;

template <typename E>
concept SupportedSignedElement = SupportedIntegralElement<E> && IsSigned<E>;

template <typename E>
concept SupportedUnsignedElement = SupportedIntegralElement<E> && IsUnsigned<E>;

template <typename E, bool kNeedZvfh>
concept SupportedFloatingPointElement =
    !NeedUnsupportedZvfh<E, kNeedZvfh> && !NeedUnsupportedZve32f<E> &&
    !NeedUnsupportedZve64d<E> && IsFloatingPoint<E>;

template <typename E, bool kNeedZvfh>
concept SupportedElement =
    !NeedUnsupportedZvfh<E, kNeedZvfh> && !NeedUnsupportedZve32f<E> &&
    !NeedUnsupportedZve64d<E> && !NeedUnsupportedZve64x<E> &&
    (IsIntegral<E> || IsFloatingPoint<E>);

template <size_t kRatio>
concept NeedUnsupportedElen64 = kRatio == 64 && !HAS_ELEN64;

template <size_t kRatio>
concept SupportedRatio =
    (kRatio == 1 || kRatio == 2 || kRatio == 4 || kRatio == 8 || kRatio == 16 ||
     kRatio == 32 || kRatio == 64) &&
    !NeedUnsupportedElen64<kRatio>;

}  // namespace rvv

#endif  // RVV_TYPE_TRAITS_H_
