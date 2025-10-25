from typing import Any


def change_theme(request: Any):
    theme = request.COOKIES.get("theme", "light")
    return {"theme": theme}
