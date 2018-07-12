from classificador_lyra.regex import classifica_item_sequencial
from classificador_lyra.procedencia import (
    classificadores,
    ImprocedenteClassifier
)
from .fixtures.improcedencia import improcedentes


def test_classificador_improcedente():
    resultado = classifica_item_sequencial(
        improcedentes[0],
        classificadores
    )
    assert isinstance(resultado['classificacao'], ImprocedenteClassifier)
