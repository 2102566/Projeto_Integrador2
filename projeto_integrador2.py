# Código da aplicação referente a disciplina de projeto integrador 2 do curso de Ciência de dados da Univesp
import time

from flask import Flask, request, Response, g, redirect, url_for, flash, render_template_string
import pyodbc
import pandas as pd
import plotly.graph_objs as go
import requests
import matplotlib.pyplot as plt
import numpy
import sys
import plotly.offline as pyo


app = Flask(__name__)

# Variaveis globais para controle

log = False
usuar = ''
permissao = ''
vid = ''
vnome = ''
vsobrenome = ''
vdocumento = ''
vid_cliente = ''
vcelular = ''
vemail= ''
vdata_nasc = ''
vtelefone = ''
vcep = ''
vbairro = ''
vrua = ''
vcomplemento = ''
tabela = ''
cadastro = ''
# Página de LOGIN
@app.route("/")
def homepage():
    global log
    global usuar
    global permissao
    log = False

    usuario = usuar

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')
    count = ''' select count(*) as row from [dbo].[acessos]  '''
    ssql = ''' select * from [dbo].[acessos] '''
    dff = pd.read_sql(ssql, cnxn)
    rows = pd.read_sql(count, cnxn)
    linhas = rows['row'][0]
    usuario = request.args.get('user_login')
    usuar = usuario
    password = request.args.get('senha_login')

    for i in range(linhas):
        if dff['nome'][i] == usuario and dff['senha'][i] == password:
            log = True
            permissao = dff['tipo_acesso'][i]
            break
        elif dff['nome'][i] != usuario or dff['senha'][i] != password:
            log = False

    form = '''<b>Primeira página</b> <br><br> LOGIN <br><br><br><br> <form method="PUT" >
             <body><div><style>
             <p><img src=({{url_for('static',filename='imagem_teste.jpg' }})></p>
             </style></div></body>
            <input type="text" name="user_login" placeholder="Digite nome" >
            <input type="password" name="senha_login" placeholder="Digite senha">
            <input type="submit" name="enviar" value="Login">
        </form> 
            <br><br><i> Seu acesso está recusado <i> '''

    form_2 = '''<b>Página de acesso</b> <br><br> <br><br><br><br> <form method="GET" >
            <body>
            <style>
            body{


            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: violet



             }
             </style></body><center>

            <input type="text" name="user_login" placeholder="Digite nome" >
            <br><br><input type="password" name="senha_login" placeholder="Digite senha" >
            <br><br><input type="submit" name="enviar" value="Login">
        </form></center>


        '''


    if (log == True and usuar != None and permissao == 'F'):
        return redirect(url_for("menu"))

    elif (log == True and usuar != None and permissao == 'C'):
        return redirect(url_for("consulta"))

    elif (log == False and usuar != None):
        return form

    else:
        return form_2

# Página do MENU de acordo com o tipo de acesso do usuário

@app.route("/menu")
def menu():
    global usuar
    global permissao
    global log
    log = True

    html = ''' <html><b>Menu</b><br><br>
                <left>

                <body>
                <br><br><br>
                <b>Escolha sua ação:</b>
                <style>
                body{

                    background-color: Violet

                    }
                </style>

                </body>
                <br><br><br>
                <a href = "http://127.0.0.1:5000/cadastro"> Cadastrar cliente </a>

                <br><br> <a href = "http://127.0.0.1:5000/consulta"> Consultar dados do cliente </a>

                <br><br> <a href = "http://127.0.0.1:5000/alterar" > Alterar dados do cliente </a>
                
                <br><br> <a href = "http://127.0.0.1:5000/vendas" > Nova venda </a>
                
                <br><br> <a href = "http://127.0.0.1:5000/estoque" > Estoque </a>
                
                <br><br> <a href = "http://127.0.0.1:5000/graficos" > Gráficos </a>
                

                </html>

    '''
    if permissao == 'C':
        return redirect(url_for("consulta"))
    elif (usuar == None or usuar == "") or log == False:
        return redirect("/")

    else:
        return html


# Pagina de cadastro de dados dos clientes
@app.route("/cadastro")
def cadastro():
    global log
    global usuar
    global permissao
    global msg

    nome = request.args.get('nome')
    sobrenome = request.args.get('sobrenome')
    documento = request.args.get('doc')
    celular = request.args.get('cel')
    dt_nascimento = request.args.get('nascimento')
    telefone = request.args.get('fone')
    email = request.args.get('email')
    cep = request.args.get('cep')
    rua = request.args.get('rua')
    bairro = request.args.get('bairro')
    numero = request.args.get('numero')
    complemento = request.args.get('complemento')


    html = f'''<b>Cadastro dos dados</b> <br><br>  <br><br><br><br> 
    <form method="PUT" >
    <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

    <input type="text" name="nome" placeholder="Digite Nome" >
    <input type="text" name="sobrenome" placeholder="Digite Sobrenome">
    <input type="text" size='28' name="doc" placeholder="Digite documento(apenas numeros)">
    <input type="text" name="nascimento" placeholder="Digite data de nascimento">
    <input type="text" name="cel" placeholder="Digite Celular">
    <input type="text" name="fone" placeholder="Digite Telefone(opcional)">
    <input type="text" name="email" placeholder="Digite e-mail"><br><br>
    <input type="text" name="cep" placeholder="Digite cep(opcional)">
    <input type="text" name="rua" placeholder="Digite Nome da rua">
    <input type="text" name="bairro" placeholder="Digite Nome do bairro">
    <input type="text" name="numero" placeholder="Digite Numero">
    <input type="text" size='25' name="complemento" placeholder="Digite Complemento(opcional)">
    
    <br><br><br><input type="submit" name="enviar" value="Cadastrar">
    <br><br><br><br>
</form> 


'''

    html2 = f'''<b>ERRO no cadastro dos dados</b> <br><br>  <br><br><br><br> 
    <form method="PUT" >
    <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

    <input type="text" name="nome" placeholder="Digite Nome" >
    <input type="text" name="sobrenome" placeholder="Digite Sobrenome">
    <input type="text" size='30' name="doc" placeholder="Digite documento(apenas numeros)">
    <input type="text" name="nascimento" placeholder="Digite data de nascimento">
    <input type="text" name="cel" placeholder="Digite Celular">
    <input type="text" name="fone" placeholder="Digite Telefone(opcional)">
    <input type="text" name="email" placeholder="Digite e-mail"><br><br>
    <input type="text" name="cep" placeholder="Digite cep(opcional)">
    <input type="text" name="rua" placeholder="Digite Nome da rua">
    <input type="text" name="bairro" placeholder="Digite Nome do bairro">
    <input type="text" name="numero" placeholder="Digite Numero">
    <input type="text" size='25' name="complemento" placeholder="Digite Complemento(opcional)">
    
    <br><br><br><input type="submit" name="enviar" value="Cadastrar">
    
    <br><br>
    
    
</form> 

    '''
    if (usuar == None or usuar == "") or log == 'pastel': #or permissao != "F":
        return redirect('/')
    elif nome == None:
        return html
    elif documento == None:
        return html
    elif len(nome) <= 1:
        return html
    elif (nome != None and nome != ""):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')
        try:

            try:
                rdocumento = documento.replace('-', '').replace('.', '')
                valida_entrada = f''' SELECT id_cliente FROM [Projeto_Integrador2].[dbo].[clietes] WHERE documento = {rdocumento} '''
                df = pd.read_sql(valida_entrada, cnxn)
                id_cli = df['id_cliente'][0]
            except:
                id_cli = None

            if id_cli >0:
                return html2 + f'Cliente já cadastrado, registro {id_cli}'








        except:
            if documento.__contains__('.')==True:
                return html2 + f'Verifique o documento do cliente: {documento}, preencha o campo apenas com números'
            elif (rua == None or rua == '') or (bairro == None or bairro == '') or (sobrenome == None or sobrenome == '') \
                        or (celular == None or celular == '') or (numero == '') or (email == None or email == ''):
                return html2 + f'Houve um erro no cadastramento, preencha todos os dados obrigatórios'




            try:
                cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')

                # Inserindo dados na tabela de cliente
                query_cliente = f''' insert into  [Projeto_Integrador2].[dbo].[clietes] (nome,sobrenome,data_nascimento,documento) 
                              values('{nome}','{sobrenome}','{dt_nascimento}',{documento}) '''
                cnxn.execute(query_cliente)
                cnxn.commit()
                time.sleep(5)


                ################################################################################################################
                # Pegando o id_cliente da Tabela
                query_id = f''' SELECT id_cliente FROM [Projeto_Integrador2].[dbo].[clietes] WHERE documento = {documento} '''
                df = pd.read_sql(query_id, cnxn)
                id_cli = df['id_cliente'][0]
                ################################################################################################################

                # Inserindo dados na tabela de contatos
                query_contato = f''' insert into [Projeto_Integrador2].[dbo].[contato] (celular,telefone,email,id_cliente) 
                                      values('{celular}','{telefone}','{email}',{id_cli})  '''
                cnxn.execute(query_contato)
                cnxn.commit()

                # Inserindo dados na tabela de endereco
                query_endereco = f''' insert into [Projeto_Integrador2].[dbo].[endereco] (cep,rua,bairro,numero,complemento,id_cliente) 
                                              values('{cep}','{rua}','{bairro}','{numero}','{complemento}',{id_cli})  '''
                cnxn.execute(query_endereco)
                cnxn.commit()



                return html + f" Dados de {nome} {sobrenome} foram cadastrados com sucesso"

            except:
                return html2 + f'Houve um erro no cadastramento, verifique os dados e tente novamente'




# Gerando o front para consultar os dados dos clientes

@app.route("/consulta")
def consulta():
    global vsobrenome
    global vnome
    global vdocumento
    global vid_cliente
    global vcelular
    global vemail
    global vdata_nasc
    global vtelefone
    global vcep
    global vbairro
    global vrua
    global vcomplemento
    global tabela
    global usuar
    global permissao
    global cadastro


    nome = request.args.get('nome')
    sobrenome = request.args.get('sobrenome')
    documento = request.args.get('doc')


    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')

    #Consulta por nome
    if (nome != None and nome != "") and (sobrenome == None or sobrenome == '') and (documento == None or documento == ''):
        query = f''' EXEC [dbo].[consulta_cliente_nome] {nome} '''
        df = pd.read_sql(query, cnxn)
        tabela = df.to_html(col_space="100px", index=False, justify='center')

    # COnsulta por Nome e Sobrenome
    if (nome != None and nome != "") and (sobrenome != None and sobrenome != '') and (documento == None or documento == ''):
        query1 = f''' EXEC consulta_cliente_nome_sobrenome {nome},{sobrenome}'''
        df = pd.read_sql(query1, cnxn)
        tabela = df.to_html(col_space="100px", index=False, justify='center')

    # Consulta por documento
    if (nome == None or nome == "") and (sobrenome == None or sobrenome == '') and (documento != None and documento != ''):
        vardoc = documento.replace('.','').replace('-','')
        query2 = f''' EXEC [dbo].[consulta_cliente_documento] {vardoc} '''
        df = pd.read_sql(query2, cnxn)
        tabela = df.to_html(col_space="100px", index=False, justify='center')

    # Consulta por todos os campos
    if (nome != None and nome != "") and (sobrenome != None and sobrenome != '') and (documento != None and documento != ''):
        query3 = f''' EXEC [dbo].[consulta_cliente_full] {nome},'{sobrenome}',{documento} '''
        df = pd.read_sql(query3, cnxn)
        tabela = df.to_html(col_space="100px", index=False, justify='center')

    try:


        vnome = df['nome'].unique()
        vsobrenome = df['sobrenome'].unique()
        vdocumento = df['documento '].unique()
        vid_cliente = df['id_cliente'].unique()
        vcelular = df['celular'].unique()
        vemail = df['email'].unique()
        vdata_nasc = df['data_nascimento'].unique()
        vtelefone = df['telefone'].unique()
        vcep = df['cep'].unique()
        vbairro = df['bairro'].unique()
        vrua = df['rua'].unique()
        vcomplemento = df['complemento'].unique()
        #cadastro = df['data_cadastro'].unique()
        # vtelefone = df['data_ultima_alteracao'].unique()
        # vtelefone = df['data_ultima_alteracao'].unique()



    except:
        vcep = 'vazio'
        vdocumento = 'vazio'

    html = f''' 
    <b>Página de Consulta</b> <br><br> <br><br><br><br> <form method="GET">
                <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>

                 <center>
                NOME:
                <input type="text" name="nome">

                <br><br>SOBRENOME:
                <input type="text" name="sobrenome">

                <br><br>DOCUMENTO:
                <input type="text" name="doc">

              

                <br><br><input type="submit" name="enviar" value="Consultar">

                <br><br><br><br><br>


                <b>*Escolha um campo para fazer a consulta</b>




            </form></center>
            '''

    if (log == 'pastel' and permissao == 'iNone' and permissao == '1023'):
        return redirect('/')
    elif (nome == None and sobrenome == None and documento == None):
        return html
    elif (nome != None or sobrenome != None or documento != None):
        return redirect('/tabela_consulta')




@app.route('/tabela_consulta')
def tabela_consulta():
    global tabela



    html2 = tabela

    return f'''  <b>TABELA DE CONSULTA</b> 
                <br><br><html><center>
                <style>
                table, th, td
                {{
                    border: 1px solid black;
                }}
                </style>
                <body>{html2}</body></center></html>
                <br><br>  
            <a href = "http://127.0.0.1:5000/consulta"> Voltar para consulta </a>

            <p style="text-align:right;"> <a href = "http://127.0.0.1:5000/alterar"> Alterar dados do cliente </a> </p>
            <br>
            </form> 
                '''


@app.route("/alterar")
def alterar():
    global log
    global usuar
    global permissao
    global vsobrenome
    global vnome
    global vdocumento
    global vid_cliente
    global vcelular
    global vemail
    global vdata_nasc
    global vtelefone
    global vcep
    global vbairro
    global vrua
    global vcomplemento
    global tabela
    global usuar
    global permissao
    global cadastro
    global psobrenome
    global pdoc
    global pnome
    global id
    global html

    id = ''
    psobrenome = ''
    pnome = ''
    pdoc = ''

    altera_nome = request.args.get('nome')
    altera_sobrenome = request.args.get('sobrenome')
    altera_documento = request.args.get('doc')
    altera_celular = request.args.get('cel')
    altera_dt_nascimento = request.args.get('nascimento')
    altera_telefone = request.args.get('fone')
    altera_email = request.args.get('email')
    altera_cep = request.args.get('cep')
    altera_rua = request.args.get('rua')
    altera_bairro = request.args.get('bairro')
    altera_numero = request.args.get('numero')
    altera_complemento = request.args.get('complemento')

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')

    try:
        if altera_documento != None and altera_documento != '' :
            pdoc = altera_documento.replace('.','').replace('-','')
            pnome = altera_nome.strip()
            psobrenome = altera_sobrenome.strip()
            select = f''' SELECT id_cliente from clietes where documento = {pdoc} '''
            df = pd.read_sql(select, cnxn)
            id = df['id_cliente'][0]

        elif altera_nome != None and altera_sobrenome != None:
            pnome = altera_nome.strip()
            psobrenome = altera_sobrenome.strip()
            pdoc = altera_documento.replace('.', '').replace('-', '')
            select = f''' SELECT id_cliente from clietes where nome = '{pnome}' and sobrenome = '{psobrenome}' '''
            df = pd.read_sql(select, cnxn)
            id = df['id_cliente'][0]

    except:

        try:
            if altera_nome != None and altera_sobrenome != None:
                pnome = altera_nome.strip()
                psobrenome = altera_sobrenome.strip()
                pdoc = altera_documento.replace('.', '').replace('-', '')
                select = f''' SELECT id_cliente from clietes where nome = '{pnome}'  and sobrenome = '{psobrenome}' '''
                df = pd.read_sql(select, cnxn)
                id = df['id_cliente'][0]
        except: return html


    # Atualiza a tabela clietes
    if altera_documento != None and altera_documento != '' and psobrenome != None and psobrenome != ''\
        and pnome != None and pnome !='' and altera_celular != None and altera_celular != '' and altera_email != None \
        and altera_email != '' and altera_rua != None and altera_rua != '' and altera_bairro != None and \
        altera_bairro != '':

        clietes = f""" UPDATE dbo.clietes  SET sobrenome = '{psobrenome}' , nome = '{pnome}'
        , data_nascimento = '{altera_dt_nascimento}', data_cadastro = GETDATE(), usuario_ultalteracao = '{usuar}', documento = {altera_documento} 
                WHERE id_cliente = {id}"""
        cnxn.execute(clietes)
        cnxn.commit()
        time.sleep(5)


        # Atualiza a tabela contato
        atualiza_tb_contato = f""" UPDATE contato  SET celular = '{altera_celular}'
                                                , telefone = '{altera_telefone}'
                                                ,email = '{altera_email}'

                                                WHERE id_cliente = {id}

        """
        cnxn.execute(atualiza_tb_contato)
        cnxn.commit()
        time.sleep(5)

        # Atualiza a tabela endereco
        atualiza_tb_endereco = f""" UPDATE endereco  SET cep = '{altera_cep}'
                                                    ,rua = '{altera_rua}'
                                                    ,bairro = '{altera_bairro}'
                                                    ,numero = '{altera_numero}'
                                                    ,complemento = '{altera_complemento}'

                                                    WHERE id_cliente = {id}

            """
        cnxn.execute(atualiza_tb_endereco)
        cnxn.commit()
        time.sleep(5)



    html = f'''<b>Alteração das informações</b> <br><br> <br><br><br><br> <form method="PUT" >
    
    <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

    <input type="text" name="nome" placeholder="Digite Nome" >
    <input type="text" name="sobrenome" placeholder="Digite Sobrenome">
    <input type="text" size='30' name="doc" placeholder="Digite documento(apenas numeros)">
    <input type="text" name="nascimento" placeholder="Digite data de nascimento">
    <input type="text" name="cel" placeholder="Digite Celular">
    <input type="text" name="fone" placeholder="Digite Telefone(opcional)">
    <input type="text" name="email" placeholder="Digite e-mail"><br>
    <br><input type="text" name="cep" placeholder="Digite cep(opcional)">
    <input type="text" name="rua" placeholder="Digite Nome da rua">
    <input type="text" name="bairro" placeholder="Digite Nome do bairro">
    <input type="text" name="numero" placeholder="Digite Numero">
    <input type="text" size='25' name="complemento" placeholder="Digite Complemento(opcional)">
    
    <br><br><br><input type="submit" name="enviar" value="Cadastrar">
    <br><br><br><br>
    <b>PREENCHA TODOS OS CAMPOS OBRIGATÓRIOS<b>
    
</form> 
'''

    html2 = f'''<b>Alteração das informações</b> <br><br> <br><br><br><br> <form method="PUT" >
        
    <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

    <input type="text" name="nome" placeholder="Digite Nome" >
    <input type="text" name="sobrenome" placeholder="Digite Sobrenome">
    <input type="text" size='30' name="doc" placeholder="Digite documento(apenas numeros)">
    <input type="text" name="nascimento" placeholder="Digite data de nascimento">
    <input type="text" name="cel" placeholder="Digite Celular">
    <input type="text" name="fone" placeholder="Digite Telefone(opcional)">
    <input type="text" name="email" placeholder="Digite e-mail">
    <input type="text" name="cep" placeholder="Digite cep(opcional)">
    <input type="text" name="rua" placeholder="Digite Nome da rua">
    <input type="text" name="bairro" placeholder="Digite Nome do bairro">
    <input type="text" name="numero" placeholder="Digite Numero">
    <input type="text" size='25' name="complemento" placeholder="Digite Complemento(opcional)">
    
    <br><br><input type="submit" name="enviar" value="Cadastrar">
    <br><br><br><br>
</form> 

    Dados Alterados por {usuar}

    '''

    if (usuar == None or usuar == "") or log == False or permissao != "F":
        return redirect("/")
    elif altera_nome != "" and altera_nome != None:
        return html2
    else:
        return html


# Front para o registro de vendas

@app.route("/vendas")
def vendas():
    global log
    global usuar
    global permissao
    global msg
    global id_cli
    global id_produto
    global valor
    global quantidade
    global documento



    nome = request.args.get('nome')
    sobrenome = request.args.get('sobrenome')
    documento = request.args.get('doc')
    quantidade = request.args.get('qtd')
    produto = request.args.get('produto')



    html = f'''<b>Cadastro das vendas</b> <br><br>  <br><br><br><br> 
    <form method="PUT" >
    <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

    <input type="text" name="nome" placeholder="Digite Nome" >
    <input type="text" name="sobrenome" placeholder="Digite Sobrenome">
    <input type="text" size='30' name="doc" placeholder="Digite documento(apenas numeros)">
    <input type="text" size='25' name="qtd" placeholder="Digite a quantidade comprada">
    <input type="text" name="produto" placeholder="Digite nome do produto">
    

    <br><br><br><input type="submit" name="enviar" value="Cadastrar">
    <br><br><br><br>
</form> 


'''

    html2 = f'''<b>ERRO no Cadastro das vendas</b> <br><br>  <br><br><br><br> 
    <form method="PUT" >
    <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

    <input type="text" name="nome" placeholder="Digite Nome" >
    <input type="text" name="sobrenome" placeholder="Digite Sobrenome">
    <input type="text" size='30' name="doc" placeholder="Digite documento(apenas numeros)">
    <input type="text" size='25' name="qtd" placeholder="Digite a quantidade comprada">
    <input type="text" name="produto" placeholder="Digite nome do produto">
    

    <br><br><br><input type="submit" name="enviar" value="Cadastrar">
    <br><br><br><br>
</form> 


'''
    if (usuar == 'iNone' or usuar == "1025") or log == 'pastel':# or permissao != "F":
        return redirect('/')
    # elif nome == None:
    #     return html
    elif documento == None:
        return html
    elif len(documento) <= 1:
        return html
    elif (documento != None and documento != ""):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')
        try:

            try:
                cnxn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')
                rdocumento = documento.replace('-', '').replace('.', '')
                valida_cliente = f''' SELECT id_cliente FROM [Projeto_Integrador2].[dbo].[clietes] WHERE documento = {rdocumento} '''
                df = pd.read_sql(valida_cliente, cnxn)
                id_cli = df['id_cliente'][0]

                cproduto = produto.strip().upper()
                cid_produto = f''' SELECT id_produto FROM [Projeto_Integrador2].dbo.dim_produto WHERE upper(trim(nome_produto)) = '{produto}' '''
                df = pd.read_sql(cid_produto, cnxn)
                id_produto = df['id_produto'][0]
                #
                cvalor = f''' SELECT valor FROM [Projeto_Integrador2].dbo.dim_produto WHERE id_produto = {id_produto} '''
                df = pd.read_sql(cvalor, cnxn)
                valor_unidade = df['valor'][0]
                valor = valor_unidade * float(quantidade)

            except:
                return html2 + f'Cliente não cadastrado<br><br> Nome: {nome}, <br><br> Documento: {documento}'








        except:
            cproduto = documento.strip().upper()
            cid_produto = f''' SELECT id_produto FROM [Projeto_Integrador2].dbo.dim_produto WHERE nome_produto = {cproduto} '''
            df = pd.read_sql(cid_produto, cnxn)
            id_produto = df['id_produto'][0]

        try:
            cnxn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')

            # Inserindo dados na tabela de vendas
            query_venda = f''' insert into  [Projeto_Integrador2].[dbo].[vendas]
                                (id_cliente,id_produto,quantidade,vendedor,valor,data_venda) 
                          values({id_cli},{id_produto},{quantidade},'{usuar}',{valor},GETDATE()) '''
            cnxn.execute(query_venda)
            cnxn.commit()
            time.sleep(5)

            vendas = f''' SELECT id_venda FROM [Projeto_Integrador2].[dbo].[vendas] WHERE data_venda = (select max(data_venda) from [Projeto_Integrador2].[dbo].[vendas]) '''
            df = pd.read_sql(vendas, cnxn)
            id_venda = df['id_venda'][0]
            time.sleep(5)



            # Atualizando a tabela da estoque

            saldo_estoque = f''' SELECT [quantidade_estoque] FROM [Projeto_Integrador2].[dbo].[estoque] WHERE data_atualizacao = (select max(data_atualizacao) from [Projeto_Integrador2].[dbo].[estoque]) '''
            df = pd.read_sql(saldo_estoque, cnxn)
            saldo_estoque = df['quantidade_estoque'][0]
            time.sleep(5)


            qtd_entrada = 0
            qtd_saida = quantidade
            saldo = int(saldo_estoque) - int(quantidade)

            query_estoque = f''' insert into  [Projeto_Integrador2].[dbo].[estoque]
                                    (id_produto,qtd_entrada,qtd_saida,quantidade_estoque,id_venda,data_atualizacao) 
                                    values({id_produto},{qtd_entrada},{qtd_saida},{saldo},{id_venda},GETDATE()) '''
            cnxn.execute(query_estoque)
            cnxn.commit()
            time.sleep(3)



            return html + f" venda cadastrada com sucesso"

        except:
            return html2 + f'Houve um erro no cadastramento, clie {id_cli}, prod: {id_produto}, qtd: {quantidade}, us: {usuar}, val: {valor}'



@app.route("/estoque")
def estoque():
    global log
    global usuar
    global permissao
    global qtd_entrada
    global qtd_saida
    global saldo
    global cod_prod
    global query_estoque
    log = False
    usuario = usuar
    entrada = ''
    qtd_entrada = ''
    qtd_saida = ''
    saldo = ''
    cod_prod = ''
    query_estoque = ''

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')


    qtd = request.args.get('valor')
    # usuar = usuario
    acao = request.args.get('acao')

    produto = request.args.get('produto')


    saldo_estoque = f''' SELECT [quantidade_estoque] FROM [Projeto_Integrador2].[dbo].[estoque] WHERE data_atualizacao = (select max(data_atualizacao) from [Projeto_Integrador2].[dbo].[estoque]) '''
    df = pd.read_sql(saldo_estoque, cnxn)
    saldo_estoque = df['quantidade_estoque'][0]



    form = f'''<b>Fluxo de estoque</b> <br><br> <br><br><br><br> <form method="PUT" >
             <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

            <select type="text" name="acao"> 
                <option value='entrada'>Entrada</option>
                 <option value='saida'>Saida</option>
                 placeholder="Escolha sua acao" /select>
            
            <input type="text" name="valor" placeholder="Digite quantidade">
            <input type="text" name="produto" placeholder="Digite produto">
            <input type="submit" name="enviar" value="Atualizar">
        </form> 
            <br><br><i> Houve algum problema com a atualização do estoque  <i> '''

    form_2 = f'''<b>Fluxo de estoque</b> <br><br> <br><br><br><br> <form method="PUT" >
             <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

            <select type="text" name="acao"> 
                <option value='entrada'>Entrada</option>
                 <option value='saida'>Saida</option>
                 placeholder="Escolha sua acao" /select>
                 
            <input type="text" name="valor" placeholder="Digite quantidade">
            <input type="text" name="produto" placeholder="Digite produto">
            <input type="submit" name="enviar" value="Atualizar">
        </form> 
            <br><br>'''

    html_sucesso = f'''<b>Fluxo de estoque</b> <br><br> <br><br><br><br> <form method="PUT" >
             <body>
                <style>
                body{{

                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: Violet


                 }}
                 </style></body>
                 <label for >

            <select type="text" name="acao"> 
                <option value='entrada'>Entrada</option>
                 <option value='saida'>Saida</option>
                 placeholder="Escolha sua acao" /select>
                 
            <input type="text" name="valor" placeholder="Digite quantidade">
            <input type="text" name="produto" placeholder="Digite produto">
            <input type="submit" name="enviar" value="Atualizar">
        </form> 
            <br><br> <b>Estoque atualizado !!! </b>'''


    if (log == True and usuario != None and permissao == 'F'):
        return redirect(url_for("menu"))

    elif (log == True and usuario != None and permissao == 'C'):
        return redirect(url_for("/"))






    elif (acao != None and acao != '') and (qtd != None and qtd != ''):
        # Atualizando estoque

        query = f''' SELECT [id_produto] FROM [Projeto_Integrador2].[dbo].dim_produto 
        where trim(upper([nome_produto])) = trim(upper('{produto}')) '''
        df_prod = pd.read_sql(query, cnxn)
        cod_prod = df_prod['id_produto'][0]
        cod_prod = int(cod_prod)


        if acao == 'entrada':
            qtd_entrada = qtd
            qtd_saida = 0
            saldo = int(saldo_estoque) + int(qtd)

        elif acao == 'saida':
            qtd_entrada = 0
            qtd_saida = qtd
            saldo = int(saldo_estoque) - int(qtd)

        query_estoque = f''' insert into  [Projeto_Integrador2].[dbo].[estoque]
                                        (id_produto,qtd_entrada,qtd_saida,quantidade_estoque,usuario_alteracao,data_atualizacao)
                                  values({cod_prod},{qtd_entrada},{qtd_saida},{saldo},'{usuar}',GETDATE()) '''
        cnxn.execute(query_estoque)
        cnxn.commit()
        time.sleep(3)
        return html_sucesso

    elif (log == False and usuario != None):
        return form_2

    else:
        return form


@app.route("/graficos")
def graficos():
    global usuar
    global permissao
    global log
    log = True

    html = ''' <html><b>Menu</b><br><br>
                <left>

                <body>
                <br><br><br>
                <b>Escolha sua ação:</b>
                <style>
                body{

                    background-color: Violet

                    }
                </style>

                </body>
                <br><br><br>
                <a href = "http://127.0.0.1:5000/dash_dia"> Visão por dia </a>

                <br><br> <a href = "http://127.0.0.1:5000/dash_mes" > Visão por mês </a>



                </html>

    '''
    if (usuar == None or usuar == "") or log == False:
        return redirect("/")

    else:
        return html





@app.route("/dash_dia")
def dash():
    global tipo
    tipo = request.args.get('visao')


    dashboard_html = ''' <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>Dashboard de Vendas</title>
                    </head>
                    <body>
                    <br> <form method="PUT" >
                    <select type="text" name="visao">
                    <option value=''></option> 
                <option value='estoque'>Estoque</option>
                 <option value='vendas'>Vendas</option>
                 <option value='faturamento'>Faturamento</option>
                 
                 
                 placeholder="Escolha a visão" /select>
                 <input type="submit" name="enviar" value="Atualizar"><br></form>
                    
                    
                        {{ plot | safe }}
                        
                        <br><br>
                    </body>
                    </html> '''



    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')

    query = f''' SELECT max(quantidade_estoque) estoque
                  ,cast(convert(date,data_atualizacao,107) as varchar) as [data]
                  FROM [Projeto_Integrador2].[dbo].[estoque]
                  group by cast(convert(date,data_atualizacao,107) as varchar) '''

    df_prod = pd.read_sql(query, cnxn)
    qtd_estoque = df_prod['estoque']
    dias = pd.to_datetime(df_prod['data'])
    dd = go.Scatter(x=dias, y=qtd_estoque, mode='markers + lines',line={'color':'#8722E0'})
    layout = go.Layout(title = 'Estoque por dia', xaxis= dict(title='Dias'), yaxis=dict(title='Estoque'))



    #Visao de estoque
    fig = go.Figure(data=dd, layout=layout)




    #Visao de vendas
    query_v = f''' SELECT sum(quantidade) as qtd_vendas, convert(date, data_venda) as dt_venda
                        FROM [Projeto_Integrador2].[dbo].[vendas]
                        group by  convert(date, data_venda) '''

    df_prod_v = pd.read_sql(query_v, cnxn)
    qtd_estoque_v = df_prod_v['qtd_vendas']
    dias_v = pd.to_datetime(df_prod_v['dt_venda'])
    dd_v = go.Scatter(x=dias_v, y=qtd_estoque_v, mode='markers + lines', line={'color': '#8722E0'})
    layout_v = go.Layout(title='Vendas por dia', xaxis=dict(title='Dias'), yaxis=dict(title='Vendas'))

    fig2 = go.Figure(data=dd_v, layout=layout_v)



    # Faturamento
    query_faturamento = '''  SELECT sum(valor) as valor, convert(date,data_venda) as dt_venda
                        FROM [Projeto_Integrador2].[dbo].[vendas]
                        group by  convert(date,data_venda)
                        order by  convert(date,data_venda)  '''
    df_fatu = pd.read_sql(query_faturamento, cnxn)
    fatu = df_fatu['valor']
    mes_fatu = df_fatu['dt_venda']
    dd_fatu = go.Scatter(x=mes_fatu, y=fatu, mode='markers + lines', line={'color': '#8722E0'})
    layout_fatu = go.Layout(title='Faturamento por dia', xaxis=dict(title='Mês'), yaxis=dict(title='Faturamento'))

    figf = go.Figure(data=dd_fatu, layout=layout_fatu)



    tipo = request.args.get('visao')
    if (tipo == 'estoque') or (tipo == '') or (tipo == None):
        return render_template_string(dashboard_html, plot=fig.to_html())
    elif tipo == 'vendas':
        return render_template_string(dashboard_html, plot=fig2.to_html())
    elif tipo == 'faturamento':
        return render_template_string(dashboard_html, plot=figf.to_html())


@app.route("/dash_mes")
def dash_mes():
    global tipo
    tipo = request.args.get('visao')

    dashboard_html = ''' <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>Dashboard de Vendas</title>
                    </head>
                    <body>
                    <br> <form method="PUT" >
                    <select type="text" name="visao">
                    <option value=''></option> 
                <option value='estoque'>Estoque</option>
                 <option value='vendas'>Vendas</option>
                 <option value='faturamento'>Faturamento</option>
                 
                 placeholder="Escolha a visão" /select>
                 <input type="submit" name="enviar" value="Atualizar"><br></form>


                        {{ plot | safe }}

                        <br><br> 
                    </body>
                    </html> '''

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-0Q3N0LC\SQLEXPRESS;DATABASE=Projeto_Integrador2;Trusted_Connection=yes')

    query = f''' SELECT max(quantidade_estoque) estoque
                  ,format(data_atualizacao,'MMM') as [data]
                  FROM [Projeto_Integrador2].[dbo].[estoque]
                  group by format(data_atualizacao,'MMM')
                    order by  format(data_atualizacao,'MMM') desc'''

    df_prod = pd.read_sql(query, cnxn)
    qtd_estoque = df_prod['estoque']
    dias = df_prod['data']
    dd = go.Scatter(x=dias, y=qtd_estoque, mode='markers + lines', line={'color': '#8722E0'})
    layout = go.Layout(title='Estoque por mês', xaxis=dict(title='Mês'), yaxis=dict(title='Estoque'))

    # Visao de estoque
    fig = go.Figure(data=dd, layout=layout)

    # Visao de vendas
    query_v = f''' SELECT sum(quantidade) as qtd_vendas, format(data_venda,'MMM') as dt_venda
                    FROM [Projeto_Integrador2].[dbo].[vendas]
                    group by  format(data_venda,'MMM')
                    order by  format(data_venda,'MMM') desc; '''

    df_prod_v = pd.read_sql(query_v, cnxn)
    qtd_estoque_v = df_prod_v['qtd_vendas']
    dias_v = df_prod_v['dt_venda']
    dd_v = go.Scatter(x=dias_v, y=qtd_estoque_v, mode='markers + lines', line={'color': '#8722E0'})
    layout_v = go.Layout(title='Vendas por mês', xaxis=dict(title='Mês'), yaxis=dict(title='Vendas'))

    fig2 = go.Figure(data=dd_v, layout=layout_v)



    #Faturamento

    query_faturamento = '''  SELECT sum(valor) as valor, format(data_venda,'MMM') as mes
                    FROM [Projeto_Integrador2].[dbo].[vendas]
                    group by  format(data_venda,'MMM')
                    order by  format(data_venda,'MMM') desc  '''
    df_fatu = pd.read_sql(query_faturamento, cnxn)
    fatu = df_fatu['valor']
    mes_fatu = df_fatu['mes']
    dd_fatu = go.Scatter(x=mes_fatu, y=fatu, mode='markers + lines', line={'color': '#8722E0'})
    layout_fatu = go.Layout(title='Faturamento por mês', xaxis=dict(title='Mês'), yaxis=dict(title='Faturamento'))

    figf = go.Figure(data=dd_fatu, layout=layout_fatu)






    tipo = request.args.get('visao')
    if (tipo == 'estoque') or (tipo == '') or (tipo == None):
        return render_template_string(dashboard_html, plot=fig.to_html())
    elif tipo == 'vendas':
        return render_template_string(dashboard_html, plot=fig2.to_html())
    elif tipo == 'faturamento':
        return render_template_string(dashboard_html, plot=figf.to_html())


if __name__ == "__main__":
    app.run(debug=True)
