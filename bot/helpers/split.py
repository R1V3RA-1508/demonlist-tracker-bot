def split(text: str, max_length: int = 4096) -> list[str]:
    if len(text) <= max_length:
        return [text]

    parts = []
    start = 0

    while start < len(text):
        end = start + max_length

        if end >= len(text):
            parts.append(text[start:])
            break

        last_close_tag = text.rfind("</code>", start, end)

        if last_close_tag != -1:
            end = last_close_tag + len("</code>")
        else:
            last_open_tag = text.rfind("<code>", start, end)

            if last_open_tag != -1:
                next_close_tag = text.find("</code>", last_open_tag)

                if next_close_tag != -1 and next_close_tag < len(text):
                    end = next_close_tag + len("</code>")
                else:
                    end = last_open_tag
            else:
                last_semicolon = text.rfind(";", start, end)
                if last_semicolon != -1:
                    end = last_semicolon + 1

        parts.append(text[start:end])
        start = end

    return parts
