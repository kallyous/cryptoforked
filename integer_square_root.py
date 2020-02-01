def isqrt(x):
    """Retorna inteiro menor mais próximo da raiz quadrada de númeors que não possúem raiz
        quadrada inteira, e a raiz quadrada exata de números que possúem raiz perfeita."""

    # Casos base.
    if x == 0 or x == 1:
        return x

    """Usando busca binária, encontra a raiz desejada."""
    start = 0
    end = x // 2  # Raiz nunca será maior que x/2 .

    while start <= end:

        # Calcula meio da array.
        mid = (start + end) // 2

        # Detecta e retorna raiz perfeita.
        if mid * mid == x:
            return mid

        """ Não sendo raiz perfeita, queremos o menor inteiro mais próximo.
            Assim sendo, atualizamos 'ans' sempre que mid*mid for menor que X,
            e seguimos para próxima iteração. """
        if mid * mid < x:
            start = mid + 1
            ans = mid

        else:
            """ Como igualdade já foi checada (raíz perfeita), chegamos aqui se mid*mid for
                maior que X. Assim, apenas ajustamos o limite à direita da busca binária."""
            end = mid - 1

    # Ao sair do laço sem  mid*mid==x ,  ans  possui o menor inteiro mais pŕoximo da raiz desejada.
    return ans
