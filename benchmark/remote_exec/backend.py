import ast


def exec_str(func_str, func_name, func_param):
    # return ast.literal_eval(func_param)
    # print(func_str)
    # print(func_name)
    param = func_param
    # print(param)
    if param is list:
        param_str = '[' + ','.join(func_param) + ']'
    else:
        param_str = param

    # print(param)
    exec(func_str)
    # r = eval(func_name + '({})'.format(param))
    # r = [eval(func_name + '({})'.format(i)) for i in param]
    r = []
    for p in param:
        r0 = eval(func_name + '({})'.format(p))
        r.append(r0)

    # print('param_str', param_str)
    # print('r', r)

    return r
