import re
import nltk
from operator import itemgetter

from classificador_lyra.pre_processamento.utils import (
    dicionario,
    stopwords,
    bigramas_corpora,
    palavras_importantes
)


def corrige_documento(documento_original):
    documento_corrigido = documento_original.lower()
    bigramas_erro, palavras_erro = prepara_documento(
        documento_original
    )

    for indice, palavra_com_erro in enumerate(palavras_erro):
        palavras_sugeridas = sugestoes(palavra_com_erro)
        sugestoes_existentes = (
                palavras_sugeridas & dicionario & palavras_importantes
        )
        sugestao = correcao(
            palavra_com_erro,
            bigramas_erro[indice],
            sugestoes_existentes
        )
        if sugestao:
            documento_corrigido = documento_corrigido.replace(
                palavra_com_erro, sugestao
            )
            # Substitui palavra errada pela sugestão nos bigramas
            bigramas_erro = corrige_bigramas(
                bigramas_erro,
                palavra_com_erro,
                sugestao
            )

    return documento_corrigido


def corrige_bigramas(grupo_bigramas, erro, correcao):
    sep = '$'

    grupos_corrigidos = []
    for grupo in grupo_bigramas:
        bigrama_corrigido = []
        for bigrama in grupo:
            if erro in bigrama:
                bigrama = tuple(
                    sep.join(bigrama).replace(erro, correcao).split(sep)
                )

            bigrama_corrigido.append(bigrama)
        grupos_corrigidos.append(bigrama_corrigido)

    return grupos_corrigidos


def correcao(palavra_erro, bigramas_erro, sugestoes):
    pos = itemgetter(1)
    frequencias = []
    sugestao_provavel = ''
    for sugestao in sugestoes:
        for bigrama in bigramas_erro:
            copia_bigrama = list(bigrama)
            copia_bigrama.append(sugestao)
            copia_bigrama.remove(palavra_erro)
            freq = bigramas_corpora[tuple(copia_bigrama)]
            freq_inv = bigramas_corpora[
                (copia_bigrama[1], copia_bigrama[0])
            ]

            # Levar em consideracao bigramas com frequencia > 2
            if freq < 2 and freq_inv < 2:
                continue

            frequencias.append([sugestao, max(freq, freq_inv)])

        if frequencias:
            sugestao_provavel = sorted(
                frequencias,
                key=pos,
                reverse=True)[0][0]

    return sugestao_provavel


def prepara_documento(documento):
    palavras = [p for p in tokeniza(documento) if p not in stopwords]
    bigramas = constroi_ngramas(palavras)
    erros = filtro_dicionario(palavras)
    bigramas_erro = []
    for erro in erros:
        bigramas_erro.append([b for b in bigramas if erro in b])

    return bigramas_erro, erros


def _combinacoes(palavra):
    # fonte: http://norvig.com/spell-correct.html
    letters = 'abcdefghijklmnopqrstuvwxyzçéáóãõíüâô'
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
    erros = []
    for palavra in palavras:
        if palavra not in dicionario and palavra not in erros:
            erros.append(palavra)

    return erros


def tokeniza(documento):
    return re.findall(r'[a-záâãéêóõôúàíçü]+-?[a-z]+', documento.lower())


def remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords]


def constroi_ngramas(palavras, tamanho=2):
    return list(nltk.ngrams(palavras, tamanho))
