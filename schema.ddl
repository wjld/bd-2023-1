drop table if exists avaliacao;
drop table if exists denuncia;
drop table if exists departamento;
drop table if exists departamento_professor;
drop table if exists disciplina;
drop table if exists professor;
drop table if exists professor_turma;
drop table if exists turma;
drop table if exists usuario;

create table avaliacao (
     texto varchar(200),
     nota tinyint(1) not null,
     FK_usuario_matricula char(9) not null,
     FK_professor_matricula varchar(9) not null,
     FK_disciplina_codigo char(7) not null,
     FK_turma_numero char(5) not null,
     FK_turma_semestre char(6) not null,
     constraint ID_avaliacao_ID primary key (FK_usuario_matricula, FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre),
     constraint REF_avali_usuar_FK foreign key (FK_usuario_matricula) references usuario,
     constraint REF_avali_profe_FK foreign key (FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre) references professor_turma
     constraint MAX_avaliacao_nota check (nota >= 0 and nota <= 5));

create table denuncia (
     justificativa varchar(100),
     FK_usuario_matricula char(9) not null,
     FK_usuario_denunciado_matricula char(9) not null,
     FK_professor_matricula varchar(9) not null,
     FK_disciplina_codigo char(7) not null,
     FK_turma_numero char(5) not null,
     FK_turma_semestre char(6) not null,
     constraint ID_denuncia_ID primary key (FK_usuario_denunciado_matricula, FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre, FK_usuario_matricula),
     constraint REF_denun_avali_FK foreign key (FK_usuario_denunciado_matricula, FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre) references avaliacao,
     constraint REF_denun_usuar foreign key (FK_usuario_matricula) references usuario);

create table departamento (
     codigo char(4) not null,
     nome varchar(150) not null,
     constraint ID_departamento_ID primary key (codigo));

create table departamento_professor (
     FK_departamento_codigo char(4) not null,
     FK_professor_matricula char(9) not null,
     constraint ID_departamento_professor_ID primary key (FK_departamento_codigo, FK_professor_matricula),
     constraint REF_depar_depar_FK foreign key (FK_departamento_codigo) references departamento,
     constraint REF_depar_profe_FK foreign key (FK_professor_matricula) references professor);

create table disciplina (
     codigo varchar(13) not null,
     nome char(150) not null,
     FK_departamento_codigo char(4) not null,
     constraint ID_disciplina_ID primary key (codigo),
     constraint REF_disci_depar_FK foreign key (FK_departamento_codigo) references departamento);

create table professor (
     matricula char(9) not null,
     nom_prim_nome varchar(15) not null,
     nom_sobrenome varchar(60) not null,
     constraint ID_professor_ID primary key (matricula));

create table professor_turma (
     FK_professor_matricula varchar(9) not null,
     FK_disciplina_codigo char(7) not null,
     FK_turma_numero char(5) not null,
     FK_turma_semestre char(6) not null,
     constraint ID_professor_turma_ID primary key (FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre),
     constraint REF_profe_turma foreign key (FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre) references turma,
     constraint REF_profe_profe_FK foreign key (FK_professor_matricula) references professor);

create table turma (
     FK_disciplina_codigo char(7) not null,
     numero varchar(5) not null,
     semestre char(6) not null,
     constraint ID_turma_ID primary key (FK_disciplina_codigo, numero, semestre),
     constraint REF_turma_disci foreign key (FK_disciplina_codigo) references disciplina);

create table usuario (
     matricula char(9) not null,
     senha char(64) not null,
     nom_prim_nome varchar(15) not null,
     nom_sobrenome varchar(60) not null,
     email char(100) not null,
     curso char(50) not null,
     administrador boolean not null,
     constraint ID_usuario_ID primary key (matricula),
     constraint MIN_usuario_senha check (length(senha) = 64));

create unique index ID_avaliacao_IND
     on avaliacao (FK_usuario_matricula, FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre);

create index REF_avali_profe_IND
     on avaliacao (FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre);

create unique index ID_denuncia_IND
     on denuncia (FK_usuario_denunciado_matricula, FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre, FK_usuario_matricula);

create index REF_denun_usuar_IND
     on denuncia (FK_usuario_matricula);

create unique index ID_departamento_IND
     on departamento (codigo);

create unique index ID_departamento_professor_IND
     on departamento_professor (FK_departamento_codigo, FK_professor_matricula);

create index REF_depar_profe_IND
     on departamento_professor (FK_professor_matricula);

create unique index ID_disciplina_IND
     on disciplina (codigo);

create index REF_disci_depar_IND
     on disciplina (FK_departamento_codigo);

create unique index ID_professor_IND
     on professor (matricula);

create unique index ID_professor_turma_IND
     on professor_turma (FK_professor_matricula, FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre);

create index REF_profe_turma_IND
     on professor_turma (FK_disciplina_codigo, FK_turma_numero, FK_turma_semestre);

create unique index ID_turma_IND
     on turma (FK_disciplina_codigo, numero, semestre);

create unique index ID_usuario_IND
     on usuario (matricula);