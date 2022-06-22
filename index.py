from flask import Flask, jsonify, render_template, request
import conexao

app = Flask(__name__)

#variaveis globais para alocação de dados dos bancos do usuário
bdData1 = None
bdData2 = None
bdOut1 = []
bdOut2 = []

# Rota inicial, responsável por exibir a pagina inicial
@app.route('/') 
def home():
    global bdData1
    global bdData2
    global bdOut1
    global bdOut2

    bdData1 = None
    bdData2 = None
    bdOut1 = []
    bdOut2 = []

    return (
       render_template('index.html')
    )

@app.route('/teste') 
def teste():

    teste = "<div><button>Teste</button></div>"

    return (render_template('index.html', teste = teste))

#Rora de primeira conexao com banco, as variaveis globais visam manter as informações para outras consultas desejadas pelo usuário
@app.route('/conexao1', methods=['GET', 'POST']) # nome da rota
def connectionBd1():
    bdOut1 = []
    global bdData1
    global bdData2

    if request.method == 'POST':
        bdData1 = {
            "user": request.form.get('user1'),
            "password": request.form.get('password1'),
            "id": request.form.get('id1'),
            "port": request.form.get('port1'),
            "bdType": request.form.get('bd1')
        } 
        if (not bdData2):
            bdData2 = {
                "user": "",
                "password": "",
                "id": "",
                "port": "",
                "bdType": ""
            }

    if (True):
        try:
            if bdData1["bdType"] == 'Oracle':
                bdOut1 = conexao.oracleConnection(bdData1["user"], bdData1["password"], bdData1["id"], "SELECT 1") 
            if bdData1["bdType"] == 'MySQL':
                bdOut1 = conexao.mysqlConnection(bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], "SELECT 1")
            if bdData1["bdType"] == 'PostgreSQL':
                bdOut1 = conexao.postgresConnection(bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], "SELECT 1")
            if bdData1["bdType"] == 'SQLite':
                bdOut1 = conexao.sqLiteConnection("SELECT 1")
        except:
            return render_template(
                'index.html',
                user1 = "CONNECTION ERROR",
                password1 = "CONNECTION ERROR",
                id1 = "CONNECTION ERROR",
                port1 = "CONNECTION ERROR",
                bd1 = "CONNECTION ERROR",
                consulta1 = bdOut1   
            )

        return render_template(
            'index.html',
            user1 = bdData1["user"],
            password1 = bdData1["password"],
            id1 = bdData1["id"],
            port1 = bdData1["port"],
            bd1 = bdData1["bdType"],
            user2 = bdData2["user"],
            password2 = bdData2["password"],
            id2 = bdData2["id"],
            port2 = bdData2["port"],
            bd2 = bdData2["bdType"],
            consulta1 = bdOut1  
        )

#Rora de segunda conexao, as variaveis globais visam manter as informações para outras consultas desejadas pelo usuário
@app.route('/conexao2', methods=['GET', 'POST']) # nome da rota
def connectionBd2():
    bdOut2 = []
    global bdData1
    global bdData2

    if request.method == 'POST':
        bdData2 = {
            "user": request.form.get('user2'),
            "password": request.form.get('password2'),
            "id": request.form.get('id2'),
            "port": request.form.get('port2'),
            "bdType": request.form.get('bd2')
        }
        if (not bdData1):
            bdData1 = {
                "user": "",
                "password": "",
                "id": "",
                "port": "",
                "bdType": ""
            }


    if (True):
        try:
            if bdData2["bdType"] == 'Oracle':
                bdOut2 = conexao.oracleConnection(bdData2["user"], bdData2["password"], bdData["id"], "SELECT 1") 
            if bdData2["bdType"] == 'MySQL':
                bdOut2 = conexao.mysqlConnection(bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], "SELECT 1")
            if bdData2["bdType"] == 'PostgreSQL':
                bdOut2 = conexao.postgresConnection(bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], "SELECT 1")
            if bdData2["bdType"] == 'SQLite':
                bdOut2 = conexao.sqLiteConnection("SELECT 1")
            
            
        except:
            return render_template(
                'index.html',
                user2 = "CONNECTION ERROR",
                password2 = "CONNECTION ERROR",
                id2 = "CONNECTION ERROR",
                port2 = "CONNECTION ERROR",
                bd2 = "CONNECTION ERROR",
                consulta2 = bdOut2   
            )

        return render_template(
            'index.html',
            user1 = bdData1["user"],
            password1 = bdData1["password"],
            id1 = bdData1["id"],
            port1 = bdData1["port"],
            bd1 = bdData1["bdType"],
            user2 = bdData2["user"],
            password2 = bdData2["password"],
            id2 = bdData2["id"],
            port2 = bdData2["port"],
            bd2 = bdData2["bdType"],
            consulta2 = bdOut2   
        )

@app.route('/consultasql', methods=['GET', 'POST'])
def consultasql():
    global bdOut1
    global bdOut2
    global bdData1
    global bdData2

    consulta1 = request.form.get('sql1')
    consulta2 = request.form.get('sql2')

    print("bdData1", bdData1)
    print("bdData2", bdData2)
    print("sql1", consulta1)
    print("sql2", consulta2)

    if request.method == 'POST':
        if (bdData1 != None and consulta1 != None):
            try:
                if bdData1["bdType"] == 'Oracle':
                    bdOut1 = conexao.oracleConnection(bdData1["user"], bdData1["password"], bdData1["id"], consulta1) 
                if bdData1["bdType"] == 'MySQL':
                    bdOut1 = conexao.mysqlConnection(bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta1)
                if bdData1["bdType"] == 'PostgreSQL':
                    bdOut1 = conexao.postgresConnection(bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta1)
                if bdData1["bdType"] == 'SQLite':
                    bdOut1 = conexao.sqLiteConnection(consulta1)
            except:
                return render_template(
                    'index.html',
                    user1 = bdData1["user"],
                    password1 = bdData1["password"],
                    id1 = bdData1["id"],
                    port1 = bdData1["port"],
                    bd1 = bdData1["bdType"],
                    user2 = bdData2["user"],
                    password2 = bdData2["password"],
                    id2 = bdData2["id"],
                    port2 = bdData2["port"],
                    bd2 = bdData2["bdType"],
                    consulta1 = "ALGUM ERRO OCORREU NA CONSULTA"   
               )
            return render_template(
                    'index.html',
                    user1 = bdData1["user"],
                    password1 = bdData1["password"],
                    id1 = bdData1["id"],
                    port1 = bdData1["port"],
                    bd1 = bdData1["bdType"],
                    user2 = bdData2["user"],
                    password2 = bdData2["password"],
                    id2 = bdData2["id"],
                    port2 = bdData2["port"],
                    bd2 = bdData2["bdType"],
                    consulta1 = bdOut1   
               )
        else:
            if (bdData2 != None and consulta2 != None):
                try:
                    if bdData2["bdType"] == 'Oracle':
                        bdOut2 = conexao.oracleConnection(bdData2["user"], bdData2["password"], bdData["id"], consulta2) 
                    if bdData2["bdType"] == 'MySQL':
                        bdOut2 = conexao.mysqlConnection(bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta2)
                    if bdData2["bdType"] == 'PostgreSQL':
                        bdOut2 = conexao.postgresConnection(bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta2)
                    if bdData2["bdType"] == 'SQLite':
                        bdOut2 = conexao.sqLiteConnection("SELECT 1")
                except:
                    return render_template(
                        'index.html',
                        user1 = bdData1["user"],
                        password1 = bdData1["password"],
                        id1 = bdData1["id"],
                        port1 = bdData1["port"],
                        bd1 = bdData1["bdType"],
                        user2 = bdData2["user"],
                        password2 = bdData2["password"],
                        id2 = bdData2["id"],
                        port2 = bdData2["port"],
                        bd2 = bdData2["bdType"],
                        consulta1 = "ALGUM ERRO OCORREU NA CONSULTA"   
                    )
            else:
                return render_template(
                    'index.html',
                    erro = "Erro de consulta ou banco desconectado. Clique em 'Limpar Tela' depois conecte algum banco para refazer a query"
                )
            return render_template(
                'index.html',
                user1 = bdData1["user"],
                password1 = bdData1["password"],
                id1 = bdData1["id"],
                port1 = bdData1["port"],
                bd1 = bdData1["bdType"],
                user2 = bdData2["user"],
                password2 = bdData2["password"],
                id2 = bdData2["id"],
                port2 = bdData2["port"],
                bd2 = bdData2["bdType"],
                consulta2 = bdOut2
            )
    else:
        return render_template('index.html')

@app.route('/generator', methods=['GET', 'POST']) # nome da rota
def getGenerator():
    bdOut = []
    saida = request.args.get('tool') 
    print(saida)
    print(saida.find('2'))
    if (saida.find('1') != -1):
        return render_template('graphGenerator.html') 
    else:
        if (saida.find('2') != -1):
            return render_template('index.html')
        else:
            return render_template('index.html')






















'''    
@app.route('/pessoas/<string:nome>/<string:cidade>')
def pessoa(nome, cidade):
    return 'Nome: {}, Cidade: {}'.format(nome, cidade) #format joga os valores da função nos campos com "{}" 

@app.route('/pessoa/<string:nome>/<string:cidade>') #Mesma coisa da anterior mas com JSON
def pessoas(nome, cidade):
    return jsonify({'nome': nome, 'cidade':cidade})


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    return 'Recebido: {}\n'.format(data['data']) #trabalhando com post'''

app.run(debug=True) #debug=True é utilizado para reiniciar o servidor sempre que alterado