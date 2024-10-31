from email.policy import default
from types import FunctionType
from typing import Any, Dict

CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    arg_names = func.__code__.co_varnames
    defaults = func.__defaults__
    default_kws = func.__kwdefaults__
    num_of_args = len(arg_names)
    num_of_pos_args = len(args)
    res = {}
    num_of_kwonly_args = func.__code__.co_kwonlyargcount
    h = func.__code__
    has_pos = args is not None and  len(args) > 0
    has_def_pos = defaults is not None and len(defaults) > 0
    has_kw = kwargs is not None and  len(kwargs) > 0
    has_def_kw = default_kws is not None and  len(default_kws) > 0
    has_args = bool(func.__code__.co_flags & CO_VARARGS)
    has_kwargs = bool(func.__code__.co_flags & CO_VARKEYWORDS)
    num_of_keys = len(kwargs)
    """Raising error"""
    if not has_args and num_of_pos_args > num_of_args:
        raise TypeError(ERR_TOO_MANY_POS_ARGS)
    if not has_args and num_of_kwonly_args + len(args) > num_of_args:
        raise TypeError(ERR_TOO_MANY_POS_ARGS)
    if num_of_kwonly_args > len(kwargs) + (len(default_kws) if has_def_kw else 0):
        raise TypeError(ERR_MISSING_KWONLY_ARGS)
    args_tuple = tuple()
    for i in range(num_of_pos_args):
        if has_args and (i >= (len(arg_names) - 2 if has_kwargs else -1) or (has_kw and kwargs.__contains__(arg_names[i])) or (has_def_kw and default_kws.__contains__(arg_names[i]))):
            args_tuple += (args[i],)
        else:
            res.update({arg_names[i]: args[i]})

    kwargs_dic = dict()
    for key in kwargs:
        if key in res:
            raise TypeError(ERR_MULT_VALUES_FOR_ARG)
        if arg_names.__contains__(key):
            res.update({key: kwargs[key]})
        elif has_kwargs:
            kwargs_dic.update({key: kwargs[key]})
        else:
            raise TypeError(ERR_TOO_MANY_KW_ARGS)
    if has_def_kw:
        for key in default_kws:
            if not res.__contains__(key):
                num_of_keys += 1
                res.update({key: default_kws[key]})
    if has_def_pos:
        i_def_pos = num_of_args - num_of_kwonly_args - len(defaults) - (1 if has_args else 0) - (1 if has_kwargs else 0)
        for i in range(i_def_pos, i_def_pos + len(defaults)):
                if not res.__contains__(arg_names[i]):
                    res.update({arg_names[i]: defaults[i - i_def_pos]})

    if has_kwargs:
        if has_args:
            res.update({arg_names[-2]: args_tuple})
        res.update({arg_names[-1]: kwargs_dic})
    else:
        if has_args:
            res.update({arg_names[-1]: args_tuple})

    """"
    if kwargs.__contains__(arg_names[i]):
        if len(args) > i:
            raise TypeError(ERR_MULT_VALUES_FOR_ARG)
        res.update({arg_names[i]: kwargs[arg_names[i]]})
    elif i < len(args):
        res.update({arg_names[i]: args[i]})
    elif defaults is None or i < num_of_args - len(defaults):
        raise TypeError(ERR_MISSING_POS_ARGS)
    elif defaults is not None and len(defaults) + len(args) > i
        res.update({arg_names[i]: defaults[i - len(args)]})
    if num_of_kwonly_args > 0:
        if num_of_pos_args > 0:
            raise TypeError(ERR_TOO_MANY_POS_ARGS)
        elif num_of_kw_args > num_of_kwonly_args:
            raise TypeError(ERR_TOO_MANY_KW_ARGS)
        for key in kwargs:
            res.update({key: kwargs[key]})
        if default_kws is not None:
            for key in default_kws:
                if key not in res:
                    res.update({key: default_kws[key]})
        if len(res) < num_of_kwonly_args:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)
        elif len(res) > num_of_kwonly_args:
            raise TypeError(ERR_TOO_MANY_KW_ARGS)
        else:
            return res
    if len(arg_names) == 0 and func.__code__.co_varnames is not None:
        res.update({func.__code__.co_varnames[0]: args})
        return res

    if num_of_pos_args > num_of_args:
        raise TypeError(ERR_TOO_MANY_POS_ARGS)
    elif num_of_kw_args > num_of_args:
        raise TypeError(ERR_TOO_MANY_KW_ARGS)"""
    if len(res) < num_of_args:
        raise TypeError(ERR_MISSING_POS_ARGS)
    return res



print("Hello, World!")
ans = {}
ans.update({'a': 2})
print(ans['a'])