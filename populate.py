import csv
import sqlite3
import validate

from random import choice

db = sqlite3.connect('./ratings.db',)
cursor = db.cursor()
cursor.execute('pragma foreign_keys = on')

matGen = lambda : ''.join([str(choice(range(10))) for _ in range(9)])
proMat: dict[tuple[str,str],str] = {}
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
    with open(f'{folder}turmas_{semester}.csv',encoding='utf8') as file:
        for row in csv.reader(file):
            if row[0] == 'turma':
                continue
            matricula: str = matGen()
            numero: str = row[0]
            semestre: str = row[1]
            hasName: bool = bool(row[2].split('(')[0])
            if hasName:
                professor_nome: str = row[2].split()[0]
                professor_sobrenome: str = row[2].split(maxsplit=1)[1]
                professor_sobrenome = professor_sobrenome.split('(')[0].strip()
                key: tuple[str, str] = (professor_nome,professor_sobrenome)
            else:
                professor_nome,professor_sobrenome,key = '','',('','')
            codigoDisciplina: str = row[7].replace('/','').replace('-','')
            codigoDepartamento: str = row[8].rjust(4,'0')
            insProf: bool  = (validate.proMatricula(matricula)
                              and validate.primNome(professor_nome)
                              and validate.sobrenome(professor_sobrenome)
                              and validate.depCodigo(codigoDepartamento))
            try:
                if insProf and not (key in proMat):
                    proMat[key] = matricula
                    cursor.execute('''insert into professor (matricula,
                                      nom_prim_nome,nom_sobrenome)
                                      values (?,?,?)''',
                                      [matricula,professor_nome,
                                       professor_sobrenome])
                    cursor.execute('''insert into departamento_professor
                                      (FK_professor_matricula,
                                      FK_departamento_codigo) 
                                      values (?,?)''',
                                      [matricula,codigoDepartamento])
                elif insProf:
                    matricula = proMat[key]
                    cursor.execute('''insert into departamento_professor
                                      (FK_professor_matricula,
                                      FK_departamento_codigo) 
                                      values (?,?)''',
                                      [matricula,codigoDepartamento])
            except sqlite3.IntegrityError as e:
                for arg in e.args:
                    if not ('UNIQUE' in arg or 'FOREIGN KEY' in arg):
                        raise e
            if (not validate.turNumero(numero)
                or not validate.turSemestre(semestre)):
                continue
            try:
                cursor.execute('''insert into turma (FK_disciplina_codigo,
                                  numero,semestre)
                                  values (?,?,?)''',
                                  [codigoDisciplina,numero,semestre])
                if insProf:
                    cursor.execute('''insert into professor_turma (
                                      FK_professor_matricula,
                                      FK_disciplina_codigo,
                                      FK_turma_numero,FK_turma_semestre)
                                      values (?,?,?,?)''',
                                      [matricula,codigoDisciplina,numero,
                                       semestre,])
            except sqlite3.IntegrityError as e:
                for arg in e.args:
                    if not ('UNIQUE' in arg or 'FOREIGN KEY' in arg):
                        raise e
db.commit()
cursor.close()