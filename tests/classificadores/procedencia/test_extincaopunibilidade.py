from classificador_lyra.procedencia import ExtincaoPunibilidadeClassifier
from ..utils import RegexTest


class ExtincaoPunibilidadeTest(RegexTest):
    classificador = ExtincaoPunibilidadeClassifier

    def test_extincao(self):
        pass
