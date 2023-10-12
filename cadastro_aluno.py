import tela_inicial
import tkinter.messagebox


class Aluno:

    def __init__(self):
        self._ra = None

    def set_ra(self, ra):
        self._ra = ra

    def get_ra(self):
        return self._ra

    def cadastro(self, ra):
        try:
            if len(ra) < 7:
                raise ValueError("Número de caracteres insuficientes")
            elif len(ra) == 0:
                raise Exception("RA vazio")

            # Perform the actual student data insertion here

        except ValueError as ve:
            tkinter.messagebox.showerror('ERROR', f'Erro: {ve}')
        except Exception as e:
            tkinter.messagebox.showerror('ERROR', f'Erro desconhecido: {e}')


if __name__ == "__main__":
    # Primeiro, inicie a classe de tela inicial
    tela_inicial_instance = tela_inicial.Inicial()
    tela_inicial_instance.mainloop()

    aluno_instance = tela_inicial_instance.aluno_instance
    aluno_instance.cadastro()
