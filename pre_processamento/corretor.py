import re

import nltk

from operator import itemgetter

from pre_processamento.utils import (dicionario,
                                     stopwords,
                                     bigramas_corpora,
                                     palavras_importantes)


PADRAO_LIMPEZA = re.compile(r'[^a-záéíóúãõâêç]', re.IGNORECASE)
LIMIAR_SEMELHANCA = 0.8


def corrige_documento(documento_original):
    documento_corrigido = documento_original.lower()
    pos = itemgetter(1)
    bigramas, bigramas_erro, palavras_erro = prepara_documento(
        documento_original
    )

    for palavra_com_erro in palavras_erro:
        palavras_sugeridas = sugestoes(palavra_com_erro)
        sugestoes_existentes = (
            palavras_sugeridas & dicionario & palavras_importantes
        )

        # TODO: Inverter ordem das palavras do bigrama i.e: (p1, p2), (p2, p1)
        frequencias = []
        for sugestao in sugestoes_existentes:
            for bigrama in bigramas_erro:
                copia_bigrama = list(bigrama)
                copia_bigrama.append(sugestao)
                copia_bigrama.remove(palavra_com_erro)
                freq = bigramas_corpora[tuple(copia_bigrama)]

                # Levar em consideracao bigramas com frequencia > 2
                if freq < 2:
                    continue

                frequencias.append([sugestao, freq])

            sugestao_provavel = sorted(
                frequencias,
                key=pos,
                reverse=True)[0][0]

            documento_corrigido = documento_corrigido.replace(
                palavra_com_erro, sugestao_provavel
            )

    return documento_corrigido


def prepara_documento(documento):
    palavras = [p for p in tokeniza(documento) if p not in stopwords]
    bigramas = constroi_ngramas(palavras)
    erros = filtro_dicionario(palavras)
    bigramas_erro = [b for b in bigramas for p in erros if p in b]
    return bigramas, bigramas_erro, erros


def _combinacoes(palavra):
    # fonte: http://norvig.com/spell-correct.html
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(palavra[:i], palavra[i:]) for i in range(len(palavra) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def sugestoes(palavra):
    # TODO: retornar conjunto para evitar repeticoes
    "All edits that are two edits away from `word`."
    return set((c2 for c1 in _combinacoes(palavra) for c2 in _combinacoes(c1)))


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


def filtro_dicionario(palavras):
    return [p for p in palavras if p not in dicionario]


def tokeniza(documento):
    return re.findall(r'[a-záâãéêóõúàíçü]+-?[a-z]+', documento.lower())


def remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords]


def constroi_ngramas(palavras, tamanho=2):
    return list(nltk.ngrams(palavras, tamanho))
