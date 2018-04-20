from unittest import TestCase


class RegexTest(TestCase):
    textos = []
    classificador = None
    operador = None

    class meta:
        abstract = True

    def testador_textos(self):
        for texto in self.textos:
            with self.subTest():
                classificador = self.classificador(texto)
                classificador.classificar()

                assert self.operador(classificador.positivo)
