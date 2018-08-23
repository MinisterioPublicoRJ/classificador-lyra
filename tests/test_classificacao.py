from unittest import TestCase
from classificador_lyra.regex import classifica_item
from classificador_lyra.procedencia import classificadores
from tests.fixtures import sentencas, nao_sentencas


def _verifica_resultado(resultado):
    return resultado['positivo']


class Classificacao(TestCase):
    def test_classifica_sentenca(self):
        documento = sentencas[0]

        resultado = classifica_item(documento, classificadores)

        self.assertTrue(_verifica_resultado(resultado))

    def test_classifica_nao_sentenca(self):
        documento = nao_sentencas[0]

        resultado = classifica_item(documento, classificadores)

        self.assertFalse(_verifica_resultado(resultado))
