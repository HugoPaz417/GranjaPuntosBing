import tkinter as tk
from tkinter import messagebox
import requests
import time
import pyautogui

def abrir_edge():
    pyautogui.press("win")
    time.sleep(1)   
    pyautogui.write("Microsoft Edge")
    time.sleep(1)
    pyautogui.press("enter") 
    time.sleep(2)
def cerrar_edge():
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    
def obtener_palabras(cantidad=2):
    url = f"https://random-word-api.herokuapp.com/word?number={cantidad}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    else:
        messagebox.showerror("Error", "No se pudieron obtener palabras.")
        return []

def iniciar_busquedas():
    abrir_edge()
    pyautogui.write("https://rewards.bing.com/?ref=rewardspanel", interval=0.1)
    pyautogui.press("enter")
    time.sleep(1)
    for i in range(30):
        pyautogui.press("tab")
        time.sleep(0.01)
    time.sleep(2)
    for i in range(4):
        print("1:", i)
        if i!= 3:
            pyautogui.press("tab")
            pyautogui.press("tab")
        else:
            pyautogui.press("tab")
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "w")
        time.sleep(1)
        print("2:", i)
    try:
        cantidad = int(entry_cantidad.get())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido.")
        return
    
    busquedas = obtener_palabras(cantidad)
    if not busquedas:
        return
    
    for busqueda in busquedas:
        pyautogui.hotkey("ctrl", "t")
        time.sleep(1)
        pyautogui.write(busqueda, interval=0.2)
        time.sleep(1)
        pyautogui.press("enter")  
        time.sleep(3)
        pyautogui.hotkey("ctrl", "w")
        time.sleep(1) 
    
    messagebox.showinfo("Completado", "Búsquedas finalizadas.")


root = tk.Tk()
root.title("Buscador Automático")
root.geometry("300x150")

tk.Label(root, text="Palabras a buscar:").pack(pady=5)
entry_cantidad = tk.Entry(root)
entry_cantidad.insert(0, "30")
entry_cantidad.pack(pady=5)

tk.Button(root, text="Iniciar", command=iniciar_busquedas).pack(pady=10)

root.mainloop()
