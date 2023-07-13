import sqlite3

class DbConnect:

    def __init__(self) -> None:
        self.db = sqlite3.connect('./ratings.db',)
        cursor = self.db.cursor()
        self.ex = cursor.execute
        self.fa = cursor.fetchall
        self.cl = cursor.close
        self.ex('pragma foreign_keys = on')
        self.ex('pragma case_sensitive_like=off')
        self.views()
    
    def views(self):
        self.ex('drop view if exists search')
        self.ex('''create view search as select d.codigo as disciplina_codigo,
                   d.nome as disciplina_nome,pt.FK_turma_numero as turma_numero,
                   p.nom_prim_nome || ' ' || p.nom_sobrenome as professor_nome,
                   pt.FK_turma_semestre as turma_semestre,
                   p.matricula as matricula from disciplina d inner join
                   professor_turma pt on d.codigo = pt.FK_disciplina_codigo
                   inner join professor p
                   on pt.fk_professor_matricula = p.matricula''')

    def close(self) -> None:
        self.db.commit()
        self.cl()

    def getSemester(self):
        self.ex('''select semestre from turma group by semestre
                   order by semestre desc''')
        return [x[0] for x in self.fa()]

    def avg(self,order: str,type: str,semester: str) -> list[tuple[str,str]]:
        if type == 'Turmas':
            self.ex(f'''select avg(a.nota) as media,d.codigo,d.nome,
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
            self.ex(f'''select avg(a.nota) as media,p.nom_prim_nome,
                        p.nom_sobrenome from professor p inner join avaliacao a
                        on p.matricula = a.FK_professor_matricula
                        and a.FK_turma_semestre = "{semester}"
                        group by p.matricula
                        order by media {order} limit 100;''')
        return self.fa()[::-1]

    def hasAdmins(self):
        self.ex('''select count(*) from usuario where administrador = 1''')
        return self.fa()[0][0]

    def signin(self,username,password):
        self.ex(f'''select * from usuario where (matricula = "{username}"
                    or email = "{username}") and senha = "{password}"''')
        return self.fa()

    def search(self,s,semester):
        self.ex(f'''select * from search
                where (disciplina_nome like "%{s}%"
                      or disciplina_codigo like "%{s}%"
                      or professor_nome like "%{s}%")
                      and turma_semestre = {semester}
                order by min(
                coalesce(nullif(instr(lower(disciplina_nome),"{s}"),0),9999),
                coalesce(nullif(instr(lower(disciplina_codigo),"{s}"),0),9999),
                coalesce(nullif(instr(lower(professor_nome),"{s}"),0),9999))
                limit 50;''')
        return self.fa()[::-1] if s else None
    
    def viewOwn(self,matricula,semester):
        self.ex(f'''select a.FK_disciplina_codigo,d.nome,a.FK_turma_numero,
                    p.nom_prim_nome || ' ' || p.nom_sobrenome,
                    a.FK_turma_semestre,p.matricula,a.nota,
                    a.texto from avaliacao a inner join professor p 
                    on p.matricula = a.FK_professor_matricula
                    inner join disciplina d
                    on d.codigo = a.FK_disciplina_codigo
                    where a.FK_usuario_matricula = "{matricula}"
                    and a.FK_turma_semestre = {semester}''')
        return self.fa()[::-1]

    def rated(self,matricula,info):
        self.ex(f'''select exists (select * from avaliacao a 
                    where a.FK_usuario_matricula = "{matricula}"
                    and FK_professor_matricula = "{info[5]}"
                    and FK_disciplina_codigo = "{info[0]}"
                    and FK_turma_numero = "{info[2]}"
                    and FK_turma_semestre = "{info[4]}")''')
        return bool(self.fa()[0][0])
    
    def updateRating(self,matricula,info,grade,text):
        self.ex(f'''update avaliacao set texto = ?,nota = ?
                    where FK_usuario_matricula = ?
                    and FK_professor_matricula = ? and FK_disciplina_codigo = ?
                    and FK_turma_numero = ? and FK_turma_semestre = ?''',
                    [text,grade,matricula,info[5],info[0],info[2],
                        info[4]])
    
    def recordRating(self,matricula,info,grade,text):
        self.ex(f'''insert into avaliacao(texto,nota,
                    FK_usuario_matricula,FK_professor_matricula,
                    FK_disciplina_codigo,FK_turma_numero,
                    FK_turma_semestre) values (?,?,?,?,?,?,?)''',
                    [text,grade,matricula,info[5],info[0],info[2],
                    info[4]])

    def getAval(self,info):
        self.ex('''select a.nota, a.texto, u.nom_prim_nome, u.matricula
                    from avaliacao a inner join usuario u
                    on a.FK_usuario_matricula = u.matricula
                    where a.FK_professor_matricula = ?
                    and a.FK_disciplina_codigo = ? and a.FK_turma_numero = ?
                    and a.FK_turma_semestre = ? order by a.nota desc''',
                    [info[5],info[0],info[2],info[4]])
        return self.fa()[::-1]

    def report(self,matricula,info,reportedMatricula):
        self.ex(f'''insert into denuncia (FK_usuario_matricula,
                    FK_usuario_denunciado_matricula,FK_professor_matricula,
                    FK_disciplina_codigo,FK_turma_numero,FK_turma_semestre)
                    values (?,?,?,?,?,?)''',[matricula,reportedMatricula,
                                             info[5],info[0],info[2],info[4]])

    def reported(self,matricula,info,reportedMatricula):
        self.ex(f'''select exists (select * from denuncia d 
                    where FK_usuario_matricula = "{matricula}"
                    and FK_usuario_denunciado_matricula = "{reportedMatricula}"
                    and FK_professor_matricula = "{info[5]}"
                    and FK_disciplina_codigo = "{info[0]}"
                    and FK_turma_numero = "{info[2]}"
                    and FK_turma_semestre = "{info[4]}")''')
        return bool(self.fa()[0][0])

    def getReports(self):
        self.ex('''select u.nom_prim_nome || " " || u.nom_sobrenome,s.*,
                   a.nota,a.texto,u.matricula
                   from denuncia d inner join avaliacao a on
                   d.FK_professor_matricula = a.FK_professor_matricula
                   and d.FK_disciplina_codigo = a.FK_disciplina_codigo
                   and d.FK_turma_numero = a.FK_turma_numero
                   and d.FK_turma_semestre = a.FK_turma_semestre
                   and d.FK_usuario_denunciado_matricula = 
                       a.FK_usuario_matricula
                   inner join search s on
                   d.FK_professor_matricula = s.matricula
                   and d.FK_disciplina_codigo = s.disciplina_codigo
                   and d.FK_turma_numero = s.turma_numero
                   and d.FK_turma_semestre = s.turma_semestre
                   inner join usuario u
                   on u.matricula = d.FK_usuario_denunciado_matricula
                   group by u.matricula,s.matricula,s.disciplina_codigo,
                   s.turma_numero,s.turma_semestre
                   order by d.FK_turma_semestre''')
        return self.fa()[::-1]

    def deleteReport(self,*args):
        self.ex('''delete from denuncia
                   where FK_usuario_denunciado_matricula = ?
                   and FK_professor_matricula = ?
                   and FK_disciplina_codigo = ?
                   and FK_turma_numero = ?
                   and FK_turma_semestre = ?''',args)

    def deleteUser(self,matricula):
        self.ex(f'''delete from denuncia
                    where FK_usuario_denunciado_matricula = "{matricula}"
                    or FK_usuario_matricula = "{matricula}"''')
        self.ex(f'''delete from avaliacao 
                    where FK_usuario_matricula = "{matricula}"''')
        self.ex(f'''delete from usuario where matricula = "{matricula}"''')