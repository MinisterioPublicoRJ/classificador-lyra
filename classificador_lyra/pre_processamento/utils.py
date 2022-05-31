from os import environ as env
from collections import Counter
from pathlib import Path

import nltk

root_path = Path(__file__).parent.absolute()
arquivo_dicionario = Path(root_path, 'dicionario.txt')
arquivo_stopwords = Path(root_path, 'stopwords.txt')
arquivo_corpora = Path(root_path, 'corpora.txt')

# 'classificador_lyra/pre_processamento/dicionario.txt'
dicionario = set([p.lower().strip() for p in open(
    env.get(
        'DICIONARIO', arquivo_dicionario),
    encoding='utf-8')])

# 'classificador_lyra/pre_processamento/stopwords.txt'
stopwords = [s.strip().lower() for s in open(
    env.get(
        'STOPWORDS', arquivo_stopwords))]

# Prepara corpora
# 'classificador_lyra/pre_processamento/corpora.txt'
corpora = [p.strip() for p in open(
    env.get(
        'BAG_OF_WORDS', arquivo_corpora))]

bigramas_corpora = Counter(nltk.bigrams(corpora))

palavras_importantes = set([
    'julgo',
    'julga-se',
    'julgam-se',
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
    'improvimento',
    'resolver',
    'mérito',
    'arquivamento',
    'medida',
    'autorização',
    'habilitação',
    'parcialmente',
    'sumariamente',
    'nego-lhes',
    'dou',
    'dou-lhes',
    'deixo',
    'ordem',
    'presente'
    'resolução',
    'extingo',
    'extinguindo',
])
