def get_offset(page_number: int, page_size: int) -> int:
    return (page_number - 1) * page_size
