import pyodbc
import datetime

def ConectarSql():
    direccion_servidor = 'HP-SST-P3\SQLEXPRESS'
    nombre_bd = 'prueba'
    nombre_usuario = 'sa'
    password = 'A123456.'
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=' +
                                  direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
        print('Conexion Exitosa')
        # OK! conexión exitosa
    except Exception as e:
        # Atrapar error
        print("Ocurrió un error al conectar a SQL Server: ", e)
    return conexion

def extraertexto(cadena):
    return cadena[0]

def getDatos(numeracion): 
    conn = ConectarSql()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM  Formulario WHERE ID=?",numeracion)
    id_1 = cursor.fetchall()
    id_1 = extraertexto(id_1)
    cursor.execute("SELECT fecha FROM  Formulario WHERE ID=?",numeracion)
    fecha = cursor.fetchall()
    fecha = extraertexto(fecha)
    cursor.execute("SELECT numero FROM  Formulario WHERE ID = ?",numeracion)
    numeracion = cursor.fetchall()
    numeracion = extraertexto(numeracion)
    cursor.execute("SELECT proyecto FROM  Formulario WHERE ID=?",numeracion)
    proyecto = cursor.fetchall()
    proyecto = extraertexto(proyecto)
    cursor.execute("SELECT codigolabor FROM  Formulario WHERE ID=?",numeracion)
    codigolabor = cursor.fetchall()
    codigolabor = extraertexto(codigolabor)
    cursor.execute("SELECT codigosupervisor FROM  Formulario WHERE ID=?",numeracion)
    codigosupervisor = cursor.fetchall()
    codigosupervisor = extraertexto(codigosupervisor)
    cursor.execute("SELECT cecolabor FROM  Formulario WHERE ID=?",numeracion)
    cecolabor = cursor.fetchall()
    cecolabor = extraertexto(codigosupervisor)
    cursor.execute("SELECT cecosupervisor FROM  Formulario WHERE ID=?",numeracion)
    cecosupervisor = cursor.fetchall()
    cecosupervisor = extraertexto(cecosupervisor)
    lista =[id_1[0], fecha[0], numeracion[0], proyecto[0], codigolabor[0], codigosupervisor[0], cecolabor[0],cecosupervisor[0]]
    return lista




lista =getDatos(1)
print (lista[1])



