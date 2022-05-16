from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QAbstractTableModel, QStringListModel, Qt 
from main9 import Ui_Form
from PyQt5 import QtCore
import sys
import pyodbc
import pandas as pd
import os
myDir = os.getcwd()
sys.path.append(myDir)

def ConectarSql():
    direccion_servidor = 'HP-SST-P3\SQLEXPRESS'
    nombre_bd = 'prueba'
    nombre_usuario = 'sa'
    password = 'A123456.'
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=' +
                                  direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
        print('Conexion Exitosa')
        
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)
    return conexion

def extraertexto(cadena):
    return cadena[0]

def getDatos(numeracion):   
    conn = ConectarSql()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM  Formularios WHERE ID=?",numeracion)
    id_1 = cursor.fetchall()
    id_1 = extraertexto(id_1)
    cursor.execute("SELECT fecha FROM  Formularios WHERE ID=?",numeracion)
    fecha = cursor.fetchall()
    fecha = extraertexto(fecha)
    cursor.execute("SELECT numero FROM  Formularios WHERE ID = ?",numeracion)
    numero= cursor.fetchall()
    numero = extraertexto(numero)
    cursor.execute("SELECT proyecto FROM  Formularios WHERE ID = ?",numeracion)
    proyecto = cursor.fetchall()
    proyecto = extraertexto(proyecto)
    cursor.execute("SELECT codigolabor FROM  Formularios WHERE ID=?",numeracion)
    codigolabor = cursor.fetchall()
    codigolabor = extraertexto(codigolabor)
    cursor.execute("SELECT codigosupervisor FROM  Formularios WHERE ID=?",numeracion)
    codigosupervisor = cursor.fetchall()
    codigosupervisor = extraertexto(codigosupervisor)
    cursor.execute("SELECT cecolabor FROM  Formularios WHERE ID=?",numeracion)
    cecolabor = cursor.fetchall()
    cecolabor = extraertexto(cecolabor)
    cursor.execute("SELECT cecosupervisor FROM  Formularios WHERE ID=?",numeracion)
    cecosupervisor = cursor.fetchall()
    cecosupervisor = extraertexto(cecosupervisor)
    cursor.execute("SELECT suphoras FROM  Formularios WHERE ID=?",numeracion)
    suphoras = cursor.fetchall()
    suphoras = extraertexto(suphoras)
    lista =[id_1[0], fecha[0], numero[0], proyecto[0], codigolabor[0], codigosupervisor[0], cecolabor[0],cecosupervisor[0], suphoras[0]]
    return lista

def getDataTable(numeracion):
    conn = ConectarSql()
    cursor= conn.cursor()
    cursor.execute('''select	FD.Dni,D.nombrecompleto,horas, turno from Formulariosdetalle 
            as FD left join DNI AS D on FD.dni = D.dni where FD.id=?''', numeracion)
    result = cursor.fetchall()
    return result

def getFormu(dni):
    conn = ConectarSql()
    cursor= conn.cursor()
    cursor.execute('SELECT * FROM formulariosdetalle WHERE DNI = ?',dni)
    result = cursor.fetchone()
    if result:
        return result

def getFormus():
    conn = ConectarSql()
    cursor= conn.cursor()
    cursor.execute('SELECT * FROM formulariosdetalle ')
    result = cursor.fetchall()
    return result

#def updateFormularios (numeracion):
#    conn = ConectarSql()
#    cursor = conn.cursor()
#    cursor.execute('UPDATE produc')
#    conn.commit()



def deletFormulario(dni):
    conn = ConectarSql()
    cursor = conn.cursor()
    cursor.execute('delete  from Formulariosdetalle where dni = ? ',dni)
    conn.commit()



def getLista():
    conn = ConectarSql()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM  Formularios") 
    lista =[]
    for row in cursor:
        for elem in row:
            row_to_list = str(elem) 
            lista.append(row_to_list)
    return lista




class FloatDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__()

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(QDoubleValidator())
        return editor

class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setStyleSheet('font-size: 12px;')
        # set table dimension
        nRows, nColumns = self.df.shape
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        self.setHorizontalHeaderLabels(('DNI', 'Nombre Completo', 'Horas', 'Turno'))
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setItemDelegateForColumn(1, FloatDelegate())
        # data insertion
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))
        #   self.cellChanged[int, int].connect(self.updateDF)   

    def updateDF(self, row, column):
        anterior =self.df.iloc[row, column] 
        text = self.item(row, column).text()
        self.df.iloc[row, column] = text
        nuevo = self.df.iloc[row, column] = text
        print('Identificador')
        print (row)
        print (column)
        print (self.item(row, column).text())
        print(anterior)
        conn = ConectarSql()
        cursor = conn.cursor()
        cursor.execute("UPDATE FORMULARIOSDETALLE SET DNI=?  WHERE DNI=?", nuevo, anterior)
        conn.commit()




class TablaView(QDialog):

    conn = ConectarSql()
    id = 20
    frase = ("SELECT FD.DNI, D.NOMBRECOMPLETO,FD.HORAS, FD.TURNO FROM FORMULARIOSDETALLE AS FD LEFT JOIN DNI AS D ON FD.DNI = D.DNI where FD.ID="+str(id))
    consulta = pd.read_sql_query(frase, conn)
    df = consulta.replace({None: 'No se encontro'}) 
    
    def __init__(self):
        super(TablaView, self).__init__()
        self.tabla = Ui_Form()
        self.tabla.setupUi(self)      
        
        slm =   QStringListModel()
        self.tabla.qList=getLista()
        slm.setStringList(self.tabla.qList)
        listacombobox= getLista()
        self.tabla.comboBox.addItems(listacombobox)
        self.tabla.comboBox.activated[str].connect(self.clicked) 
        self.tabla.pushButton.clicked.connect(self.clickprev)
        self.tabla.pushButton_2.clicked.connect(self.clicknext)
        
        self.tabla.pushButton_3.setText( "Eliminar")
        self.d = self.tabla.pushButton_3.clicked.connect(lambda:self.deleteform())
        self.tabla.tableWidget =TableWidget(TablaView.df)
        self.tabla.verticalLayout.addWidget(self.tabla.tableWidget)
        
    
        
    
    def prueba(self, dato):
        print(dato.row(), dato.column())

    def procedlabel(self, cadsql):
        self.tabla.label_4.setText(cadsql[2])
        self.tabla.label_5.setText(str(cadsql[1]))
        self.tabla.label_8.setText(cadsql[3])
        self.tabla.label_10.setText(cadsql[6])
        self.tabla.label_12.setText(cadsql[4])
        self.tabla.label_17.setText(cadsql[7])
        self.tabla.label_16.setText(cadsql[5])
        self.tabla.label.setText(str(cadsql[0]))
        self.tabla.label_22.setText(cadsql[8])
    
    def clicked(self,qModelIndex):
        variable =self.tabla.comboBox.currentText()
        cadsql = getDatos(variable)
        self.procedlabel(cadsql)
        #self.tabla.tableWidget.clear()
        #Intentar crear el listar al seleccionar una lista
        vista = getDataTable(variable)
        table = self.tabla.tableWidget
        table.setRowCount(0)
        for row_number, row_data in enumerate(vista):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        
    
    def clickprev(self):
        prev = int(self.tabla.label.text()) -1
        cadsql = getDatos(prev)
        
        self.procedlabel(cadsql)
        vista = getDataTable(prev)
        table = self.tabla.tableWidget
        table.setRowCount(0)
        for row_number, row_data in enumerate(vista):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        
    
    def clicknext(self):
        next = int(self.tabla.label.text()) +1
        cadsql = getDatos(next)
        self.procedlabel(cadsql)
        vista = getDataTable(next)
        table = self.tabla.tableWidget
        table.setRowCount(0)
        for row_number, row_data in enumerate(vista):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        


    def listFormus(self):
        table = self.tabla.tableWidget
        formu = getDataTable(int(self.tabla.label.text()))
        table.setRowCount(0)
        for row_number, row_data in enumerate(formu):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))


    def deleteform (self):
        table = self.tabla.tableWidget
        if table.currentItem() != None:
            dni = table.currentItem().text()
            formu = getFormu(dni)
            if formu:
                deletFormulario(dni)
        self.listFormus()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_aplicacion = TablaView()
    mi_aplicacion.show()
    sys.exit(app.exec_())

