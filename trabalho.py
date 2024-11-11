import re
import requests
from bs4 import BeautifulSoup

# Função para validar CPF usando o algoritmo de validação de CPF
def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    def calcular_digito(digitos):
        soma = sum(int(digitos[i]) * (10 - i) for i in range(9))
        resto = 11 - (soma % 11)
        return '0' if resto >= 10 else str(resto)

    return cpf[-2:] == calcular_digito(cpf[:9]) + calcular_digito(cpf[:10])


# Função para validar email usando regex
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


# Função para validar o formato do telefone
def validar_telefone(telefone):
    regex = r'^\(\d{2}\) \d{4,5}-\d{4}$'
    return re.match(regex, telefone) is not None


# Função para buscar o menor preço do produto no site do Carrefour
def buscar_preco_teclado():
    url = "https://www.carrefour.com.br/busca/Teclado%20Yamaha%20PSR-E473"
    headers = {"User-Agent": "Chrome/5.0"}

    # Faz a requisição para o site e extrai o menor preço
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Tentativa de extrair o preço e link do produto (ajustado conforme a estrutura do Carrefour)
    produto = soup.find("a", {"title": "Teclado Yamaha PSR-E473"})
    if produto:
        link = "https://www.carrefour.com.br" + produto["href"]
        preco = produto.find_next("span", {"class": "sc-b823b5d6-0"})
        
        if preco:
            preco_texto = preco.text
        else:
            preco_texto = "Preço não encontrado"
    else:
        preco_texto = "Produto não encontrado"
        link = ""

    return preco_texto, link


# Função principal do programa
def main():
    # Coletar dados do usuário
    nome = input("Digite o seu nome: ")
    cpf = input("Digite o seu CPF (xxx.xxx.xxx-xx): ")
    email = input("Digite o seu email: ")
    telefone = input("Digite o seu telefone ((xx) xxxxx-xxxx): ")

    # Validação dos dados
    if not validar_cpf(cpf):
        print("CPF inválido!")
        return
    if not validar_email(email):
        print("Email inválido!")
        return
    if not validar_telefone(telefone):
        print("Telefone inválido!")
        return

    # Consulta e exibição do menor preço do teclado
    preco, link = buscar_preco_teclado()
    print("\nProduto: Teclado Yamaha PSR-E473")
    print("Menor preço:", preco)
    print("Link da oferta:", link)


if __name__ == "__main__":
    main()
