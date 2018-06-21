
import operator
from classificador_lyra.consumidor import (
    CobrancaSobAmeaca,
    CobrancaServicoNaoFornecido,
    DanosEletrodomesticos
)
from ..fixtures.consumidor import (
    cobranca_sob_ameaca,
    nao_cobranca_sob_ameaca,
    cobranca_servico_nao_fornecido,
    nao_cobranca_servico_nao_fornecido_toi,
    nao_cobranca_servico_nao_fornecido,
    dano_eletrodomestico,
    nao_dano_eletrodomestico_toi,
    nao_dano_eletrodomestico
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
