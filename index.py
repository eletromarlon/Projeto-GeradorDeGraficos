from flask import Flask, jsonify, render_template, request
import conexao
app = Flask(__name__)

#@app.route('/')
#def root(): # funcao de retorno da rota
#    return 'Hello World!'

@app.route('/') # nome da rota
def teste():
    return (
       render_template('index.html')
    )

@app.route('/graph', methods=['GET', 'POST']) # nome da rota
def postTest():
    bdOut = []
    bdData = {}
    if request.method == 'POST':
        bdData = {
            "user": request.form.get('user1'),
            "password": request.form.get('password1'),
            "id": request.form.get('id1'),
            "port": request.form.get('port1'),
            "bdType": request.form.get('bd1')
        }
    
    print(bdData["user"])

    try:
        if bdData["bdType"] == 'Oracle':
            bdOut = conexao.oracleConnection(bdData["user"], bdData["password"], bdData["id"])
    except:
        return render_template(
            'index.html',
            user = "CONNECTION ERROR",
            password = "CONNECTION ERROR",
            id = "CONNECTION ERROR",
            port = "CONNECTION ERROR",
            bd = "CONNECTION ERROR",
            consulta = bdOut   
        )
        
    return render_template(
        'index.html',
        user = bdData["user"],
        password = bdData["password"],
        id = bdData["id"],
        port = bdData["port"],
        bd = bdData["bdType"],
        consulta = bdOut   
    )

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