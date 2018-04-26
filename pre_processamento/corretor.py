import re

from difflib import SequenceMatcher


PADRAO_LIMPEZA = re.compile(r'[^a-záéíóúãõâêç]', re.IGNORECASE)
LIMIAR_SEMELHANCA = 0.6
PALAVRAS_IMPORTANTES = [
    'julgo',
    'procedente',
    'subsustente',
    'condeno',
    'acusado',
    'acolho',
    'pedido',
    'inicial',
    'indefiro',
    'defiro',
    'requerido',
    'declaro',
    'decreto',
    'improcedente',
    'extinto',
    'determino',
    'extinção',
    'absolvo',
    'absolvido',
    'nego',
    'provimento',
    'resolver',
    'merito',
    'arquivamento',
]


def corrige_palavras(documento_original, palavras_importantes):
    documento_corrigido = documento_original
    documento_splitted = documento_original.split()

    for token in documento_splitted:
        token_limpo = limpa_palavra(token)
        if token_limpo.lower() not in palavras_importantes:
            palavra_similar = encontra_palavra_similiar(
                token_limpo.lower(),
                palavras_importantes
            )
        else:
            palavra_similar = token_limpo

        n_letras = len(token)
        # Se o token possui mais de 50% de letras em caixa alta
        # manter caixa alta
        if sum(map(lambda x: x.isupper(), token)) / n_letras > 0.5:
            documento_corrigido = documento_corrigido.replace(
                token,
                palavra_similar.upper()
            )
        else:
            documento_corrigido = documento_corrigido.replace(
                token,
                palavra_similar.lower()
            )

    return documento_corrigido


def formata_palavras(documento_original):
    padrao = re.compile(r'(\b([A-ZÁÉÃÕÇ]{1}\s+){3,}\b([A-Z]\s?(\r\n|\n|\r))?)')
    documento_corrigido = documento_original

    encontrado = re.search(padrao, documento_corrigido)
    while encontrado:
        palavra_corrigida = re.sub(r'\s+', '', encontrado.group(0))

        quebra_de_linha = re.search(r'(\r\n|\n|\r)\s+$', encontrado.group(0))
        if quebra_de_linha:
            palavra_corrigida += quebra_de_linha.group(0)
        else:
            palavra_corrigida += ' '

        documento_corrigido = documento_corrigido.replace(
            encontrado.group(0),
            palavra_corrigida
        )
        encontrado = re.search(padrao, documento_corrigido)

    return documento_corrigido


def encontra_palavra_similiar(palavra, palavras_importantes):
    palavras_candidatas = []
    for indice, palavra_importante in enumerate(palavras_importantes):
        semelhanca = SequenceMatcher(None, palavra, palavra_importante).ratio()
        if semelhanca >= LIMIAR_SEMELHANCA:
            palavras_candidatas.append((semelhanca, indice))

    if palavras_candidatas:
        return palavras_importantes[
            sorted(palavras_candidatas, reverse=True)[0][1]
        ]

    return palavra


def limpa_palavra(palavra):
    return re.sub(PADRAO_LIMPEZA, '', palavra)
