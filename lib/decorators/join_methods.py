def join_methods(*funcs, **kwfuncs):
    def decorator(Class):
        for func in funcs:
            setattr(Class, func.__name__, func)

        for key, func in kwfuncs.items():
            setattr(Class, key, func)

        return Class

    return decorator
