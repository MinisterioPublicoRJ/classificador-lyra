
import operator
from classificador_lyra.consumidor import (
    CobrancaSobAmeaca,
    CobrancaServicoNaoFornecido,
    DanosEletrodomesticos,
    DificuldadeContratacaoRecusaInjustificada,
    InterrupcaoInstabilidadeFornecimento,
    NegativacaoIndevida,
    DificuldadeRenegociacao,
    DemandaNaoResolvida,
    CobrancaTarifa,
)
from ..fixtures.consumidor import (
    cobranca_sob_ameaca,
    nao_cobranca_sob_ameaca,
    cobranca_servico_nao_fornecido,
    nao_cobranca_servico_nao_fornecido_toi,
    nao_cobranca_servico_nao_fornecido,
    dano_eletrodomestico,
    nao_dano_eletrodomestico_toi,
    nao_dano_eletrodomestico,
    dificuldade_contratar,
    interrupcao_fornecimento,
    negativacao_indevida,
    nao_negativacao_indevida,
    dificuldade_renegociacao,
    sac,
    tarifa,
)
from ..utils import RegexTest


class TestCobrancaSobAmeaca(RegexTest):
    classificador = CobrancaSobAmeaca

    def test_ameaca(self):
        self.textos = cobranca_sob_ameaca
        self.operador = operator.truth
        self.testador_textos()

    def test_nao_ameaca(self):
        self.textos = nao_cobranca_sob_ameaca
        self.operador = operator.not_
        self.testador_textos()


class TestCobrancaServicoNaoFornecido(RegexTest):
    classificador = CobrancaServicoNaoFornecido

    def test_nao_fornecido(self):
        self.textos = cobranca_servico_nao_fornecido
        self.operador = operator.truth
        self.testador_textos()

    def test_nao_fornecido_nao_toi(self):
        self.textos = nao_cobranca_servico_nao_fornecido_toi
        self.operador = operator.not_
        self.testador_textos()

    def test_nao_fornecido_nao(self):
        self.textos = nao_cobranca_servico_nao_fornecido
        self.operador = operator.not_
        self.testador_textos()


class TestDanosEletrodomesticos(RegexTest):
    classificador = DanosEletrodomesticos

    def test_danos_eletrodomesticos(self):
        self.textos = dano_eletrodomestico
        self.operador = operator.truth
        self.testador_textos()

    def test_nao_danos_eletrodomesticos_toi(self):
        self.textos = nao_dano_eletrodomestico_toi
        self.operador = operator.not_
        self.testador_textos()

    def test_nao_danos_eletrodomesticos(self):
        self.textos = nao_dano_eletrodomestico
        self.operador = operator.not_
        self.testador_textos()


class TestDificuldadeContratacaoRecusaInjustificada(RegexTest):
    classificador = DificuldadeContratacaoRecusaInjustificada

    def test_dificuldade_contratar(self):
        self.textos = dificuldade_contratar
        self.operador = operator.truth
        self.testador_textos()


class TestInterrupcaoInstabilidadeFornecimento(RegexTest):
    classificador = InterrupcaoInstabilidadeFornecimento

    def test_instabilidade_fornecimento(self):
        self.textos = interrupcao_fornecimento
        self.operador = operator.truth
        self.testador_textos()


class TestNegativacaoIndevida(RegexTest):
    classificador = NegativacaoIndevida

    def test_negativacao_indevida(self):
        self.textos = negativacao_indevida
        self.operador = operator.truth
        self.testador_textos()

    def test_nao_negativacao_indevida(self):
        self.textos = nao_negativacao_indevida
        self.operador = operator.not_
        self.testador_textos()


class TestDificuldadeRenegociacao(RegexTest):
    classificador = DificuldadeRenegociacao

    def test_dificuldade_renegociacao(self):
        self.textos = dificuldade_renegociacao
        self.operador = operator.truth
        self.testador_textos()


class TestDemanadaNaoResolvida(RegexTest):
    classificador = DemandaNaoResolvida

    def test_demanda_nao_resolvida(self):
        self.textos = sac
        self.operador = operator.truth
        self.testador_textos()


class TestCobrancaTarifa(RegexTest):
    classificador = CobrancaTarifa

    def test_cobranca_tarifa(self):
        self.textos = tarifa
        self.operador = operator.truth
        self.testador_textos()
