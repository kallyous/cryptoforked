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
        Calcula ϕ(p,q), escolhe 'e' e usa Euclides Extendido para calcular 'd'.
        A função ϕ(p,q) é dada por  ϕ(p,q) = (p-1)*(q-1)  e lê-se "fi de p q".
        1ª regra de e: 1 < e < ϕ(p*q)
        2ª regra de e: e é co-primo de ϕ(p*q)
        1ª regra de d: e*d ≅ 1 mod p*q  →  e*d mod p*q = 1
        Embora ϕ() seja tecnicamente uma função, a gente taca logo o resultado de ϕ(p,q)
        na variável fin.
    """
    # Totient / Totiente  (sei lá a escrita correta em pt)
    fin = (p - 1) * (q - 1)  # fin / ϕ(p,q)

    # Pega valores aleatórios até um servir.
    while True:
        # Pega um e qualquer pra tirar o mdc(e, fin) e a inversa de e mod fin .
        e = randrange(2, fin)  # 1 não serve por motivos óbvios...

        # Euclides Extendido nos da mdc(e, fin)
        res, coef = mdc_e(e, fin)

        # Se o mdc for 1, pega a inversa de  e mod fin  de dentro da tabela gerada pelo algoritmo.
        """ Vale ressaltar aqui que quando o mdc for 1, o valor de 'a' tal que
            'a' é a inversa modular de  e mod fin  , será o valor de 's' da última linha com
            resto não nulo da tabela. Na sintaxe de python, len(coef) - 2 acerta a penultima linha
            da tabela que, por conta do próprio algorítmo, possui o último valor não nulo do resto e
            é onde 's' assumi o valor da desejada inversa multiplicativa 'a'. """
        if res == 1:  # Se mdc == 1:
            i = len(coef) - 2  # Acessa penúltima linha, onde está ultimo resto não nulo.
            inv = coef[i]['s']  # Pega o valor da inversa

            # Certifica que a inversa não é negativa. Teoricamente, isso nunca ocorrerá...
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
        return a ** k % m
    else:
        return (p2_exp_mod(a, k // 2, m) * p2_exp_mod(a, k // 2, m)) % m


def exp_mod(a, k, m):
    """Exponenciação modular rápida usando aritmética modular.
        Calcula  a^k mod m  para  a,k,m  sendo números inteiros.
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
            p = bitcount - 1 - i  # O -1 é devido às arrays irem de  0  a  bitcount-1  em seus índices.
            # Chama recursão que calcula exp. mod. para potêcnias de 2 para o bit atual e atualiza A.
            A *= p2_exp_mod(a, 2 ** p, m)

    # Tira o módulo de A e o retorna.
    return A % m


def modmultinv(e, fin):
    """Calcula, por força bruta, a inversa multiplicativa modular de dois números.
        regra de d: d*e mod ϕ(n) = 1
        Essa função seria totalmente desnecessária não fosse uma exigência redundante
        do próprio trabalho de Matemática Discreta.
        Contexto e mais detalhes nos comentários em  cryptoforked.py  .
    """
    for d in range(1, fin):
        if (e * d) % fin == 1:
            return d
    return None
