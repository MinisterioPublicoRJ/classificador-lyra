from unittest import TestCase
from classificador_lyra.regex import (
    constroi_classificador_dinamica
)


_TEXTO = "texto"
_REGEX = ["REGEX"]
_REGEX_REFORCO = ["regex_reforco"]
_REGEX_EXCLUSAO = ["regex_exclusao"]
_REGEX_INVALIDACAO = ["regex_invalidacao"]
_COADUNADAS = False
_PARAMETROS = {
    "regex": _REGEX,
    "regex_reforco": _REGEX_REFORCO,
    "regex_exclusao": _REGEX_EXCLUSAO,
    "regex_invalidacao": _REGEX_INVALIDACAO,
    "coadunadas": _COADUNADAS
}


class TesteClassificadorParametrizado(TestCase):
    def teste_construtor_classificador_parametrizado(self):
        nova = constroi_classificador_dinamica("nova", _PARAMETROS)

        teste = nova(
            _TEXTO
        )

        self.assertEqual(teste.__class__.__name__, "nova")
        self.assertEqual(teste.texto, _TEXTO)
        self.assertEqual(teste.regex, _REGEX)
        self.assertEqual(teste.regex_reforco, _REGEX_REFORCO)
        self.assertEqual(teste.regex_invalidacao, _REGEX_INVALIDACAO)
        self.assertEqual(teste.regex_exclusao, _REGEX_EXCLUSAO)
        self.assertEqual(teste.coadunadas, _COADUNADAS)
