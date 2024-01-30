# Librarias que eu Usei para esta aplicação em Python ---------------------------------------- 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import customtkinter
import os
import threading
#--------------------------------------------------------------------------------------------
# criar o backend ---------------------------------------------------------------------------
# função sair do programa --------------------------------------------------------------------
def Sair_programa ():
   resposta = messagebox.askyesno('SAIR', 'Deseja sair do programa ?...')
   if resposta:
       Janela.destroy()
#---------------------------------------------------------------------------------------------

# função limpar Campos -----------------------------------------------------------------------
def limpar_campos():
    url.delete(0, tk.END)
    rdMp3.deselect()
    rdMp4.deselect()
    QMp3.set('Qualidade MP3')
    QMp4.set('Qualidade MP4')
    Limagem.delete("all")

     # Limpar as listas de valores nas ComboBoxes QMp3 e QMp4
    QMp3['values'] = []
    QMp4['values'] = []

    messagebox.showinfo("Limpeza Concluída", "Limpeza efetuada com sucesso!")
# -------------------------------------------------------------------------------------------
# Mostra a qualidade nas comboboxes  ---------------------------------------------------------
def mostrar_qualidade():
    url_str = url.get()
    if not url_str:
        return

    yt = YouTube(url_str)

    if rdMp3_var.get() == "MP3":
        # Mostrar qualidade de áudio na ComboBox QMp3
        audio_qualities = [f"{stream.abr}" for stream in yt.streams.filter(only_audio=True, file_extension='mp4')]
        QMp3['values'] = audio_qualities
        QMp3.set('Qualidade MP3')  # Defina o valor padrão para QMp3

    elif rdMp4_var.get() == "MP4":
        # Mostrar qualidade de vídeo na ComboBox QMp4
        video_qualities = [f"{stream.resolution} {stream.abr}" for stream in yt.streams.filter(file_extension='mp4')]
        QMp4['values'] = video_qualities
        QMp4.set('Qualidade MP4')  # Defina o valor padrão para QMp4
# ---------------------------------------------------------------------------------------------
# mostra a imagem em Limagem ------------------------------------------------------------------        
def mostrar():
    messagebox.showinfo('Processar', 'A processar dados Pf Aguarde ...')

    url_str = url.get()
    if not url_str:
        messagebox.showwarning('Aviso', 'URL inválida.')
        return

    try:
        yt = YouTube(url_str)
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao processar URL: {str(e)}')
        return

    video_title = yt.title
    messagebox.showinfo("Título do Vídeo", f'Título do vídeo: {video_title}')

    mostrar_qualidade()  # Chama a função para mostrar as qualidades

    # Exibir a imagem de capa
    img_url = yt.thumbnail_url
    response = requests.get(img_url)
    img_data = Image.open(BytesIO(response.content))

    # Redimensionar a imagem para as dimensões do Canvas
    canvas_width = Limagem.winfo_reqwidth()
    canvas_height = Limagem.winfo_reqheight()
    img_data = img_data.resize((canvas_width, canvas_height))

    img = ImageTk.PhotoImage(img_data)

    # Crie a imagem usando as dimensões do Canvas
    Limagem.create_image(0, 0, anchor='nw', image=img)
    Limagem.image = img  # Para evitar a coleta de lixo

    # Atualizar valores nas ComboBoxes após mostrar a imagem
    mostrar_qualidade()
#----------------------------------------------------------------------------------------------
# função para fazer o download ----------------------------------------------------------------       
def download():
    url_str = url.get()
    if not url_str:
        return

    yt = YouTube(url_str)

    if rdMp3_var.get() == "MP3":
        selected_quality = QMp3.get()
        stream = yt.streams.filter(only_audio=True, abr=selected_quality).first()
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            stream.download(filename=file_path)
            mensagem = f'Downloaded MP3: {stream.title}'
            messagebox.showinfo('Download Mp3', mensagem + ' concluído com sucesso')

    elif rdMp4_var.get() == "MP4":
        selected_quality = QMp4.get()
        stream = yt.streams.filter(file_extension='mp4', resolution=selected_quality.split()[0]).first()
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            stream.download(filename=file_path)
            mensagem = f'Downloaded MP4: {stream.title}'
            messagebox.showinfo('Download Mp4', mensagem + ' concluído com sucesso')
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# cria o frontend -----------------------------------------------------------------------------
# configuração do formulario ------------------------------------------------------------------
Janela = customtkinter.CTk()
Janela.geometry('617x591+100+100')
Janela.resizable(False, False)
Janela.title('Youtube Downloader V1 Dev Joel Portugal')
Janela.iconbitmap('icon.ico')
#----------------------------------------------------------------------------------------------
# criar a barra para inserir o Url ------------------------------------------------------------
url = customtkinter.CTkEntry(Janela, width=590, placeholder_text='Insira a URL do Youtube')
url.place(x=10, y=10)
#----------------------------------------------------------------------------------------------
# criar o Radiobuton Mp3 ----------------------------------------------------------------------
rdMp3_var = tk.StringVar()
rdMp3 = customtkinter.CTkRadioButton(Janela, text='Formato MP3', variable=rdMp3_var, value="MP3")
rdMp3.place(x=50, y=55)
#----------------------------------------------------------------------------------------------
# criar o radiobuton mp4 ----------------------------------------------------------------------
rdMp4_var = tk.StringVar()
rdMp4 = customtkinter.CTkRadioButton(Janela, text='Formato MP4', variable=rdMp4_var, value="MP4")
rdMp4.place(x=185, y=55)
#-----------------------------------------------------------------------------------------------
# criar a combobox que contem os valores de Qualidade Mp3 -------------------------------------
QMp3 = Combobox(Janela, width=19, font=('Arial 17'))
QMp3.place(x=10, y=115)
QMp3.set('Qualidade MP3')
#----------------------------------------------------------------------------------------------
# criar a combobox que contem os valores de Qualidade Mp4 -------------------------------------
QMp4 = Combobox(Janela, width=19, font=('arial 17'))
QMp4.place(x=350, y=115)
QMp4.set('Qualidade MP4')
#----------------------------------------------------------------------------------------------
# criar o botão Dwonload ----------------------------------------------------------------------
Bdown = customtkinter.CTkButton(Janela, text='Download', command=download)
Bdown.place(x=10, y=155)
#----------------------------------------------------------------------------------------------
# criar o Botão  Mostrar ----------------------------------------------------------------------
BMostrar = customtkinter.CTkButton(Janela, text='Mostrar', command=mostrar)
BMostrar.place(x=155, y=155)
#----------------------------------------------------------------------------------------------
# criar O botão Limpar ------------------------------------------------------------------------
BLimpar = customtkinter.CTkButton(Janela, text='Limpar', command=limpar_campos)
BLimpar.place(x=300, y=155)
# ---------------------------------------------------------------------------------------------
# criar o botão sair --------------------------------------------------------------------------
BSair = customtkinter.CTkButton(Janela, text='Sair', command=Sair_programa)
BSair.place(x=445, y=155)
#----------------------------------------------------------------------------------------------
# criar o painel para exbir a imagem do video -------------------------------------------------
Limagem = customtkinter.CTkCanvas(Janela)
Limagem.place(x=10, y=255)
Limagem.config(width=730, height=430)
#----------------------------------------------------------------------------------------------
# iniciar a janela ----------------------------------------------------------------------------
Janela.mainloop()
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------