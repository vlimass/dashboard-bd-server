# API Dashboard BD  

O **Dashboard BD** é um projeto realizado para o trabalho final da disciplina de Banco de Dados do curso de Ciência da Computação da UFRJ, feito em colaboração com Fábio Patão e Rhana Gomes. O objetivo foi desenvolver um dashboard para uma loja de roupas fictícia integrado à uma API que fornece dados armazenados em um banco MySQL. A base de dados pode ser acessada em https://www.kaggle.com/datasets/iamsouravbanerjee/customer-shopping-trends-dataset.

### 🛠 Tecnologias utilizadas

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [MySQL](https://www.mysql.com/)

### ⚙️ Como rodar o projeto?

Primeiramente, é necessário ter o `python` e o `npm` instalados em sua máquina. É possível verificar se essas dependências já estão no sistema por meio dos seguintes comandos: 
```
python --version 
python3 --version // Execute este comando caso tenha instalado o Python3
mysql -V
```

Uma vez instaladas as depêndencias acima, faremos um `git clone` do projeto: (O código a seguir considera uma clonagem no Github por chave SSH)
```
git clone git@github.com:vlimass/dashboard-bd-server.git
```

O próximo passo é entrar na pasta do projeto clonado:
```
cd dashboard-bd-server
```

É necessário criar um banco MySQL em sua máquina que forneça os dados do back-end. Para isso, vamos inicialmente executar o seguinte comando para entrar no console `mysql`: 
```
// Substitua as variáveis USERNAME, PASSWORD e HOSTNAMEORIP conforme as configurações do seu MySQL
mysql -u USERNAME -pPASSWORD -h HOSTNAMEORIP // Exemplo: mysql -u usuario123 -psenha123 -h localhost
```

Dentro do console `mysql`, crie o banco de dados para armazenar os dados da aplicação, acesse-o e preencha-o com os dados do arquivo presente neste repositório chamado `CreateDatabase.sql`, que está na pasta `db`. Para isso, é necessário executar os seguintes comandos: 
```
create database dashboard_bd;
use dashboard_bd;
source caminho/do/seu/computador/dashboard-bd-server/db/CreateDatabase.sql
``` 

Após isso, aguarde as queries do banco de dados serem executadas e, ao final, saia do console do `mysql` com o comando:
```
exit
```

Neste momento, com o terminal já na pasta `dashboard-bd-server` clonada anteriormente, execute o seguinte comando para copiar o arquivo das variáveis de ambiente que realizarão a conexão com o banco de dados: 
```
cp .env.example .env 
```

No novo arquivo `.env` criado, preencha as variáveis de ambiente com as configurações do seu MySQL. É importante que a variável `MYSQL_DATABASE` seja preenchida com o nome do banco de dados criado para o projeto anteriormente. Observe o exemplo: 
```
# Variáveis ambientes para conexão com o MySQL

MYSQL_HOST=localhost
MYSQL_USER=usuario123
MYSQL_PASSWORD=senha123
MYSQL_DATABASE=dashboard_bd
```

Por fim, basta rodar o comando para rodar a aplicação: 
```
python main.py
python3 main.py // Execute este comando caso tenha instalado o Python3
```

Tudo pronto! Sua aplicação back-end está rodando e você pode observar os dados na interface do dashboard através de seu navegador em http://localhost:5173/. 

<u>OBS</u>: Para ver os dados na interface do dashboard é necessário rodar a aplicação front-end simultaneamente! Saiba como rodar o front-end do projeto em https://github.com/vlimass/dashboard-bd-web.

<hr>
<div align="center">made with 🤍 by viny</div>