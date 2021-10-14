from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
@app.route('/Login.html',methods=['GET','POST'])
def home():
    return render_template('Login.html')

@app.route("/Registro.html", methods=['GET', 'POST'])
def crearcuenta():
    return render_template('Registro.html')

@app.route('/Recuperar.html', methods=['GET', 'POST'])
def Recuperar():
    return render_template('Recuperar.html')

@app.route('/Code',methods=['GET', 'POST'])
def RecuperarCode():
    return render_template('RecuperarCode.html')

@app.route('/nuevacontraseña',methods=['GET', 'POST'])
def NewContra():
    return render_template('Contraseña_nueva.html')

@app.route('/vuelo',methods=['GET', 'POST'])
def vervuelo():
    return render_template('codigodevuelo.html')

@app.route('/administrador')
def admin():
    return render_template('administrador.html')

@app.route("/aviones")
def admminaviones():
    return render_template('aviones.html')
    
@app.route('/vuelos')
def adminvuelos():
    return render_template('vuelos.html')

@app.route("/usuarios")
def adminsusuarios():
    return render_template('usuarios.html')

@app.route("/pilotos")
def adminspilotos():
    return render_template('vuelosasigadospilotos.html')

@app.route('/gestioncomentarios')
def gestionComentarios():
    return render_template('gestionComentarios.html')

@app.route('/confirmarreserva')
def confirmarReserva():
    return render_template('confirmarReserva.html')
    
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)