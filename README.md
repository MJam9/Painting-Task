# Painting Task

Kleine Hilfs-App zum zufälligen Auswählen und Verwalten von Painting-Themen.
Einfache Kivy-App zum Hinzufügen, Kategorisieren und Zufallsauswählen von Themen.

**Features**
- Themen hinzufügen, Kategorien zuweisen
- Zufällige Auswahl eines Themas
- Themen löschen (in `Thema-Kategorie zuweisen`)

## Installation
- Python 3.8+
- Kivy (z. B. `pip install kivy`)

**Installation**
1. Klone das Repository oder lade die Dateien herunter.
2. Erstelle ein virtuelles Environment (empfohlen) und installiere Abhängigkeiten:

```bash
python -m venv .venv
.
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install kivy
```

**Starten**

```bash
python main.py
```

Die App öffnet sich im Desktop-Fenster.

**Wichtige Dateien**
- `main.py` — App-Start, ScreenManager
- `main.kv` — Root-Layout
- `screens/` — einzelne Screens und `.kv`-Dateien
- `utils.py`, `data.json` — Datenpersistenz

**Lizenz**
- Frei zur privaten Nutzung; bei Veröffentlichung bitte Autor angeben.
