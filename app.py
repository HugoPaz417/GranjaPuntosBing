import tkinter as tk
from tkinter import messagebox
import requests
import time
import pyautogui
import os

CURRENT_VERSION = "1.0.0"
VERSION_URL = "https://example.com/version.json"

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
    for _ in range(30):
        pyautogui.press("tab")
        time.sleep(0.01)
    time.sleep(2)
    for i in range(4):
        if i != 3:
            pyautogui.press("tab")
            pyautogui.press("tab")
        else:
            pyautogui.press("tab")
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.hotkey("ctrl", "w")
        time.sleep(1)
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

def check_for_updates():
    try:
        response = requests.get(VERSION_URL)
        if response.status_code == 200:
            data = response.json()
            latest_version = data["version"]
            download_url = data["download_url"]

            if latest_version > CURRENT_VERSION:
                if messagebox.askyesno("Actualización disponible", f"Hay una nueva versión ({latest_version}). ¿Desea descargarla?"):
                    download_update(download_url)
            else:
                messagebox.showinfo("Actualización", "Ya tiene la última versión.")
        else:
            messagebox.showerror("Error", "No se pudo verificar actualizaciones.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al verificar actualizaciones: {e}")

def download_update(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open("update.exe", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            messagebox.showinfo("Actualización", "Descarga completada. Ejecute 'update.exe' para instalar la nueva versión.")
            os.startfile("update.exe")
        else:
            messagebox.showerror("Error", "No se pudo descargar la actualización.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar la actualización: {e}")

root = tk.Tk()
root.title("Buscador Automático")
root.geometry("300x200")

tk.Label(root, text="Palabras a buscar:").pack(pady=5)
entry_cantidad = tk.Entry(root)
entry_cantidad.insert(0, "30")
entry_cantidad.pack(pady=5)

tk.Button(root, text="Iniciar", command=iniciar_busquedas).pack(pady=10)
tk.Button(root, text="Buscar actualizaciones", command=check_for_updates).pack(pady=5)

root.mainloop()
