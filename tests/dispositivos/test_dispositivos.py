from unittest import TestCase
from .fixtures.fixtures import procedencia, recorte_procedencia
from classificador_lyra.dispositivo import Dispositivo
from classificador_lyra.procedencia import ProcedenteClassifier


class Dispositivos(TestCase):
    def test_recortar(self):
        assert Dispositivo._recortar(procedencia, 1000) == recorte_procedencia

    def test_classificaco_com_dispositivo(self):
        classificador = ProcedenteClassifier(procedencia)
        classificador.classificar()

        dispositivo = Dispositivo(classificador)
        dispositivo.extrair()

        assert dispositivo.dispositivos[0]['conteudo'] == recorte_procedencia
