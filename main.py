from flask import Flask
from flask import request
from flask import render_template


from datetime import date

import sqlite3
from sqlite3 import Error


#######################################################
# Instancia da Aplicacao Flask
app = Flask(__name__)

#######################################################
# 1. Pagina Inicial Simples
#######################################################

@app.route('/', methods =['GET'])
def home():
    return('Pagina Inicial')

#######################################################
# 2. Cadastrar produtos
#######################################################
    
@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    if request.method == 'POST':

        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        datacriacao = date.today()

        mensagem = 'Erro - nao cadastrado'

        if descricao and precocompra and precovenda and datacriacao:
            registro = (descricao, precocompra, precovenda, datacriacao)

            try:
                conn = sqlite3.connect('database/db-produtos.db')

                sql = ''' INSERT INTO produtos(descricao, precocompra, precovenda, datacriacao) VALUES(?,?,?,?) '''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - cadastrado'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('cadastrar.html')

#######################################################
# 3. Excluir produtos
#######################################################

@app.route('/produtos/excluir', methods=['GET', 'POST'])
def excluir():
    if request.method== 'POST':
        codigoproduto = request.form['codproduto']
        print(codigoproduto)
        if codigoproduto :
            try:
                conn = sqlite3.connect('database/db-produtos.db')
                cur = conn.cursor()
                sql = '''DELETE FROM produtos WHERE codproduto = ?'''
                id=codigoproduto
                cur.execute(sql, (id,))
                conn.commit()
                mensagem = 'Sucesso - apagado'
            except Error as e:
                print(e)
            finally:
                conn.close()
    return render_template('excluir.html')

#######################################################
# 4. Editar produtos
#######################################################
    
@app.route('/produtos/editar', methods=['GET', 'POST'])
def editar():
    if request.method== 'POST':
        codigoproduto = request.form['codproduto']
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        if descricao and precocompra and precovenda and codigoproduto:
            registro = (descricao, precocompra, precovenda, codigoproduto )
            try:
                conn = sqlite3.connect('database/db-produtos.db')
                sql = ''' UPDATE produtos SET descricao = ?, precocompra = ?, precovenda = ? WHERE codproduto = ?'''
                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - Editado'

                
            except Error as e:
                print(e)
            finally:
                conn.close()
    return render_template('editar.html')







#######################################################
# 5. Listar produtos
#######################################################

@app.route('/produtos/listar', methods=['GET'])
def listar():
    try:
        conn = sqlite3.connect('database/db-produtos.db')
        sql = '''SELECT * FROM produtos'''
        cur = conn.cursor()
        cur.execute(sql)
        registros = cur.fetchall()
        return render_template('listar.html', regs=registros)
    except Error as e:
        print(e)
    finally:
        conn.close()

#######################################################
# Rota de Erro
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

#######################################################

app.run(host='0.0.0.0', port=80)