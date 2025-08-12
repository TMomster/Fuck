from typing import List, Tuple, Dict
from overload import overload


def hex_to_rgb(hex_color: str) -> Tuple:
    if isinstance(hex_color, str) and len(hex_color) == 7 and hex_color.startswith('#'):
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return r, g, b
        except ValueError:
            return 0, 0, 0
    else:
        return 0, 0, 0


@overload
def rgb_to_ansi(red: int, green: int, blue: int) -> str:
    return f"\033[38;2;{red};{green};{blue}m"


@overload
def rgb_to_ansi(rgb_tuple: Tuple) -> str:
    return f"\033[38;2;{rgb_tuple[0]};{rgb_tuple[1]};{rgb_tuple[2]}m"


def gradient_text(text: str, start_color, end_color=None, steps=0) -> str:
    res = []

    if steps == 0:
        steps = len(text)

    if end_color is None:
        end_color = start_color

    for i in range(steps):
        red = int(start_color[0] + (end_color[0] - start_color[0]) * i / steps)
        green = int(start_color[1] + (end_color[1] - start_color[1]) * i / steps)
        blue = int(start_color[2] + (end_color[2] - start_color[2]) * i / steps)

        res.append(f"{rgb_to_ansi(red, green, blue)}{text[i % len(text)]}")

    res.append("\033[0m")

    return "".join(res)


def execute_color(color: str) -> None:
    print(color, end="")
