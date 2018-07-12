import re
from abc import ABC


class BaseClassifier(ABC):
    """Classificador utilizando expressões regulares"""
    def __init__(self,
                 texto,
                 regex=None,
                 regex_reforco=None,
                 regex_exclusao=None,
                 regex_invalidacao=None,
                 coadunadas=False):
        """
        Constrói um Classificador REGEX

        O validador irá processar o texto informado após a execução
        do método "classificar", atribuindo às propriedades:
            positivo bool
            pesos [str]
            posicao [(int,)]
            matches [re]

        Que podem ser utilizadas posteriormente para análise dos
        matches encontrados.

        Keywords arguments:
        texto -- str
                    Texto a ser classificado.
                    Pode ser um texto de múltiplas linhas
        regex -- [str]
                    Conjunto de expressões regulares principais
                    a serem confrontadas com o texto informado.
                    A regex deve possuir pelo menos uma opção
                    englobando toda a expressão, ex.:
                    r'(expressao|outra expressao)'
                    Podem ser informadas quantas expressões
                    forem necessárias para realizar buscas
                    no texto
        regex_reforco -- [str]
                    Conjunto de expressões que, caso tenha
                    sido encontrado pelo menos uma expressão
                    válida nas expressões principais acima,
                    informa também em quais locais do texto
                    foram encontradas expressões que podem
                    auxiliar na validação de um documento e
                    dar mais "peso" a ele.
                    Armazenará o resultado na propriedade
                    "pesos" para posterior análise
        regex_exclusao -- [str]
                    Para cada expressão principal encontrada o
                    validador irá confrontar expressões que
                    não deveriam estar no match, ex.:
                    Texto: 'parcialmente procedente'
                    Regex: r'(parcialmente.{,10}procedente)'
                    Regex Exclusão: r'(improcedente)'
                    Fará com que o validador encontre:
                        "Parcialmente procedente"
                    E não valide expressões como
                        "Parcialmente improcedente"
        regex_invalidacao -- [str]
                    Marca como negativa a validação de
                    um texto caso qualquer uma das expressões
                    informadas neste parâmetro seja encontrada
                    em todo o texto.
        coadunadas -- bool (default=False)
                    Caso esse parâmetro seja True, o classificador
                    irá obrigar que todas as expressões regulares
                    informadas estejam presentes no texto a ser
                    classificado.
                    Caso qualquer uma das expressões informadas não
                    esteja no texto, ela será marcada como negativa.
        """
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
        """
        Classifica o Texto parametrizado com os critérios informados
        no construtor
        """

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

        # match principal para identificação de documento
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


def classifica_item_sequencial(texto, classificadores):
    for classificador in classificadores:
        classificador = classificador(texto)
        classificador.classificar()

        if classificador.positivo:
            return {
                'conteudo': texto,
                'classificacao': classificador,
            }
