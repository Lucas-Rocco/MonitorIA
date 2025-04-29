import serial
import cv2
import time
import tkinter as tk
from tkinter import Button, Label
from cvzone.HandTrackingModule import HandDetector
from PIL import Image, ImageTk
import threading
import os
import sys

# Configura a comunicação serial com o Arduino (Substitua 'COM7' pela sua porta)
arduino = serial.Serial()

# Variáveis de controle globais
controle_de_acoes = 0
centralizado_inicio = None
centralizado_por_10_segundos = False
centralizado_persistente = False
ultimo_envio_serial = time.time()
intervalo_envio_serial = 0  # Intervalo de 1 segundo entre os envios

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera!")
    exit()

# Configura o detector de mãos
detector = HandDetector(detectionCon=0.7)

# Função para encerrar o programa
def fechar_programa():
    cap.release()
    cv2.destroyAllWindows()
    window.quit()

# Função para reiniciar o código
def reiniciar_programa():
    cap.release()  # Libera a câmera
    cv2.destroyAllWindows()  # Fecha as janelas do OpenCV
    os.execl(sys.executable, sys.executable, *sys.argv)  # Reinicia o script

# Função para animar a mudança do menu lateral
def toggle_menu():
    global menu_aberto
    if not menu_aberto:
        menu_aberto = True
        menu.place(x=0, y=0, relwidth=0.25, relheight=1)
        menu.after(100, menu.config(width=0))  # Finaliza a animação de transição do menu
        menu.config(bg="#2f2f2f")
    else:
        menu_aberto = False
        menu.place_forget()

# Função para atualizar a imagem da câmera
def atualizar_frame():
    global controle_de_acoes, centralizado_inicio, centralizado_por_10_segundos, centralizado_persistente, ultimo_envio_serial  # Declare as variáveis globais
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o frame da webcam!")
        return

    frame_height, frame_width = frame.shape[:2]
    center_x = frame_width // 2
    center_y = frame_height // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    closest_face = None
    closest_distance = float('inf')

    for (x, y, w, h) in faces:
        face_center_x = x + w // 2
        face_center_y = y + h // 2
        distance_to_center = abs(face_center_x - center_x) + abs(face_center_y - center_y)

        if distance_to_center < closest_distance:
            closest_distance = distance_to_center
            closest_face = (x, y, w, h)

    if closest_face is not None:
        x, y, w, h = closest_face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        face_center_x = x + w // 2
        face_center_y = y + h // 2

    hands, img = detector.findHands(frame)

    # Aqui seria o código de controle para os movimentos, como já vimos anteriormente...
    # E atualizando a imagem da câmera...

    # Atualiza a interface com a imagem da câmera
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = img.resize((640, 480))  # Ajuste conforme necessário
    img_tk = ImageTk.PhotoImage(img)

    label_camera.img_tk = img_tk
    label_camera.config(image=img_tk)

    window.after(10, atualizar_frame)  # Chama novamente para manter a captura contínua

# Função para alterar o botão
def hover_effect(event):
    event.widget.config(bg="#44b3c2")

def leave_effect(event):
    event.widget.config(bg="#00b3b3")

# Funções para os botões de controle
def subir():

    arduino.write(b'D')
    label_status.config(text="Subindo")

def descer():

    arduino.write(b'U')
    label_status.config(text="Descendo")

def parar():

    arduino.write(b'H')
    label_status.config(text="Parado")

# Configuração da janela do Tkinter
window = tk.Tk()
window.title("TCC MONITOR IA-JUSTÁVEL")
window.geometry("1240x780")  # Tamanho da janela
window.config(bg="#1f1f1f")  # Fundo escuro

# Definindo o menu lateral e o botão para abrir/fechar
menu_aberto = False
menu = tk.Frame(window, bg="#2f2f2f", width=0, height=window.winfo_height())
menu.place(x=-250, y=0)

# Botão para abrir o menu lateral
menu_button = Button(window, text="☰", font=("Arial", 20), bg="#333333", fg="white", relief="flat", command=toggle_menu)
menu_button.place(x=10, y=10)

# Colocando os botões dentro do menu
botao_subir = Button(menu, text="Subir", font=("Arial", 15), command=subir, bg="#00b3b3", fg="white", relief="raised", bd=5)
botao_subir.pack(pady=10)

botao_descer = Button(menu, text="Descer", font=("Arial", 15), command=descer, bg="#00b3b3", fg="white", relief="raised", bd=5)
botao_descer.pack(pady=10)

botao_parar = Button(menu, text="Parar", font=("Arial", 15), command=parar, bg="#00b3b3", fg="white", relief="raised", bd=5)
botao_parar.pack(pady=10)

botao_reiniciar = Button(menu, text="Reiniciar", font=("Arial", 15), command=reiniciar_programa, bg="#00b3b3", fg="white", relief="raised", bd=5)
botao_reiniciar.pack(pady=10)

botao_sair = Button(menu, text="Sair", font=("Arial", 15), command=fechar_programa, bg="red", fg="white", relief="raised", bd=5)
botao_sair.pack(pady=10)

# Atualizar a interface com a imagem da câmera
label_camera = Label(window)
label_camera.pack(pady=20)

label_status = Label(window, text="Parado", font=("Arial", 15), bg="black", fg="white", width=40, height=2)
label_status.pack(pady=20)

# Inicia a atualização da câmera
atualizar_frame()

# Inicia a execução da interface
window.mainloop()
