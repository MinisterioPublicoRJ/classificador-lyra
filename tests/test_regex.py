from unittest import TestCase
from classificador_lyra.regex import ClassificadorParametrizado


_TEXTO = "texto"
_REGEX = ["REGEX"]
_REGEX_REFORCO = ["regex_reforco"]
_REGEX_EXCLUSAO = ["regex_exclusao"]
_REGEX_INVALIDACAO = ["regex_invalidacao"]
_COADUNADAS = False


class TesteClassificadorParametrizado(TestCase):
    def test_instanciamento(self):
        classificador = ClassificadorParametrizado(
            _TEXTO,
            {
                "regex": _REGEX,
                "regex_reforco": _REGEX_REFORCO,
                "regex_exclusao": _REGEX_EXCLUSAO,
                "regex_invalidacao": _REGEX_INVALIDACAO,
                "coadunadas": _COADUNADAS
            }
        )

        self.assertEqual(classificador.texto, _TEXTO)
        self.assertEqual(classificador.regex, _REGEX)
        self.assertEqual(classificador.regex_reforco, _REGEX_REFORCO)
        self.assertEqual(classificador.regex_invalidacao, _REGEX_INVALIDACAO)
        self.assertEqual(classificador.regex_exclusao, _REGEX_EXCLUSAO)
        self.assertEqual(classificador.coadunadas, _COADUNADAS)
