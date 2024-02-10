#ifndef RVV_CONVERSION_H_
#define RVV_CONVERSION_H_

#include <rvv/type.h>

namespace rvv {

// General conversion facilities.
template <template <typename T> typename Convert, typename T, bool kNeedZvfh>
concept ConvertibleElement = SupportedElement<T, kNeedZvfh> &&
                             SupportedElement<typename Convert<T>::Type, false>;

template <template <typename T> typename ConvertElement, typename V,
          bool kNeedZvfh>
concept ConvertibleVReg =
    SupportedVReg<V, kNeedZvfh> &&
    ConvertibleElement<ConvertElement, elem_t<V>, kNeedZvfh> &&
    CompatibleElemRatio<typename ConvertElement<elem_t<V>>::Type, ratio<V>>;

template <template <typename T> typename ConvertElement, typename V,
          bool kNeedZvfh>
concept Convertible = ConvertibleElement<ConvertElement, V, kNeedZvfh> ||
                      ConvertibleVReg<ConvertElement, V, kNeedZvfh>;

namespace internal {
template <template <typename T> typename ConvertElement, typename T,
          bool kNeedZvfh>
  requires Convertible<ConvertElement, T, kNeedZvfh>
struct ConvertType;
template <template <typename T> typename ConvertElement, typename E,
          bool kNeedZvfh>
  requires ConvertibleElement<ConvertElement, E, kNeedZvfh>
struct ConvertType<ConvertElement, E, kNeedZvfh> {
  using Type = typename ConvertElement<E>::Type;
};
template <template <typename T> typename ConvertElement, typename V,
          bool kNeedZvfh>
  requires ConvertibleVReg<ConvertElement, V, kNeedZvfh>
struct ConvertType<ConvertElement, V, kNeedZvfh> {
  using Type = vreg_t<typename ConvertElement<elem_t<V>>::Type, ratio<V>>;
};
}  // namespace internal

template <template <typename T> typename ConvertElement, typename T,
          bool kNeedZvfh>
using convert_t =
    typename internal::ConvertType<ConvertElement, T, kNeedZvfh>::Type;

// Conversion between signed, unsigned, and floating points.
namespace internal {
template <typename E>
  requires IsElement<E>
struct ToUnsignedElement {
  using Type = UnsignedType<sizeof(E) * 8>::Type;
};
template <typename E>
  requires IsElement<E>
struct ToSignedElement {
  using Type = SignedType<sizeof(E) * 8>::Type;
};
template <typename E>
  requires IsElement<E>
struct ToFloatingPointElement {
  using Type = FloatingPointType<sizeof(E) * 8>::Type;
};
}  // namespace internal

template <typename T, bool kNeedZvfh>
concept ConvertibleToUnsigned =
    Convertible<internal::ToUnsignedElement, T, kNeedZvfh>;

template <typename T, bool kNeedZvfh = true>
  requires ConvertibleToUnsigned<T, kNeedZvfh>
using to_unsigned_t =
    typename internal::ConvertType<internal::ToUnsignedElement, T,
                                   kNeedZvfh>::Type;

template <typename T, bool kNeedZvfh>
concept ConvertibleToSigned =
    Convertible<internal::ToSignedElement, T, kNeedZvfh>;

template <typename T, bool kNeedZvfh = true>
  requires ConvertibleToSigned<T, kNeedZvfh>
using to_signed_t = typename internal::ConvertType<internal::ToSignedElement, T,
                                                   kNeedZvfh>::Type;

template <typename T, bool kNeedZvfh>
concept ConvertibleToFloatingPoint =
    Convertible<internal::ToFloatingPointElement, T, kNeedZvfh>;

template <typename T, bool kNeedZvfh = true>
  requires ConvertibleToFloatingPoint<T, kNeedZvfh>
using to_float_t =
    typename internal::ConvertType<internal::ToFloatingPointElement, T,
                                   kNeedZvfh>::Type;

// Widening conversion.
namespace internal {

template <typename E>
  requires IsElement<E>
struct WidenedElementType {
  using Type = std::conditional_t<
      IsUnsigned<E>, typename UnsignedType<sizeof(E) * 2 * 8>::Type,
      std::conditional_t<IsSigned<E>,
                         typename SignedType<sizeof(E) * 2 * 8>::Type,
                         typename FloatingPointType<sizeof(E) * 2 * 8>::Type>>;
};

}  // namespace internal

template <typename T, bool kNeedZvfh>
concept Widenable = Convertible<internal::WidenedElementType, T, kNeedZvfh>;

template <typename T, bool kNeedZvfh = true>
  requires Widenable<T, kNeedZvfh>
using widen_t = convert_t<internal::WidenedElementType, T, kNeedZvfh>;

template <typename T, bool kNeedZvfh>
concept Widenable2 = Widenable<T, kNeedZvfh>;

template <typename T, bool kNeedZvfh>
concept Widenable4 =
    Widenable<T, kNeedZvfh> && Widenable<widen_t<T, kNeedZvfh>, kNeedZvfh>;

template <typename T, bool kNeedZvfh>
concept Widenable8 =
    Widenable<T, kNeedZvfh> && Widenable<widen_t<T, kNeedZvfh>, kNeedZvfh> &&
    Widenable<widen_t<widen_t<T, kNeedZvfh>, kNeedZvfh>, kNeedZvfh>;

namespace internal {
template <size_t kN, bool kNeedZvfh>
struct WidenedNType;
template <bool kNeedZvfh>
struct WidenedNType<2, kNeedZvfh> {
  template <typename T>
    requires Widenable2<T, kNeedZvfh>
  using Type = widen_t<T, kNeedZvfh>;
};
template <bool kNeedZvfh>
struct WidenedNType<4, kNeedZvfh> {
  template <typename T>
    requires Widenable4<T, kNeedZvfh>
  using Type = widen_t<widen_t<T, kNeedZvfh>, kNeedZvfh>;
};
template <bool kNeedZvfh>
struct WidenedNType<8, kNeedZvfh> {
  template <typename T>
    requires Widenable8<T, kNeedZvfh>
  using Type = widen_t<widen_t<widen_t<T, kNeedZvfh>, kNeedZvfh>, kNeedZvfh>;
};
}  // namespace internal

template <size_t kN, typename T, bool kNeedZvfh>
concept WidenableN = (kN == 2   ? Widenable2<T, kNeedZvfh>
                      : kN == 4 ? Widenable4<T, kNeedZvfh>
                      : kN == 8 ? Widenable8<T, kNeedZvfh>
                                : false);
template <size_t kN, typename T, bool kNeedZvfh = true>
  requires WidenableN<kN, T, kNeedZvfh>
using widen_n_t =
    typename internal::WidenedNType<kN, kNeedZvfh>::template Type<T>;

// Narrowing conversion
namespace internal {
template <typename E>
  requires IsElement<E>
struct NarrowElementType {
  using Type = std::conditional_t<
      IsUnsigned<E>, typename UnsignedType<sizeof(E) * 4>::Type,
      std::conditional_t<IsSigned<E>, typename SignedType<sizeof(E) * 4>::Type,
                         typename FloatingPointType<sizeof(E) * 4>::Type>>;
};
}  // namespace internal

template <typename T, bool kNeedZvfh>
concept Narrowable = Convertible<internal::NarrowElementType, T, kNeedZvfh>;

template <typename T, bool kNeedZvfh = true>
  requires Narrowable<T, kNeedZvfh>
using narrow_t = convert_t<internal::NarrowElementType, T, kNeedZvfh>;

}  // namespace rvv

#endif  // RVV_CONVERSION_H_
