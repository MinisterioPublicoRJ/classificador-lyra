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
        self.posicao = None

    def classificar(self):
        match = re.search(self.regex, self.texto, re.MULTILINE | re.IGNORECASE)

        if not match:
            return

        encontrado = match.group(0)

        # não permite termos indesejados na expressão encontrada
        if self.regex_exclusao and re.findall(self.regex_exclusao,
                                              encontrado, re.IGNORECASE):
            return

        # legal, parece que temos o que queremos, vamos atribuir pesos
        self.positivo = True

        # reforço aplica um novo conjunto de regras a todo o texto
        if self.regex_reforco:
            self.pesos = re.findall(self.regex_reforco, self.texto,
                                    re.MULTILINE | re.IGNORECASE)

        self.posicao = (match.start(), match.end())


class ProcedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = (r'((julga-?se|julgo|declaro|DECRETO)[\w ,]{,60}(procedente))|'
                 '(condeno (o|a)(s)? acusad(o|a)(s)?)')
        regex_exclusao = r'improcedente|parcialmente'
        regex_reforco = r'condeno'
        super(ProcedenteClassifier,
              self).__init__(texto,
                             regex=regex,
                             regex_exclusao=regex_exclusao,
                             regex_reforco=regex_reforco)


class ImprocedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = r'((julga-?se|julgo|declaro|DECRETO)[\w ,]{,60}(improcedente))'
        regex_exclusao = r' procedente|parcialmente'
        super(ImprocedenteClassifier,
              self).__init__(texto,
                             regex=regex,
                             regex_exclusao=regex_exclusao)


class ExtincaoPunibilidadeClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = (r'((julga-?se|julgo|declaro|determino|DECRETO)[\w+ ,]{,60}'
                 '(extinto|(extinta|extinc)([\w ,]{,60}(punibilidade|'
                 'pena privativa))?))')
        regex_reforco = r'art\. 107'
        super(ExtincaoPunibilidadeClassifier,
              self).__init__(texto,
                             regex=regex,
                             regex_reforco=regex_reforco)


class ParcialmenteProcedenteClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = (r'((julga-?se|julgo|declaro)[\w+ ,]{,60}(parcialmente)'
                 '[\w ,]{,60}(procedente))')
        regex_exclusao = r'improcedente'
        regex_reforco = r'condeno'
        super(ParcialmenteProcedenteClassifier,
              self).__init__(texto,
                             regex=regex,
                             regex_exclusao=regex_exclusao,
                             regex_reforco=regex_reforco)


class AbsolvoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = (r'(ABSOLVO SUMARIAMENTE)|(ABSOLVO +(o|a)(s)?'
                 ' +acusad(o|a)(s)?)|((fica )?absolvido +(o|a)(s)?'
                 ' +acusad(o|a)(s)?)')
        super(AbsolvoClassifier,
              self).__init__(texto,
                             regex=regex)


class NegacaoProvimentoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = r'(NEGO(-LHE(S)?)? PROVIMENTO)'
        super(NegacaoProvimentoClassifier,
              self).__init__(texto,
                             regex=regex)


class DaProvimentoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = r'(DOU(-LHE(S)?)? PROVIMENTO)'
        super(DaProvimentoClassifier,
              self).__init__(texto,
                             regex=regex)


class DeixoResolverMeritoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = r'(DEIXO[\w+ ,]{,60}RESOLVER[\w ,]{,60}MERITO)'
        super(DeixoResolverMeritoClassifier,
              self).__init__(texto,
                             regex=regex)


class IndeferenciaClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = (r'(indefiro (a(s)? orde(m|ns)|o(s)? pedido(s)?|o(s)?'
                 ' requerimento(s)?))')
        super(IndeferenciaClassifier,
              self).__init__(texto,
                             regex=regex)


class ArquivamentoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = r'((DETERMINO|HOMOLOGO) O ARQUIVAMENTO)'
        super(ArquivamentoClassifier,
              self).__init__(texto,
                             regex=regex)


class ExtincaoProcessoClassifier(BaseClassifier):
    def __init__(self, texto):
        regex = r'(extingo o presente processo)'
        super(ExtincaoProcessoClassifier,
              self).__init__(texto,
                             regex=regex)


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
                   ExtincaoProcessoClassifier]


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
