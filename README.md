# macOS App Distribution Tools

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgray)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📝 Descrizione
Una raccolta di strumenti e guide per la distribuzione di applicazioni Python su macOS, includendo:
- Script per la creazione automatica di file DMG
- Guida completa alla compilazione con PyInstaller
- Template per setup e configurazione dell'ambiente

## 🛠️ Componenti
1. **DMG Creator Script** (`create_dmg_for_app.py`)
   - Creazione automatica di DMG da applicazioni .app
   - Configurazione personalizzabile via JSON
   - Supporto per background e layout personalizzati
   - Gestione automatica dei link ad Applications

2. **Guida alla Compilazione** (`docs/Guida_Compilazione_Mac.md`)
   - Processo dettagliato di build con PyInstaller
   - Script per bash e zsh
   - Configurazione dell'offuscamento del codice
   - Best practices per la distribuzione

## 📋 Requisiti
- macOS 10.14+
- Python 3.9+
- PyInstaller 6.11.0+
- create-dmg
- Homebrew (per installazione create-dmg)

## 🚀 Installazione
```bash
# Clona il repository
git clone https://github.com/yourusername/macos-app-distribution-tools.git

# Installa create-dmg via Homebrew
brew install create-dmg

# Crea e attiva l'ambiente conda
chmod +x create_env.sh
./create_env.sh
```

## 💻 Utilizzo

### Creazione DMG
```python
python create_dmg_for_app.py
```

Lo script ti guiderà attraverso:
1. Selezione dell'applicazione .app
2. Configurazione del DMG
3. Creazione del file DMG finale

### Configurazione Personalizzata
Crea un file `dmg_config.json`:
```json
{
    "app_name": "Your App Name",
    "size": "200m",
    "filesystem": "HFS+",
    "volume_name": "Your-App-Name",
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

## 📚 Struttura del Progetto
```plaintext
macos-app-distribution-tools/
├── create_dmg_for_app.py
├── create_env.sh
├── create_env.zsh
├── requirements.txt
├── setup.py
├── docs/
│   └── Guida_Compilazione_Mac.md
└── utils/
    └── dmg_config.json
```

## 📖 Documentazione
Per una guida dettagliata al processo di build e distribuzione, consulta:
- [Guida alla Compilazione](docs/Guida_Compilazione_Mac.md)
- [Configurazione DMG](docs/dmg_configuration.md)

## 🤝 Contribuire
1. Fork del repository
2. Crea un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza
Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 👥 Autori
- Antonio Demarcus ([@AntonioDEM](https://github.com/AntonioDEM))

## 📧 Contatti
Antonio Demarcus - iperstatica@gmail.com

Project Link: [https://github.com/AntonioDEM/macOS-App-Distribution-Tools](https://github.com/AntonioDEM/macOS-App-Distribution-Tools)
