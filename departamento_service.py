
import json
from pathlib import Path

arquivo = Path(__file__).resolve().parent.parent / "database" / "departamentos.json"


def listar_departamentos():
    if not arquivo.exists():
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text("[]", encoding="utf-8")

    conteudo = arquivo.read_text(encoding="utf-8").strip()

    if not conteudo:
        arquivo.write_text("[]", encoding="utf-8")
        return []

    return json.loads(conteudo)


def salvar_departamentos(departamentos):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(departamentos, f, ensure_ascii=False, indent=4)


def cadastrar_departamento(dados):
    departamentos = listar_departamentos()

    if any(
        d["nome"].strip().lower() == dados["nome"].strip().lower()
        for d in departamentos
    ):
        return False

    novo_id = max(
        [d["id"] for d in departamentos],
        default=0
    ) + 1

    dados["id"] = novo_id
    departamentos.append(dados)

    salvar_departamentos(departamentos)

    return novo_id


def atualizar_departamento(id_departamento, novos_dados):
    departamentos = listar_departamentos()

    for i, departamento in enumerate(departamentos):
        if departamento["id"] == id_departamento:
            duplicado = any(
                d["id"] != id_departamento
                and d["nome"].strip().lower() == novos_dados["nome"].strip().lower()
                for d in departamentos
            )

            if duplicado:
                return False

            novos_dados["id"] = id_departamento
            departamentos[i] = novos_dados
            salvar_departamentos(departamentos)

            return True

    return False


def excluir_departamento(id_departamento):
    departamentos = listar_departamentos()

    novos_departamentos = [
        d for d in departamentos
        if d["id"] != id_departamento
    ]

    if len(novos_departamentos) == len(departamentos):
        return False

    salvar_departamentos(novos_departamentos)

    return True
