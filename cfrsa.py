from random import randrange
from euclidian_mdc import mdc_e
from integer_square_root import isqrt


def is_prime(num):
    """Checa se número é primo.
        Usa raiz inteira mais próxima para limitar busca por primos, agilizando a verificação.
    """
    if num < 2:
        return False
    for n in range(2, isqrt(num) + 1):
        if num % n == 0:
            return False
    return True


def gen_e_d(p, q):
    """Gera (e d) usando o Algoritmo de Euclides Estendido.
        Calcula ϕ(p*q), escolhe 'e' e usa Euclides Extendido para calcular 'd'.
        eR1: 1 < e < ϕ(p*q)
        eR2: e é co-primo de ϕ(p*q)
        dR1: e*d ≅ 1 mod p*q  →  e*d mod p*q = 1
    """
    # The totient.
    fin = (p - 1) * (q - 1)
    # Grab a valid value for e at random.
    while True:
        # Pega um e qualquer pra tirar o mdc(e, fin) e a inversa de e mod fin .
        e = randrange(2, fin)

        # Euclides Extendido nos da mdc(e, fin) == res
        res, coef = mdc_e(e, fin)

        # Se o mdc for 1, pega a inversa de e mod fin de dentro da tabela gerada pelo algoritmo.
        """ Vale ressaltar aqui que quando o mdc for 1, o valor de 'a' tal que
            'a' é a inversa modular de e mod fin, será o valor de 's' da última linha com
            resto não nulo da tabela. Na sintaxe de python, len(coef) - 2 acerta a penultima linha
            da tabela que, por conta do próprio algorítmo, possui o último valor não nulo do resto e
            é onde 's' assumi o valor da desejada inversa multiplicativa 'a'. """
        if res == 1:
            i = len(coef) - 2
            inv = coef[i]['s']
            # Normaliza inversa quando negativa
            if inv > 0:
                return e, inv


def genkeypairs(p, q):
    """Gera o par de chaves privada e pública.
        Com (p q), cancula n e chama função que calcula (e d)
        Monta e retorna os pares de números compondo as chaves
        pública e privada.
    """
    n = p * q
    e, d = gen_e_d(p, q)
    return (e, n), (d, n)


def encryptpart(m, e, n):
    """Criptografa um caracter"""
    return exp_mod(m, e, n)
    # return (m ** e) % n


def decryptpart(c, d, n):
    """Descriptografa um caracter"""
    return exp_mod(c, d, n)
    # return (c ** d) % n


def encrypt_encoded(encoded_txt, e, n):
    """Criptografa uma string encodada pelo acordo do projeto.
        0. Recebe string contendo os números dos caracteres encodados no acordo
            do projeto (números encodados separados por espaços).
        1. Quebramos a string em várias estrings menores, cada uma contendo os
            caracteres representando o número de um caracter encodado.
        2. Interpreta cada string da lista, obtendo o número inteiro que representa.
        3. Gera string contendo os números dos caracteres criptografados,
            separados por espaços, e a retorna.
    """
    decoded_nums = list(map(int, encoded_txt.split()))
    cripto = ''
    for c in decoded_nums:
        cripto += ' {}'.format(encryptpart(c, e, n))
    return cripto.strip(' ')


def decrypt_encoded(encry_text, d, n):
    """Descriptografa string criptografada e encodada pelo acordo do projeto.
        0. Recebe string contendo os números dos caracteres criptografados,
            separados por espaços.
        1. Quebramos a string em várias estrings menores, cada uma contendo os
            caracteres representando o número de um caracter criptografado.
        2. Interpreta cada string da lista, obtendo o número inteiro que representa.
        3. Gera string contendo os números dos caracteres descriptografados,
            separados por espaços, e a retorna.
    """
    encry_nums = list(map(int, encry_text.split()))
    plain = ''
    for c in encry_nums:
        plain += ' {}'.format(decryptpart(c, d, n))
    return plain.strip()


def p2_exp_mod(a, k, m):
    """Calcula  a^k mod m  para  a,k,m sendo números inteiros e  k  sendo potência de 2.
    :param a: Valor base.
    :param k: Potência de 2.
    :param m: Valor para o qual calcular módulo.
    :return: (a^k) mod m
    """
    if k <= 2:
        return a**k % m
    else:
        return (p2_exp_mod(a, k//2, m) * p2_exp_mod(a, k//2, m)) % m


def exp_mod(a, k, m):
    """Calcula  a^k mod m  para  a,k,m  sendo números inteiros.
    :param a: Valor base.
    :param k: Potência de a.
    :param m: Valor para o qual calcular módulo.
    :return: (a^k) mod m .
    """
    # Gera string com representação binária do valor de k.
    binary_k = f'{k:b}'
    # Pega contagem de bits.
    bitcount = len(binary_k)

    # Prepara variável para segurar as multiplicações.
    A = 1

    # Passa de bit em bit,
    for i in range(0, bitcount):
        # Checa se bit é 1, pois não nos interessa os 0.
        if binary_k[i] == '1':
            # Calcula a potência a elevar o 2, baseado na casa do bit.
            p = bitcount - 1 - i  # O -1 é pq arrays começam no índice 0.
            # Chama recursão que calcula exponenciação modular para potêcnias de 2 para o bit atual e incrementa A.
            A *= p2_exp_mod(a, 2 ** p, m)

    # Tira o módulo de A e o retorna.
    return A % m


def modmultinv(e, fin):
    """Calcula, por força bruta, a inversa multiplicativa modular de dois números.
        dR1: d*e mod ϕ(n) = 1
    """
    for d in range(1, fin):
        if (e * d) % fin == 1:
            return d
    return None


#################################### Não Usados ##########################################


def ext_eucl_mdc(a, b):
    """ Algoritmo de Euclides Extendido (Não usado).
        mdc(a, b) = a*x + b*y
        b*x_ + (a % b)*y_
        "Algoritmos - Teoria e Prática", página 680
    """
    if b == 0:
        return a, 1, 0
    else:
        m_, x_, y_ = ext_eucl_mdc(b, a % b)
        m = m_
        x = y_
        y = x_ - (a / b) * y_
        return m, x, y


def exp_mod_rap(base, power, modulus):
    """Exponenciação Modular Rápida (não usado).
        "Algoritmos - Teoria e Prática", página 695.
        power_bit_len recebe a quantidade de bits armazenando o número power.
        Python usa a quantidade de bytes necessária para armazenar um número.
        Isso pode ser observado definindo números de diferentes tamanhos para
        uma variável a, e então chamando a.bit_length(). Quanto maior o número
        definindo para a, mais bits estarão em uso.
    """
    result = 1
    power_bit_len = power.bit_length()
    for i in range(0, power_bit_len):
        result = (result * result) % modulus
        mask = 1 << i
        bit_val = power & mask
        if bit_val:  # bit_val != 0 ?
            result = (result * base) % modulus
    return result


def fpow(b, e):
    """Exponenciação rápida (Não usado).
        Se 'e' for par:    b² ** (e/2)
        Se 'e' for impar:  b  * (b² ** (e-1)/2)
    """
    # Fim de recursão
    if e < 3 and e > -3: return b ** e
    if e % 2 == 0:
        # Retorne (b*b) ** (e/2)
        return fpow(b * b, e // 2)
    else:
        # Retorne b * ( (b*b) ** ((e-1)/2) )
        return b * fpow(b * b, (e - 1) // 2)


def encrypt(plain_txt, e, n):
    """Criptografa uma string (Não usado)."""
    cripto = ''
    for c in plain_txt:
        cripto += ' {}'.format(encryptpart(ord(c), e, n))
    return cripto.strip(' ')


def decrypt(encry_text, d, n):
    """Descriptografa string criptografada (Não usado)."""
    plain = ''
    encry_code_list = encry_text.split(' ')
    for code in encry_code_list:
        plain += chr(decryptpart(int(code), d, n))
    return plain
