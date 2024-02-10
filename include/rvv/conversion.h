#ifndef RVV_CONVERSION_H_
#define RVV_CONVERSION_H_

#include <rvv/type.h>

namespace rvv {

// General conversion facilities.
template <template <typename T> typename Convert, typename T>
concept ConvertibleElement = SupportedElement<T, false> &&
                             SupportedElement<typename Convert<T>::Type, false>;

template <template <typename T> typename ConvertElement, typename V>
concept ConvertibleVReg =
    SupportedVReg<V, false> && ConvertibleElement<ConvertElement, elem_t<V>> &&
    CompatibleElemRatio<typename ConvertElement<elem_t<V>>::Type, ratio<V>>;

template <template <typename T> typename ConvertElement, typename V>
concept Convertible =
    ConvertibleElement<ConvertElement, V> || ConvertibleVReg<ConvertElement, V>;

namespace internal {
template <template <typename T> typename ConvertElement, typename T>
  requires Convertible<ConvertElement, T>
struct ConvertType;
template <template <typename T> typename ConvertElement, typename E>
  requires ConvertibleElement<ConvertElement, E>
struct ConvertType<ConvertElement, E> {
  using Type = typename ConvertElement<E>::Type;
};
template <template <typename T> typename ConvertElement, typename V>
  requires ConvertibleVReg<ConvertElement, V>
struct ConvertType<ConvertElement, V> {
  using Type = vreg_t<typename ConvertElement<elem_t<V>>::Type, ratio<V>>;
};
}  // namespace internal

template <template <typename T> typename ConvertElement, typename T>
using convert_t = typename internal::ConvertType<ConvertElement, T>::Type;

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

template <typename T>
concept ConvertibleToUnsigned = Convertible<internal::ToUnsignedElement, T>;

template <typename T>
  requires ConvertibleToUnsigned<T>
using to_unsigned_t =
    typename internal::ConvertType<internal::ToUnsignedElement, T>::Type;

template <typename T>
concept ConvertibleToSigned = Convertible<internal::ToSignedElement, T>;

template <typename T>
  requires ConvertibleToSigned<T>
using to_signed_t =
    typename internal::ConvertType<internal::ToSignedElement, T>::Type;

template <typename T>
concept ConvertibleToFloatingPoint =
    Convertible<internal::ToFloatingPointElement, T>;

template <typename T>
  requires ConvertibleToFloatingPoint<T>
using to_float_t =
    typename internal::ConvertType<internal::ToFloatingPointElement, T>::Type;

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

template <typename T>
concept Widenable = Convertible<internal::WidenedElementType, T>;

template <typename T>
  requires Widenable<T>
using widen_t = convert_t<internal::WidenedElementType, T>;

template <typename T>
concept Widenable2 = Widenable<T>;

template <typename T>
concept Widenable4 = Widenable<T> && Widenable<widen_t<T>>;

template <typename T>
concept Widenable8 =
    Widenable<T> && Widenable<widen_t<T>> && Widenable<widen_t<widen_t<T>>>;

namespace internal {
template <size_t kN>
struct WidenedNType;
template <>
struct WidenedNType<2> {
  template <typename T>
    requires Widenable2<T>
  using Type = widen_t<T>;
};
template <>
struct WidenedNType<4> {
  template <typename T>
    requires Widenable4<T>
  using Type = widen_t<widen_t<T>>;
};
template <>
struct WidenedNType<8> {
  template <typename T>
    requires Widenable8<T>
  using Type = widen_t<widen_t<widen_t<T>>>;
};
}  // namespace internal

template <size_t kN, typename T>
using widen_n_t = typename internal::WidenedNType<kN>::template Type<T>;

template <size_t kN, typename T>
concept WidenableN = (kN == 2   ? Widenable2<T>
                      : kN == 4 ? Widenable4<T>
                      : kN == 8 ? Widenable8<T>
                                : false);

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

template <typename T>
concept Narrowable = Convertible<internal::NarrowElementType, T>;

template <typename T>
  requires Narrowable<T>
using narrow_t = convert_t<internal::NarrowElementType, T>;

}  // namespace rvv

#endif  // RVV_CONVERSION_H_
