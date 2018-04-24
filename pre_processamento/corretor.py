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
