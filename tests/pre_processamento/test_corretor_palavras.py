from unittest import TestCase

from pre_processamento.corretor import (corrige_documento,
                                        PALAVRAS_IMPORTANTES,
                                        formata_palavras,
                                        encontra_palavra_similiar,
                                        limpa_palavra,
                                        filtro_dicionario,
                                        tokeniza,
                                        remove_stopwords,
                                        )


class CorretorPalavras(TestCase):
    def test_corrige_documento(self):
        documento_com_erro = 'JUGO PROCEDENTE o pedido'

        documento_corrigido = corrige_documento(
            documento_com_erro, PALAVRAS_IMPORTANTES
        )

        documento_esperado = 'JULGO PROCEDENTE o pedido'

        self.assertEqual(documento_corrigido, documento_esperado)

    def test_corrige_multiplas_palavras_do_documento(self):
        documento_com_erro = 'JUGO PROCENTE o pedido'

        documento_corrigido = corrige_documento(
            documento_com_erro, PALAVRAS_IMPORTANTES
        )

        documento_esperado = 'JULGO PROCEDENTE o pedido'

        self.assertEqual(documento_corrigido, documento_esperado)

    def test_retorna_palavra_corrigida_com_padrao_da_palavra_original(self):
        """
            Caso a palavra importante que possua um erro ortográfico
            tenha 50% ou mais de suas letras em caixa alta, esta será
            substituída pela correção também em caixa alta. Caso contrário,
            será substituída pela correção em caixa baixa.
        """
        documento_com_erro_1 = 'JULGO PROCedeTE'
        documento_com_erro_2 = 'JULGO PROecdente'

        documento_corrigido_1 = corrige_documento(
            documento_com_erro_1, PALAVRAS_IMPORTANTES
        )
        documento_corrigido_2 = corrige_documento(
            documento_com_erro_2, PALAVRAS_IMPORTANTES
        )
        documento_esperado_1 = 'JULGO PROCEDENTE'
        documento_esperado_2 = 'JULGO procedente'

        self.assertEqual(documento_corrigido_1, documento_esperado_1)
        self.assertEqual(documento_corrigido_2, documento_esperado_2)

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

    def test_substitui_por_palavra_mais_similiar(self):
        """
            Em alguns casos, existem palavras muito parecidas que podem
            ser substituídas pela opção errada. I.e: Declaro e Decreto.
            As palavras devem ser corrigidas pelas palavras mais próximas
            e palavras corretas não devem ser corrigidas.
        """
        documento_com_erro = 'Decaro prodecente o decreto'

        documento_corrigido = corrige_documento(documento_com_erro,
                                                PALAVRAS_IMPORTANTES)
        documento_esperado = 'declaro procedente o decreto'

        self.assertEqual(documento_corrigido, documento_esperado)

    def test_encontra_palavra_mais_similar(self):
        palavra_com_erro = 'decaro'

        palavra_corrigida = encontra_palavra_similiar(
            palavra_com_erro,
            PALAVRAS_IMPORTANTES
        )
        palavra_esperada = 'declaro'

        self.assertEqual(palavra_corrigida, palavra_esperada)

    def test_limpa_palavra_antes_da_correcao(self):
        palavra = 'Pedido...'

        palavra_limpa = limpa_palavra(palavra)
        palavra_esperada = 'Pedido'

        self.assertEqual(palavra_limpa, palavra_esperada)

    def test_mantem_estrutura_original_do_texto(self):
        """
            Ao substituir uma palavra manter o restante da estrutura do texto
            intacta.
        """
        documento = "Jlgo procedente o peddio..."

        documento_corrigido = corrige_documento(documento,
                                                PALAVRAS_IMPORTANTES)

        documento_esperado = 'julgo procedente o pedido...'
        self.assertEqual(documento_corrigido, documento_esperado)


class CorretorProbabilistico(TestCase):
    def test_filtra_palavras_presentes_no_dicionario(self):
        """
            Retorna palavras que não estão no dicionário.
        """
        palavras = ['artigo', 'sentença', 'aaabbbccc']
        dicionario = ['artigo', 'sentença']

        palavras_conhecidas = filtro_dicionario(palavras, dicionario)
        esperado = ['aaabbbccc']

        self.assertEqual(palavras_conhecidas, esperado)

    def test_tokeniza_documentos(self):
        documento = 'Um texto qualquer para testar uma função'

        tokens = tokeniza(documento)
        esperado = ['um', 'texto', 'qualquer', 'para', 'testar', 'uma',
                    'função']

        self.assertEqual(tokens, esperado)

    def test_remove_stopwords(self):
        tokens = ['um', 'texto', 'qualquer', 'para', 'testar', 'uma',
                  'função']

        stopwords = ['um', 'para', 'uma']
        tokens_filtrados = remove_stopwords(tokens, stopwords)
        esperado = ['texto', 'qualquer', 'testar', 'função']

        self.assertEqual(tokens_filtrados, esperado)
