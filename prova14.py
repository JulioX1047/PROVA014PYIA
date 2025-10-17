import flet as ft
from datetime import datetime

class Cliente:
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.id_unico = email

class Quarto:
    def __init__(self, numero, tipo, preco_diaria):
        self.numero = numero
        self.tipo = tipo
        self.preco_diaria = preco_diaria

class Reserva:
    def __init__(self, cliente, quarto, data_checkin, data_checkout):
        self.cliente = cliente
        self.quarto = quarto
        self.data_checkin = data_checkin
        self.data_checkout = data_checkout
        self.status = "Ativa"

class GerenciadorDeReservas:
    def __init__(self):
        self.quartos = []
        self.clientes = []
        self.reservas = []
        self._inicializar_quartos()

    def _inicializar_quartos(self):
        self.quartos.append(Quarto(101, "Single", 150.00))
        self.quartos.append(Quarto(102, "Single", 150.00))
        self.quartos.append(Quarto(201, "Double", 250.00))
        self.quartos.append(Quarto(202, "Double", 250.00))
        self.quartos.append(Quarto(301, "Suíte", 400.00))

    def verificar_disponibilidade(self, quarto, data_checkin, data_checkout):
        for reserva in self.reservas:
            if reserva.quarto.numero == quarto.numero and reserva.status == "Ativa":
                if (data_checkin < reserva.data_checkout and data_checkout > reserva.data_checkin):
                    return False
        return True

    def criar_reserva(self, nome_cliente, telefone_cliente, email_cliente, numero_quarto, data_checkin, data_checkout):
        quarto_selecionado = None
        for q in self.quartos:
            if q.numero == numero_quarto:
                quarto_selecionado = q
                break
        
        if not quarto_selecionado:
            return "Erro: Quarto não encontrado."

        if not self.verificar_disponibilidade(quarto_selecionado, data_checkin, data_checkout):
            return f"Erro: Quarto {numero_quarto} não está disponível nessas datas."

        cliente_existente = None
        for c in self.clientes:
            if c.email == email_cliente:
                cliente_existente = c
                break
        
        if not cliente_existente:
            cliente_existente = Cliente(nome_cliente, telefone_cliente, email_cliente)
            self.clientes.append(cliente_existente)

        nova_reserva = Reserva(cliente_existente, quarto_selecionado, data_checkin, data_checkout)
        self.reservas.append(nova_reserva)
        return f"Sucesso: Reserva para {nome_cliente} no quarto {numero_quarto} confirmada!"

    def cancelar_reserva(self, reserva_a_cancelar):
        reserva_a_cancelar.status = "Cancelada"

def main(page: ft.Page):
    page.title = "Refúgio dos Sonhos - Sistema de Reservas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 800
    page.window_height = 600

    gerenciador = GerenciadorDeReservas()

    def mostrar_dialogo(mensagem):
        tipo_msg = mensagem.split(":")[0].lower()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Status da Operação", weight=ft.FontWeight.BOLD),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(e))],
            actions_alignment=ft.MainAxisAlignment.END,
            icon=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE if tipo_msg == "sucesso" else ft.icons.ERROR_OUTLINE, 
                        color=ft.colors.GREEN if tipo_msg == "sucesso" else ft.colors.RED)
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def fechar_dialogo(e):
        page.dialog.open = False
        page.update()

    txt_nome = ft.TextField(label="Nome do Cliente", width=300)
    txt_email = ft.TextField(label="Email", width=300)
    txt_telefone = ft.TextField(label="Telefone", width=300)
    txt_checkin = ft.TextField(label="Data Check-in (DD/MM/AAAA)", width=200)
    txt_checkout = ft.TextField(label="Data Check-out (DD/MM/AAAA)", width=200)
    dd_quarto = ft.Dropdown(
        label="Escolha o Quarto",
        width=300,
        options=[ft.dropdown.Option(f"{q.numero} - {q.tipo}") for q in gerenciador.quartos]
    )

    def confirmar_reserva_click(e):
        try:
            numero_quarto = int(dd_quarto.value.split(" - ")[0])
            data_checkin = datetime.strptime(txt_checkin.value, "%d/%m/%Y")
            data_checkout = datetime.strptime(txt_checkout.value, "%d/%m/%Y")

            if data_checkin >= data_checkout:
                mostrar_dialogo("Erro: A data de check-out deve ser posterior à de check-in.")
                return

            resultado = gerenciador.criar_reserva(
                txt_nome.value,
                txt_telefone.value,
                txt_email.value,
                numero_quarto,
                data_checkin,
                data_checkout
            )
            mostrar_dialogo(resultado)
            
            if "Sucesso" in resultado:
                navegar_para_tela(e, "home")

        except (ValueError, TypeError):
            mostrar_dialogo("Erro: Preencha todos os campos corretamente. Use o formato DD/MM/AAAA para datas.")

    def navegar_para_tela(e, tela):
        page.controls.clear()
        
        if tela == "home":
            btn_fazer_reserva = ft.ElevatedButton("Fazer Nova Reserva", on_click=lambda e: navegar_para_tela(e, "reserva"), icon=ft.icons.ADD)
            btn_ver_reservas = ft.ElevatedButton("Visualizar Reservas", on_click=lambda e: navegar_para_tela(e, "lista_reservas"), icon=ft.icons.LIST)
            
            tabela_quartos = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Número")),
                    ft.DataColumn(ft.Text("Tipo")),
                    ft.DataColumn(ft.Text("Preço/Diária")),
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(q.numero)),
                        ft.DataCell(ft.Text(q.tipo)),
                        ft.DataCell(ft.Text(f"R$ {q.preco_diaria:.2f}")),
                    ]) for q in gerenciador.quartos
                ]
            )
            page.add(
                ft.Text("Bem-vindo ao Refúgio dos Sonhos!", size=32, weight=ft.FontWeight.BOLD),
                ft.Row([btn_fazer_reserva, btn_ver_reservas], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Text("Nossos Quartos", size=20),
                tabela_quartos
            )

        elif tela == "reserva":
            btn_confirmar = ft.ElevatedButton("Confirmar Reserva", on_click=confirmar_reserva_click, icon=ft.icons.CHECK)
            btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: navegar_para_tela(e, "home"), icon=ft.icons.ARROW_BACK)

            page.add(
                ft.Text("Formulário de Reserva", size=24, weight=ft.FontWeight.BOLD),
                txt_nome, txt_email, txt_telefone,
                ft.Row([txt_checkin, txt_checkout]),
                dd_quarto,
                ft.Row([btn_confirmar, btn_voltar], alignment=ft.MainAxisAlignment.CENTER)
            )

        elif tela == "lista_reservas":
            def cancelar_reserva_click(reserva):
                gerenciador.cancelar_reserva(reserva)
                mostrar_dialogo("Sucesso: Reserva cancelada!")
                navegar_para_tela(None, "lista_reservas")

            rows = []
            for r in gerenciador.reservas:
                rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(r.cliente.nome)),
                        ft.DataCell(ft.Text(r.quarto.numero)),
                        ft.DataCell(ft.Text(r.data_checkin.strftime("%d/%m/%Y"))),
                        ft.DataCell(ft.Text(r.data_checkout.strftime("%d/%m/%Y"))),
                        ft.DataCell(ft.Text(r.status, color=ft.colors.GREEN if r.status == 'Ativa' else ft.colors.RED)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.CANCEL, icon_color=ft.colors.RED, on_click=lambda e, res=r: cancelar_reserva_click(res), tooltip="Cancelar Reserva") if r.status == "Ativa" else ft.Text("-")),
                    ])
                )

            tabela_reservas = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Cliente")),
                    ft.DataColumn(ft.Text("Quarto")),
                    ft.DataColumn(ft.Text("Check-in")),
                    ft.DataColumn(ft.Text("Check-out")),
                    ft.DataColumn(ft.Text("Status")),
                    ft.DataColumn(ft.Text("Ação")),
                ],
                rows=rows
            )
            btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: navegar_para_tela(e, "home"), icon=ft.icons.ARROW_BACK)
            page.add(
                ft.Text("Todas as Reservas", size=24, weight=ft.FontWeight.BOLD),
                btn_voltar,
                tabela_reservas if rows else ft.Text("Nenhuma reserva encontrada.")
            )
        
        page.update()

    navegar_para_tela(None, "home")

if __name__ == "__main__":
    ft.app(target=main)
