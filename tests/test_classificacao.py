from unittest import TestCase, main

from classificadores.regex import classifica_item
from tests.fixtures import sentencas


def _verifica_resultado(resultado):
    return sum([r[0] for r in resultado['classificacoes']])


class Classificacao(TestCase):
    def test_classifica_sentenca(self):
        documento = sentencas[0]

        resultado = classifica_item(documento)

        self.assertTrue(_verifica_resultado(resultado))


if __name__ == '__main__':
    main()
