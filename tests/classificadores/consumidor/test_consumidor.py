
import operator

from classificador_lyra.consumidor import 

from .fixtures.improcedencia import improcedentes, nao_improcedentes
from .utils import RegexTest


class Cobran(RegexTest):
    classificador = ImprocedenteClassifier

    def test_improcedente(self):
        self.textos = improcedentes
        self.operador = operator.truth
        self.testador_textos()

    def test_nao_improcedente(self):
        self.textos = nao_improcedentes
        self.operador = operator.not_
        self.testador_textos()
