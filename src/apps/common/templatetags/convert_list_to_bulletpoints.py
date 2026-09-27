import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="convert_list_to_bulletpoints")
def convert_list_to_bulletpoints(text_str: str) -> str:
    text = Text(text_str)
    __convert_bulletpoints_to_html(text, "-", "ul", "li")
    __convert_bulletpoints_to_html_numbers(text, "ol", "li")

    text = Text(text.get_text(), "\n")
    for count, text_item in enumerate(text.listed_text):
        text.set_element(count, f"<p>{text_item}</p>")

    return mark_safe(text.get_text())


def __convert_bulletpoints_to_html(
    text: Text, symbol: str, outer_tag: str, inner_tag: str
) -> None:
    if symbol in text.listed_text:
        tag = Tag(outer_tag, inner_tag)

        for count, text_item in enumerate(text.listed_text):
            if "\\" in text_item:
                text.set_element(count, text_item.replace("\\", ""))

            elif text_item == symbol:
                text.set_element(count, tag.get_opened_tags())

                if symbol in text.listed_text[count:]:
                    text.set_element_by_symbol(symbol, count, f"</{inner_tag}>")
                else:
                    if any("\n" in text_str for text_str in text.listed_text[count:]):
                        index_by_newline = text.get_element_by_next_newline(count)

                        text.set_element(
                            index_by_newline,
                            tag.get_closed_tags(text.listed_text[index_by_newline]),
                        )


def __convert_bulletpoints_to_html_numbers(
    text: Text,
    outer_tag: str,
    inner_tag: str,
) -> str:
    tag = Tag(outer_tag, inner_tag)

    for count, text_item in enumerate(text.listed_text):
        if "\\" in text_item:
            text.set_element(count, text_item.replace("\\", ""))

        elif bool(re.match(r"^\d+\.", text_item)):
            text.set_element(count, tag.get_opened_tags())

            match = next(
                (
                    i
                    for i, t in enumerate(text.listed_text)
                    if i > count and re.match(r"^\d+\.$", t)
                ),
                None,
            )
            if match is not None:
                text.set_element(match - 1, tag.get_closed_inner_tag())
            else:
                if any("\n" in text_str for text_str in text.listed_text[count:]):
                    index_by_newline = text.get_element_by_next_newline(count)

                    text.set_element(
                        index_by_newline,
                        tag.get_closed_tags(text.listed_text[index_by_newline]),
                    )


class Tag:
    outer_tag: str
    inner_tag: str

    is_outer_tag_opened: bool

    def __init__(self, outer_tag: str, inner_tag: str) -> None:
        self.outer_tag = outer_tag
        self.inner_tag = inner_tag
        self.is_outer_tag_opened = False

    def get_opened_tags(self) -> str:
        if not self.is_outer_tag_opened:
            self.is_outer_tag_opened = True

            return f"<{self.outer_tag}><{self.inner_tag}>"
        else:
            return f"<{self.inner_tag}>"

    def get_closed_tags(self, token: str) -> str:
        nl_pos = token.index("\n")

        return (
            token[:nl_pos] + f"</{self.inner_tag}></{self.outer_tag}>" + token[nl_pos:]
        )

    def get_closed_inner_tag(self) -> str:
        return f"</{self.inner_tag}>"


class Text:
    listed_text: list[str]

    def __init__(self, text: str, split_type: str = " ") -> None:
        self.listed_text: list[str] = list(filter(None, text.split(split_type)))

    def set_element(self, index: int, value: str) -> None:
        self.listed_text[index] = value

    def set_element_by_symbol(self, symbol: str, index: int, value: str) -> None:

        if symbol in self.listed_text[index:]:
            index_by_symbol: int = self.listed_text.index(symbol, index) - 1

            self.set_element(index_by_symbol, value)

    def get_element_by_next_newline(self, count: int) -> int:
        index_in_newline: int = next(
            count + index
            for index, text_str in enumerate(self.listed_text[count:])
            if "\n" in text_str
        )

        return index_in_newline

    def get_text(self) -> str:
        return " ".join(self.listed_text)
