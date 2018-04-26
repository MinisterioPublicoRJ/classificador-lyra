import re

from difflib import SequenceMatcher


PALAVRAS_IMPORTANTES = [
    'julgo',
    'procedente',
]


def corrige_palavras(documento_original, palavras_importantes):
    documento_corrigido = documento_original
    documento_splitted = documento_original.split()

    for palavra in PALAVRAS_IMPORTANTES:
        for token in documento_splitted:
            if SequenceMatcher(None, palavra, token.lower()).ratio() > 0.6:
                n_letras = len(palavra)
                if sum(map(lambda x: x.isupper(), token)) / n_letras > 0.5:
                    documento_corrigido = documento_corrigido.replace(
                        token,
                        palavra.upper()
                    )
                else:
                    documento_corrigido = documento_corrigido.replace(
                        token,
                        palavra
                    )

    return documento_corrigido


def formata_palavras(documento_original):
    padrao = re.compile(r'(\b([A-ZÁÉÃÕÇ]{1}\s+){3,}\b([A-Z]\s?(\r\n|\n|\r))?)')
    documento_corrigido = documento_original

    encontrado = re.search(padrao, documento_corrigido)
    while encontrado:
        palavra_corrigida = re.sub(r'\s+', '', encontrado.group(0))

        quebra_de_linha = re.search(r'(\r\n|\n|\r)$', encontrado.group(0))
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
