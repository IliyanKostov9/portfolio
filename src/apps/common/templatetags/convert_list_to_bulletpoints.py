from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="convert_list_to_bulletpoints")
def convert_list_to_bulletpoints(text: str) -> str:
    text_edited: list[str] = text.split(" ")

    if "-" in text_edited:
        print(text_edited)
        opened_ul: bool = False
        for count, text_item in enumerate(text_edited):
            if text_item == "-":
                if not opened_ul:
                    text_edited[count] = "<ul><li>"
                    opened_ul = True
                else:
                    text_edited[count] = "<li>"

                try:
                    text_edited[text_edited.index("-", count) - 1] = "</li>"
                except ValueError:
                    text_edited[-1] = "</li></ul>"

        text = " ".join(text_edited)
        print(text)

    return mark_safe(text)
