from classificador_lyra.regex import BaseClassifier


_TOI = r'(TOI|T\.O\.I|Termo de Ocorr.ncia.{,6}Irregularidade)'


class CobrancaSobAmeaca(BaseClassifier):
    def __init__(self, texto):
        regex = [
            _TOI,
            r'(multa|irregularidade)',
        ]

        super().__init__(
            self,
            regex=regex,
            coadunadas=True
        )


class CobrancaServicoNaoFornecido(BaseClassifier):
    def __init__(self, texto):
        regex = [
            r'(conta|fatura|cobran.a|m.dia|estimativa|consumo)'
        ]

        regex_invalidacao = [
            _TOI,
            r'(multa|irregularidade|perda|dano|queimou|queima|assist.ncia)'
        ]

        super().__init__(
            self,
            regex=regex,
            regex_invalidacao=regex_invalidacao
        )


class DanosEletrodomesticos(BaseClassifier):
    def __init__(self, texto):
        regex = [
            r'(perda|dano|queimou|queima|assist.ncia|aparelho|'
            r'eletrodom.stico|TV|geladeira|refrigerador|danificado)'
        ]

        regex_invalidacao = [
            r'(conta|fatura|cobran.a|m[éÉe]dia)'
        ]

        super().__init__(
            self,
            regex=regex,
            regex_invalidacao=regex_invalidacao
        )


classificadores = [
    CobrancaSobAmeaca,
    CobrancaServicoNaoFornecido,
    DanosEletrodomesticos
]
