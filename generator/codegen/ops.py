from typing import Callable, Sequence

from codegen import constraints, func, header, ops
from codegen.param_list import function
from codegen.typing import base, misc, vl, vmask, vreg


def vreg_require_clauses(
    allowed_type_category: str,
    vreg_type: vreg.VRegType,
    ratio: misc.SizeTValue,
    widening: bool | int = False,
    narrowing: bool = False,
) -> list[str]:
    ret: list[str] = []
    match allowed_type_category:
        case "int":
            ret.append(constraints.supported_integral_vreg(vreg_type))
        case "signed":
            ret.append(constraints.supported_signed_vreg(vreg_type))
        case "unsigned":
            ret.append(constraints.supported_unsigned_vreg(vreg_type))
        case "fp":
            ret.append(
                constraints.supported_floating_point_vreg(vreg_type, True)
            )
        case "all":
            pass
        case _:
            raise ValueError(
                f"Unknown allowed type category: {allowed_type_category}"
            )
    ret.append(constraints.compatible_vreg_ratio(vreg_type, ratio))
    if widening is True:
        ret.append(constraints.widenable(vreg_type))
        ret.append(
            constraints.compatible_vreg_ratio(vreg.widen(vreg_type), ratio)
        )
    elif widening in [2, 4, 8]:
        ret.append(constraints.widenable_n(widening, vreg_type))
        ret.append(
            constraints.compatible_vreg_ratio(
                vreg.widen_n(widening, vreg_type), ratio
            )
        )
    elif narrowing:
        ret.append(constraints.narrowable(vreg_type))
        ret.append(
            constraints.compatible_vreg_ratio(vreg.narrow(vreg_type), ratio)
        )
    return ret


def parse_type(
    vreg_type: vreg.VRegType, ratio: misc.SizeTValue, c: str
) -> base.Type:
    match c:
        case "v":
            return vreg_type
        case "w":
            return vreg.widen(vreg_type)
        case "ws":
            return vreg.widen(vreg.to_signed(vreg_type))
        case "2":
            return vreg.widen_n(2, vreg_type)
        case "4":
            return vreg.widen_n(4, vreg_type)
        case "8":
            return vreg.widen_n(8, vreg_type)
        case "n":
            return vreg.narrow(vreg_type)
        case "u":
            return vreg.to_unsigned(vreg_type)
        case "nu":
            return vreg.narrow(vreg.to_unsigned(vreg_type))
        case "ns":
            return vreg.narrow(vreg.to_signed(vreg_type))
        case "size":
            return misc.size_t
        case "e":
            return vreg.get_elem(vreg_type)
        case "en":
            return vreg.get_elem(vreg.narrow(vreg_type))
        case "eu":
            return vreg.get_elem(vreg.to_unsigned(vreg_type))
        case "es":
            return vreg.get_elem(vreg.to_signed(vreg_type))
        case "m":
            return vmask.vmask(ratio)
        case _:
            raise ValueError(f"Unknown type category: {c}")


def parse_name(
    c: str,
    *,
    name_num: str = "",
) -> str:
    match c:
        case "v" | "w" | "ws" | "n" | "u" | "nu" | "ns":
            return f"vs{name_num}"
        case "size" | "e" | "en" | "eu" | "es":
            return f"rs{name_num}"
        case "m":
            return f"v{name_num}"
        case _:
            raise ValueError(f"Unknown type category for naming: {c}")


def parse_type_list(
    vreg_type: vreg.VRegType,
    ratio: misc.SizeTValue,
    arg_type_spec: list[str],
    *,
    names: Sequence[str] = tuple(),
    name_nums: str = "",
) -> function.FunctionTypedParamList:
    types = [parse_type(vreg_type, ratio, c) for c in arg_type_spec]
    if len(names) == 0:
        assert len(name_nums) >= len(arg_type_spec)
        names = [
            parse_name(c, name_num=n) for c, n in zip(arg_type_spec, name_nums)
        ]
    return function.param_list(types, names)


def op(
    inst: str | tuple[str, str],
    allowed_type_category: str,
    ret_type_spec: str,
    arg_type_spec: list[str],
    *,
    have_dest_arg: bool = False,
    names: Sequence[str] = tuple(),
) -> Callable[[str], func.Function]:
    if isinstance(inst, str):
        rvv_inst = f"__riscv_{inst}"
    else:
        rvv_inst = inst[1]
        inst = inst[0]

    def ret_type(vreg_type: vreg.VRegType, ratio: misc.SizeTValue) -> base.Type:
        return parse_type(vreg_type, ratio, ret_type_spec)

    def function_param_list(
        variant: str, vreg_type: vreg.VRegType, ratio: misc.SizeTValue
    ) -> function.FunctionTypedParamList:
        base_list = parse_type_list(
            vreg_type,
            ratio,
            arg_type_spec,
            names=names,
            name_nums="210" if len(names) == 0 else "",
        ) + (vl.vl(ratio), "vl")
        dest_type = ret_type(vreg_type, ratio)
        return func.vreg_ratio_extend_param_list(
            dest_type,
            ratio,
            variant,
            (
                function.param_list([dest_type], ["vd"]) + base_list
                if have_dest_arg
                else base_list
            ),
            undisturbed_need_dest_arg=not have_dest_arg,
        )

    if "w" in arg_type_spec or "w" == ret_type_spec:
        widening = True
    elif ret_type_spec in ["2", "4", "8"]:
        widening = int(ret_type_spec)
    else:
        widening = False
    return func.template_vreg_ratio(
        ret_type,
        inst,
        function_param_list,
        lambda variant, vreg_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                rvv_inst + func.rvv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
            allowed_type_category,
            vreg_type,
            ratio,
            narrowing="n" in arg_type_spec
            or "en" in arg_type_spec
            or "n" == ret_type_spec,
            widening=widening,
        ),
    )


def bin_part(
    inst: str,
    allowed_type_category: str,
    f: Callable[[str, str], Callable[[str], func.Function]],
) -> header.HeaderPart:
    return header.WithVariants(f(inst, allowed_type_category))


def simple_vx_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", ["v", "e"])


def simple_vv_op(
    inst: str,
    allowed_type_category: str,
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", ["v", "v"])


def simple_v_op(
    inst: str, allowed_type_category: str
) -> Callable[[str], func.Function]:
    return ops.op(inst, allowed_type_category, "v", ["v"], names=["vs"])


def sign_aware_vx_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "v",
        ["v", "e"],
    )


def fma_vx_op(
    inst: str,
) -> Callable[[str], func.Function]:
    if inst.startswith("vf"):
        allowed_type_category = "fp"
    else:
        allowed_type_category = "int"
    return ops.op(
        inst,
        allowed_type_category,
        "v",
        ["e", "v"],
        names=["rs1", "vs2"],
        have_dest_arg=True,
    )


def fma_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    if inst.startswith("vf"):
        allowed_type_category = "fp"
    else:
        allowed_type_category = "int"
    return ops.op(
        inst,
        allowed_type_category,
        "v",
        ["v", "v"],
        names=["vs1", "vs2"],
        have_dest_arg=True,
    )


def sign_aware_vv_op(
    inst: str,
) -> Callable[[str], func.Function]:
    return ops.op(
        inst,
        "unsigned" if inst.endswith("u") else "signed",
        "v",
        ["v", "v"],
    )


def inferred_type_part(
    inst: str,
    f: Callable[[str], Callable[[str], func.Function]],
) -> header.HeaderPart:
    return header.WithVariants(f(inst))
