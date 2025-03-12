def file_to_byte(file: str) -> bytes:
    with open(file, 'rb') as file:
        file_bytes = file.read()
    return file_bytes
