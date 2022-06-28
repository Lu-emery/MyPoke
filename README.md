![](../src/website/static/mypoke.png)
# MyPoké
> MyPoké é um sistema de gerenciamento de base de dados que gerencia treinadores pokémon e seus respectivos pokémons em um ambiente fechado de um campeonato ou grupo de jogos pokémon.



Parte do trabalho de um Treinador Pokémon, seja ele um competidor casual em um grupo novo ou um competidor profissional em um campeonato, é fazer as escolhas certas na montagem de sua equipe. Isso envolve vários fatores, dentre eles a prevalência de tipos específicos de pokémon entre as equipes registradas (que é relevante para vantagens e desvantagens de tipo) e de pokémons específicos (que é relevante para comparações de estratégias). 
A construção e disponibilização de uma base de dados de fácil acesso, portanto, facilitaria o trabalho dos organizadores dos grupos e/ou eventos, que devem registrar todos os pokémons e regras específicas do evento; dos treinadores, que devem se inscrever e inscrever seus pokémons no evento; e dos analistas, que fazem a análise estatística de prevalência de tipos de pokémons e de pokémons específicos.


![](../example.png)

## Instalação

Dependências
```
(necessário instalar)
Postgresql v14

(contidos no venv)
psycopg2
flask
flask-login
```

OS X & Linux:

```sh
cd src
. venv/bin/activate
python3 main.py

acessar o site a partir de http://127.0.0.1:5000
criar uma conta (caso a senha seja 3333 o usuário é administrador e tem acesso a todas as funcionalidades)
```

## Exemplo de uso

A base de dados é inicialmente populada por alguns treinadores e pokémons.

Pode-se, por exemplo, adicionar um novo treinador preenchendo o formulário correspondente em /trn/add
![](../example.png)

## Configuração para Desenvolvimento

Para desenvolvimento, é recomendado que as configurações de base de dados no arquivo /src/website/mypokeAPI.py sejam mudados.
Também recomenda-se que seja adicionada a opção `debug=True` na função `app.run()` no arquivo /src/main.py

## Histórico de lançamentos

* 1.0.0
    * Versão inicial funcional do sistema MyPoké

## Meta

Lucas Mendonça Emery Cade – 2017100210 – lucas.cade@edu.ufes.br
Thiago Damasceno da Silva – 2017100217 – thiago.silva@edu.ufes.br

Esse sistema foi desenvolvido para fins educacionais. Favor não copiar ou utilizar sem permissão.