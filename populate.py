import csv
import sqlite3
import validate

from random import choice

db = sqlite3.connect('./ratings.db',)
cursor = db.cursor()
cursor.execute('pragma foreign_keys = on')

for semester in ['2022-1','2022-2','2023-1']:
    folder: str = './populate_data/'
    with open(f'{folder}departamentos_{semester}.csv',encoding='utf8') as file:
        for row in csv.reader(file):
            if row[0] == 'cod':
                continue
            codigo: str = row[0].rjust(4,'0')
            nome: str = row[1].removesuffix('- BRASÍLIA')
            if not validate.depNome(nome) or not validate.depCodigo(codigo):
                continue
            try:
                cursor.execute('''insert into departamento (codigo,nome)
                                  values (?,?)''',[codigo,nome])
            except sqlite3.IntegrityError as e:
                for arg in e.args:
                    if not ('UNIQUE' in arg or 'FOREIGN KEY' in arg):
                        raise e
    with open(f'{folder}disciplinas_{semester}.csv',encoding='utf8') as file:
        for row in csv.reader(file):
            if row[0] == 'cod':
                continue
            codigo: str = row[0].replace('/','').replace('-','')
            nome: str = row[1]
            codigoDepartamento: str = row[2].rjust(4,'0')
            if (not validate.disCodigo(codigo) or not validate.disNome(nome)
                or not validate.depCodigo(codigoDepartamento)):
                continue
            try:
                cursor.execute('''insert into disciplina (codigo,nome,
                                  FK_departamento_codigo) values (?,?,?)''',
                                  [codigo,nome,codigoDepartamento])
            except sqlite3.IntegrityError as e:
                for arg in e.args:
                    if not ('UNIQUE' in arg or 'FOREIGN KEY' in arg):
                        raise e
db.commit()
cursor.close()