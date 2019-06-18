from classificador_lyra.regex import BaseClassifier


class ProcedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro|DECRETO)[\w ,]{1,60}'
                 r'(procedente|subsistente))|'
                 r'(condeno (o|a)(s)? acusad(o|a)(s)?)',
                 r'(acolho o pedido inicial)',
                 r'((?<!in)defiro (o|a) (autoriza[CÇç][AÃã]o|habilita[CÇç]'
                 r'[AÃã]o|medida|'
                 r'pedido|requerido))']
        regex_exclusao = [r'improcedente|parcialmente']
        regex_reforco = r'condeno'
        super().__init__(texto,
                         regex=regex,
                         regex_exclusao=regex_exclusao,
                         regex_reforco=regex_reforco)


class ImprocedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro|DECRETO)[\w ,]{1,60}'
                 r'(improcedente))']
        regex_exclusao = [r' procedente|parcialmente']
        super().__init__(texto,
                         regex=regex,
                         regex_exclusao=regex_exclusao)


class ExtincaoPunibilidadeClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro|determino|DECRETO)'
                 r'[\w+ ,]{1,60}(extinto|(extinta|extin[CÇç][AÃã]o)'
                 r'([\w ,]{1,60}'
                 r'(punibilidade|pena privativa))?))']
        regex_reforco = r'art\. 107'
        super().__init__(texto,
                         regex=regex,
                         regex_reforco=regex_reforco)


class ParcialmenteProcedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'((julgam?[- ]?se|julgo|declaro)[\w+ ,]{1,60}(parcialmente)'
                 r'[\w ,]{1,60}(procedente))']
        regex_exclusao = [r'improcedente']
        regex_reforco = r'condeno'
        super().__init__(texto,
                         regex=regex,
                         regex_exclusao=regex_exclusao,
                         regex_reforco=regex_reforco)


class AbsolvoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = [r'(ABSOLVO SUMARIAMENTE)|(ABSOLVO +(o|a)(s)?'
                 r' +acusad(o|a)(s)?)|((fica )?absolvido +(o|a)(s)?'
                 r' +acusad(o|a)(s)?)',
                 r' absolvo ']
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
        regex = [r'(DEIXO[\w+ ,]{1,60}RESOLVER[\w ,]{1,60}M[EÉé]RITO)']
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
