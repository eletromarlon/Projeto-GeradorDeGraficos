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
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        id = request.form.get('id')
        port = request.form.get('port')
        bd = request.form.get('bd')
        if bd == 'Oracle':
            bdOut = conexao.oracleConnection(user, password, id)
        
        return render_template(
            'graphGenerator.html',
            user = user,
            password = password,
            id = id,
            port = port,
            bd = bd,
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