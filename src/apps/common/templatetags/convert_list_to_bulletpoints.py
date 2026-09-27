import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="convert_list_to_bulletpoints")
def convert_list_to_bulletpoints(text: str) -> str:
    text = __convert_bulletpoints_to_html(text, "-", "ul", "li")
    text = __convert_bulletpoints_to_html_numbers(text, "ol", "li")

    text_edited = list(filter(None, text.split("\n")))
    for count, text_item in enumerate(text_edited):
        text_edited[count] = f"<p>{text_item}</p>"

    text = " ".join(text_edited)
    return mark_safe(text)


def __convert_bulletpoints_to_html(
    text, symbol: str, outer_tag: str, inner_tag: str
) -> str:
    text_edited: list[str] = list(filter(None, text.split(" ")))
    if symbol in text_edited:
        opened_ul: bool = False
        for count, text_item in enumerate(text_edited):
            if (text_item == symbol) and "\\" not in text_item:
                if not opened_ul:
                    text_edited[count] = f"<{outer_tag}><{inner_tag}>"
                    opened_ul = True
                else:
                    text_edited[count] = f"<{inner_tag}>"

                try:
                    next_dash_index: int = text_edited.index(symbol, count) - 1
                    text_edited[next_dash_index] = f"</{inner_tag}>"
                except ValueError:
                    # NOTE: E.g if these are no next dashes left
                    if any("\n" in text_str for text_str in text_edited[count:]):
                        index_in_newline: int = next(
                            count + index
                            for index, text_str in enumerate(text_edited[count:])
                            if "\n" in text_str
                        )
                        token = text_edited[index_in_newline]
                        nl_pos = token.index("\n")
                        text_edited[index_in_newline] = (
                            token[:nl_pos]
                            + f"</{inner_tag}></{outer_tag}>"
                            + token[nl_pos:]
                        )

            if "\\" in text_item:
                text_edited[count] = text_item.replace("\\", "")

        text = " ".join(text_edited)

    return text


def __convert_bulletpoints_to_html_numbers(
    text,
    outer_tag: str,
    inner_tag: str,
) -> str:
    text_edited: list[str] = list(filter(None, text.split(" ")))
    opened_ul: bool = False
    for count, text_item in enumerate(text_edited):
        if bool(re.match(r"^\d+\.", text_item)) and "\\" not in text_item:
            if not opened_ul:
                text_edited[count] = f"<{outer_tag}><{inner_tag}>"
                opened_ul = True
            else:
                text_edited[count] = f"<{inner_tag}>"

            try:
                match = next(
                    (
                        i
                        for i, t in enumerate(text_edited)
                        if i > count and re.match(r"^\d+\.$", t)
                    ),
                    None,
                )
                if match is None:
                    raise ValueError

                next_dash_index: int = match - 1
                text_edited[next_dash_index] = f"</{inner_tag}>"
            except ValueError:
                # NOTE: E.g if these are no next dashes left
                if any("\n" in text_str for text_str in text_edited[count:]):
                    index_in_newline: int = next(
                        count + index
                        for index, text_str in enumerate(text_edited[count:])
                        if "\n" in text_str
                    )
                    token = text_edited[index_in_newline]
                    nl_pos = token.index("\n")
                    text_edited[index_in_newline] = (
                        token[:nl_pos]
                        + f"</{inner_tag}></{outer_tag}>"
                        + token[nl_pos:]
                    )

        if "\\" in text_item:
            text_edited[count] = text_item.replace("\\", "")

    text = " ".join(text_edited)

    return text
