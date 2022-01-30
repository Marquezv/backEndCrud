from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/crudflask'

db = SQLAlchemy(app)

class Usuario(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(50))
	email = db.Column(db.String(100))

# Depois de escrever os campos da tabela cmd>python>from app import db>db.create_all()
	
	def to_json(self):
		return {
				"id": self.id, 
				"nome": self.nome, 
				"email": self.email
				}
	# methodo que abre o Objeto recebido e transforma em json	

# Selecionar Tudo
@app.route("/usuarios", methods=["GET"])
# cria uma rota no flask
def seleciona_usuarios():
	usuarios_objetos = Usuario.query.all()
	# Seleciona tds usuarios do db

	usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]
	# Para cada usuario no objeto executar o methodo (to_json)

	# return Response(json.dumps(usuarios_json))
	return gera_response(200, 'usuarios', usuarios_json, 'ok')

# Selecionar Individual
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
	usuario_objeto = Usuario.query.filter_by(id=id).first()
	# Como a busca é por id somente 1 sera selecionado
	usuarios_json = usuario_objeto.to_json()

	return gera_response(200, 'usuario', usuarios_json)

# Cadastras

@app.route("/usuario", methods=["POST"])
def cria_usuario():
	body = request.get_json()

	# Validar se veio os parametros
	# Ou gerar um try catch para gerar erro

	try:
		usuario = Usuario(nome=body["nome"], email=body["email"])
		# Cria um usuario utlizando a Classe usuario passando os parametros
		db.session.add(usuario)
		# Adiciona o usuario ao db
		db.session.commit()
		# Commita a modificação no db

		return gera_response(201, "usuario", usuario.to_json(), "Criado com Sucesso!")
	except Exception as e:
		print(e)
		return gera_response(400, "usuario", {}, "Erro ao Cadastrar!")

# Atualizar
@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
	usuario_objeto = Usuario.query.filter_by(id=id).first()
	# Pegar o usuario
	body = request.get_json()
	# Pegar as modificações

	try:
		if('nome' in body):
			usuario_objeto.nome = body['nome']
			# Modifica o nome se for solicitado
		if('email' in body):
			usuario_objeto.email = body['email']
			# Modifica o email se for solicitado

		db.session.add(usuario_objeto)
		# Atualiza o usuario no db
		db.session.commit()
		# Commita a modificação no db
		return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com Sucesso!")
	except Exception as e:
		print(e)
		return gera_response(400, "usuario", {}, "Erro ao Atualizar!")


# Deletar
@ app.route("/usuario/<id>", methods=["DELETE"])
def deletar_usuario(id):
	usuario_objeto = Usuario.query.filter_by(id=id).first()

	try:
		db.session.delete(usuario_objeto)
		db.session.commit()
		return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com Sucesso!" )
	except Exception as e:
		print('Erro', e)
		return gera_response(400, "usuario", {}, "Erro ao Deletar!")



def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
# Função crida para padronizar o response, toda vez que precisar de um response sera utilizado
	body = {}
	body[nome_do_conteudo] = conteudo

	if(mensagem):
		body["mensagem"] = mensagem

	return Response(json.dumps(body), status=status, mimetype="application/json")
	# Retorna o response em json
app.run(debug=True)