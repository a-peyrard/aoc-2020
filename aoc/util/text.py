from typing import Iterator, List


def generate_paragraphs(raw_entries: Iterator[str]) -> Iterator[List[str]]:
    buf = []
    for raw_entry in raw_entries:
        entry = raw_entry.rstrip()
        if entry:
            buf.append(entry)
        else:
            if buf:
                yield buf
                buf = []

    if buf:
        yield buf
