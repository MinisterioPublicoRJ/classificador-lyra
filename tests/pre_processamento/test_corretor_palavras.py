from unittest import TestCase, mock

from pre_processamento.corretor import (corrige_documento,
                                        formata_palavras,
                                        filtro_dicionario,
                                        tokeniza,
                                        remove_stopwords,
                                        )


class CorretorPalavras(TestCase):
    def test_corrige_palavras_separadas_internamente_por_espacos(self):
        """
            Em alguns casos, palavras importante veem separadas por espacos,
            como por exemplo H O M O L O G A D O. Estas serão corrigidas
            para a forma sem espaços.
        """
        documento = 'Pelo exposto, H O M O L O G O o pedido'

        documento_corrigido = formata_palavras(documento)

        documento_esperado = 'Pelo exposto, HOMOLOGO o pedido'

        self.assertEqual(documento_corrigido, documento_esperado)

    def test_corrige_palavras_separadas_internamente_com_quebra_de_linha(self):
        documento = 'Pelo exposto, H O M O L O G O\r\n o pedido'

        documento_corrigido = formata_palavras(documento)

        documento_esperado = 'Pelo exposto, HOMOLOGO\r\n o pedido'

        self.assertEqual(documento_corrigido, documento_esperado)

    def test_corrige_palavras_separadas_com_multiplos_espacos(self):
        documento = 'Pelo exposto, H O M  O L O G  O o pedido'

        documento_corrigido = formata_palavras(documento)

        documento_esperado = 'Pelo exposto, HOMOLOGO o pedido'

        self.assertEqual(documento_corrigido, documento_esperado)


class CorretorProbabilistico(TestCase):
    @mock.patch('pre_processamento.utils.dicionario',
                return_values=['artigo', 'sentença'])
    def test_filtra_palavras_presentes_no_dicionario(self, _dicionario):
        """
            Retorna palavras que não estão no dicionário.
        """
        palavras = ['artigo', 'sentença', 'aaabbbccc']

        palavras_conhecidas = filtro_dicionario(palavras)
        esperado = ['aaabbbccc']

        self.assertEqual(palavras_conhecidas, esperado)

    def test_tokeniza_documentos(self):
        documento = 'Um texto qualquer para testar uma função'

        tokens = tokeniza(documento)
        esperado = ['um', 'texto', 'qualquer', 'para', 'testar', 'uma',
                    'função']

        self.assertEqual(tokens, esperado)

    @mock.patch('pre_processamento.utils.stopwords',
                return_values=['um', 'para', 'uma'])
    def test_remove_stopwords(self, _stopwords):
        tokens = ['um', 'texto', 'qualquer', 'para', 'testar', 'uma',
                  'função']

        tokens_filtrados = remove_stopwords(tokens)
        esperado = ['texto', 'qualquer', 'testar', 'função']

        self.assertEqual(tokens_filtrados, esperado)

    def test_corrige_documento(self):
        documento_com_erro = "JULGA-SE PROCENTE O PEDIDO"

        documento_corrigido = corrige_documento(documento_com_erro)
        esperado = "julga-se procedente o pedido"

        self.assertEqual(documento_corrigido, esperado)
