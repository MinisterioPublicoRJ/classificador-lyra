from difflib import SequenceMatcher


PALAVRAS_IMPORTANTES = [
    'julgo',
]


def corrige_palavras(documento_original, palavras_importantes):
    documento_corrigido = documento_original
    documento_splitted = documento_original.split()

    for palavra in PALAVRAS_IMPORTANTES:
        for token in documento_splitted:
            if SequenceMatcher(None, palavra, token.lower()).ratio() > 0.6:
                documento_corrigido = documento_corrigido.replace(token,
                                                                  palavra)

    return documento_corrigido
