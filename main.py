import random

class Caracteristicas:
    racas_disponiveis = ["Humano", "Elfo", "Anão", "Orc", "Halfling"]
    classes_disponiveis = ["Guerreiro", "Mago", "Ladino", "Clérigo", "Bárbaro"]

    def __init__(self, nome, raca, classe):
        self.nome = nome
        self.raca = raca
        self.classe = classe

    @staticmethod
    def validar_nome(nome):
        return isinstance(nome, str) and nome.isalpha()

    @classmethod
    def validar_raca(cls, raca):
        return raca in cls.racas_disponiveis

    @classmethod
    def validar_classe(cls, classe):
        return classe in cls.classes_disponiveis

    def __str__(self):
        return f'Nome: {self.nome}\nRaça: {self.raca}\nClasse: {self.classe}'


def criar_caracteristicas():
    print("=== Criação de Personagem ===")
    nome = input("Digite seu nome: ")
    print("\nRaças disponíveis:", ", ".join(Caracteristicas.racas_disponiveis))
    raca = input("Escolha sua raça: ")
    print("\nClasses disponíveis:", ", ".join(Caracteristicas.classes_disponiveis))
    classe = input("Escolha sua classe: ")
    erros = []
    if not Caracteristicas.validar_nome(nome):
        erros.append("Nome inválido. Use apenas letras.")
    if not Caracteristicas.validar_raca(raca):
        erros.append("Raça inválida.")
    if not Caracteristicas.validar_classe(classe):
        erros.append("Classe inválida.")
    if erros:
        print("\nErros encontrados:")
        for e in erros:
            print("-", e)
        return None
    return Caracteristicas(nome, raca, classe)


class Atributos:
    bonus_raciais = {
        "Humano": {"forca": 1, "destreza": 1, "constituicao": 1, "sabedoria": 1, "inteligencia": 1, "carisma": 1},
        "Elfo": {"destreza": 2, "sabedoria": 1},
        "Anão": {"constituicao": 2, "forca": 1},
        "Orc": {"forca": 2, "constituicao": 1},
        "Halfling": {"destreza": 2, "carisma": 1}
    }

    bonus_classes = {
        "Guerreiro": {"forca": 2, "constituicao": 1},
        "Mago": {"inteligencia": 2, "sabedoria": 1},
        "Ladino": {"destreza": 2, "carisma": 1},
        "Clérigo": {"sabedoria": 2, "carisma": 1},
        "Bárbaro": {"forca": 2, "constituicao": 1}
    }

    def __init__(self, forca, destreza, constituicao, sabedoria, inteligencia, carisma):
        self.forca = forca
        self.destreza = destreza
        self.constituicao = constituicao
        self.sabedoria = sabedoria
        self.inteligencia = inteligencia
        self.carisma = carisma
        self.bonus_raca = {"forca":0,"destreza":0,"constituicao":0,"sabedoria":0,"inteligencia":0,"carisma":0}
        self.bonus_classe = {"forca":0,"destreza":0,"constituicao":0,"sabedoria":0,"inteligencia":0,"carisma":0}

    @staticmethod
    def validar_valor(nome, valor):
        if not isinstance(valor, int):
            return f"{nome} deve ser um número inteiro."
        if valor < 1 or valor > 20:
            return f"{nome} deve estar entre 1 e 20."
        return None

    @classmethod
    def validar_atributos(cls, **atributos):
        erros = []
        for nome, valor in atributos.items():
            erro = cls.validar_valor(nome, valor)
            if erro:
                erros.append(erro)
        return erros

    def aplicar_bonus_raca(self, raca):
        bonus = Atributos.bonus_raciais.get(raca, {})
        for atributo, valor_bonus in bonus.items():
            setattr(self, atributo, getattr(self, atributo) + valor_bonus)
            self.bonus_raca[atributo] = valor_bonus

    def aplicar_bonus_classe(self, classe):
        bonus = Atributos.bonus_classes.get(classe, {})
        for atributo, valor_bonus in bonus.items():
            setattr(self, atributo, getattr(self, atributo) + valor_bonus)
            self.bonus_classe[atributo] = valor_bonus

    def __str__(self):
        linhas = []
        for attr in ["forca","destreza","constituicao","sabedoria","inteligencia","carisma"]:
            base = getattr(self, attr) - self.bonus_raca[attr] - self.bonus_classe[attr]
            linha = f"{attr.capitalize()}: {base} + {self.bonus_raca[attr]} (raça) + {self.bonus_classe[attr]} (classe) = {getattr(self, attr)}"
            linhas.append(linha)
        return "\n".join(linhas)


def rolar_dado():
    dados = [random.randint(1, 6) for _ in range(4)]
    dados.remove(min(dados))
    return sum(dados)

def rolar_atributos():
    print("\nRolando atributos (4d6, descarta o menor)...")
    nomes = ["forca", "destreza", "constituicao", "sabedoria", "inteligencia", "carisma"]
    valores = {nome: rolar_dado() for nome in nomes}
    print("Resultados:")
    for nome, valor in valores.items():
        print(f"{nome.capitalize()}: {valor}")
    return Atributos(
        valores["forca"],
        valores["destreza"],
        valores["constituicao"],
        valores["sabedoria"],
        valores["inteligencia"],
        valores["carisma"]
    )

def distribuir_atributos():
    print("\n=== Distribuição de Atributos Manual ===")
    nomes = ["forca", "destreza", "constituicao", "sabedoria", "inteligencia", "carisma"]
    valores = {}
    for nome in nomes:
        while True:
            try:
                valor = int(input(f"Digite o valor de {nome.capitalize()} (1 a 20): "))
                valores[nome] = valor
                break
            except ValueError:
                print("Valor inválido.")
    erros = Atributos.validar_atributos(**valores)
    if erros:
        print("\nErros encontrados:")
        for e in erros:
            print("-", e)
        return None
    return Atributos(
        valores["forca"],
        valores["destreza"],
        valores["constituicao"],
        valores["sabedoria"],
        valores["inteligencia"],
        valores["carisma"]
    )

def escolher_modo_atributos():
    print("\nEscolha o modo de definição dos atributos:")
    print("1 - Distribuir manualmente")
    print("2 - Rolar dados (4d6)")
    escolha = input("Opção: ")
    if escolha == "1":
        return distribuir_atributos()
    elif escolha == "2":
        return rolar_atributos()
    else:
        print("Opção inválida.")
        return None


class Personagem:
    def __init__(self, caracteristicas, atributos):
        self.caracteristicas = caracteristicas
        self.atributos = atributos
        self.atributos.aplicar_bonus_raca(caracteristicas.raca)
        self.atributos.aplicar_bonus_classe(caracteristicas.classe)

    def __str__(self):
        return f"{self.caracteristicas}\n\nAtributos (com bônus):\n{self.atributos}"


if __name__ == "__main__":
    caracteristicas = criar_caracteristicas()
    if caracteristicas:
        atributos = escolher_modo_atributos()
        if atributos:
            personagem = Personagem(caracteristicas, atributos)
            print("\nPersonagem criado com sucesso!\n")
            print(personagem)
