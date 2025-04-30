from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
with app.app_context():
    db.create_all()

CORS(app)
# pro postman
@app.route('/api/mensagens/', methods=['GET'])
def get_mensagens():
    mensagens = Mensagem.query.all()
    return jsonify([{'id': m.id, 'conteudo': m.conteudo} for m in mensagens])

@app.route('/api/mensagens/<int:id>', methods=['GET'])
def get_mensagem_by_id(id):
    mensagem = Mensagem.query.get_or_404(id)
    return jsonify({'id': mensagem.id, 'conteudo': mensagem.conteudo})

@app.route('/api/mensagens/', methods=['POST'])
def criar_mensagem():
    return f'teste'
    data = request.get_json()
    nova = Mensagem(conteudo=data['conteudo'])
    db.session.add(nova)
    db.session.commit()
    return jsonify({'id': nova.id, 'conteudo': nova.conteudo}), 201

@app.route('/api/mensagens/<int:id>', methods=['PUT'])
def atualizar_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    data = request.get_json()
    mensagem.conteudo = data['conteudo']
    db.session.commit()
    return jsonify({'id': mensagem.id, 'conteudo': mensagem.conteudo})

@app.route('/api/mensagens/<int:id>', methods=['DELETE'])
def deletar_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({'mensagem': 'Deletado com sucesso'})

# html
@app.route('/')
def index():
    mensagens = Mensagem.query.all()
    return render_template('index.html', mensagens=mensagens)

@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        conteudo = request.form['conteudo']
        nova = Mensagem(conteudo=conteudo)
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit(id):
    mensagem = Mensagem.query.get_or_404(id)
    if request.method == 'POST':
        mensagem.conteudo = request.form['conteudo']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', mensagem=mensagem)

@app.route('/delete/<int:id>/')
def delete(id):
    mensagem = Mensagem.query.get_or_404(id)
    db.session.delete(mensagem)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
