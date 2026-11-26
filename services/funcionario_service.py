

import json
from pathlib import Path

arquivo = Path(__file__).resolve().parent.parent / "database" / "funcionarios.json"


def listar_funcionarios():
    if not arquivo.exists():
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text("[]", encoding="utf-8")

    conteudo = arquivo.read_text(encoding="utf-8").strip()

    if not conteudo:
        arquivo.write_text("[]", encoding="utf-8")
        return []

    return json.loads(conteudo)


def salvar_funcionarios(funcionarios):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(funcionarios, f, ensure_ascii=False, indent=4)


def cadastrar_funcionario(dados):
    funcionarios = listar_funcionarios()

    novo_id = max(
        [funcionario["id"] for funcionario in funcionarios],
        default=0
    ) + 1

    dados["id"] = novo_id
    funcionarios.append(dados)

    salvar_funcionarios(funcionarios)

    return novo_id


def atualizar_funcionario(id_funcionario, novos_dados):
    funcionarios = listar_funcionarios()

    for funcionario in funcionarios:
        if funcionario["id"] == id_funcionario:
            novos_dados["id"] = id_funcionario
            funcionarios[funcionarios.index(funcionario)] = novos_dados
            salvar_funcionarios(funcionarios)
            return True

    return False


def excluir_funcionario(id_funcionario):
    funcionarios = listar_funcionarios()

    novos_funcionarios = [
        funcionario for funcionario in funcionarios
        if funcionario["id"] != id_funcionario
    ]

    if len(novos_funcionarios) == len(funcionarios):
        return False

    salvar_funcionarios(novos_funcionarios)

    return True
