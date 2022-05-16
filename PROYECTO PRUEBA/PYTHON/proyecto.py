# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:41:51 2021

@author:Anthony Araujo Fernandez
"""
import os
import pandas as pd
import boto3
import sys
import pyodbc
from pprint import pprint

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

def get_kv_map(file_name):

    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)

    # process using image bytes
    client = boto3.client('textract')
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['FORMS'])

    # Get the text blocks
    blocks=response['Blocks']    

    # get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block
    return key_map, value_map, block_map

def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key] = val
    return kvs

def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '    
    return text

def lista_kvs(kvs):
    lista=[]
    for key, value in kvs.items():
          print (key, value)
          lista.append(key.strip())
          lista.append(value.strip())
    return lista


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    # get the text value
                    rows[row_index][col_index] = get_textT(cell, blocks_map)
    return rows

def get_textT(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text


def get_table_csv_results(file_name):

    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)

    # process using image bytes
    # get the results
    client = boto3.client('textract')

    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])

    # Get the text blocks
    blocks=response['Blocks']
    #pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index +1)
        csv += '\n\n'

    return csv

def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'
        
    csv += '\n\n\n'
    return csv



def corregircadena(cadena):
    cadena=cadena.replace(" ", "")
    cadena=cadena.replace("D", "0")
    cadena=cadena.replace("O", "0")
    cadena=cadena.replace("o", "0")
    cadena=cadena.replace("w", "4")
    return cadena



os.chdir(r'C:\Users\Usuario\Desktop\PROYECTO PRUEBA\IMG')
file_name='page0.jpg'

key_map, value_map, block_map = get_kv_map(file_name)
kvs = get_kv_relationship(key_map, value_map, block_map)
lista = lista_kvs(kvs)
fecha=lista[lista.index("FECHA:")+1]
numero=lista[lista.index("N°")+1]
proyecto=lista[lista.index("PROYECTO:")+1]
codigolabor=lista[lista.index("CÓDIGO DE LABOR:")+1]
ceco=lista[lista.index("CeCo:")+1]
codigosup=lista[lista.index("Código del Sup:")+1]
cecosup=lista[lista.index("CeCo del Sup:")+1]
fecha=corregircadena(fecha)
numero=corregircadena(numero)
proyecto=corregircadena(proyecto)
codigolabor=corregircadena(codigolabor)
ceco=corregircadena(ceco)
codigosup=corregircadena(codigosup)
cecosup=corregircadena(cecosup)
#falta variable supervisor centro de costo
print(fecha, numero, proyecto, codigolabor,ceco,codigosup, cecosup)

table_csv = get_table_csv_results(file_name)
os.chdir(r'C:\Users\Usuario\Desktop\PROYECTO PRUEBA\CSV')
output_file = 'output.csv'
with open(output_file, "wt") as fout:
    fout.write(table_csv)

df = pd.read_csv('output.csv', skiprows=2)
df = df.drop(df.columns[[0,2,3,4,5,6,9,10]], axis='columns')
#df = df.drop([39,40],axis=0)
df = df.dropna()
df.columns = ['DNI','TOTALHORAS','TURNO']
print(df.columns)
print(df['DNI'].dtype)  
df['DNI'] = df['DNI'].astype(int)
df['DNI'] = df['DNI'].astype(str)
df['DNI'] = df['DNI'].str.zfill(8)
 
print(df)
print(df['TOTALHORAS'].dtype)
df['TOTALHORAS'] = df['TOTALHORAS'].astype(str)
df['TOTALHORAS'] = df['TOTALHORAS'].str.replace("-", ".")



print(df)

conn=ConectarSql()
cursor=conn.cursor()
cursor.execute('SELECT * FROM Formulario')
for row in cursor:
    print(row)










