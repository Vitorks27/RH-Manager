
import flet as ft

from services.funcionario_service import (
    listar_funcionarios,
    cadastrar_funcionario,
    atualizar_funcionario,
    excluir_funcionario
)

from services.departamento_service import (
    listar_departamentos,
    cadastrar_departamento,
    atualizar_departamento,
    excluir_departamento
)


def main(page: ft.Page):

    page.title = "RH Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="#17365D")
    page.bgcolor = "#F1F5F9"
    page.padding = 0

    AZUL = "#17365D"
    BRANCO = "#FFFFFF"
    CINZA = "#64748B"
    FUNDO = "#F1F5F9"

    conteudo = ft.Column(expand=True, spacing=20)

    def criar_cartao(titulo, valor, descricao):
        return ft.Container(
            expand=True,
            height=145,
            padding=22,
            bgcolor=BRANCO,
            border_radius=14,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=9,
                controls=[
                    ft.Text(titulo, size=14, color=CINZA),
                    ft.Text(
                        valor,
                        size=34,
                        weight=ft.FontWeight.BOLD,
                        color=AZUL
                    ),
                    ft.Text(descricao, size=12, color=CINZA)
                ]
            )
        )

    def mostrar_dashboard(e=None):
        funcionarios = listar_funcionarios()
        departamentos = listar_departamentos()

        ativos = sum(
            1 for f in funcionarios
            if f.get("status") == "Ativo"
        )

        cards = ft.Row(
            spacing=18,
            controls=[
                criar_cartao(
                    "Total de funcionários",
                    str(len(funcionarios)),
                    "Pessoas cadastradas"
                ),
                criar_cartao(
                    "Funcionários ativos",
                    str(ativos),
                    "Colaboradores ativos"
                ),
                criar_cartao(
                    "Departamentos",
                    str(len(departamentos)),
                    "Setores cadastrados"
                )
            ]
        )

        lista_departamentos = []
        maior_quantidade = max(
            [
                sum(
                    1 for f in funcionarios
                    if f.get("departamento") == d.get("nome")
                )
                for d in departamentos
            ],
            default=1
        )
        maior_quantidade = max(maior_quantidade, 1)

        for departamento in departamentos:
            quantidade = sum(
                1 for f in funcionarios
                if f.get("departamento") == departamento.get("nome")
            )
            largura = max(8, 190 * quantidade / maior_quantidade)

            lista_departamentos.append(
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    departamento.get("nome", ""),
                                    size=12,
                                    color="#334155"
                                ),
                                ft.Text(
                                    str(quantidade),
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color=AZUL
                                )
                            ]
                        ),
                        ft.Container(
                            width=190,
                            height=9,
                            bgcolor="#E2E8F0",
                            border_radius=10,
                            content=ft.Container(
                                width=largura,
                                height=9,
                                bgcolor="#315D91",
                                border_radius=10
                            )
                        )
                    ]
                )
            )

        if not lista_departamentos:
            lista_departamentos.append(
                ft.Text(
                    "Nenhum departamento cadastrado.",
                    color=CINZA,
                    size=13
                )
            )

        painel_departamentos = ft.Container(
            expand=3,
            padding=22,
            bgcolor=BRANCO,
            border_radius=14,
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Text(
                        "Funcionários por departamento",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=AZUL
                    ),
                    ft.Column(
                        spacing=13,
                        controls=lista_departamentos
                    )
                ]
            )
        )

        painel_acoes = ft.Container(
            expand=2,
            padding=22,
            bgcolor=BRANCO,
            border_radius=14,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text(
                        "Ações rápidas",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=AZUL
                    ),
                    ft.Text(
                        "Acesse rapidamente as principais funções do sistema.",
                        size=12,
                        color=CINZA
                    ),
                    ft.Button(
                        "Cadastrar funcionário",
                        icon=ft.Icons.PERSON_ADD,
                        on_click=lambda e: mostrar_formulario()
                    ),
                    ft.Button(
                        "Novo departamento",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: mostrar_formulario_departamento()
                    ),
                    ft.Button(
                        "Consultar funcionários",
                        icon=ft.Icons.GROUP,
                        on_click=mostrar_funcionarios
                    )
                ]
            )
        )

        ultimos_funcionarios = funcionarios[-5:][::-1]
        linhas_recentes = []

        for funcionario in ultimos_funcionarios:
            linhas_recentes.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            expand=True,
                            spacing=3,
                            controls=[
                                ft.Text(
                                    funcionario.get("nome", "Sem nome"),
                                    weight=ft.FontWeight.BOLD,
                                    color="#334155",
                                    size=13
                                ),
                                ft.Text(
                                    funcionario.get("cargo", ""),
                                    color=CINZA,
                                    size=11
                                )
                            ]
                        ),
                        ft.Text(
                            funcionario.get("departamento", ""),
                            color=CINZA,
                            size=12
                        )
                    ]
                )
            )
            linhas_recentes.append(ft.Divider(color="#E2E8F0"))

        if not linhas_recentes:
            linhas_recentes.append(
                ft.Text(
                    "Os funcionários cadastrados aparecerão aqui.",
                    color=CINZA,
                    size=13
                )
            )

        painel_recentes = ft.Container(
            expand=True,
            padding=22,
            bgcolor=BRANCO,
            border_radius=14,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text(
                        "Últimos funcionários cadastrados",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=AZUL
                    ),
                    ft.Column(
                        spacing=7,
                        controls=linhas_recentes
                    )
                ]
            )
        )

        conteudo.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text(
                                "Visão Geral",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color="#1E293B"
                            ),
                            ft.Text(
                                "Acompanhe os principais indicadores da sua equipe.",
                                size=13,
                                color=CINZA
                            )
                        ]
                    )
                ]
            ),
            cards,
            ft.Row(
                expand=True,
                spacing=18,
                controls=[
                    painel_departamentos,
                    painel_acoes
                ]
            ),
            painel_recentes
        ]

        page.update()

    def mostrar_funcionarios(e=None):
        funcionarios = listar_funcionarios()
        departamentos = sorted(
            d["nome"] for d in listar_departamentos()
        )

        pesquisa = ft.TextField(
            label="Pesquisar funcionário",
            hint_text="Digite um nome ou CPF",
            prefix_icon=ft.Icons.SEARCH,
            expand=True
        )

        filtro_departamento = ft.Dropdown(
            label="Departamento",
            width=210,
            value="Todos",
            options=[
                ft.DropdownOption(key="Todos", text="Todos")
            ] + [
                ft.DropdownOption(key=d, text=d)
                for d in departamentos
            ]
        )

        filtro_status = ft.Dropdown(
            label="Situação",
            width=180,
            value="Todos",
            options=[
                ft.DropdownOption(key="Todos", text="Todas"),
                ft.DropdownOption(key="Ativo", text="Ativo"),
                ft.DropdownOption(key="Inativo", text="Inativo"),
                ft.DropdownOption(key="Férias", text="Férias"),
                ft.DropdownOption(key="Afastado", text="Afastado"),
                ft.DropdownOption(key="Desligado", text="Desligado")
            ]
        )

        tabela = ft.Column(spacing=10)
        contador = ft.Text(color=CINZA, size=12)

        def aplicar_filtros(e=None):
            termo = (pesquisa.value or "").strip().lower()
            termo_cpf = "".join(c for c in termo if c.isdigit())

            filtrados = []

            for funcionario in funcionarios:
                nome = funcionario.get("nome", "").lower()
                cpf = funcionario.get("cpf", "")
                cpf_numeros = "".join(
                    c for c in cpf if c.isdigit()
                )

                corresponde_pesquisa = (
                    termo in nome or
                    (termo_cpf and termo_cpf in cpf_numeros)
                )

                corresponde_departamento = (
                    filtro_departamento.value == "Todos" or
                    funcionario.get("departamento") ==
                    filtro_departamento.value
                )

                corresponde_status = (
                    filtro_status.value == "Todos" or
                    funcionario.get("status") ==
                    filtro_status.value
                )

                if (
                    corresponde_pesquisa
                    and corresponde_departamento
                    and corresponde_status
                ):
                    filtrados.append(funcionario)

            tabela.controls.clear()
            contador.value = (
                f"{len(filtrados)} funcionário(s) encontrado(s)"
            )

            for funcionario in filtrados:

                def editar(e, f=funcionario):
                    mostrar_formulario(f)

                def excluir(e, f=funcionario):
                    confirmar_exclusao(f)

                tabela.controls.append(
                    ft.Container(
                        padding=15,
                        bgcolor=BRANCO,
                        border_radius=10,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    expand=True,
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            funcionario["nome"],
                                            weight=ft.FontWeight.BOLD,
                                            color=AZUL
                                        ),
                                        ft.Text(
                                            f'{funcionario["cargo"]} - '
                                            f'{funcionario["departamento"]}',
                                            size=12,
                                            color=CINZA
                                        ),
                                        ft.Text(
                                            f'CPF: {funcionario["cpf"]}',
                                            size=11,
                                            color=CINZA
                                        )
                                    ]
                                ),
                                ft.Text(
                                    funcionario.get("status", "Ativo"),
                                    color="#15803D"
                                    if funcionario.get("status") == "Ativo"
                                    else CINZA,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar funcionário",
                                    on_click=editar
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    tooltip="Excluir funcionário",
                                    icon_color="#DC2626",
                                    on_click=excluir
                                )
                            ]
                        )
                    )
                )

            if not filtrados:
                tabela.controls.append(
                    ft.Container(
                        padding=25,
                        bgcolor=BRANCO,
                        border_radius=10,
                        content=ft.Text(
                            "Nenhum funcionário encontrado.",
                            color=CINZA
                        )
                    )
                )

            page.update()

        def limpar_filtros(e):
            pesquisa.value = ""
            filtro_departamento.value = "Todos"
            filtro_status.value = "Todos"
            aplicar_filtros()

        pesquisa.on_change = aplicar_filtros
        filtro_departamento.on_select = aplicar_filtros
        filtro_status.on_select = aplicar_filtros

        conteudo.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        "Funcionários",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color="#1E293B"
                    ),
                    ft.Button(
                        "Novo Funcionário",
                        on_click=lambda e: mostrar_formulario()
                    )
                ]
            ),
            ft.Text(
                "Consulte e gerencie os colaboradores da empresa.",
                size=13,
                color=CINZA
            ),
            ft.Row(
                controls=[
                    pesquisa,
                    filtro_departamento,
                    filtro_status
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    contador,
                    ft.TextButton(
                        "Limpar filtros",
                        on_click=limpar_filtros
                    )
                ]
            ),
            tabela
        ]

        aplicar_filtros()

    def mostrar_formulario(funcionario=None):
        editando = funcionario is not None
        departamentos = listar_departamentos()

        opcoes_departamentos = [
            ft.DropdownOption(
                key=d["nome"],
                text=d["nome"]
            )
            for d in departamentos
        ]

        nome = ft.TextField(
            label="Nome completo",
            value=funcionario["nome"] if editando else "",
            expand=True
        )

        cpf = ft.TextField(
            label="CPF",
            value=funcionario["cpf"] if editando else "",
            expand=True
        )

        email = ft.TextField(
            label="E-mail",
            value=funcionario["email"] if editando else "",
            expand=True
        )

        telefone = ft.TextField(
            label="Telefone",
            value=funcionario["telefone"] if editando else "",
            expand=True
        )

        cargo = ft.TextField(
            label="Cargo",
            value=funcionario["cargo"] if editando else "",
            expand=True
        )

        departamento = ft.Dropdown(
            label="Departamento",
            options=opcoes_departamentos,
            value=funcionario["departamento"]
            if editando and funcionario["departamento"] in
            [d["nome"] for d in departamentos]
            else None,
            expand=True
        )

        salario = ft.TextField(
            label="Salário",
            value=funcionario["salario"] if editando else "",
            expand=True
        )

        admissao = ft.TextField(
            label="Data de admissão",
            value=funcionario["admissao"] if editando else "",
            hint_text="DD/MM/AAAA",
            expand=True
        )

        status = ft.Dropdown(
            label="Situação do funcionário",
            value=funcionario.get("status", "Ativo") if editando else "Ativo",
            options=[
                ft.DropdownOption(key="Ativo", text="Ativo"),
                ft.DropdownOption(key="Inativo", text="Inativo"),
                ft.DropdownOption(key="Férias", text="Férias"),
                ft.DropdownOption(key="Afastado", text="Afastado"),
                ft.DropdownOption(key="Desligado", text="Desligado")
            ],
            expand=True
        )

        mensagem = ft.Text(color="#DC2626", size=13)

        def salvar_funcionario(e):
            campos = [
                nome.value,
                cpf.value,
                email.value,
                telefone.value,
                cargo.value,
                departamento.value,
                salario.value,
                admissao.value
            ]

            if not all(campo and campo.strip() for campo in campos):
                mensagem.value = "Preencha todos os campos."
                page.update()
                return

            dados = {
                "nome": nome.value.strip(),
                "cpf": cpf.value.strip(),
                "email": email.value.strip(),
                "telefone": telefone.value.strip(),
                "cargo": cargo.value.strip(),
                "departamento": departamento.value,
                "salario": salario.value.strip(),
                "admissao": admissao.value.strip(),
                "status": status.value or "Ativo"
            }

            try:
                if editando:
                    resultado = atualizar_funcionario(
                        funcionario["id"],
                        dados
                    )

                    if not resultado:
                        mensagem.value = "Funcionário não encontrado."
                        page.update()
                        return
                else:
                    cadastrar_funcionario(dados)

                mostrar_funcionarios()

            except (OSError, ValueError) as erro:
                mensagem.value = f"Erro ao salvar: {erro}"
                page.update()

        conteudo.controls = [
            ft.Text(
                "Editar Funcionário" if editando else "Novo Funcionário",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#1E293B"
            ),
            ft.Container(
                padding=25,
                bgcolor=BRANCO,
                border_radius=12,
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Text(
                            "Dados pessoais",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AZUL
                        ),
                        ft.Row(controls=[nome]),
                        ft.Row(controls=[cpf, email]),
                        ft.Row(controls=[telefone]),
                        ft.Divider(color="#E2E8F0"),
                        ft.Text(
                            "Dados profissionais",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AZUL
                        ),
                        ft.Row(controls=[cargo, departamento]),
                        ft.Row(controls=[salario, admissao]),
                        ft.Row(controls=[status]),
                        mensagem,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.Button(
                                    "Cancelar",
                                    on_click=mostrar_funcionarios
                                ),
                                ft.Button(
                                    "Salvar Alterações" if editando
                                    else "Salvar Funcionário",
                                    on_click=salvar_funcionario
                                )
                            ]
                        )
                    ]
                )
            )
        ]

        if not departamentos:
            mensagem.value = (
                "Cadastre um departamento antes de cadastrar funcionários."
            )

        page.update()

    def confirmar_exclusao(funcionario):

        def excluir(e):
            try:
                excluir_funcionario(funcionario["id"])
                page.pop_dialog()
                mostrar_funcionarios()
            except (OSError, ValueError) as erro:
                page.pop_dialog()
                conteudo.controls.append(
                    ft.Text(f"Erro ao excluir: {erro}", color="#DC2626")
                )
                page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(
                f'Deseja realmente excluir {funcionario["nome"]}?'
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: page.pop_dialog()
                ),
                ft.TextButton(
                    "Excluir",
                    on_click=excluir
                )
            ]
        )

        page.show_dialog(dialogo)

    def mostrar_departamentos(e=None):
        departamentos = listar_departamentos()
        funcionarios = listar_funcionarios()

        tabela = ft.Column(spacing=10)

        for departamento in departamentos:
            quantidade = sum(
                1 for f in funcionarios
                if f.get("departamento") == departamento["nome"]
            )

            def editar(e, d=departamento):
                mostrar_formulario_departamento(d)

            def excluir(e, d=departamento):
                confirmar_exclusao_departamento(d)

            tabela.controls.append(
                ft.Container(
                    padding=18,
                    bgcolor=BRANCO,
                    border_radius=10,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                expand=True,
                                spacing=5,
                                controls=[
                                    ft.Text(
                                        departamento["nome"],
                                        weight=ft.FontWeight.BOLD,
                                        color=AZUL,
                                        size=16
                                    ),
                                    ft.Text(
                                        departamento.get("descricao", ""),
                                        color=CINZA,
                                        size=12
                                    ),
                                    ft.Text(
                                        f"{quantidade} funcionário(s)",
                                        color=CINZA,
                                        size=12
                                    )
                                ]
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar departamento",
                                on_click=editar
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Excluir departamento",
                                icon_color="#DC2626",
                                on_click=excluir
                            )
                        ]
                    )
                )
            )

        if not departamentos:
            tabela.controls.append(
                ft.Container(
                    padding=25,
                    bgcolor=BRANCO,
                    border_radius=10,
                    content=ft.Text(
                        "Nenhum departamento cadastrado.",
                        color=CINZA
                    )
                )
            )

        conteudo.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        "Departamentos",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color="#1E293B"
                    ),
                    ft.Button(
                        "Novo Departamento",
                        on_click=lambda e: mostrar_formulario_departamento()
                    )
                ]
            ),
            ft.Text(
                "Organize os setores e acompanhe seus colaboradores.",
                size=13,
                color=CINZA
            ),
            tabela
        ]

        page.update()

    def mostrar_formulario_departamento(departamento=None):
        editando = departamento is not None

        nome = ft.TextField(
            label="Nome do departamento",
            value=departamento["nome"] if editando else "",
            expand=True
        )

        descricao = ft.TextField(
            label="Descrição",
            value=departamento.get("descricao", "") if editando else "",
            multiline=True,
            min_lines=3,
            max_lines=4
        )

        mensagem = ft.Text(color="#DC2626", size=13)

        def salvar(e):
            if not nome.value or not nome.value.strip():
                mensagem.value = "Informe o nome do departamento."
                page.update()
                return

            dados = {
                "nome": nome.value.strip(),
                "descricao": descricao.value.strip()
            }

            funcionarios = listar_funcionarios()

            if editando:
                vinculado = any(
                    f.get("departamento") == departamento["nome"]
                    for f in funcionarios
                )

                if vinculado and dados["nome"] != departamento["nome"]:
                    mensagem.value = (
                        "Não é possível renomear um departamento "
                        "que possui funcionários vinculados."
                    )
                    page.update()
                    return

            try:
                if editando:
                    resultado = atualizar_departamento(
                        departamento["id"],
                        dados
                    )

                    if not resultado:
                        mensagem.value = "Nome já cadastrado."
                        page.update()
                        return
                else:
                    resultado = cadastrar_departamento(dados)

                    if not resultado:
                        mensagem.value = "Esse departamento já existe."
                        page.update()
                        return

                mostrar_departamentos()

            except (OSError, ValueError) as erro:
                mensagem.value = f"Erro ao salvar: {erro}"
                page.update()

        conteudo.controls = [
            ft.Text(
                "Editar Departamento" if editando else "Novo Departamento",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#1E293B"
            ),
            ft.Container(
                padding=25,
                bgcolor=BRANCO,
                border_radius=12,
                content=ft.Column(
                    spacing=15,
                    controls=[
                        nome,
                        descricao,
                        mensagem,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.Button(
                                    "Cancelar",
                                    on_click=mostrar_departamentos
                                ),
                                ft.Button(
                                    "Salvar Departamento",
                                    on_click=salvar
                                )
                            ]
                        )
                    ]
                )
            )
        ]

        page.update()

    def confirmar_exclusao_departamento(departamento):

        def excluir(e):
            funcionarios = listar_funcionarios()

            vinculado = any(
                f.get("departamento") == departamento["nome"]
                for f in funcionarios
            )

            page.pop_dialog()

            if vinculado:
                aviso = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Departamento em uso"),
                    content=ft.Text(
                        "Não é possível excluir este departamento "
                        "porque existem funcionários vinculados a ele."
                    ),
                    actions=[
                        ft.TextButton(
                            "Entendi",
                            on_click=lambda e: page.pop_dialog()
                        )
                    ]
                )
                page.show_dialog(aviso)
                return

            try:
                excluir_departamento(departamento["id"])
                mostrar_departamentos()
            except (OSError, ValueError) as erro:
                conteudo.controls.append(
                    ft.Text(f"Erro ao excluir: {erro}", color="#DC2626")
                )
                page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(
                f'Deseja excluir o departamento {departamento["nome"]}?'
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: page.pop_dialog()
                ),
                ft.TextButton(
                    "Excluir",
                    on_click=excluir
                )
            ]
        )

        page.show_dialog(dialogo)

    menu = ft.Container(
        width=235,
        bgcolor=AZUL,
        padding=20,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text(
                    "RH Manager",
                    size=23,
                    weight=ft.FontWeight.BOLD,
                    color=BRANCO
                ),
                ft.Text(
                    "GESTÃO DE PESSOAS",
                    size=10,
                    color="#CBD5E1"
                ),
                ft.Divider(color="#456080"),
                ft.Button(
                    "Visão Geral",
                    width=195,
                    on_click=mostrar_dashboard
                ),
                ft.Button(
                    "Funcionários",
                    width=195,
                    on_click=mostrar_funcionarios
                ),
                ft.Button(
                    "Departamentos",
                    width=195,
                    on_click=mostrar_departamentos
                ),
                ft.Container(expand=True),
                ft.Divider(color="#456080"),
                ft.Text(
                    "Sistema de Gerenciamento",
                    size=11,
                    color="#CBD5E1"
                )
            ]
        )
    )

    layout = ft.Row(
        expand=True,
        spacing=0,
        controls=[
            menu,
            ft.Container(
                expand=True,
                padding=30,
                bgcolor=FUNDO,
                content=conteudo
            )
        ]
    )

    page.add(layout)
    mostrar_dashboard()


if __name__ == "__main__":
    ft.run(main)
