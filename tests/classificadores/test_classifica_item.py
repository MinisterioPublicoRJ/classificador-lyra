import operator
from unittest import TestCase

from classificadores.regex import classifica_item

from .fixtures.improcedencia import improcedentes, nao_improcedentes
from .fixtures.procedencia import procedentes, nao_procedentes


class ClassificaTest(TestCase):

    def test_classificador_improcedente(self):
        resultado = classifica_item(improcedentes[0])
        assert resultado['classificacoes'] == {
            'ProcedenteClassifier': {'positivo': False, 'pesos': []},
            'ImprocedenteClassifier': {'positivo': True, 'pesos': []},
            'ParcialmenteProcedenteClassifier':
                {'positivo': False, 'pesos': []},
            'ExtincaoPunibilidadeClassifier':
                {'positivo': False, 'pesos': []},
            'AbsolvoClassifier': {'positivo': False, 'pesos': []},
            'NegacaoProvimentoClassifier': {'positivo': False, 'pesos': []},
            'DeixoResolverMeritoClassifier': {'positivo': False, 'pesos': []},
            'DaProvimentoClassifier': {'positivo': False, 'pesos': []},
            'IndeferenciaClassifier': {'positivo': False, 'pesos': []},
            'ArquivamentoClassifier': {'positivo': False, 'pesos': []},
            'ExtincaoProcessoClassifier': {'positivo': False, 'pesos': []}
        }
