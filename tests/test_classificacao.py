from unittest import TestCase, main

from classificadores.regex import classifica_item
from tests.fixtures import sentencas, nao_sentencas


def _verifica_resultado(resultado):
    return resultado['positivo']


class Classificacao(TestCase):
    def test_classifica_sentenca(self):
        documento = sentencas[0]

        resultado = classifica_item(documento)

        self.assertTrue(_verifica_resultado(resultado))

    def test_classifica_nao_sentenca(self):
        documento = nao_sentencas[0]

        resultado = classifica_item(documento)

        self.assertFalse(_verifica_resultado(resultado))


if __name__ == '__main__':
    main()
