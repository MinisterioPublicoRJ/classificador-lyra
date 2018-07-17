from classificador_lyra.regex import BaseClassifier


_TOI = r'(TOI|T\.O\.I|Termo de Ocorr.ncia.{,6}Irregularidade)'


class CobrancaSobAmeaca(BaseClassifier):
    def __init__(self, texto):
        regex = [
            _TOI,
            r'(multa|irregularidade)',
        ]

        super().__init__(
            texto,
            regex=regex,
            coadunadas=True
        )


class DificuldadeContratacaoRecusaInjustificada(BaseClassifier):
    def __init__(self, texto):
        regex = [
            r'(titularidade|antigo morador|morador antigo|'
            r'locat.rio|inquilino)'
        ]

        regex_invalidacao = [
            _TOI,
            r'(medidor)'
        ]

        super().__init__(
            texto,
            regex=regex,
            regex_invalidacao=regex_invalidacao
        )


class DanosEletrodomesticos(BaseClassifier):
    def __init__(self, texto):
        regex = [
            r'(perda|dano|queimou|queima|assist.ncia|aparelho|'
            r'eletrodom.stico|\sTV\s|geladeira|refrigerador|danificado)'
        ]

        regex_invalidacao = [
            r'(\sconta\s|fatura|cobran.a|\sm[éÉe]dia\s|estimativa)',
            _TOI
        ]

        super().__init__(
            texto,
            regex=regex,
            regex_invalidacao=regex_invalidacao
        )


class InterrupcaoInstabilidadeFornecimento(BaseClassifier):
    def __init__(self, texto):
        regex = [
            r'(interrup..o|queda|oscila..o|)'
        ]

        regex_invalidacao = [
            r'(queimou|aparelho|eletrodom.stico|\sm.dia\s|estimativa)',
            _TOI
        ]

        super().__init__(
            texto,
            regex=regex,
            regex_invalidacao=regex_invalidacao
        )


class NegativacaoIndevida(BaseClassifier):
    def __init__(self, texto):
        regex = [
            r'(cadastro de (inadimplentes|devedores|'
            r'restritivo de cr.dito|restri..o de cr.dito|prote..o de credito'
            r'maus pagadores)|'
            r'restri..o em cadastro de consumo|SPC|CADIN|SERASA)'
        ]

        regex_invalidacao = [
            r'(parcelamento|negocia..o)'
        ]

        super().__init__(
            texto,
            regex=regex,
            regex_invalidacao=regex_invalidacao
        )


class DificuldadeRenegociacao(BaseClassifier):
    def __init__(self, texto):
        regex = [
            r'(parcelamento|renegocia..o)'
        ]

        super().__init__(
            texto=texto,
            regex=regex
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
            texto,
            regex=regex,
            regex_invalidacao=regex_invalidacao
        )


classificadores = [
    CobrancaSobAmeaca,
    DificuldadeContratacaoRecusaInjustificada,
    DanosEletrodomesticos,
    InterrupcaoInstabilidadeFornecimento,
    NegativacaoIndevida,
    CobrancaServicoNaoFornecido,
]
