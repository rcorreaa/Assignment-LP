class Produto:
  def __init__(self, codigo_barras, nome, preco):
      self.codigo_barras = codigo_barras
      self.nome = nome
      self.preco = preco

class ProdutoFisico(Produto):
  def __init__(self, codigo_barras, nome, preco, peso):
      super().__init__(codigo_barras, nome, preco)
      self.peso = peso

class ProdutoDigital(Produto):
  def __init__(self, codigo_barras, nome, preco, tamanho_arquivo):
      super().__init__(codigo_barras, nome, preco)
      self.tamanho_arquivo = tamanho_arquivo

class ProdutoVirtual(Produto):
  def __init__(self, codigo_barras, nome, preco, link_download):
      super().__init__(codigo_barras, nome, preco)
      self.link_download = link_download

class ProdutoNaoEncontradoException(Exception):
  pass

class QuantidadeInsuficienteException(Exception):
  pass

class Inventario:
  def __init__(self):
      self.produtos = []

  def adicionar_produto(self, produto, quantidade):
      self.produtos.extend([produto] * quantidade)

  def vender_produto(self, codigo_barras):
      for produto in self.produtos:
          if produto.codigo_barras == codigo_barras:
              self.produtos.remove(produto)
              return produto
      raise ProdutoNaoEncontradoException("Produto não encontrado no estoque.")

  def retornar_produto(self, produto):
      self.produtos.append(produto)
    
  def obter_informacoes_inventario(self):
    produtos_diferentes = {}  # Usaremos um dicionário para armazenar produtos distintos e suas quantidades

    for produto in self.produtos:
      if isinstance(produto, ProdutoFisico):
          tipo_produto = "Produto Físico"
      elif isinstance(produto, ProdutoDigital):
          tipo_produto = "Produto Digital"
      elif isinstance(produto, ProdutoVirtual):
          tipo_produto = "Produto Virtual"
      else:
          tipo_produto = "Tipo de Produto Desconhecido"

      chave_produto = (produto.codigo_barras, tipo_produto)  # Usamos uma tupla como chave do dicionário
      if chave_produto in produtos_diferentes:
          produtos_diferentes[chave_produto]["quantidade"] += 1
      else:
          produtos_diferentes[chave_produto] = {
              "nome": produto.nome,
              "preco": produto.preco,
              "quantidade": 1,
              "informacoes_adicionais": produto.peso if isinstance(produto, ProdutoFisico) else produto.tamanho_arquivo if isinstance(produto, ProdutoDigital) else produto.link_download
          }

    informacoes = []
    for chave, produto_info in produtos_diferentes.items():
      informacoes.append(f"{chave[1]} - Código de Barras: {chave[0]}, Nome: {produto_info['nome']}, Preço: {produto_info['preco']}, Quantidade: {produto_info['quantidade']}, Informações Adicionais: {produto_info['informacoes_adicionais']}")
    return informacoes

if __name__ == "__main__":
  inventario = Inventario()

  produto1 = ProdutoFisico("123456", "Camiseta", 29.99, 0.3)
  produto2 = ProdutoDigital("789012", "Ebook", 9.99, 2)
  produto3 = ProdutoVirtual("345678", "Curso Online", 49.99, "http://curso.com/download")

  inventario.adicionar_produto(produto1, 10)
  inventario.adicionar_produto(produto2, 5)
  inventario.adicionar_produto(produto3, 3)

  while True:
      print("\nOpções:")
      print("1. Vender Produto")
      print("2. Adicionar Produto")
      print("3. Sair")
      print("4. Consultar Inventário")
      escolha = input("Escolha uma opção: ")

      if escolha == "1":
          codigo_barras = input("Digite o código de barras do produto a ser vendido: ")
          try:
              produto_vendido = inventario.vender_produto(codigo_barras)
              print(f"Produto vendido: {produto_vendido.nome}")
          except ProdutoNaoEncontradoException:
              print("Produto não encontrado no estoque.")
          except QuantidadeInsuficienteException:
              print("Quantidade insuficiente em estoque.")
      elif escolha == "2":
        codigo_barras = input("Digite o código de barras do novo produto: ")
        nome = input("Digite o nome do produto: ")
        preco = float(input("Digite o preço do produto: "))
        tipo_produto = input("Digite o tipo de produto (Físico, Digital ou Virtual): ").capitalize()
  
        if tipo_produto == "Físico":
            peso = float(input("Digite o peso do produto físico: "))
            novo_produto = ProdutoFisico(codigo_barras, nome, preco, peso)
        elif tipo_produto == "Digital":
            tamanho_arquivo = float(input("Digite o tamanho do arquivo digital (em MB): "))
            novo_produto = ProdutoDigital(codigo_barras, nome, preco, tamanho_arquivo)
        elif tipo_produto == "Virtual":
            link_download = input("Digite o link de download do produto virtual: ")
            novo_produto = ProdutoVirtual(codigo_barras, nome, preco, link_download)
        else:
            print("Tipo de produto inválido.")
            continue
  
        quantidade = int(input("Digite a quantidade a ser adicionada ao estoque: "))
        inventario.adicionar_produto(novo_produto, quantidade)
        print("Produto adicionado ao estoque.")
      elif escolha == "3":
          print("Saindo do programa. Até logo!")
          break
      elif escolha == "4":
        informacoes_inventario = inventario.obter_informacoes_inventario()
        for info in informacoes_inventario:
            print(info)
      else:
          print("Opção inválida. Por favor, escolha uma opção válida.")
