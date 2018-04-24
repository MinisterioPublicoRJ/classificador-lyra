from unittest import TestCase

from pre_processamento.corretor import corrige_palavras, PALAVRAS_IMPORTANTES


class CorretorPalavras(TestCase):
    def test_corrige_palavras_especificas_do_documento(self):
        documento_com_erro = 'JUGO PROCEDENTE o pedido...'

        documento_corrigido = corrige_palavras(
            documento_com_erro, PALAVRAS_IMPORTANTES
        )

        documento_esperado = 'JULGO PROCEDENTE o pedido...'

        self.assertEqual(documento_corrigido, documento_esperado)

    def test_corrige_multiplas_palavras_do_documento(self):
        documento_com_erro = 'JUGO PROCENTE o pedido...'

        documento_corrigido = corrige_palavras(
            documento_com_erro, PALAVRAS_IMPORTANTES
        )

        documento_esperado = 'JULGO PROCEDENTE o pedido...'

        self.assertEqual(documento_corrigido, documento_esperado)
