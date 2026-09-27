from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="convert_list_to_bulletpoints")
def convert_list_to_bulletpoints(text: str) -> str:

    text_edited: list[str] = list(filter(None, text.split("\n")))
    for count, text_item in enumerate(text_edited):
        text_edited[count] = f"<p>{text_item}</p>"

    text_edited = "".join(text_edited).split(" ")
    if "-" in text_edited:
        opened_ul: bool = False
        for count, text_item in enumerate(text_edited):
            if text_item == "-":
                if not opened_ul:
                    text_edited[count] = "<ul><li>"
                    opened_ul = True
                else:
                    text_edited[count] = "<li>"

                try:
                    next_dash_index: int = text_edited.index("-", count) - 1
                    print(next_dash_index, count)
                    if next_dash_index - count >= 50:
                        text_edited[next_dash_index] = "</li></ul>"
                    else:
                        text_edited[next_dash_index] = "</li>"
                except ValueError:
                    # NOTE: E.g if these are no next dashes left
                    text_edited[-1] = "</li></ul>"

        text = " ".join(text_edited)
        print(text)

    return mark_safe(text)
