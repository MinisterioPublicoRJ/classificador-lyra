import re
from collections import namedtuple


class BaseClassifier:
    def __init__(self,
                 texto,
                 regex=None,
                 regex_reforco=None,
                 regex_exclusao=None):
        self.regex = regex
        self.regex_reforco = regex_reforco
        self.regex_exclusao = regex_exclusao
        self.texto = texto
        self.positivo = False
        self.pesos = []
        self.posicao = []
        self.matches = []

    def classificar(self):
        # match principal para identificação de sentença
        for item in self.regex:
            match = re.search(item, self.texto, re.MULTILINE | re.IGNORECASE)
            if match:
                self.matches += [match]

        # não permite termos indesejados na expressão encontrada
        # cria uma lista cópia da original para iterar e trabalha
        # na remoção dos itens da lista original
        for item in list(self.matches):
            encontrado = item.group(0)
            if self.regex_exclusao and re.findall(self.regex_exclusao,
                                                  encontrado, re.IGNORECASE):
                self.matches.remove(item)

        if not self.matches:
            return

        self.positivo = True

        # legal, parece que temos o que queremos, vamos atribuir pesos
        # reforço aplica um novo conjunto de regras a todo o texto
        if self.regex_reforco:
            self.pesos = re.findall(self.regex_reforco, self.texto,
                                    re.MULTILINE | re.IGNORECASE)

        for match in self.matches:
            self.posicao += [(match.start(), match.end())]


class ProcedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro|DECRETO)[\w ,]{,60}'
                 r'(procedente|subsistente))|'
                 r'(condeno (o|a)(s)? acusad(o|a)(s)?)',
                 r'(acolho o pedido inicial)',
                 r'((?<!in)defiro (o|a) (autorização|habilitação|medida|'
                 r'pedido|requerido))']
        regex_exclusao = r'improcedente|parcialmente'
        regex_reforco = r'condeno'
        super().__init__(texto,
                         regex=regex,
                         regex_exclusao=regex_exclusao,
                         regex_reforco=regex_reforco)


class ImprocedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro|DECRETO)[\w ,]{,60}'
                 r'(improcedente))']
        regex_exclusao = r' procedente|parcialmente'
        super().__init__(texto,
                         regex=regex,
                         regex_exclusao=regex_exclusao)


class ExtincaoPunibilidadeClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro|determino|DECRETO)'
                 r'[\w+ ,]{1,60}(extinto|(extinta|extinc)([\w ,]{,60}'
                 r'(punibilidade|pena privativa))?))']
        regex_reforco = r'art\. 107'
        super().__init__(texto,
                         regex=regex,
                         regex_reforco=regex_reforco)


class ParcialmenteProcedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro)[\w+ ,]{,60}(parcialmente)'
                 r'[\w ,]{1,60}(procedente))']
        regex_exclusao = r'improcedente'
        regex_reforco = r'condeno'
        super().__init__(texto,
                         regex=regex,
                         regex_exclusao=regex_exclusao,
                         regex_reforco=regex_reforco)


class AbsolvoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'(ABSOLVO SUMARIAMENTE)|(ABSOLVO +(o|a)(s)?'
                 r' +acusad(o|a)(s)?)|((fica )?absolvido +(o|a)(s)?'
                 r' +acusad(o|a)(s)?)']
        super().__init__(texto, regex=regex)


class NegacaoProvimentoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'(NEGO(-LHE(S)?)? PROVIMENTO)']
        super().__init__(texto, regex=regex)


class DaProvimentoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'(DOU(-LHE(S)?)? PROVIMENTO)']
        super().__init__(texto, regex=regex)


class DeixoResolverMeritoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'(DEIXO[\w+ ,]{1,60}RESOLVER[\w ,]{1,60}MERITO)']
        super().__init__(texto, regex=regex)


class IndeferenciaClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'(indefiro (a(s)? orde(m|ns)|o(s)? pedido(s)?|o(s)?'
                 r' requerimento(s)?))']
        super().__init__(texto, regex=regex)


class ArquivamentoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((DETERMINO|HOMOLOGO) O ARQUIVAMENTO)']
        super().__init__(texto, regex=regex)


class ExtincaoProcessoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'(extingo o presente processo)']
        super().__init__(texto, regex=regex)


class ExtincaoComResolucaoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((JULGO|JULGAR).{0,10}(EXTINTO)|extingo|extinguindo)'
                 r'.{0,30}(FEITO|PROCESSO)'
                 r'?( COM )(JULGAMENTO|RESOLU[CÇç][AÃã]O).+(M[EÉé]RITO)']
        super().__init__(texto, regex=regex)


class ExtincaoSemResolucaoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((JULGO|JULGAR).{0,10}(EXTINTO)|extingo|extinguindo)'
                 r'.{0,30}(FEITO|PROCESSO)'
                 r'?( SEM )(JULGAMENTO|RESOLU[CÇç][AÃã]O).+(M[EÉé]RITO)']
        super().__init__(texto, regex=regex)


class Classificador:
    def __init__(self, classifiers, corpus):
        self.classifiers = classifiers
        self.corpus = corpus

    def classificar(self):
        for i in range(0, len(self.corpus)):
            texto = self.corpus[i]
            classificacoes = []
            for classificador in self.classifiers:
                classificador = classificador(texto)
                classificador.classificar()
                classificacoes += [(classificador.positivo,
                                    classificador.pesos)]
            self.corpus[i] = {
                'conteudo': self.corpus[i],
                'classificacoes': classificacoes}


classificadores = [ProcedenteClassifier,
                   ImprocedenteClassifier,
                   ParcialmenteProcedenteClassifier,
                   ExtincaoPunibilidadeClassifier,
                   AbsolvoClassifier,
                   NegacaoProvimentoClassifier,
                   DeixoResolverMeritoClassifier,
                   DaProvimentoClassifier,
                   IndeferenciaClassifier,
                   ArquivamentoClassifier,
                   ExtincaoProcessoClassifier,
                   ExtincaoComResolucaoClassifier,
                   ExtincaoSemResolucaoClassifier]


def classifica_item(texto):
    classificacoes = {}
    namedtuple

    for classificador in classificadores:
        classificador = classificador(texto)
        classificador.classificar()

        classificacoes[classificador.__class__.__name__] = {
            'positivo': classificador.positivo,
            'pesos': classificador.pesos,
        }

    return {
        'conteudo': texto,
        'classificacoes': classificacoes,
        'positivo': sum(
            [classificacoes[x]['positivo'] for x in classificacoes]
        )
    }
