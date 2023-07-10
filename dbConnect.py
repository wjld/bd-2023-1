import sqlite3

class DbConnect:

    def __init__(self) -> None:
        self.db = sqlite3.connect('./ratings.db',)
        self.cursor = self.db.cursor()
        self.cursor.execute('pragma foreign_keys = on')

    def close(self) -> None:
        self.db.commit()
        self.cursor.close()

    def avg(self, order: str, type: str) -> list[tuple[str, str]]:
        if type == 'Disciplinas':
            self.cursor.execute(f'''select avg(a.nota) as media, d.nome
                                    from disciplina d inner join avaliacao a
                                    on d.codigo = a.FK_disciplina_codigo
                                    group by d.codigo
                                    order by media {order} limit 100;''')
        elif type == 'Professores':
            self.cursor.execute(f'''select avg(a.nota) as media,
                                    p.nom_prim_nome, p.nom_sobrenome
                                    from professor p inner join avaliacao a
                                    on p.matricula = a.FK_professor_matricula
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