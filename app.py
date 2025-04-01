import tkinter as tk
from tkinter import messagebox
import requests
import time
import pyautogui
import os
import zipfile
import shutil
import sys

# Versión actual del programa
CURRENT_VERSION = "1.1.1"

# URL del archivo version.json en GitHub
VERSION_URL = "https://raw.githubusercontent.com/HugoPaz417/GranjaPuntosBing/main/version.json"

def abrir_edge():
    pyautogui.press("win")
    time.sleep(1)   
    pyautogui.write("Microsoft Edge")
    time.sleep(1)
    pyautogui.press("enter") 
    time.sleep(2)

def obtener_palabras(cantidad=2):
    url = f"https://api.datamuse.com/words?ml=example&max={cantidad}"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            return [palabra["word"] for palabra in respuesta.json()]
        else:
            messagebox.showerror("Error", "No se pudieron obtener palabras.")
            return []
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener palabras: {e}")
        return []

def iniciar_busquedas():
    messagebox.showinfo("Iniciando", "Tite")
    abrir_edge()
    pyautogui.write("https://rewards.bing.com/?ref=rewardspanel", interval=0.1)
    pyautogui.press("enter")
    time.sleep(3)
    for _ in range(30):
        pyautogui.press("tab")
        time.sleep(0.01)
    time.sleep(2)
    
    for i in range(4):
        pyautogui.press("tab", presses=2 if i != 3 else 1)
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
                if messagebox.askyesno("Actualización disponible", f"Hay una nueva versión ({latest_version}). ¿Desea actualizar ahora?"):
                    download_update(download_url)
            else:
                messagebox.showinfo("Actualización", "Ya tienes la última versión.")
        else:
            messagebox.showerror("Error", "No se pudo verificar actualizaciones.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al verificar actualizaciones: {e}")

def download_update(url):
    try:
        update_zip = "update.zip"
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(update_zip, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            messagebox.showinfo("Actualización", "Descarga completada. Instalando la nueva versión...")
            install_update(update_zip)
        else:
            messagebox.showerror("Error", "No se pudo descargar la actualización.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar la actualización: {e}")

def install_update(zip_path):
    try:
        temp_folder = "update_temp"
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_folder)
        
        extracted_folder = os.path.join(temp_folder, os.listdir(temp_folder)[0])
        
        for item in os.listdir(extracted_folder):
            s = os.path.join(extracted_folder, item)
            d = os.path.join(os.getcwd(), item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.move(s, d)
            else:
                shutil.move(s, d)
        
        os.remove(zip_path)
        shutil.rmtree(temp_folder)

        messagebox.showinfo("Actualización", "Actualización completada. Reiniciando aplicación...")
        restart_app()
    except Exception as e:
        messagebox.showerror("Error", f"Error al instalar la actualización: {e}")

def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Interfaz gráfica
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