import tkinter
import tkinter.messagebox
import customtkinter
import sys
import cadastro_aluno
import pyodbc

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class Inicial(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._deletar_var = tkinter.BooleanVar()
        self._deletar_var.set(False)
        self._registros = []

        self._aluno_instance = cadastro_aluno.Aluno()
        self._dados_conexao = (
            'Driver={SQL Server};'
            'Server={LAPTOP-QLUA0QFC};'
            'Database=ALUNOS;'
        )

        self._conexao = pyodbc.connect(self._dados_conexao)
        self._cursor = self._conexao.cursor()
        self.janela = self.title('Sistema alunos')
        self.tamanho_fixo = (500, 500)
        self.minsize(*self.tamanho_fixo)
        self.maxsize(*self.tamanho_fixo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 1), weight=0)
        self.header = customtkinter.CTkFrame(self, width=1, corner_radius=0, height=5)
        self.header.grid(row=0, column=1, rowspan=1, sticky='nsew')
        self.header.grid_rowconfigure(3, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.header, text='Escola Estadual', font=('Arial', 20))
        self.logo_label.grid(row=0, column=0, padx=140, pady=(20, 10))
        self.logo_label.config_font(size=16)
        self.bottom = customtkinter.CTkFrame(self, width=1, corner_radius=0, height=5)
        self.bottom.grid(row=1, column=1, rowspan=1, sticky='nsew', pady=(150, 50))
        self.opcao = customtkinter.CTkLabel(self.bottom, text='O que deseja fazer?', anchor='w')
        self.opcao.grid(row=5, column=0, padx=200, pady=(10, 0))
        self.opcao_escolher = customtkinter.CTkOptionMenu(self.bottom,
                                                          values=['Adicionar Alunos', 'Deletar Alunos',
                                                                  'Verificar Alunos', 'Sair'],
                                                          command=self.opcao_secretaria)

        self.opcao_escolher.grid(row=7, column=0, padx=20, pady=(10, 10))

    def set_entry_value(self):

        ra = self.__entry_ra.get()
        nome = self.__entry_nome.get()
        email = self.__entry_email.get()
        data_nasc = self.__entry_dataNasc.get()
        ano_escola = self.__entry_ano_escola.get()
        aluno_instance = self._aluno_instance
        aluno_instance.set_ra(ra)

        aluno_instance.cadastro(ra)

        self._comando = "INSERT INTO ALUNO(RA, NOME, ANO_ESCOLA, DATA_NASCIMENTO, EMAIL) VALUES (?, ?, ?, ?, ?)"
        self._cursor.execute(self._comando, (ra, nome, ano_escola, data_nasc, email))
        self._cursor.commit()

        self._comando2 = "SELECT * FROM ALUNO"
        self._cursor.execute(self._comando2)
        self._registros = self._cursor.fetchall()

        for registro in self._registros:
            self.listbox_adc_studante.insert(tkinter.END, registro)

        return self._comando2



    def adicionar_func(self):
        self.janela_adicionar = tkinter.Toplevel()
        self.janela_adicionar.title('Adicionar Alunos')
        self.janela_adicionar.geometry(f'{2000}x{1080}')
        self.janela_adicionar.grab_set()

        self.listbox_adc_studante = tkinter.Listbox(self.janela_adicionar, selectmode=tkinter.SINGLE, height=30,
                                                    width=150)
        self.listbox_adc_studante.grid(row=3, column=1, padx=20, pady=10)

        self.__entry_ra = customtkinter.CTkEntry(self.janela_adicionar, placeholder_text="RA: ", width=100)
        self.__entry_ra.grid(row=5, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.__entry_nome = customtkinter.CTkEntry(self.janela_adicionar, placeholder_text="Nome: ")
        self.__entry_nome.grid(row=6, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.__entry_email = customtkinter.CTkEntry(self.janela_adicionar, placeholder_text="E-mail: ")
        self.__entry_email.grid(row=7, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.__entry_dataNasc = customtkinter.CTkEntry(self.janela_adicionar, placeholder_text="Data Niscimento ")
        self.__entry_dataNasc.grid(row=8, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.__entry_ano_escola = customtkinter.CTkEntry(self.janela_adicionar, placeholder_text="Semestre Escola: ")
        self.__entry_ano_escola.grid(row=9, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.sidebar_button_1 = customtkinter.CTkButton(self.janela_adicionar, command=self.set_entry_value,
                                                        text="Adicionar")
        self.sidebar_button_1.grid(row=10, column=1, padx=20, pady=10)

    def value_entry_razin(self):
        return self.__entry_ra.get()

    def value_entry_nomezin(self):
        return self.__entry_nome.get()

    def value_entry_email(self):
        return self.__entry_email.get()


    def deletar_func(self):
            self.janela_deletar = tkinter.Toplevel()
            self.janela_deletar.title('Deletar Alunos')
            self.janela_deletar.geometry(f'{2000}x{1080}')
            self.janela_deletar.grab_set()

            self.students_listbox_delet = tkinter.Listbox(self.janela_deletar, selectmode=tkinter.SINGLE, height=20,
                                                    width=200)
            self.students_listbox_delet.grid(row=3, column=1, padx=20, pady=10)
            self.__delet_ra = customtkinter.CTkEntry(self.janela_deletar, placeholder_text="RA: ")
            self.__delet_ra.grid(row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

            self._listar = "SELECT * FROM ALUNO"
            self._cursor.execute(self._listar)
            self._registros = self._cursor.fetchall()

            for registro in self._registros:
                self.students_listbox_delet.insert(tkinter.END, registro)

            self.delete_button = customtkinter.CTkButton(self.janela_deletar, command=self.delete_student,
                                                         text="Deletar")
            self.delete_button.grid(row=5, column=1, padx=20, pady=10)
            self.janela_deletar.update()

    def delete_student(self):

        ra = self.__delet_ra.get()

        self._delet_index = "DELETE FROM ALUNO WHERE RA = ?"
        self._cursor.execute(self._delet_index, (ra,))
        self._conexao.commit()
        self.janela_deletar.update()
        # Atualize a lista após a exclusão
        self._listar = "SELECT * FROM ALUNO"
        self._cursor.execute(self._listar)
        self._registros = self._cursor.fetchall()

    def verificar_func(self):
        self.janela_verificar = tkinter.Toplevel()
        self.janela_verificar.title('Verificar Alunos')
        self.janela_verificar.geometry(f'{2000}x{1080}')
        self.janela_verificar.grab_set()
        self.janela_verificar.update()

        self.students_listbox = tkinter.Listbox(self.janela_verificar, selectmode=tkinter.SINGLE, height=20,
                                                width=225)
        self.students_listbox.grid(row=3, column=1, padx=20, pady=10)

        self._comando_verificar = "SELECT * FROM ALUNO"
        self._cursor.execute(self._comando_verificar)
        self._registros = self._cursor.fetchall()

        for registro in self._registros:
            self.students_listbox.insert(tkinter.END, registro)

    def sair(self):
        sys.exit()

    def opcao_secretaria(self, value):
        if value == 'Adicionar Alunos':
            self.adicionar_func()
            self.update()
        elif value == 'Deletar Alunos':
            self.deletar_func()
            self.update()
        elif value == 'Verificar Alunos':
            self.verificar_func()
            self.update()
        elif value == 'Sair':
            self.sair()

if __name__ == "__main__":
    app = Inicial()
    app.mainloop()
