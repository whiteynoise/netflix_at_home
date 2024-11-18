def paginator(page_number: int | None, page_size: int | None):
    page_number = page_number or 1
    page_size = page_size or 50

    # считаю смещение вручную
    offset = (page_number - 1) * page_size
    return page_number, page_size, offset