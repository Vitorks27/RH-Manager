Sistema de gerenciamento de recursos humanos desenvolvido em Python utilizando o framework Flet.

Sobre o projeto

O RH Manager é um aplicativo desktop desenvolvido como atividade acadêmica do curso de Análise e Desenvolvimento de Sistemas.

O sistema tem como objetivo facilitar o gerenciamento de funcionários e departamentos de uma organização, permitindo realizar operações de cadastro, consulta, atualização e exclusão de registros.

Funcionalidades

Funcionários

Cadastrar funcionários.

Consultar funcionários cadastrados.

Editar informações dos funcionários.

Excluir funcionários.

Pesquisar por nome ou CPF.

Filtrar por departamento e situação.

Alterar a situação do funcionário.

Departamentos

Cadastrar departamentos.

Consultar departamentos cadastrados.

Editar departamentos.

Excluir departamentos.

Consultar a quantidade de funcionários vinculados a cada departamento.

Dashboard

Visualizar o total de funcionários.

Acompanhar a quantidade de funcionários ativos.

Consultar o total de departamentos cadastrados.


Tecnologias utilizadas

Python

Flet 1.1.3

Arquivos JSON para armazenamento dos dados

Visual Studio Code



Como executar o projeto

Instale o Python.

Clone este repositório.

Entre na pasta do projeto.

Crie um ambiente virtual.

Instale as dependências:

pip install -r requirements.txt



Execute o aplicativo:

flet run main.py

Armazenamento dos dados

O sistema utiliza arquivos JSON para armazenar e recuperar os registros de funcionários e departamentos.