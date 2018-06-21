import re


class BaseClassifier:
    def __init__(self,
                 texto,
                 regex=None,
                 regex_reforco=None,
                 regex_exclusao=None,
                 regex_invalidacao=None,
                 coadunadas=False):
        self.regex = regex
        self.regex_reforco = regex_reforco
        self.regex_exclusao = regex_exclusao
        self.regex_invalidacao = regex_invalidacao
        self.coadunadas = coadunadas
        self.texto = texto
        self.positivo = False
        self.pesos = []
        self.posicao = []
        self.matches = []

    def classificar(self):
        # antes de qualquer coisa, não trabalha com textos que contém
        # termos que são indesejados no texto inteiro e o invalidam
        if self.regex_invalidacao:
            for item in self.regex_invalidacao:
                match = re.search(
                    item,
                    self.texto,
                    re.MULTILINE | re.IGNORECASE)
                if match:
                    return

        # match principal para identificação de sentença
        for item in self.regex:
            match = re.search(item, self.texto, re.MULTILINE | re.IGNORECASE)
            if match:
                self.matches += [match]

        # Se as sentenças regex devem coadunar umas as outras, então
        # todas as regex tem que dar match em algum lugar do texto
        # pelo menos uma vez
        if self.coadunadas and len(self.matches) != len(self.regex):
            return

        # não permite termos indesejados na expressão encontrada
        # cria uma lista cópia da original para iterar e trabalha
        # na remoção dos itens da lista original
        for item in list(self.matches):
            encontrado = item.group(0)
            if self.regex_exclusao and re.findall(self.regex_exclusao,
                                                  encontrado, re.IGNORECASE):
                self.matches.remove(item)

        if not self.matches:
            return

        self.positivo = True

        # legal, parece que temos o que queremos, vamos atribuir pesos
        # reforço aplica um novo conjunto de regras a todo o texto
        if self.regex_reforco:
            self.pesos = re.findall(self.regex_reforco, self.texto,
                                    re.MULTILINE | re.IGNORECASE)

        for match in self.matches:
            self.posicao += [(match.start(), match.end())]


def classifica_item(texto, classificadores):
    classificacoes = {}

    for classificador in classificadores:
        classificador = classificador(texto)
        classificador.classificar()

        classificacoes[classificador.__class__.__name__] = {
            'positivo': classificador.positivo,
            'pesos': classificador.pesos,
        }

    return {
        'conteudo': texto,
        'classificacoes': classificacoes,
        'positivo': sum(
            [classificacoes[x]['positivo'] for x in classificacoes]
        )
    }
