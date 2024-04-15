def split_code(full_code):
    prefix = ""
    code = ""

    for char in full_code:
        if char.isdigit():
            code += char
        else:
            prefix += char
    return prefix, code
