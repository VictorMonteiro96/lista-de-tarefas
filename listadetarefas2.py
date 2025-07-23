import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

tarefas = []

def adicionar_tarefa():
    texto = entrada.get()
    prioridade = prioridade_var.get()
    if texto:
        tarefas.append((texto, prioridade, False))  # False = não concluída
        atualizar_lista()
        salvar_tarefas()
        entrada.delete(0, END)

def remover_tarefa():
    try:
        indice = lista.curselection()[0]
        tarefas.pop(indice)
        atualizar_lista()
        salvar_tarefas()
    except IndexError:
        pass

def marcar_concluida():
    try:
        indice = lista.curselection()[0]
        texto, prioridade, concluida = tarefas[indice]
        tarefas[indice] = (texto, prioridade, not concluida)  # alterna True/False
        atualizar_lista()
        salvar_tarefas()
    except IndexError:
        pass

def atualizar_lista():
    lista.delete(0, tk.END)
    for texto, prioridade, concluida in tarefas:
        if concluida:
            texto_formatado = f"✓ {texto} ({prioridade})"
            lista.insert(tk.END, texto_formatado)
            lista.itemconfig(tk.END, {'fg': 'gray'})
        else:
            icone = "⚠️" if prioridade == "Alta" else "⭐" if prioridade == "Média" else "🔹"
            texto_formatado = f"{icone} {texto} ({prioridade})"
            lista.insert(tk.END, texto_formatado)
            cor = {"Alta": "red", "Média": "orange", "Baixa": "green"}.get(prioridade, "black")
            lista.itemconfig(tk.END, {'fg': cor})

def salvar_tarefas():
    with open("tarefas.txt", "w", encoding="utf-8") as f:
        for texto, prioridade, concluida in tarefas:
            f.write(f"{texto}||{prioridade}||{concluida}\n")

def carregar_tarefas():
    try:
        with open("tarefas.txt", "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split("||")
                if len(partes) == 3:
                    texto, prioridade, concluida_str = partes
                    concluida = concluida_str == "True"
                    tarefas.append((texto, prioridade, concluida))
        atualizar_lista()
    except FileNotFoundError:
        pass

# ------------------- Interface -------------------

janela = ttk.Window(themename="flatly")
janela.title('Minha Lista de Tarefas')
janela.geometry('300x450')

entrada = ttk.Entry(janela, width=30)
entrada.pack(pady=5)

prioridade_var = tk.StringVar(value="Média")
prioridade_menu = tk.OptionMenu(janela, prioridade_var, "Alta", "Média", "Baixa")
prioridade_menu.pack(pady=5)

botao_adicionar = ttk.Button(janela, text='Adicionar', command=adicionar_tarefa)
botao_adicionar.pack(pady=5)

botao_remover = ttk.Button(janela, text='Remover', command=remover_tarefa)
botao_remover.pack(pady=5)

botao_concluir = ttk.Button(janela, text='Marcar como Concluída', command=marcar_concluida)
botao_concluir.pack(pady=5)

lista = tk.Listbox(janela, width=40, height=12)
lista.pack(pady=10)

carregar_tarefas()

janela.mainloop()

