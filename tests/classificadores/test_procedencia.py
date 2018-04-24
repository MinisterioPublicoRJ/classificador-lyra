import operator

from classificadores.regex import ProcedenteClassifier

from .fixtures.procedencia import nao_procedentes, procedentes
from .utils import RegexTest


class ProcedenciaTest(RegexTest):
    classificador = ProcedenteClassifier

    def test_procedente(self):
        self.textos = procedentes
        self.operador = operator.truth
        self.testador_textos()

    def test_nao_procedente(self):
        self.textos = nao_procedentes
        self.operador = operator.not_
        self.testador_textos()
