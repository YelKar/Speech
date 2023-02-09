from sys import stdout

name = ["кеша", "иннокентий", "кешан", "ассистент"]


def load_bar(percent: int, length: int = 100, style="", complete: str = "Complete", on="▓", off="▒"):
    on_length = length * percent // 100
    print(
        f"\r{style}▏{on * on_length + off * (length - on_length)} ▏ -> {percent:3}%",
        ("" if percent != 100 else f"{complete}\n"),
        end="\x1b[0m",
    )
    stdout.flush()
