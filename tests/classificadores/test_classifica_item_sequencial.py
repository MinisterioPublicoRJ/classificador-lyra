from unittest import TestCase
from classificador_lyra.regex import classifica_item_sequencial
from classificador_lyra.procedencia import (
    classificadores,
    ImprocedenteClassifier
)
from .fixtures.improcedencia import improcedentes


class ClassificaTest(TestCase):

    def test_classificador_improcedente(self):
        resultado = classifica_item_sequencial(
            improcedentes[0],
            classificadores
        )
        assert type(resultado['classificacao']) == ImprocedenteClassifier
