from flask import Flask, request, Response, g, redirect, url_for, flash, render_template_string

global usuario
global password
global saida



app = Flask(__name__)

@app.route("/")
def homepage():

    global usuario
    global password
    global saida

    usuario = request.args.get('user_login')
    password = request.args.get('senha_login')



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

    if usuario == '' or usuario == None:

        saida = form_2

    else:
        saida = form

    return saida

if __name__ == "__main__":
    app.run(debug=True)
