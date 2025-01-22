import os
import subprocess
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def select_paths():
    root = tk.Tk()
    root.withdraw()

    # Mostra dialogo per selezionare la directory che contiene .app
    app_dir = filedialog.askdirectory(
        title="Seleziona la directory contente la .app",
        initialdir=os.path.expanduser("~/Desktop")
    )
    if not app_dir:
        return None, None

    # Lista tutte le .app nella directory selezionata
    apps = [f for f in os.listdir(app_dir) if f.endswith('.app')]
    if not apps:
        messagebox.showerror("Errore", "Nessun bundle .app trovato nella directory selezionata")
        return None, None

    # Crea una finestra per selezionare la .app
    selection = tk.Toplevel(root)
    selection.title("Selezioine la .app")
    
    app_var = tk.StringVar(selection)
    app_var.set(apps[0])
    
    tk.OptionMenu(selection, app_var, *apps).pack()
    
    def done():
        selection.quit()
        
    tk.Button(selection, text="Seleziona", command=done).pack()
    
    selection.mainloop()
    selection.destroy()
    
    selected_app = os.path.join(app_dir, app_var.get())
    
    # Seleziona directory output
    output_dir = filedialog.askdirectory(
        title="Seleziona la directory per il DMG",
        initialdir=app_dir
    )
    
    if not output_dir:
        return None, None

    return selected_app, output_dir

def verify_create_dmg():
   """Check if create-dmg is installed"""
   try:
       result = subprocess.run(['which', 'create-dmg'], 
                             capture_output=True, 
                             text=True)
       return (True, result.stdout.strip()) if result.returncode == 0 else (False, None)
   except Exception as e:
       print(f"Error checking create-dmg: {e}")
       return False, None

def manage_create_dmg():
   """Manage create-dmg installation"""
   try:
       installed, path = verify_create_dmg()
       
       if installed:
           response = messagebox.askyesno(
               "Create-DMG Found",
               f"create-dmg è stato trovato nella {path}. Vuoi Reinstallarlo?"
           )
           if not response:
               return True
           subprocess.run(['sudo', 'rm', path], check=True)
       
       print("Installazione di create-dmg...")
       subprocess.run(['npm', 'install', '-g', 'create-dmg'], check=True)
       
       installed, _ = verify_create_dmg()
       if not installed:
           raise Exception("Verifica dell'installazione non riuscita")
           
       return True
       
   except Exception as e:
       messagebox.showerror("Errore", f"Errore nella gestione di create-dmg: {e}")
       return False

def create_dmg(app_path, output_dir):
   """Create DMG from app bundle"""
   try:
       if not os.path.exists(app_path):
           raise Exception(f"Bundle dell'app non trovato: {app_path}")
           
       if not os.path.exists(output_dir):
           os.makedirs(output_dir)
           
       app_name = os.path.splitext(os.path.basename(app_path))[0]
       paths = {
           'tmp_dmg': os.path.join(output_dir, "tmp.dmg"),
           'final_dmg': os.path.join(output_dir, f"{app_name}.dmg"),
           'volume': f"/Volumes/{app_name}-tmp"
       }

       for dmg in [paths['tmp_dmg'], paths['final_dmg']]:
           if os.path.exists(dmg):
               os.remove(dmg)

       subprocess.run([
           "hdiutil", "create", 
           "-size", "200m", 
           "-fs", "HFS+", 
           "-volname", f"{app_name}-tmp",
           "-o", paths['tmp_dmg']
       ], check=True)

       subprocess.run(["hdiutil", "attach", paths['tmp_dmg']], check=True)
       time.sleep(2)

       subprocess.run(["cp", "-R", app_path, paths['volume']], check=True)
       subprocess.run(["hdiutil", "detach", paths['volume']], check=True)

       subprocess.run([
           "hdiutil", "convert",
           paths['tmp_dmg'],
           "-format", "UDZO",
           "-o", paths['final_dmg']
       ], check=True)

       os.remove(paths['tmp_dmg'])
       messagebox.showinfo("Success", f"DMG cerato: {paths['final_dmg']}")
       return True

   except Exception as e:
       messagebox.showerror("Errore", f"Errore nella crazione del DMG: {e}")
       return False

def main():
   app_path, output_dir = select_paths()
   if not app_path or not output_dir:
       print("Operrazione Cancellata")
       return
       
   if not manage_create_dmg():
       return
       
   create_dmg(app_path, output_dir)

if __name__ == "__main__":
   main()