

def pagination(offset:int, end:int) -> list:
    if offset < 3:
        pagination = [1, 2, 3, "...", end]
    elif offset == 3:
        pagination = [1, 2, 3, 4, "...", end]
    elif offset < end-2:
        pagination = [1, "..." , offset-1, offset, offset+1, "...", end]
    elif offset >= end-2:
        pagination = [1, "...", end-3, end-2, end-1, end]
    else:
        pagination = [1, 2, 3, "...", end]

    return pagination