import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask, jsonify

load_dotenv()

# Conexão com o banco de dados MySQL
mydb = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'),
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DATABASE'),
)

# Criação da API de consultas
app = Flask(__name__)

app.json.sort_keys = False
myCursor = mydb.cursor()

# CONSULTA #1: Venda total 
@app.route('/overview/totalSale', methods=['GET'])
def getTotalSale():

  myCursor.execute("""
    SELECT SUM(Produto.valor) as Total_Gasto
    FROM Produto;
  """)
  result = myCursor.fetchall()

  totalSale = result[0][0]

  response = jsonify({
    'totalSale': totalSale
  })

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #2: Assinaturas
@app.route('/overview/subscriptions', methods=['GET'])
def getSubscriptions():

  myCursor.execute("""
    SELECT COUNT(Cliente_Assinatura.Status_compra)
    FROM Cliente_Assinatura
    WHERE Cliente_Assinatura.Status_compra = 'No';
  """)
  result = myCursor.fetchall()

  subscriptions = result[0][0]

  response = jsonify({
    'subscriptions': subscriptions
  })

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #3: Número de clientes
@app.route('/overview/customersNumber', methods=['GET'])
def getCustomersNumber():

  myCursor.execute("""
    SELECT COUNT(id) as Numero_Clientes 
    FROM Cliente_Assinatura;
  """)
  result = myCursor.fetchall()

  customersNumber = result[0][0]

  response = jsonify({
    'customersNumber': customersNumber
  })

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #4: Produtos vendidos
@app.route('/overview/productsSold', methods=['GET'])
def getProductsSold():

  myCursor.execute("""
    SELECT COUNT(ID_Compra) as Total_Produtos_Vendidos 
    FROM Compra;
  """)
  result = myCursor.fetchall()

  productsSold = result[0][0]
  
  response = jsonify({
    'productsSold': productsSold
  })

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #5: Vendas por temporada
@app.route('/overview/sales/season', methods=['GET'])
def getSalesPerSeason():

  myCursor.execute("""
    SELECT Estacao, SUM(Valor) as Vendas_Temporada 
    FROM Produto 
    GROUP BY Estacao;
  """)
  result = myCursor.fetchall()

  salesPerSeason = list()
  for amountSeason in result:
    salesPerSeason.append(
      {
        'name': amountSeason[0],
        'total': amountSeason[1]
      }
    )
  
  response = jsonify(salesPerSeason)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #6: Vendas por localização
@app.route('/overview/sales/location', methods=['GET'])
def getSalesPerLocation():

  myCursor.execute("""
    SELECT Localizacao, SUM(Valor) as Venda_Cidade
    FROM Cliente_Assinatura INNER JOIN Compra ON Cliente_Assinatura.id = Compra.FK_Cliente_Assinatura_id INNER JOIN Tem ON Compra.ID_Compra = Tem.FK_Compra_id INNER JOIN Produto ON Tem.FK_Produto_id = Produto.ID_Produto
    GROUP BY Localizacao
    ORDER BY Venda_Cidade DESC;
  """)
  result = myCursor.fetchall()

  salesPerLocation = list()
  for amountLocation in result:
    salesPerLocation.append(
      {
        'location': amountLocation[0],
        'amount': amountLocation[1]
      }
    )

  response = jsonify(salesPerLocation)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #7: Comparação entre os sexos
@app.route('/customers/genders/count', methods=['GET'])
def getNumberOfEachGenre():

  myCursor.execute("""
    SELECT Genero, COUNT(Genero) as Contagem_Genero 
    FROM Cliente_Assinatura 
    GROUP BY Genero;
  """)
  result = myCursor.fetchall()

  countPerGender = list()
  for genderCount in result:
    countPerGender.append(
      {
        'gender': genderCount[0],
        'count': genderCount[1]
      }
    )

  response = jsonify(countPerGender)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #8: Vendas por faixa etária 
@app.route('/customers/sales/age', methods=['GET'])
def getSalesPerAge():

  myCursor.execute("""
    SELECT Cliente_Assinatura.Idade, COUNT(Tem.FK_Produto_id) AS numero_de_itens, SUM(Produto.valor) AS total_gasto
    FROM Cliente_Assinatura 
    INNER JOIN Compra ON Cliente_Assinatura.id = Compra.FK_Cliente_Assinatura_id INNER JOIN Tem ON Compra.ID_Compra = Tem.FK_Compra_id INNER JOIN Produto ON Tem.FK_Produto_id = Produto.ID_Produto
    GROUP BY Cliente_Assinatura.Idade
    ORDER BY total_gasto DESC;
  """)
  result = myCursor.fetchall()

  salesPerAge = list()
  for ageAmount in result:
    salesPerAge.append(
      {
        'name': ageAmount[0],
        'total': ageAmount[2]
      }
    )

  response = jsonify(salesPerAge)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200

# CONSULTA #9: Frequência de compras
@app.route('/customers/sales/frequency', methods=['GET'])
def getSalesFrequency():

  myCursor.execute("""
    SELECT Frequencia_de_Compras, COUNT(Frequencia_de_Compras) AS Contagem_Frequencia_de_Compras
    FROM Cliente_Assinatura
    GROUP BY Frequencia_de_Compras;
  """)
  result = myCursor.fetchall()

  salesFrequency = list()
  for frequencyCount in result:
    salesFrequency.append(
      {
        'name': frequencyCount[0],
        'value': frequencyCount[1]
      }
    )

  response = jsonify(salesFrequency)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #10: Top clientes
@app.route('/customers/sales/customer', methods=['GET'])
def getSalerPerCustomer():

  myCursor.execute("""
    SELECT id, SUM(Produto.valor) as Total_Gasto, COUNT(Tem.FK_Produto_id) as numero_de_produtos
    FROM Cliente_Assinatura inner JOIN Compra on Cliente_Assinatura.id = Compra.FK_Cliente_Assinatura_id
    INNER JOIN Tem on Compra.ID_Compra = Tem.FK_Compra_id
    INNER JOIN Produto on Produto.ID_Produto = Tem.FK_Produto_id
    GROUP BY Cliente_Assinatura.id
    ORDER BY Total_Gasto DESC;
  """)
  result = myCursor.fetchall()

  salesPerCustomer = list()
  for customerAmount in result:
    salesPerCustomer.append(
      {
        'idCustomer': customerAmount[0],
        'amount': customerAmount[1]
      }
    )
  
  response = jsonify(salesPerCustomer)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #11: Produto mais vendido
@app.route('/products/mostSaledProduct', methods=['GET'])
def getMostSaledProduct():

  myCursor.execute("""
    SELECT Nome, COUNT(Nome) as Comprado_x_vezes
    FROM Produto
    GROUP BY Nome;
  """)
  result = myCursor.fetchall()

  amount = 0 
  for productAmount in result: 
    if(productAmount[1] > amount):
      amount = productAmount[1]
      product = productAmount[0]

  response = jsonify({
    'product': product,
    'amount': amount
  })

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #12: Avaliação média
@app.route('/products/averageRating', methods=['GET'])
def getAverageRating():

  myCursor.execute("""
    SELECT AVG(Avaliacao) as Avaliacao_Media
    FROM Produto;
  """)
  result = myCursor.fetchall()

  avgRating = result[0][0]

  response = jsonify({
    'avgRating': avgRating
  })

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #13: Categorias dos produtos
@app.route('/products/categories', methods=['GET'])
def getProductsCategories():

  myCursor.execute("""
    SELECT Categoria, COUNT(Categoria) as Quantidade
    FROM Produto
    GROUP BY Categoria
    ORDER BY Quantidade DESC;
  """)
  result = myCursor.fetchall()

  productsCategories = list()
  for categoryAmount in result: 
    productsCategories.append(
      {
        'name': categoryAmount[0],
        'value': categoryAmount[1]
      }
    )

  response = jsonify(productsCategories)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #14: Cores mais vendidas por sexo
@app.route('/products/colors/gender', methods=['GET'])
def getColorsMostSaledPerGender():

  myCursor.execute("""
    SELECT Cliente_Assinatura.Genero as Genero,
    Produto.Cor, COUNT(*) AS Quantidade_Vendida
    FROM Cliente_Assinatura
    JOIN Compra ON Cliente_Assinatura.id = Compra.FK_Cliente_Assinatura_id
    JOIN Tem ON Compra.ID_Compra = Tem.FK_Compra_id
    JOIN Produto ON Tem.FK_Produto_id = Produto.ID_Produto
    GROUP BY Cliente_Assinatura.Genero, Produto.Cor
    ORDER BY Cliente_Assinatura.Genero, Quantidade_Vendida DESC;
  """)
  result = myCursor.fetchall()

  colorsPerGender = list()
  for genderColorAmount in result: 
    colorsPerGender.append(
      {
        'gender': genderColorAmount[0],
        'color': genderColorAmount[1],
        'amount': genderColorAmount[2]
      }
    )

  response = jsonify(colorsPerGender)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #15: Tamanhos vendidos
@app.route('/products/saledSizes', methods=['GET'])
def getSaledSizes():

  myCursor.execute("""
    SELECT Tamanho, COUNT(Tamanho) as Quantidade
    FROM Produto
    GROUP BY Tamanho
    ORDER BY Quantidade;
  """)
  result = myCursor.fetchall()

  saledSizes = list()
  for sizeAmount in result: 
    saledSizes.append(
      {
        'size': sizeAmount[0],
        'amount': sizeAmount[1]
      }
    )
  
  response = jsonify(saledSizes)

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


# CONSULTA #16: Compras com desconto
@app.route('/products/salesWithDiscount', methods=['GET'])
def getSalesWithDiscount():

  myCursor.execute("""
    SELECT Desconto_Aplicado, COUNT(Desconto_Aplicado) as Quantidade
    FROM Compra
    GROUP BY Desconto_Aplicado
    ORDER BY Quantidade DESC;
  """)
  result = myCursor.fetchall()

  for discountAmount in result: 
    if(discountAmount[0] == 'True'):
      salesWithDiscount = discountAmount[1]

  response = jsonify({
    'salesWithDiscount': salesWithDiscount
  })

  response.headers.add('Access-Control-Allow-Origin', '*')

  return response, 200


app.run(debug=True)