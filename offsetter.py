""" Fluxo de codificação e criptografia:

    Criptografar:
        "A BC" -> encode -> "0 26 1 2" -> encrypt(e, n) -> "34 54 65 78"

    Descriptografar:
        "34 54 65 78" -> decrypt(d, n) -> "0 26 1 2" -> decode -> "A BC"
"""

offset = 65
space = 26


# Encoda caractere no acordo do projeto
def encode_char(c):
    if ord(c) == ord(' '):
        return space
    else:
        return ord(c) - offset


# Decoda o número de um caractere de volta ao normal
def decode_num(n):
    if n == space:
        return ord(' ')
    else:
        return n + offset


# Encoda string para ser criptografada
def encode_str(plain_str):  # 'A BC'
    encoded = ''
    for c in plain_str:
        encoded += ' {}'.format(encode_char(c))
    return encoded.strip()  # '0 26 1 2'


# Decodifica string
def decode_str(encoded_str):  # '0 26 1 2'.split()
    plain_str = ''
    encoded_list = encoded_str.split()
    for n in encoded_list:
        plain_str += chr(decode_num(int(n)))
    return plain_str  # 'A BC'


def coding_test():
    plain_txt = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    encoded_txt = encode_str(plain_txt)
    print(encoded_txt)
