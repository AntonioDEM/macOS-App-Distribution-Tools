# Indice
- [Guida alla Compilazione di LaTeX Glossary Editor per macOS](#guida-alla-compilazione-di-latex-glossary-editor-per-macos)
  
  - [1. Setup e Requisiti](#1-setup-e-requisiti)
  - [1.1 File setup.py](#11-file-setuppy)
  - [1.2 Requirements.txt](#12-requirementstxt)
  - [1.3 Script per Creazione Ambiente](#13-script-per-creazione-ambiente)
  
  - [2. Struttura File Spec](#2-struttura-file-spec)
  - [3. Script Build per Bash](#3-script-build-per-bash)
  - [4. Script Build per Zsh](#4-script-build-per-zsh)
  - [5. Processo di Build](#5-processo-di-build)
  - [6. Note Importanti](#6-note-importanti)
  
- [Guida Estesa al Build e Creazione DMG](#guida-estesa-al-build-e-creazione-dmg)
  - [7. Struttura Directory Consigliata](#7-struttura-directory-consigliata)
  - [8. Script DMG Migliorato](#8-script-dmg-migliorato)
  - [9. Configurazione DMG](#9-configurazione-dmg)
  - [10. Script Build Integrato (ZSH)](#10-script-build-integrato-zsh)
  - [11. Miglioramenti allo Script `create_dmg_for_app.py`](#5-miglioramenti-allo-script-create_dmg_for_apppy)

## 1. Setup e Requisiti

### 1.1 File setup.py
```python
from setuptools import setup, find_packages

setup(
    name="LaTeX Glossary Editor",
    version="1.0.0",
    description="Un editor grafico per la gestione di glossari LaTeX",
    author="Antonio Demarcus",
    author_email="antonio.demarcus@example.com",
    packages=find_packages(),
    install_requires=[
        'tkinter',
        'ttkthemes>=3.2.2',
        'Pillow>=9.0.0',
        'pathlib>=1.0.1',
        'sqlite3',
    ],
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.9',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Text Processing :: Markup :: LaTeX',
    ],
)
```

### 1.2 Requirements.txt
```plaintext
# Python version
python>=3.9.0

# GUI e immagini
tkinter
ttkthemes>=3.2.2
Pillow>=9.0.0

# Gestione file e sistema
pathlib>=1.0.1

# Database
sqlite3

# Build e distribuzione
pyinstaller>=6.11.0
setuptools>=42.0.0
wheel>=0.37.0

# Creazione DMG
create-dmg>=1.0.0

# Development tools
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
```

### 1.3 Script per Creazione Ambiente

Per BASH:

```bash
#!/bin/bash

# create_env.sh
echo "Creazione ambiente per LaTeX Glossary Editor..."

# Verifica se conda è installato
if ! command -v conda &> /dev/null; then
    echo "Conda non trovato. Installare Miniconda o Anaconda."
    exit 1
fi

# Nome dell'ambiente
ENV_NAME="glossary_env"

# Crea l'ambiente con Python 3.9
echo "Creando ambiente conda '$ENV_NAME' con Python 3.9..."
conda create -n $ENV_NAME python=3.9 -y

# Attiva l'ambiente
echo "Attivando l'ambiente..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Installa i requisiti
echo "Installando i requisiti..."
pip install -r requirements.txt

# Verifica l'installazione di create-dmg
if ! command -v create-dmg &> /dev/null; then
    echo "Installazione create-dmg..."
    brew install create-dmg
fi

# Verifica lo stato dell'installazione
echo "Verifica delle installazioni..."
python -c "import tkinter; import ttkthemes; import PIL" && echo "Dipendenze GUI OK" || echo "Errore dipendenze GUI"
python -c "import pathlib; import sqlite3" && echo "Dipendenze sistema OK" || echo "Errore dipendenze sistema"
pyinstaller --version && echo "PyInstaller OK" || echo "Errore PyInstaller"
create-dmg --version && echo "create-dmg OK" || echo "Errore create-dmg"

echo "Setup completato!"
echo "Per attivare l'ambiente: conda activate $ENV_NAME"
```

Per ZSH:
```zsh
#!/bin/zsh

# create_env.zsh
echo "Creazione ambiente per LaTeX Glossary Editor..."

# Verifica se conda è installato
if ! command -v conda &> /dev/null; then
    echo "Conda non trovato. Installare Miniconda o Anaconda."
    exit 1
fi

# Nome dell'ambiente
ENV_NAME="glossary_env"

# Crea l'ambiente con Python 3.9
echo "Creando ambiente conda '$ENV_NAME' con Python 3.9..."
conda create -n $ENV_NAME python=3.9 -y

# Attiva l'ambiente
echo "Attivando l'ambiente..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Installa i requisiti
echo "Installando i requisiti..."
pip install -r requirements.txt

# Verifica l'installazione di create-dmg
if ! command -v create-dmg &> /dev/null; then
    echo "Installazione create-dmg..."
    brew install create-dmg
fi

# Verifica lo stato dell'installazione
echo "Verifica delle installazioni..."
python -c "import tkinter; import ttkthemes; import PIL" && echo "Dipendenze GUI OK" || echo "Errore dipendenze GUI"
python -c "import pathlib; import sqlite3" && echo "Dipendenze sistema OK" || echo "Errore dipendenze sistema"
pyinstaller --version && echo "PyInstaller OK" || echo "Errore PyInstaller"
create-dmg --version && echo "create-dmg OK" || echo "Errore create-dmg"

echo "Setup completato!"
echo "Per attivare l'ambiente: conda activate $ENV_NAME"
```

I nuovi capitoli forniscono:
1. Un file `setup.py` completo per la distribuzione del pacchetto
2. Un file `requirements.txt` comprensivo con tutte le dipendenze necessarie
3. Script di setup dell'ambiente sia per bash che per zsh, con:
   - Creazione ambiente conda
   - Installazione dipendenze
   - Verifica dell'installazione
   - Gestione degli errori
   - Supporto per create-dmg tramite Homebrew

# Guida alla Compilazione di LaTeX Glossary Editor per macOS

## 2. Struttura File Spec

```python
# glossary_editor.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='YOUR_SECRET_KEY')  # Per offuscare il codice

a = Analysis(
    ['LaTeX-Glossary-Editor/glossary_editor.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LaTeX-Glossary-Editor/abt/*', 'abt'),
        ('LaTeX-Glossary-Editor/src/*', 'src'),
    ],
    hiddenimports=[
        'tkinter',
        'ttkthemes',
        'PIL',
        'pathlib',
        're',
        'sqlite3',
        'datetime',
        'os',
        'platform',
        'threading',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=True  # Importante per l'offuscamento
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LaTeX Glossary Editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

app = BUNDLE(
    exe,
    name='LaTeX Glossary Editor.app',
    bundle_identifier='com.antonioDEM.latexglossaryeditor',
    info_plist={
        'CFBundleName': 'LaTeX Glossary Editor',
        'CFBundleDisplayName': 'LaTeX Glossary Editor',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': 'True'
    }
)
```

## 3. Script Build per Bash
```bash
#!/bin/bash

# Definisci i percorsi
BUILD_DIR="$HOME/Documents/build"
PROJECT_DIR="$HOME/Documents/LaTeX-Glossary-Editor"
SPEC_FILE="$BUILD_DIR/glossary_editor.spec"

# Crea directory build se non esiste
mkdir -p "$BUILD_DIR"

# Copia il file spec nella directory build
cp glossary_editor.spec "$BUILD_DIR/"

# Vai alla directory di build
cd "$BUILD_DIR"

# Pulisci le build precedenti
rm -rf build dist

# Esegui pyinstaller con offuscamento
pyinstaller "$SPEC_FILE" --clean --noconfirm --key "YOUR_SECRET_KEY"

# Crea il DMG usando il tuo script Python
python3 create_dmg_for_app.py
```

## 4. Script Build per Zsh
```zsh
#!/bin/zsh

# Definisci i percorsi
BUILD_DIR="${HOME}/Documents/build"
PROJECT_DIR="${HOME}/Documents/LaTeX-Glossary-Editor"
SPEC_FILE="${BUILD_DIR}/glossary_editor.spec"

# Crea directory build se non esiste
mkdir -p "${BUILD_DIR}"

# Inizializza conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate kivy_env

# Copia il file spec nella directory build
cp glossary_editor.spec "${BUILD_DIR}/"

# Vai alla directory di build
cd "${BUILD_DIR}"

# Pulisci le build precedenti
rm -rf build dist

# Esegui pyinstaller con offuscamento
pyinstaller "${SPEC_FILE}" --clean --noconfirm --key "YOUR_SECRET_KEY"

# Crea il DMG usando il tuo script Python
python3 create_dmg_for_app.py

# Disattiva l'ambiente conda
conda deactivate
```

## 5. Processo di Build
1. Posiziona il file .spec fuori dalla cartella del progetto
2. Crea una cartella `build` fuori dal progetto:
```bash
mkdir ~/Documents/build
```

3. Copia i file necessari:
```bash
cp glossary_editor.spec ~/Documents/build/
cp create_dmg_for_app.py ~/Documents/build/
```

4. Rendi eseguibile lo script di build:
```bash
chmod +x build_mac.sh
```

5. Esegui lo script:
```bash
./build_mac.sh
```

## 6. Note Importanti
- La chiave di offuscamento (`YOUR_SECRET_KEY`) deve essere almeno 16 caratteri
- L'offuscamento del codice è ottenuto tramite:
  - Uso di `block_cipher`
  - Flag `--key` in PyInstaller
  - `noarchive=True` nel file spec
- Il file DMG viene creato automaticamente usando il tuo script Python
- Tutti i file temporanei vengono creati nella cartella `build`

# Guida Estesa al Build e Creazione DMG

## 7. Struttura Directory Consigliata
```plaintext
build/
├── glossary_editor.spec
├── build_mac.sh (o build_mac.zsh)
├── create_dmg_for_app.py
└── utils/
    └── dmg_config.json
```

## 8. Script DMG Migliorato
```python
# create_dmg_for_app.py con miglioramenti

import os
import subprocess
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import json

class DMGCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Configurazione default
        self.config = {
            'app_name': 'LaTeX Glossary Editor',
            'size': '200m',
            'filesystem': 'HFS+',
            'volume_name': 'LaTeX-Glossary-Editor'
        }
        
    def load_config(self, config_path):
        """Carica configurazione da file JSON"""
        try:
            with open(config_path, 'r') as f:
                self.config.update(json.load(f))
        except Exception as e:
            print(f"Warning: Impossibile caricare config, uso defaults: {e}")

    def auto_detect_app(self, build_dir):
        """Cerca automaticamente il .app nella directory dist"""
        dist_dir = os.path.join(build_dir, 'dist')
        apps = list(Path(dist_dir).glob('*.app'))
        if apps:
            return str(apps[0])
        return None

    def create_dmg(self, app_path, output_dir):
        """Versione migliorata della creazione DMG"""
        try:
            app_name = self.config['app_name']
            paths = {
                'tmp_dmg': os.path.join(output_dir, "tmp.dmg"),
                'final_dmg': os.path.join(output_dir, f"{app_name}.dmg"),
                'volume': f"/Volumes/{app_name}-tmp"
            }

            # Cleanup precedenti DMG
            for dmg in [paths['tmp_dmg'], paths['final_dmg']]:
                if os.path.exists(dmg):
                    os.remove(dmg)

            # Crea DMG temporaneo
            subprocess.run([
                "hdiutil", "create",
                "-size", self.config['size'],
                "-fs", self.config['filesystem'],
                "-volname", self.config['volume_name'],
                "-o", paths['tmp_dmg']
            ], check=True)

            # Monta, copia, smonta
            subprocess.run(["hdiutil", "attach", paths['tmp_dmg']], check=True)
            time.sleep(2)  # Attesa per il mount
            
            # Copia l'app e aggiungi link ad Applications
            subprocess.run(["cp", "-R", app_path, paths['volume']], check=True)
            subprocess.run([
                "ln", "-s", 
                "/Applications", 
                f"{paths['volume']}/Applications"
            ], check=True)

            # Smonta e converti
            subprocess.run(["hdiutil", "detach", paths['volume']], check=True)
            subprocess.run([
                "hdiutil", "convert",
                paths['tmp_dmg'],
                "-format", "UDZO",
                "-o", paths['final_dmg']
            ], check=True)

            # Cleanup
            os.remove(paths['tmp_dmg'])
            
            return paths['final_dmg']

        except Exception as e:
            raise Exception(f"Errore nella creazione del DMG: {e}")

def main():
    creator = DMGCreator()
    
    # Carica config se presente
    config_path = Path(__file__).parent / 'utils' / 'dmg_config.json'
    if config_path.exists():
        creator.load_config(str(config_path))

    # Auto-detect del .app nella directory dist
    build_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = creator.auto_detect_app(build_dir)
    
    if not app_path:
        # Fallback alla selezione manuale
        app_path = filedialog.askopenfilename(
            title="Seleziona il .app",
            filetypes=[("Application", "*.app")],
            initialdir=os.path.join(build_dir, 'dist')
        )
        
    if not app_path:
        print("Operazione cancellata")
        return

    output_dir = os.path.join(build_dir, 'dist')
    try:
        dmg_path = creator.create_dmg(app_path, output_dir)
        messagebox.showinfo(
            "Successo", 
            f"DMG creato con successo:\n{dmg_path}"
        )
    except Exception as e:
        messagebox.showerror("Errore", str(e))

if __name__ == "__main__":
    main()
```

## 9. Configurazione DMG
```json
// utils/dmg_config.json
{
    "app_name": "LaTeX Glossary Editor",
    "size": "200m",
    "filesystem": "HFS+",
    "volume_name": "LaTeX-Glossary-Editor",
    "background_image": "background.png",
    "window_position": {
        "x": 200,
        "y": 120
    },
    "window_size": {
        "width": 600,
        "height": 400
    },
    "icon_size": 100
}
```

## 10. Script Build Integrato (ZSH)
```zsh
#!/bin/zsh

# Funzione di cleanup
cleanup() {
    echo "Eseguo cleanup..."
    rm -rf build/temp
    conda deactivate
}

# Trap per intercettare interruzioni
trap cleanup EXIT

# Configurazioni
BUILD_DIR="${HOME}/Documents/build"
PROJECT_DIR="${HOME}/Documents/LaTeX-Glossary-Editor"
SPEC_FILE="${BUILD_DIR}/glossary_editor.spec"
SECRET_KEY="YOUR_SECRET_KEY_HERE"  # Almeno 16 caratteri

# Crea struttura directory
echo "Preparazione ambiente di build..."
mkdir -p "${BUILD_DIR}/temp"
mkdir -p "${BUILD_DIR}/utils"

# Copia file necessari
cp "${PROJECT_DIR}/glossary_editor.spec" "${BUILD_DIR}/"
cp "${PROJECT_DIR}/create_dmg_for_app.py" "${BUILD_DIR}/"
cp "${PROJECT_DIR}/utils/dmg_config.json" "${BUILD_DIR}/utils/"

# Attiva ambiente conda
source ~/miniconda3/etc/profile.d/conda.sh
conda activate kivy_env

# Build principale
echo "Avvio build principale..."
cd "${BUILD_DIR}"
pyinstaller "${SPEC_FILE}" --clean --noconfirm --key "${SECRET_KEY}"

# Creazione DMG
if [ $? -eq 0 ]; then
    echo "Build completato, creazione DMG..."
    python3 create_dmg_for_app.py
else
    echo "Errore durante il build"
    exit 1
fi
```

## 11. Miglioramenti allo Script `create_dmg_for_app.py`
Lo script è stato migliorato con:
- Gestione automatica del path dell'app
- Configurazione esterna in JSON
- Gestione degli errori più robusta
- Aggiunta automatica del link ad Applications
- Pulizia automatica dei file temporanei
- Supporto per il background e la personalizzazione della finestra del DMG
- Integrazione migliore con il processo di build

Per usare questa versione migliorata:
1. Crea la struttura delle directory
2. Copia i file nelle posizioni corrette
3. Modifica la configurazione in `dmg_config.json` secondo le tue esigenze
4. Esegui lo script di build
