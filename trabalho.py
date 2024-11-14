import re  # Importa o módulo para expressões regulares (usado para validar o formato do email e telefone)
import requests  # Importa o módulo para fazer requisições HTTP (usado para obter dados de sites)
from bs4 import BeautifulSoup  # Importa a biblioteca BeautifulSoup para análise de HTML (usado para extrair informações de páginas web)

# Função para validar CPF usando o algoritmo de validação de CPF
def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")  # Remove pontos e traços do CPF, deixando apenas os números
    if len(cpf) != 11 or not cpf.isdigit():  # Verifica se o CPF tem exatamente 11 dígitos e se são números
        return False  # Se a verificação falhar, retorna False (CPF inválido)

    # Função interna para calcular os dois últimos dígitos verificadores do CPF
    def calcular_digito(digitos):
        soma = sum(int(digitos[i]) * (10 - i) for i in range(9))  # Soma ponderada dos 9 primeiros dígitos
        resto = 11 - (soma % 11)  # Calcula o dígito com base no resto da divisão
        return '0' if resto >= 10 else str(resto)  # Se o resto for maior que 10, o dígito é 0, senão é o valor do resto

    # Compara os dois últimos dígitos do CPF com os dígitos calculados e retorna True se forem válidos
    return cpf[-2:] == calcular_digito(cpf[:9]) + calcular_digito(cpf[:10])


# Função para validar email usando regex
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Expressão regular para validar o formato do email
    return re.match(regex, email) is not None  # Verifica se o email corresponde ao padrão e retorna True ou False


# Função para validar o formato do telefone
def validar_telefone(telefone):
    regex = r'^\(\d{2}\) \d{4,5}-\d{4}$'  # Expressão regular para validar o formato do telefone (exemplo: (12) 34567-8901)
    return re.match(regex, telefone) is not None  # Verifica se o telefone corresponde ao padrão e retorna True ou False


# Função para buscar o menor preço do produto no site do Carrefour
def buscar_preco_teclado():
    url = "https://www.carrefour.com.br/busca/Teclado%20Yamaha%20PSR-E473"  # URL da busca do produto no site do Carrefour
    headers = {"User-Agent": "Chrome/5.0"}  # Cabeçalhos HTTP para simular uma requisição de navegador (impede bloqueios)

    # Faz a requisição HTTP GET para obter o conteúdo da página
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")  # Analisa o conteúdo HTML da página usando BeautifulSoup

    # Tenta encontrar o link do produto com o título "Teclado Yamaha PSR-E473"
    produto = soup.find("a", {"title": "Teclado Yamaha PSR-E473"})
    if produto:  # Se o produto foi encontrado
        link = "https://www.carrefour.com.br" + produto["href"]  # Extrai o link completo do produto
        preco = produto.find_next("span", {"class": "sc-b823b5d6-0"})  # Procura pelo preço do produto na página
        
        if preco:  # Se o preço foi encontrado
            preco_texto = preco.text  # Extrai o texto do preço
        else:
            preco_texto = "Preço não encontrado"  # Caso não encontre o preço, informa que não foi encontrado
    else:
        preco_texto = "Produto não encontrado"  # Se o produto não for encontrado, informa que não foi encontrado
        link = ""  # Não há link a ser retornado

    return preco_texto, link  # Retorna o preço e o link do produto


# Função principal do programa
def main():
    # Coleta dados do usuário via input
    nome = input("Digite o seu nome: ")  # Solicita o nome do usuário
    cpf = input("Digite o seu CPF (xxx.xxx.xxx-xx): ")  # Solicita o CPF do usuário
    email = input("Digite o seu email: ")  # Solicita o email do usuário
    telefone = input("Digite o seu telefone ((xx) xxxxx-xxxx): ")  # Solicita o telefone do usuário

    # Valida os dados inseridos pelo usuário
    if not validar_cpf(cpf):  # Se o CPF for inválido
        print("CPF inválido!")  # Informa que o CPF é inválido
        return  # Encerra a execução da função main
    if not validar_email(email):  # Se o email for inválido
        print("Email inválido!")  # Informa que o email é inválido
        return  # Encerra a execução da função main
    if not validar_telefone(telefone):  # Se o telefone for inválido
        print("Telefone inválido!")  # Informa que o telefone é inválido
        return  # Encerra a execução da função main

    # Chama a função para buscar o menor preço do produto
    preco, link = buscar_preco_teclado()
    # Exibe as informações do produto e do menor preço
    print("\nProduto: Teclado Yamaha PSR-E473")
    print("Menor preço:", preco)  # Exibe o preço encontrado
    print("Link da oferta:", link)  # Exibe o link para a oferta do produto


# Verifica se o script está sendo executado diretamente (não importado) e chama a função principal
if __name__ == "__main__":
    main()  # Executa a função principal do programa
