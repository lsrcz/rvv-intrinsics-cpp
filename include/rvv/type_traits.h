// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_TYPE_TRAITS_H_
#define RVV_TYPE_TRAITS_H_

#include <rvv/config.h>
#include <stddef.h>
#include <stdint.h>

#include <type_traits>

namespace rvv {
template <typename E, typename... Es>
concept is_any = (... || std::is_same_v<E, Es>);

#if HAS_FLOAT16
template <typename E>
concept is_float16 = std::is_same_v<E, float16_t>;
#endif

template <typename E>
concept is_float32 = std::is_same_v<E, float>;

template <typename E>
concept is_float64 = std::is_same_v<E, double>;

template <typename E>
concept is_rvv_floating_point =
#if HAS_FLOAT16
    is_float16<E> ||
#endif
    is_float32<E> || is_float64<E>;

template <typename E>
concept is_rvv_unsigned = is_any<E, uint8_t, uint16_t, uint32_t, uint64_t>;

template <typename E>
concept is_rvv_signed = is_any<E, int8_t, int16_t, int32_t, int64_t>;

template <typename E>
concept is_rvv_integral = is_rvv_signed<E> || is_rvv_unsigned<E>;

template <typename E, bool kNeedZvfh>
concept relies_on_unsupported_zvfh =
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
concept relies_on_unsupported_zve32f =
#if HAS_ZVE32F
    false;
#else
    std::is_same_v<E, float>;
#endif

template <typename E>
concept relies_on_unsupported_zve64d =
#if HAS_ZVE64D
    false;
#else
    std::is_same_v<E, double>;
#endif

template <typename E>
concept relies_on_unsupported_zve64x =
#if HAS_ZVE64X
    false;
#else
    is_any<E, int64_t, uint64_t>;
#endif

template <typename E>
concept is_supported_rvv_integral =
    !relies_on_unsupported_zve64x<E> && is_rvv_integral<E>;

template <typename E>
concept is_supported_rvv_signed =
    is_supported_rvv_integral<E> && is_rvv_signed<E>;

template <typename E>
concept is_supported_rvv_unsigned =
    is_supported_rvv_integral<E> && is_rvv_unsigned<E>;

template <typename E, bool kNeedZvfh>
concept is_supported_rvv_floating_point =
    !relies_on_unsupported_zvfh<E, kNeedZvfh> &&
    !relies_on_unsupported_zve32f<E> && !relies_on_unsupported_zve64d<E> &&
    is_rvv_floating_point<E>;

template <typename E, bool kNeedZvfh>
concept is_supported_rvv_elem_type =
    !relies_on_unsupported_zvfh<E, kNeedZvfh> &&
    !relies_on_unsupported_zve32f<E> && !relies_on_unsupported_zve64d<E> &&
    !relies_on_unsupported_zve64x<E> &&
    (is_rvv_integral<E> || is_rvv_floating_point<E>);

template <size_t kRatio>
concept relies_on_unsupported_elen64 = kRatio == 64 && !HAS_ELEN64;

template <size_t kRatio>
concept is_supported_ratio =
    (kRatio == 1 || kRatio == 2 || kRatio == 4 || kRatio == 8 || kRatio == 16 ||
     kRatio == 32 || kRatio == 64) &&
    !relies_on_unsupported_elen64<kRatio>;

}  // namespace rvv

#endif  // RVV_TYPE_TRAITS_H_
