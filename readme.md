# Sistema de Avaliação de Professores e Disciplinas

## Visão Geral
Este projeto é um sistema que permite avaliar professores e disciplinas, através de suas turmas associadas. O sistema oferece funcionalidades como cadastro de usuários, login, avaliação de professores e disciplinas, visualização de rankings, gerenciamento de avaliações e denúncias, configuração de administradores e muito mais.

## Estrutura do Projeto
O projeto está estruturado da seguinte forma:

- `init.py`: Realiza a definição do banco de dados baseada esquema definido.
- `populate.py`: Inicializa diversas instâncias de entidade, para uma melhor experiência.
- `window.py`: Define a classe `Window`, que representa a janela principal do aplicativo e gerencia a interface do usuário.
- `dbConnect.py`: Fornece a classe `DbConnect`, que lida com a conexão e consultas ao banco de dados.
- `titlescreen.py`: Define a classe `Titlescreen`, que representa a tela inicial do aplicativo.
- `ranking.py`: Implementa a classe `Ranking`, que exibe o ranking de professores e turmas.
- `signin.py`: Implementa a classe `Signin`, que lida com a funcionalidade de login.
- `signup.py`: Implementa a classe `Signup`, que lida com a funcionalidade de cadastro.
- `menu.py`: Implementa a classe `Menu`, que representa o menu do aplicativo e oferece opções personalizadas com base no tipo de usuário.
- `rate.py`: Implementa a classe `RateScreen`, que lida com a funcionalidade de avaliação de professores e turmas.
- `reports.py`: Implementa a classe `Reports`, que gerencia as denúncias.
- `setAdmins.py`: Implementa a classe `SetAdmins`, que lida com a configuração de administradores.
- `validate.py`: Contém funções para validação de dados.
- `dialog.py`: Implementa a classe `Dialog`, que cria pop-ups na interface do usuário.

O projeto é baseado na permanência do arquivo de banco de dados SQLite `ratings.db`.

## Funcionalidades

O sistema possui as seguintes funcionalidades:

- Tela inicial: exibe opções de cadastro, login, ranking geral e sair do sistema.
- Tela de cadastro: permite que os usuários se cadastrem no sistema, fornecendo seus dados.
- Tela de login: os usuários podem fazer login no sistema usando suas credenciais.
- Validação de dados: o sistema realiza validação de dados para garantir que as informações fornecidas pelos usuários estejam corretas.
- Tela de menu: exibe opções personalizadas com base no tipo de usuário (comum ou administrador).
- Tela de avaliação: permite que os usuários avaliem professores e disciplinas, atribuindo notas e fornecendo comentários.
- Tela de visualização de avaliações: exibe as avaliações feitas pelos usuários, incluindo suas próprias avaliações e avaliações gerais.
- Tela de ranking geral: mostra o ranking geral dos professores e turmas com base nas avaliações dos usuários, separadas por semestre.
- Tela de denúncias: permite que os administradores analisem e gerenciem as denúncias feitas pelos usuários.
- Tela de configuração de administradores: permite que administradores configurem os administradores no sistema.

## Pré-requisitos
Para executar o projeto, você precisa ter o seguinte instalado:

- Python 3.9+
- Bibliotecas tkinter, sqlite3 e hashlib, nativas em Python

## Como executar o sistema

1. Instale o Python em seu computador, se ainda não estiver instalado.
2. Clone o repositório do projeto.
3. Abra um terminal ou prompt de comando, no diretório onde os arquivos do sistema estão localizados.
5. Para iniciar o sistema, execute

```bash
python main.py
```

## Uso

Ao iniciar o aplicativo, a tela inicial será exibida. A partir da tela inicial, os usuários podem navegar para diferentes seções do aplicativo, como fazer login, visualizar o ranking geral e muito mais.

### Tela Inicial

A tela inicial exibe o nome do aplicativo e oferece as seguintes opções:

- **Cadastro:** permite que os usuários se cadastrem no sistema fornecendo seus dados pessoais.
- **Login:** permite que os usuários façam login no sistema usando suas credenciais. O botão de login só é habilitado se houver administradores registrados no sistema; se não houver nenhum, o próximo usuário a se cadastrar será um administrador.
- **Ranking Geral:** exibe o ranking geral dos professores e turmas com base nas avaliações dos usuários.
- **Sair:** fecha o aplicativo.

### Tela de Cadastro

A tela de cadastro permite que os usuários se cadastrem no sistema fornecendo seus dados pessoais, como matrícula, senha, nome, sobrenome, email e curso. Os campos de entrada são validados de acordo com as regras especificadas para cada campo. Após o cadastro, os usuários são redirecionados para a tela de menu, onde podem acessar as funcionalidades do sistema.

### Tela de Login

A tela de login permite que os usuários façam login no aplicativo usando suas credenciais (matrícula ou email e senha). Os campos de entrada são validados e as credenciais são verificadas no banco de dados, e os usuários são redirecionados para a tela de menu.

### Tela de Menu

A tela de menu exibe opções personalizadas com base no tipo de usuário (comum ou administrador). Os usuários comuns podem acessar funcionalidades como avaliar professores, visualizar avaliações e visualizar o ranking geral. Os administradores têm acesso adicional a funcionalidades de gerenciamento de denúncias, configuração de administradores e mais.

### Tela de Avaliação

A tela de avaliação permite que os usuários avaliem professores e disciplinas, atribuindo notas e fornecendo comentários. Os campos de entrada são validados e as avaliações são registradas no banco de dados.

### Tela de Visualização de Avaliações

A tela de visualização de avaliações exibe as avaliações feitas pelos usuários, incluindo suas próprias avaliações e avaliações gerais. Os usuários podem visualizar as avaliações de turmas específicas.

### Tela de Ranking Geral

A tela de ranking geral mostra o ranking geral dos professores e turmas com base nas avaliações dos usuários. Os rankings são atualizados com base nas avaliações registradas no banco de dados.

### Tela de Denúncias

A tela de denúncias permite que os administradores analisem e gerenciem as denúncias feitas pelos usuários. Os administradores podem ver as informações da denúncia, como o usuário denunciado, a disciplina e o professor associados, e o texto da avaliação denunciada. Os administradores podem tomar ações apropriadas com base nas denúncias recebidas, como ignorar ou excluir a conta do usuário denunciado.

### Tela de Configuração de Administradores

A tela de configuração de administradores permite que os administradores adicionem e removam outros administradores do sistema.

## Contribuições

Contribuições para o projeto são bem-vindas! Se você tiver alguma sugestão, relatório de bug ou solicitação de recurso, abra uma issue ou envie um pull request no repositório do projeto.

## Licença

O projeto é lançado sob a Licença MIT.