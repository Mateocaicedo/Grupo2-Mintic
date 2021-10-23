from flask import Flask,redirect, session,url_for,render_template,request
import os
import sqlite3
from sqlite3 import Error
from flask.helpers import flash
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import escape

app=Flask(__name__)
app.secret_key = os.urandom( 24 )

roles = {1:"SUPERADMINISTRADOR",2:"USUARIO",3:"PILOTO"}
@app.route('/',methods=['GET','POST'])
@app.route('/Login.html',methods=['GET','POST'])
def home():
    if "usuario" in session:
        return redirect("administrador")
    else:
        if request.method == "GET":
            return render_template('Login.html')
        if request.method == "POST":
            usuario = escape(request.form['usuario'])
            contraseña = escape(request.form['contraseña'])
            if usuario =="" or contraseña== "":
                flash("Campos vacios")
                return redirect("/")
            else:

                try:
                    with sqlite3.connect('reto.db') as con:
                        cur = con.cursor()
                        cur.execute("SELECT contraseña,id_rol,nombre,apellido,correo, cedula, fecha_nacimiento, id_usuarios FROM usuarios WHERE cedula = ?", [usuario])
                        row = cur.fetchone()
                        print(row)
                        if row is None:
                            flash("No se encontro el usuario")
                            return render_template("login.html")
                        else:
                            contra = str(row[0])
                           
                            if  check_password_hash(contra, contraseña):
                                print("holalolaaa")
                                if  int(row[1] )== 1:
                                    session["usuario"] = usuario 
                                    session["rol"] = row[1]
                                    session["nombre"] = row[2]
                                    session["apellido"] = row[3]
                                    session["email"] = row[4]
                                    session["cedula"] = row[5]
                                    session["fecha_nacimiento"] = row[6]
                                    session["id_usuarios"] = row[7]
                                    return redirect("administrador")
                                elif  int(row[1]) == 2:
                                    flash('No eres administrador')
                                    return render_template("Login.html")
                                elif int(row[1]) ==3:
                                    flash('No eres administrador')
                                    return render_template("Login.html")
                                
                               
                            else:
                                flash('Contraseña incorrecta')
                                return redirect("/")

                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
    

@app.route("/Registro", methods=["GET", "POST"])
def crearcuenta():
    if request.method == "POST":
        print("sexo")
        nombre = escape(request.form['nombre'])
        apellido = escape(request.form['apellido'])
        correo = escape(request.form['correo'])
        direccion = escape(request.form['direccion'])
        cedula = escape(request.form['cedula'])
        contraseña = escape(request.form['contraseña'])
        confirmcontra = escape(request.form['confirmcontra'])
        fecha = escape(request.form['fe'])
        sexo =escape(request.form['sexo'])

        if nombre =="" or apellido=="" or correo=="" or direccion=="" or cedula=="" or contraseña=="" or confirmcontra== "" or fecha=="" or sexo=="":
            flash("Hay campos vacios")
            return redirect("/Registro")
        else:
            if contraseña == confirmcontra:
                contranueva = contraseña
                contrahash = generate_password_hash(contranueva)
                try:
                    with sqlite3.connect('reto.db') as con:
                        cur = con.cursor()
                        cur.execute("select * from usuarios where cedula=?",[cedula])
                        dime = cur.fetchone()
                        if dime!= None:
                            flash('Este usuario ya existe en la base de datos')
                            
                        else:
                            cur = con.cursor()
                            cur.execute("INSERT INTO usuarios VALUES (NULL,?,?,?,?,?,?,?,?,?)", (nombre, apellido, direccion, correo, contrahash, sexo, fecha, cedula,3))
                            con.commit()
                            flash("Cuenta creada con exito")
                            
                except Error as er:
                    flash("Ocurrio un error")
                    print('SQLite error: %s' % (' '.join(er.args)))
                return redirect('/Registro')
            else:
                flash('Contraseña incorrecta')
                return render_template('Registro.html', titulo='Crear Cuenta')
    if request.method == "GET":
        return render_template('Registro.html', titulo='Crear Cuenta')

    
    
    

    

@app.route('/Recuperar.html', methods=['GET', 'POST'])
def Recuperar():
    return render_template('Recuperar.html')

@app.route('/Code',methods=['GET', 'POST'])
def RecuperarCode():
    return render_template('RecuperarCode.html')

@app.route('/nuevacontraseña',methods=['GET', 'POST'])
def NewContra():
    if request.method == 'GET':
        return render_template('Contraseña_nueva.html')
    if request.method == 'POST':
        usuario= escape(request.form['usuario'])
        contraseña = escape(request.form['contra'])
        confirmacontra =escape(request.form['confirmcontra'])

        if usuario == "" or contraseña=="" or confirmacontra=="":
            flash('Hay campos vacios')
            return redirect('/nuevacontraseña')
        else:
            if contraseña == confirmacontra:
                nueva = contraseña
                contrahash = generate_password_hash(nueva)
                try:
                    with sqlite3.connect('reto.db') as con:
                            cur = con.cursor()
                            cur.execute("select * from usuarios where cedula=?",[usuario])
                            dime = cur.fetchone()
                            if dime!= None:
                                cur.execute("update usuarios set contraseña =? where cedula=?", [contrahash,dime[8]])
                                con.commit()
                                print("dime si",[dime[8]])
                                flash('Contraseña restablecida con exito')
                            else:
                                flash('Este usuario no existe en la base de datos')
                except Error as er:
                    flash("Ocurrio un error")
                    print('SQLite error: %s' % (' '.join(er.args)))
                return redirect('/nuevacontraseña')
            else: 
                flash('Las contraseñas no coinciden')
                return redirect('/nuevacontraseña')
        

@app.route('/vuelo',methods=['GET', 'POST'])
def vervuelo():
    return render_template('codigodevuelo.html')

@app.route('/administrador',methods=['GET', 'POST'])
def admin():
    if "usuario" in session:
        
        if request.method == "GET":
            nombrecompleto = session["nombre"] +" "+ session["apellido"]
            try:
                with sqlite3.connect('reto.db') as con:
                    cur = con.cursor()
                    cur.execute("SELECT cedula,nombre,apellido, direccion, genero, fecha_nacimiento FROM usuarios")
                    row = cur.fetchone()
                    print(row)

            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('administrador.html',nombrecompleto=nombrecompleto, nombre=session["nombre"], apellido = session["apellido"], cedula = session["cedula"], nacimiento = session["fecha_nacimiento"], correo= session["email"])
        if request.method == "POST":
            contra = escape(request.form['contrase'])
            contraconfirm = escape(request.form['confirmarcontra'])
            if contra =="" or contraconfirm== "":
                flash("Campos vacios")
                return redirect("/administrador")
            else:
                if contra == contraconfirm:
                    nueva= contra
                    contrahash = generate_password_hash(nueva)
                    try:
                        with sqlite3.connect('reto.db') as con:
                            cur = con.cursor()
                            cur.execute("update usuarios set contraseña=? where id_usuarios=? ",[contrahash,session["id_usuarios"]])
                            con.commit()
                            dato = cur.fetchone()
                            flash("Contraseña actualizada con exito")
                            print(session["id_usuarios"])
                    except Error  as er:
                        print('SQLite error: %s' % (' '.join(er.args)))
                    return redirect('/administrador')
                else:
                    flash('Contraseña incorrecta')
                    return redirect('/administrador')
    else:
        return redirect("/")





@app.route("/aviones", methods=["POST","GET"])
def admminaviones():
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM aviones")
                    row = cur.fetchall()
                    print(row)

            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('aviones.html', row=row)

        if request.method == "POST":
            marca = escape(request.form['marca'])
            capacidad = escape(request.form['capacidad'])

            if marca=="" or capacidad=="":
                flash("Campos vacios")
                return redirect("/aviones")
            else:
                try:
                    with sqlite3.connect('reto.db') as con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO aviones VALUES (NULL, ?,?)",(marca, capacidad) )
                        con.commit()
                        flash("Avion agregado con exito")
                except Error as er:
                    flash("Ocurrio un error")
                    print('SQLite error: %s' % (' '.join(er.args)))
                return redirect('/aviones')
    else:
        return redirect("/")


@app.route("/editaraviones/<int:id>", methods=["POST","GET"])
def avioneseditar(id):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM aviones where id_avion=?",[id])
                    row = cur.fetchall()

                    cur.execute("select * from aviones where id_avion=?",[id])
                    unavion =cur.fetchone()
                    print(row)

            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('avioneseditar.html', row=row, unavion=unavion)
        if request.method == "POST":
            marca = escape(request.form['marca'])
            capacidad = escape(request.form['capacidad'])

            if marca=="" or capacidad=="":
                flash("Campos vacios")
                return redirect("/aviones")
            else:
                try:
                    with sqlite3.connect('reto.db') as con:
                        cur = con.cursor()
                        cur.execute("Update aviones set marca=?, capacidad=? where id_avion =?", [marca, capacidad, id])
                        con.commit()
                        flash("Avion actualizado con exito")
                except Error as er:
                    flash("Ocurrio un error")
                    print('SQLite error: %s' % (' '.join(er.args)))
                return redirect('/aviones')
    else:
        return redirect("/")

@app.route("/eliminaraviones/<int:id>", methods=["POST","GET"])
def avioneseliminar(id):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT * FROM aviones where id_avion=?",[id])
                    row = cur.fetchall()

                    cur.execute("select * from aviones where id_avion=?",[id])
                    unavion =cur.fetchone()
                    print(row)

            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('avioneseliminar.html', row=row, unavion=unavion)
        if request.method == "POST":
            try:
                with sqlite3.connect('reto.db') as con:
                    cur = con.cursor()
                    cur.execute("delete from aviones where id_avion =?", [ id])
                    con.commit()
                    flash("Avion eliminado con exito")
            except Error as er:
                flash("Ocurrio un error")
                print('SQLite error: %s' % (' '.join(er.args)))
            return redirect('/aviones')
    else:
        return redirect("/")




@app.route('/vuelos', methods=["POST","GET"])
def adminvuelos():
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT marca, id_avion FROM aviones")
                    av = cur.fetchall()

                    cur.execute("SELECT nombre, id_usuarios FROM usuarios where id_rol = 3")
                    piloto = cur.fetchall()

                    cur.execute("select v.ID, v.origen, v.destino, v.escala, u.nombre, v.cupos, a.marca, v.estado, v.precio from vuelos v inner join usuarios u on v.id_usuarios =u.id_usuarios inner join aviones a on v.id_avion =a.id_avion")
                    vuel = cur.fetchall()  

            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('vuelos.html', av=av, piloto=piloto, vuel=vuel)

        if request.method == "POST":
            origen = escape(request.form['origen'])
            destino = escape(request.form['destino'])
            escala = escape(request.form['escala'])
            Piloto = escape(request.form['Piloto'])
            cupos = escape(request.form['cupos'])
            avion = escape(request.form['avion'])
            Estado = escape(request.form['Estado'])
            precio = escape(request.form['precio'])
            print(Piloto)


            if origen=="" or destino=="" or escala=="" or Piloto=="" or cupos=="" or avion=="" or Estado=="" or precio=="":
                flash("Hay campos vacios")
                return redirect("/vuelos")
            else:
                try:
                    with sqlite3.connect('reto.db') as con:
                        print("ola")
                        cur = con.cursor()

                        """ cur.execute("SELECT id FROM usuarios where nombre = ?",Piloto)
                        pilotos = cur.fetchone()

                        cur.execute("SELECT id FROM aviones where marca = ?",avion)
                        aviones = cur.fetchone()

                        print(pilotos["ID"], aviones["Id"]) """
                        cur.execute("INSERT INTO vuelos VALUES (NULL,?,?,?,?,?,?,?,?)",[origen, destino, escala, Piloto, cupos, avion,Estado,precio] )
                        con.commit()
                        flash("Vuelo agregado con exito")
                        return redirect('/vuelos')
                except Error as er:
                    flash("Ocurrio un error")
                    print('SQLite error: %s' % (' '.join(er.args)))
                    return redirect('/vuelos')
    else:
        return redirect("/")
    

@app.route('/editarvuelos/<int:id>', methods=["POST","GET"])
def admineditarvuelos(id):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT marca, id_avion FROM aviones")
                    av = cur.fetchall()

                    cur.execute("SELECT nombre, id_usuarios FROM usuarios where id_rol = 3")
                    piloto = cur.fetchall()

                    cur.execute("SELECT a.ID, a.origen, a.destino, a.escala, u.nombre, a.cupos, v.marca, a.estado, a.precio from vuelos a join aviones v join usuarios u  on a.id_avion = v.id_avion and u.id_usuarios = a.id_usuarios where a.ID =?",[id])
                    vuel = cur.fetchall()  
                    cur.execute("SELECT a.ID, a.origen, a.destino, a.escala, u.nombre, a.cupos, v.marca, a.estado, a.precio from vuelos a join aviones v join usuarios u  on a.id_avion = v.id_avion and u.id_usuarios = a.id_usuarios where a.ID =?",[id])
                    unvuel = cur.fetchone()  

            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('vueloseditar.html', av=av, piloto=piloto, vuel=vuel, unvuel=unvuel)

    if request.method == "POST":
            origen = escape(request.form['origen'])
            destino = escape(request.form['destino'])
            escala = escape(request.form['escala'])
            Piloto = escape(request.form['Piloto'])
            cupos = escape(request.form['cupos'])
            avion = escape(request.form['avion'])
            Estado = escape(request.form['Estado'])
            precio = escape(request.form['precio'])
            print(Piloto)
            print("avion", avion)
            if origen=="" or destino=="" or escala=="" or Piloto=="" or cupos=="" or avion=="" or Estado=="" or precio=="":
                flash("Hay campos vacios")
                return redirect("/vuelos")
            else:
                try:
                    with sqlite3.connect('reto.db') as con:
                        print("ola")
                        cur = con.cursor()

                        
                        cur.execute("Update vuelos set origen=?, destino=?, escala=?, id_usuarios=?, cupos=?, id_avion=?, estado =?, precio=? where ID =?",[origen, destino, escala, Piloto, cupos, avion,Estado,precio, id] )
                        con.commit()
                        flash("Vuelo actualizado con exito")
                        return redirect('/vuelos')
                except Error as er:
                    flash("Ocurrio un error")
                    print('SQLite error: %s' % (' '.join(er.args)))
                    return redirect('/vuelos')
        
    else:
        return redirect("/")


@app.route('/eliminarvuelos/<int:id>', methods=["POST","GET"])
def admineliminarvuelos(id):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT marca, id_avion FROM aviones")
                    av = cur.fetchall()

                    cur.execute("SELECT nombre, id_usuarios FROM usuarios where id_rol = 3")
                    piloto = cur.fetchall()

                    cur.execute("SELECT a.ID, a.origen, a.destino, a.escala, u.nombre, a.cupos, v.marca, a.estado, a.precio from vuelos a join aviones v join usuarios u  on a.id_avion = v.id_avion and u.id_usuarios = a.id_usuarios where a.ID =?",[id])
                    vuel = cur.fetchall()  
                    cur.execute("SELECT a.ID, a.origen, a.destino, a.escala, u.nombre, a.cupos, v.marca, a.estado, a.precio from vuelos a join aviones v join usuarios u  on a.id_avion = v.id_avion and u.id_usuarios = a.id_usuarios where a.ID =?",[id])
                    unvuel = cur.fetchone()  

            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('vueloseliminar.html', av=av, piloto=piloto, vuel=vuel, unvuel=unvuel)

        if request.method == "POST":
            try:
                with sqlite3.connect('reto.db') as con:
                    cur = con.cursor()
                    cur.execute("delete from vuelos where ID =?", [ id])
                    con.commit()
                    flash("Vuelo eliminado con exito")
            except Error as er:
                flash("Ocurrio un error")
                print('SQLite error: %s' % (' '.join(er.args)))
            return redirect('/vuelos')
    else:
        return redirect("/")







@app.route("/usuarios", methods=["POST","GET"])
def adminsusuarios():
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT r.nombre, * FROM rol r join usuarios u on r.id_rol = u.id_rol")
                    usuarios = cur.fetchall()
                    print(usuarios)

                    cur.execute("select id_rol, nombre from rol" )
                    rol = cur.fetchall()
                    
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('usuarios.html',usuarios=usuarios, rol=rol)


        if request.method == "POST":
            nombre = escape(request.form['nombre'])
            apellido = escape(request.form['apellido'])
            direccion = escape(request.form['Direccion'])
            correo = escape(request.form['Correo'])
            contraseña = escape(request.form['contraseña'])
            confirmcontra = escape(request.form['confirmcontra'])
            sexo =escape(request.form['sexo'])
            fecha = escape(request.form['fecha'])
            cedula = escape(request.form['Cedula'])
            roll = escape(request.form['rol'])
            if nombre =="" or apellido=="" or correo=="" or direccion=="" or cedula=="" or contraseña=="" or confirmcontra== "" or fecha=="" or sexo=="" or roll =="":
                flash("Hay campos vacios")
                return redirect("/usuarios")
            else:
                if contraseña == confirmcontra:
                    contranueva = contraseña
                    contrahash = generate_password_hash(contranueva)
                    try:
                        with sqlite3.connect('reto.db') as con:
                            cur = con.cursor()
                            cur.execute("select * from usuarios where cedula=?",[cedula])
                            dime = cur.fetchone()
                            if dime!= None:
                                flash('Este usuario ya existe en la base de datos')
                            else:
                                cur = con.cursor()
                                cur.execute("INSERT INTO usuarios VALUES (NULL,?,?,?,?,?,?,?,?,?)", (nombre, apellido, direccion, correo, contrahash, sexo, fecha, cedula, roll))
                                con.commit()
                                flash("Cuenta creada con exito")
                    except Error as er:
                        flash("Ocurrio un error")
                        print('SQLite error: %s' % (' '.join(er.args)))
                    return redirect('/usuarios')
                else:
                    flash('Contraseña incorrecta')
                    return redirect('/usuarios')
    else:
        return redirect("/")
    


@app.route("/editarusaurios/<int:id>", methods=["POST","GET"])
def adminsusuarioseditar(id):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT r.nombre, * FROM rol r join usuarios u on r.id_rol = u.id_rol where u.id_usuarios =?",[id])
                    usuarios = cur.fetchall()

                    cur.execute("SELECT r.nombre, * FROM rol r join usuarios u on r.id_rol = u.id_rol where u.id_usuarios =?",[id])
                    unusuarios = cur.fetchone()
                    print(unusuarios)

                    cur.execute("select id_rol, nombre from rol" )
                    rol = cur.fetchall()
                    
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('usuarioseditar.html',usuarios=usuarios, rol=rol, unusuarios=unusuarios)


        if request.method == "POST":
            nombre = escape(request.form['nombre'])
            apellido = escape(request.form['apellido'])
            direccion = escape(request.form['Direccion'])
            correo = escape(request.form['Correo'])
            contraseña = escape(request.form['contraseña'])
            confirmcontra = escape(request.form['confirmcontra'])
            sexo =escape(request.form['genero'])
            fecha = escape(request.form['fecha'])
            cedula = escape(request.form['Cedula'])
            roll = escape(request.form['rol'])
            if nombre =="" or apellido=="" or correo=="" or direccion=="" or cedula=="" or contraseña=="" or confirmcontra== "" or fecha=="" or sexo=="" or roll =="":
                flash("Hay campos vacios")
                return redirect("/usuarios")
            else:
                if contraseña == confirmcontra:
                    contranueva = contraseña
                    contrahash = generate_password_hash(contranueva)
                    try:
                        with sqlite3.connect('reto.db') as con:
                            cur = con.cursor()
                            cur.execute("update usuarios set nombre=?, apellido=?, direccion=?, correo=?, contraseña=?, genero=?, fecha_nacimiento=?, cedula=?, id_rol=? where id_usuarios =?", (nombre, apellido, direccion, correo, contrahash, sexo, fecha, cedula, roll,id))
                            con.commit()
                            flash('Usuario actualizado con exito')
                    except Error as er:
                        flash("Ocurrio un error")
                        print('SQLite error: %s' % (' '.join(er.args)))
                    return redirect('/usuarios')
                else:
                    flash('Contraseña incorrecta')
                    return redirect('/usuarios')
    else:
        return redirect("/")
    
@app.route("/eliminarusuario/<int:id>", methods=["POST","GET"])
def adminsusuarioseliminar(id):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT r.nombre, * FROM rol r join usuarios u on r.id_rol = u.id_rol where u.id_usuarios =?",[id])
                    usuarios = cur.fetchall()

                    cur.execute("SELECT r.nombre, * FROM rol r join usuarios u on r.id_rol = u.id_rol where u.id_usuarios =?",[id])
                    unusuarios = cur.fetchone()
                    print(unusuarios)

                    cur.execute("select id_rol, nombre from rol" )
                    rol = cur.fetchall()
                    
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('usuarioseliminar.html',usuarios=usuarios, rol=rol, unusuarios=unusuarios)


        if request.method == "POST":
            try:
                with sqlite3.connect('reto.db') as con:
                    cur = con.cursor()
                    cur.execute("delete from usuarios where id_usuarios =?", [ id])
                    con.commit()
                    flash('Usuario eliminado con exito')
            except Error as er:
                flash("Ocurrio un error")
                print('SQLite error: %s' % (' '.join(er.args)))
            return redirect('/usuarios')
    else:
        return redirect("/")
    



@app.route('/logout')
def logout():
    if "usuario" in session:
        session.clear()

    return redirect("/")


@app.route("/pilotos", methods=["GET", "POST"])
def adminspilotos():
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT id_usuarios, nombre,apellido, direccion, correo, genero, fecha_nacimiento, cedula FROM usuarios where id_rol=3")
                    usuarios = cur.fetchall()
                    print(usuarios)

                    
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('pilotos.html',usuarios=usuarios)
        

    else:
        return redirect("/")
    
@app.route('/vuelosasignados/<int:id>', methods=["GET", "POST"])
def vuelosasig(id):
    
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect('reto.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur = cur.execute("Select v.ID, u.nombre, v.origen , v.destino, v.escala from vuelos v join usuarios u  on u.id_usuarios= v.id_usuarios where v.id_usuarios =?", [id])
                    asig = cur.fetchall()

                    
            except Error  as er:
                print('SQLite error: %s' % (' '.join(er.args)))
            return render_template('vuelosasigadospilotos.html', asig =asig)
        
    else:
        return redirect("/")
    

@app.route('/gestioncomentarios')
def gestionComentarios():
    if "usuario" in session:

        return render_template('gestionComentarios.html')

    else:
        return redirect("/")
    

@app.route('/confirmarreserva')
def confirmarReserva():
    if "usuario" in session:

        return render_template('confirmarReserva.html')

    else:
        return redirect("/")
    
    
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)