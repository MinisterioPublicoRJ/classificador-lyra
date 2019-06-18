from collections import Counter
from os import environ as env

import nltk


dicionario = set([p.lower().strip() for p in open(
    env.get(
        'DICIONARIO',
        'classificador_lyra/pre_processamento/dicionario.txt'),
    encoding='utf-8')])

stopwords = [s.strip().lower() for s in open(
    env.get(
        'STOPWORDS',
        'classificador_lyra/pre_processamento/stopwords.txt'))]

# Prepara corpora
corpora = [p.strip() for p in open(
    env.get(
        'BAG_OF_WORDS',
        'classificador_lyra/pre_processamento/corpora.txt'))]

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
