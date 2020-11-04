def put_empty_bytes(message):
    empty_byte_length = 16 - (len(message) % 16)
    if empty_byte_length == 16:
        return message
    else:
        return message + (empty_byte_length * b'\0')


def delete_empty_bytes(message):
    index = 0
    for i in range(0, len(message)):
        if message[i] == 0x00:
            index = i
            break
    if index == 0:
        index = len(message)
    return message[0:index]


def message_split_to_blocks(message):
    return [message[i:i + 16] for i in range(0, len(message), 16)]