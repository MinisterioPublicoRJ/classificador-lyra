class Dispositivo:
    """Agrega um classificador e, através de suas propriedades, extrai
    o disposiivo de uma sentença"""

    def __init__(self, classificador):
        """Inicia um extrator de dispositivos


        Keyword arguments:
        classificador -- classificador previamente classificado
        """

        self.classificador = classificador
        self.dispositivos = []

    def extrair(self):
        """Efetivamente extrai os dispositivos no formato:

        [{
            'slice': int -- índice de referência para extração do parágrafo
            'conteudo: str -- conteúdo extraído considerando os parágrafos
        }]

        Armazenando o resultado na propriedade `.dispositivos`
        """

        for posicao in self.classificador.posicao:
            self.dispositivos += [{
                'conteudo': Dispositivo._recortar(
                    self.classificador.texto,
                    posicao[0]
                ),
                'slice': posicao[0]
            }]

    @staticmethod
    def _recortar(texto, posicao):
        """Recorta todo um parágrafo do texto em torno da
        posição do slice no texto"""
        inicio, fim = texto[0:posicao].split("\n"), texto[posicao:].split("\n")
        return inicio[-1] + fim[0]
