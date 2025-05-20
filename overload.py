"""
overload 提供函数重载的支持。

overload provides support for function overloading.

Author: TMomster
"""

import inspect
from typing import List, Tuple, Dict


class Overload:
    def __init__(self):
        self.functions = []

    def register(self, func):
        sig = inspect.signature(func)
        parameters = sig.parameters.values()
        type_hints = []
        for param in parameters:
            if param.annotation is inspect.Parameter.empty:
                raise TypeError(f"参数 {param.name} 缺少类型注解。")
            type_hints.append(param.annotation)
        # 检查是否已存在相同的类型签名
        for existing_sig, existing_th, _ in self.functions:
            if type_hints == existing_th:
                raise ValueError(f"重复注册类型签名 {type_hints} 的函数。")
        self.functions.append((sig, type_hints, func))
        return self

    def __call__(self, *args, **kwargs):
        matched = []
        for sig, type_hints, func in self.functions:
            try:
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
            except TypeError:
                continue
            valid = True
            for name, value in bound.arguments.items():
                expected_type = sig.parameters[name].annotation
                if not isinstance(value, expected_type):
                    valid = False
                    break
            if valid:
                matched.append((type_hints, func))
        if not matched:
            raise TypeError("没有匹配的函数重载。")
        # 选择最具体的函数
        selected = None
        for th, func in matched:
            if selected is None:
                selected = (th, func)
                continue
            current_th, current_func = selected
            if self._is_more_specific(th, current_th):
                selected = (th, func)
            elif self._is_more_specific(current_th, th):
                continue
            else:
                raise TypeError("函数调用存在二义性，无法确定最具体的重载。")
        return selected[1](*args, **kwargs)

    @staticmethod
    def _is_more_specific(hints_a, hints_b):
        if len(hints_a) != len(hints_b):
            return False
        for a, b in zip(hints_a, hints_b):
            if not issubclass(a, b):
                return False
        return any(a != b for a, b in zip(hints_a, hints_b))


_registry = {}


def overload(func):
    name = func.__name__
    if name not in _registry:
        _registry[name] = Overload()
    _registry[name].register(func)
    return _registry[name]


if __name__ == "__main__":
    print("-- Myss Function Overload Tools --")
    print("This is a demo of myss function overload tools.")
    print("Now we'll demonstrate the usage of decorator 'overload'.")

    print("""
--- Code ---
@overload
def test(a: int, b: int):
    print(f"a + b = {a + b}")
    
@overload
def test(a: int, b: int, c: int):
    print(f"a + b + c = {a + b + c}")
    
test(1, 2) # a + b = 3
test(1, 2, 3) # a + b + c = 6
    
--- Output ---"""
    )

    @overload
    def test(a: int, b: int):
        print(f"a + b = {a + b}")

    @overload
    def test(a: int, b: int, c: int):
        print(f"a + b + c = {a + b + c}")

    test(1, 2) # a + b = 3
    test(1, 2, 3) # a + b + c = 6

    print("\n-- Myss, Alice, Momster, Sam --")
