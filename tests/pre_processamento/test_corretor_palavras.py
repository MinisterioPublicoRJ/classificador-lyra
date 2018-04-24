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

    def test_retorna_palavra_corrigida_com_padrao_da_palavra_original(self):
        """
            Caso a palavra importante que possua um erro ortográfico
            tenha 50% ou mais de suas letras em caixa alta, esta será
            substituída pela correção também em caixa alta. Caso contrário,
            será substituída pela correção em caixa baixa.
        """
        documento_com_erro_1 = 'JULGO PROCedenTE'
        documento_com_erro_2 = 'JULGO PROCedente'

        documento_corrigido_1 = corrige_palavras(
            documento_com_erro_1, PALAVRAS_IMPORTANTES
        )
        documento_corrigido_2 = corrige_palavras(
            documento_com_erro_2, PALAVRAS_IMPORTANTES
        )
        documento_esperado_1 = 'JULGO PROCEDENTE'
        documento_esperado_2 = 'JULGO procedente'

        self.assertEqual(documento_corrigido_1, documento_esperado_1)
        self.assertEqual(documento_corrigido_2, documento_esperado_2)
