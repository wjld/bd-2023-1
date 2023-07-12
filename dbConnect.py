import sqlite3

class DbConnect:

    def __init__(self) -> None:
        self.db = sqlite3.connect('./ratings.db',)
        self.cursor = self.db.cursor()
        self.cursor.execute('pragma foreign_keys = on')

    def close(self) -> None:
        self.db.commit()
        self.cursor.close()

    def getSemester(self):
        self.cursor.execute('''select semestre from turma 
                               group by semestre order by semestre desc''')
        return [x[0] for x in self.cursor.fetchall()]

    def avg(self,order: str,type: str,semester: str) -> list[tuple[str,str]]:
        if type == 'Turmas':
            self.cursor.execute(
                f'''select avg(a.nota) as media,d.codigo,d.nome,
                           pt.FK_turma_numero
                    from avaliacao a inner join professor_turma pt
                    on (pt.FK_professor_matricula = a.FK_professor_matricula
                    and pt.FK_disciplina_codigo = a.FK_disciplina_codigo
                    and pt.FK_turma_numero = a.FK_turma_numero
                    and "{semester}" = a.FK_turma_semestre)
                    inner join disciplina d
                    on (d.codigo = pt.FK_disciplina_codigo)
                    group by pt.FK_professor_matricula,pt.FK_disciplina_codigo,
                    pt.FK_turma_numero,pt.FK_turma_semestre,d.nome
                    order by media {order} limit 100;''')
        elif type == 'Professores':
            self.cursor.execute(f'''select avg(a.nota) as media,
                                    p.nom_prim_nome,p.nom_sobrenome
                                    from professor p inner join avaliacao a
                                    on p.matricula = a.FK_professor_matricula
                                    and a.FK_turma_semestre = "{semester}"
                                    group by p.matricula
                                    order by media {order} limit 100;''')
        return self.cursor.fetchall()[::-1]

    def hasAdmins(self):
        self.cursor.execute('''select count(*) from usuario
                               where administrador = 1''')
        return self.cursor.fetchall()[0][0]

    def signin(self,username,password):
        self.cursor.execute(f'''select * from usuario
                                where (matricula = "{username}"
                                or email = "{username}")
                                and senha = "{password}"''')
        return self.cursor.fetchall()