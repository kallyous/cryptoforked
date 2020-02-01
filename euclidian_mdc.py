def mdc(a, b):
    """ MDC usando algorítmo de euclides, versão simplificada. """
    if b == 0:
        return a
    return mdc(b, a % b)


def mdc_e(a, b):
    """ MDC usando algorítmo de euclides, versão extendida.
        Inclui todas as linhas do algorítmo contento todos os r = s*a + t*b
            q - quociente
            r - resto
            s - coeficiente de a
            t - coeficiente de b
        Retorna uma tupla de dois elementos:
            O primeiro elemento é o MDC(a,b)
            O segundo elemento é uma lista contendo os q,r,s,t de cada iteração do
            algorítmo. Útil para obter inversas de congruências e de módulos.
    """

    # Prepara as duas linhas iniciais do algoritmo e as empacota.
    pack = [{'q': None, 'r': a, 's': 1, 't': 0},
            {'q': None, 'r': b, 's': 0, 't': 1}]

    # Passa os valores e o pacote adiante para o cerne do algoritmo, e retorna o resultado.
    return mdc_e_coef(a, b, pack)


def mdc_e_coef(a, b, coef: list):
    """ Cerne da implementação do algorítmo extendido de euclides para o MDC. """

    # Condição de saída da recursão
    if b == 0:
        return a, coef

    q = a // b  # Calcula próximo quociente
    r = a % b  # Calcula próximo resto

    # Calcula os valores de  s,t  tais que  r = s*a + t*b  .
    i = len(coef)
    s = coef[i - 2]['s'] - (q * coef[i - 1]['s'])
    t = coef[i - 2]['t'] - (q * coef[i - 1]['t'])

    # Monta linha contendo os valores resultados da iteração atual
    c = {'q': q, 'r': r, 's': s, 't': t}

    # Adiciona linha montada ao final do pacote.
    coef.append(c)

    # Avança na recursão e retorna resultado.
    return mdc_e_coef(b, r, coef)
