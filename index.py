from flask import Flask, jsonify, render_template, request, redirect, url_for
import conexao
import traceback

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

@app.route('/feedback') 
def feedback():

    return (
       render_template(
        'index.html',
        contato1 = "Marlon Duarte",
        contato1_email = "eletromarlon@gmail.com",
        contato2 = 'Gustavo Moraes',
        contato2_email = 'emaildegustavo',
        contato3 = "",
        contato3_email = "",
        contato4 = "",
        contato4_email = "",
        aviso = "Clique em 'Limpar Tela' para apagar essa mensagem."
        )
    )

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
            "host": request.form.get('host1'),
            "port": request.form.get('port1'),
            "bdType": request.form.get('bd1')
        } 
        if (not bdData2):
            bdData2 = {
                "user": "",
                "password": "",
                "id": "",
                "host": "",
                "port": "",
                "bdType": ""
            }

    if (True):
        try:
            if bdData1["bdType"] == 'Oracle':
                bdOut1 = conexao.oracleConnection(bdData1["user"], bdData1["password"], bdData1["id"], "SELECT 1") 
            if bdData1["bdType"] == 'MySQL':
                bdOut1 = conexao.mysqlConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], "SELECT 1")
            if bdData1["bdType"] == 'PostgreSQL':
                bdOut1 = conexao.postgresConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], "SELECT 1")
            if bdData1["bdType"] == 'SQLite':
                bdOut1 = conexao.sqLiteConnection("SELECT 1")
            # print("valor em bddata1", bdOut1)
        except:
            return render_template(
                'index.html',
                user1 = "CONNECTION ERROR",
                password1 = "CONNECTION ERROR",
                id1 = "CONNECTION ERROR",
                host1 = "CONNECTION ERROR",
                port1 = "CONNECTION ERROR",
                bd1 = "CONNECTION ERROR"   
            )

        return render_template(
            'index.html',
            user1 = bdData1["user"],
            password1 = bdData1["password"],
            id1 = bdData1["id"],
            host1 = bdData1["host"],
            port1 = bdData1["port"],
            bd1 = bdData1["bdType"],
            user2 = bdData2["user"],
            password2 = bdData2["password"],
            id2 = bdData2["id"],
            host2 = bdData2["host"],
            port2 = bdData2["port"],
            bd2 = bdData2["bdType"] 
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
            "host": request.form.get('host2'),
            "port": request.form.get('port2'),
            "bdType": request.form.get('bd2')
        }
        if (not bdData1):
            bdData1 = {
                "user": "",
                "password": "",
                "id": "",
                "host": "",
                "port": "",
                "bdType": ""
            }


    if (True):
        try:
            if bdData2["bdType"] == 'Oracle':
                bdOut2 = conexao.oracleConnection(bdData2["user"], bdData2["password"], bdData2["id"], "SELECT 1") 
            if bdData2["bdType"] == 'MySQL':
                bdOut2 = conexao.mysqlConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], "SELECT 1")
            if bdData2["bdType"] == 'PostgreSQL':
                bdOut2 = conexao.postgresConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], "SELECT 1")
            if bdData2["bdType"] == 'SQLite':
                bdOut2 = conexao.sqLiteConnection("SELECT 1")
            
            
        except:
            return render_template(
                'index.html',
                user2 = "CONNECTION ERROR",
                password2 = "CONNECTION ERROR",
                id2 = "CONNECTION ERROR",
                port2 = "CONNECTION ERROR",
                bd2 = "CONNECTION ERROR"
            )

        return render_template(
            'index.html',
            user1 = bdData1["user"],
            password1 = bdData1["password"],
            id1 = bdData1["id"],
            host1 = bdData1["host"],
            port1 = bdData1["port"],
            bd1 = bdData1["bdType"],
            user2 = bdData2["user"],
            password2 = bdData2["password"],
            id2 = bdData2["id"],
            host2 = bdData2["host"],
            port2 = bdData2["port"],
            bd2 = bdData2["bdType"]
        )

@app.route('/consultasql', methods=['GET', 'POST'])
def consultasql():
    global bdOut1
    global bdOut2
    global bdData1
    global bdData2

    consulta1 = request.form.get('sql1')
    consulta2 = request.form.get('sql2')

    # print("bdData1", bdData1)
    # print("bdData2", bdData2)
    # print("sql1", consulta1)
    # print("sql2", consulta2)

    if request.method == 'POST':
        if (bdData1 != None and consulta1 != None):
            try:
                if bdData1["bdType"] == 'Oracle':
                    bdOut1 = conexao.oracleConnection(bdData1["user"], bdData1["password"], bdData1["id"], consulta1) 
                if bdData1["bdType"] == 'MySQL':
                    bdOut1 = conexao.mysqlConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta1)
                if bdData1["bdType"] == 'PostgreSQL':
                    bdOut1 = conexao.postgresConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta1)
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
                    bd2 = bdData2["bdType"]  
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
                    bd2 = bdData2["bdType"]
               )
        else:
            if (bdData2 != None and consulta2 != None):
                try:
                    if bdData2["bdType"] == 'Oracle':
                        bdOut2 = conexao.oracleConnection(bdData2["user"], bdData2["password"], bdData2["id"], consulta2) 
                    if bdData2["bdType"] == 'MySQL':
                        bdOut2 = conexao.mysqlConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta2)
                    if bdData2["bdType"] == 'PostgreSQL':
                        bdOut2 = conexao.postgresConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta2)
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
                        bd2 = bdData2["bdType"]  
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
                bd2 = bdData2["bdType"]
            )
    else:
        return render_template('index.html')

@app.route('/api/colunas/<valor>', methods=['GET', 'POST']) # nome da rota
def getGenerator(valor):
    global bdOut1
    global bdOut2

    content = request.json
    consulta = "(" + content['SQL'] + ") LIMIT 0"

    if request.method == 'POST':
        if valor == '1':
            try:
                if bdData1["bdType"] == 'Oracle':
                    resposta = conexao.oracleConnection(bdData1["user"], bdData1["password"], bdData1["id"], consulta) 
                if bdData1["bdType"] == 'MySQL':
                    resposta = conexao.mysqlConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta)
                if bdData1["bdType"] == 'PostgreSQL':
                    resposta = conexao.postgresConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta)
                if bdData1["bdType"] == 'SQLite':
                    resposta = conexao.sqLiteConnection(consulta)
                #print("valor em respota", resposta)
                return jsonify(resposta[1])
            except Exception as e:
                #print(consulta)
                print(f"something went wrong! - {e}")
                errosql = f"Erro! - {e} - (api/colunas/)"
                return { "erro": errosql}
        else:
            if valor == '2':
                try:
                    if bdData2["bdType"] == 'Oracle':
                        resposta = conexao.oracleConnection(bdData2["user"], bdData2["password"], bdData2["id"], consulta) 
                    if bdData2["bdType"] == 'MySQL':
                        resposta = conexao.mysqlConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta)
                    if bdData2["bdType"] == 'PostgreSQL':
                        resposta = conexao.postgresConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta)
                    if bdData2["bdType"] == 'SQLite':
                        resposta = conexao.sqLiteConnection(consulta)
                    #print("valor em respota", resposta)
                    return jsonify(resposta[1])
                except Exception as e:
                    errosql = f"Erro! - {e} - (api/colunas/)"
                    return { "erro": errosql}
            else:
                return "Error! Parece que nao tem nenhum banco conectado ou a requisição esta errada para os bancos"

    # if request.method == 'GET':
    #     if (valor == '1'):
    #         try:
    #             colunas1 = bdOut1[1]
    #             return {
    #                 "colunas": colunas1
    #             }
    #         except:
    #             print("Valores em bdOut1", bdOut1)
    #             return {
    #                 "colunas": ""
    #             }
    #     else:
    #         if (valor == '2'):
    #             try:
    #                 colunas2 = bdOut2[1]
    #                 return {
    #                     "colunas": colunas2
    #                 }
    #             except:
    #                 print("Valores em bdOut2", bdOut2)
    #                 return {
    #                     "colunas": ""
    #                 }
    
    # return "Erro na requisição - Verifique o metodo ou valores"

@app.route('/api/generate/<valor>', methods=['GET', 'POST'])
def postGenerator(valor):
    global bdData1
    global bdData2
    #global bdOut1
    #global bdOut2

    content = request.json

    sql = content['SQL']
    value = content['value']
    consulta = 'select max(' + value + ') as max, min(' + value + ') as min, count(' + value + ') as count, avg(' + value + ') as avg from  (' + sql + ') as result'

    if request.method == 'POST':
        if valor == '1':
            try:
                if bdData1["bdType"] == 'Oracle':
                    resposta = conexao.oracleConnection(bdData1["user"], bdData1["password"], bdData1["id"], consulta) 
                if bdData1["bdType"] == 'MySQL':
                    for i in value:
                        if i == '"':
                            value = value.replace(i, '')
                    print("valor em value", value)
                    consulta = 'select max(' + value + ') as max, min(' + value + ') as min, count(' + value + ') as count, avg(' + value + ') as avg from  (' + sql + ') as result'
                    print("consulta feita no mysql\n", consulta)
                    resposta = conexao.mysqlConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta)
                if bdData1["bdType"] == 'PostgreSQL':
                    resposta = conexao.postgresConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta)
                if bdData1["bdType"] == 'SQLite':
                    resposta = conexao.sqLiteConnection(consulta)
                #print("valor em respota", resposta)
                return jsonify(resposta[0])
            except Exception as e:
                if bdData1['user'] == '':
                    errosql = f"(banco desconectado)"
                else:
                    errosql = f"Erro! - {e}"
                return { "erro": errosql}
        else:
            if valor == '2':
                try:
                    if bdData2["bdType"] == 'Oracle':
                        resposta = conexao.oracleConnection(bdData2["user"], bdData2["password"], bdData2["id"], consulta) 
                    if bdData2["bdType"] == 'MySQL':
                        for i in value:
                            if i == '"':
                                value = value.replace(i, '')
                        consulta = 'select max(' + value + ') as max, min(' + value + ') as min, count(' + value + ') as count, avg(' + value + ') as avg from  (' + sql + ') as result'
                        print("consulta feita no mysql\n", consulta)
                        resposta = conexao.mysqlConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta)
                    if bdData2["bdType"] == 'PostgreSQL':
                        resposta = conexao.postgresConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta)
                    if bdData2["bdType"] == 'SQLite':
                        resposta = conexao.sqLiteConnection(consulta)
                    #print("valor em respota", resposta)
                    return jsonify(resposta[0])
                except Exception as e:
                    if bdData2['user'] == '':
                        errosql = f"(banco desconectado)"
                    else:
                        errosql = f"Erro! - {e}"
                    return { "erro": errosql}
            else:
                return "Error! Parece que nao tem nenhum banco conectado ou a requisição esta errada para os bancos"



def exec_query(valor, consulta):
    #resposta = None
    if valor == '1':
        if bdData1["bdType"] == 'Oracle':
            resposta = conexao.oracleConnection(bdData1["user"], bdData1["password"], bdData1["id"], consulta) 
        if bdData1["bdType"] == 'MySQL':
            resposta = conexao.mysqlConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta)
        if bdData1["bdType"] == 'PostgreSQL':
            resposta = conexao.postgresConnection(bdData1["host"], bdData1["port"], bdData1["id"], bdData1["user"], bdData1["password"], consulta)
        if bdData1["bdType"] == 'SQLite':
            resposta = conexao.sqLiteConnection(consulta)
        return (resposta[0])

    if valor == '2':
        if bdData2["bdType"] == 'Oracle':
            resposta = conexao.oracleConnection(bdData2["user"], bdData2["password"], bdData2["id"], consulta) 
        if bdData2["bdType"] == 'MySQL':
            resposta = conexao.mysqlConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta)
        if bdData2["bdType"] == 'PostgreSQL':
            resposta = conexao.postgresConnection(bdData2["host"], bdData2["port"], bdData2["id"], bdData2["user"], bdData2["password"], consulta)
        if bdData2["bdType"] == 'SQLite':
            resposta = conexao.sqLiteConnection(consulta)  

        return (resposta[0])

    #return None
              


@app.route('/api/analysis/', methods=['GET', 'POST']) # nome da rota
def analysis():
    try:
        content = request.json
        SQL1 = content["SQL_1"]
        SQL2 = content["SQL_2"]
        columns1 = content["columns_1"]
        columns2 = content["columns_2"]
        candidate1 = content["candidate_1"]
        candidate2 = content["candidate_2"]

        #print("SQL1: " + SQL1)
        #print("SQL2: " + SQL2)
        #print("candidate1 : " + candidate1)
        #print("candidate2 : " + candidate2)
        #print("columns1: " + ''.join(columns1))
        #print("columns2: " + ''.join(columns2))
        
        double_quotes_1 = "\""
        double_quotes_2 = "\""
        
        if bdData1["bdType"] == 'MySQL':
            double_quotes_1 = ""
        
        if bdData2["bdType"] == 'MySQL':
            double_quotes_2 = ""

        super_SQL1 = "select " + double_quotes_1 + candidate1 + double_quotes_1
        super_SQL2 = "select " + double_quotes_2 + candidate2 + double_quotes_2
        
        size_columns = 1

        for x in columns1:
            size_columns = size_columns + 1
            super_SQL1 =  super_SQL1 + ", " + double_quotes_1 + x + double_quotes_1
        for x in columns2:
            super_SQL2 =  super_SQL2 + ", " + double_quotes_2 + x + double_quotes_2 

        super_SQL1 = super_SQL1 + " from (" + SQL1 + ") as result" 
        super_SQL2 = super_SQL2 + " from (" + SQL2 + ") as result"

        print("SSQL1: " + super_SQL1)    
        print("SSQL2: " + super_SQL2) 

        resp1 = exec_query("1",super_SQL1)
        resp2 = exec_query("2",super_SQL2)
        
        result1 = []
        result2 = []

        for x1 in resp1: #COPY VALUES
            tuple_ = []
            for i in range(size_columns):
                tuple_.append(str(x1[i]))
            result1.append(tuple_)

        for x2 in resp2: #COPY VALUES
            tuple_ = []
            for i in range(size_columns):
                tuple_.append(str(x2[i]))
            result2.append(tuple_)

        remove1 = []
        remove2 = []
        final_result = []

        # INNER JOIN !!!! Nested-Loop Join Algorithm (LOW PERFORMANCE)
        for index1, tuple1 in enumerate(result1):
            for index2, tuple2 in enumerate(result2):
                if tuple1[0] == tuple2[0]:
                    isValid = True
                    for i in range(size_columns-1): 
                        if tuple1[i+1] != tuple2[i+1]:
                            isValid = False
                    if isValid == False:
                        final_result.append({"t1":tuple1, "t2":tuple2})
                    remove1.append(tuple1)
                    remove2.append(tuple2)
        
        for tuple in remove1:
            result1.remove(tuple)
        for tuple in remove2:
            result2.remove(tuple)

        for tuple in result1:
            final_result.append({"t1":tuple, "t2":None})
        for tuple in result2:
            final_result.append({"t1":None, "t2":tuple})

        return jsonify( { "result": final_result } );
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        errosql = f"Erro! - {e}"
        return { "erro": errosql}

    return { "erro": "analysis-erro"};


app.run(debug=True) #debug=True é utilizado para reiniciar o servidor sempre que alterado
