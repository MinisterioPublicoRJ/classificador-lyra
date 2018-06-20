from unittest import TestCase

from classificador_lyra.procedencia import classifica_item

from .fixtures.improcedencia import improcedentes


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
            'ExtincaoProcessoClassifier': {'positivo': False, 'pesos': []},
            'ExtincaoComResolucaoClassifier': {'positivo': False, 'pesos': []},
            'ExtincaoSemResolucaoClassifier': {'positivo': False, 'pesos': []}
        }
