# 📘 Repository Setup Guide — Arduino Class Assignments

This repository is designed to organize **weekly Arduino assignments** for an **Elegoo Uno R3 (Arduino Uno compatible)** board.  
It uses **Arduino CLI**, **VS Code tasks**, and **GitHub Actions** for continuous integration.

---

## 🗂️ Repository Structure
```
arduino-class-assignments/
├─ src/                         # All assignments live here
│  ├─ week01_blink/
│  │  └─ week01_blink.ino
│  ├─ week02_dht_lcd/
│  │  └─ week02_dht_lcd.ino
│  └─ weekNN_project/
│     └─ weekNN_project.ino
├─ .vscode/
│  └─ tasks.json                # VS Code tasks (compile, upload, monitor)
├─ .github/
│  └─ workflows/
│     └─ build.yml              # GitHub Actions (auto-compiles sketches)
├─ .gitignore                   # Ignore build artifacts
├─ README.md                    # Basic usage instructions
└─ SETUP.md                     # (this file) Repo setup documentation
```

---

## ⚙️ Naming Rules (Important)
- Each assignment has its own folder under `src/`.  
- The **folder name and `.ino` file name must match**.  
  Example:  
  ```
  src/week02_dht_lcd/week02_dht_lcd.ino
  ```

Arduino CLI requires this for compilation.

---

## 🛠️ Local Development Setup

### 1. Install Arduino CLI
- macOS:
  ```bash
  brew install arduino-cli
  ```
- Windows (PowerShell):
  ```powershell
  winget install Arduino.ArduinoCLI
  ```
- Linux:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
  sudo mv bin/arduino-cli /usr/local/bin/
  ```

Verify:
```bash
arduino-cli version
```

### 2. Install board support (AVR for Uno R3)
```bash
arduino-cli core update-index
arduino-cli core install arduino:avr
```

### 3. Install required libraries (locally)
Run these **once** on your computer:
```bash
arduino-cli lib install "LiquidCrystal"
arduino-cli lib install "DHT sensor library"
arduino-cli lib install "Adafruit Unified Sensor"
```

### 4. Verify board connection
Plug in your Elegoo Uno R3, then run:
```bash
arduino-cli board list
```
Example output:
```
/dev/cu.usbmodem21101   Arduino Uno   arduino:avr:uno
```

Take note of the port (`/dev/cu.usbmodem21101` on macOS, `COM3/COM4` on Windows).

---

## 🖥️ VS Code Integration

This repo uses **VS Code tasks** (`.vscode/tasks.json`) to automate compile, upload, and monitor.

### tasks.json (auto-detect active sketch)
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Arduino: Compile (active sketch)",
      "type": "shell",
      "command": "arduino-cli",
      "args": [
        "compile",
        "--fqbn", "arduino:avr:uno",
        "${fileDirname}"
      ],
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": []
    },
    {
      "label": "Arduino: Upload (active sketch)",
      "type": "shell",
      "command": "arduino-cli",
      "args": [
        "upload",
        "-p", "${input:serialPort}",
        "--fqbn", "arduino:avr:uno",
        "${fileDirname}"
      ],
      "problemMatcher": []
    },
    {
      "label": "Arduino: Monitor (9600)",
      "type": "shell",
      "command": "arduino-cli",
      "args": [
        "monitor",
        "-p", "${input:serialPort}",
        "-c", "baudrate=9600"
      ],
      "problemMatcher": []
    }
  ],
  "inputs": [
    {
      "id": "serialPort",
      "type": "pickString",
      "description": "Select Uno serial port",
      "options": [
        "/dev/cu.usbmodem21101",
        "/dev/cu.usbserial-XXXX",
        "COM3",
        "COM4"
      ],
      "default": "/dev/cu.usbmodem21101"
    }
  ]
}
```

### Available Tasks
- **Arduino: Compile (active sketch)** → Compiles the sketch in the currently open `.ino` folder.  
- **Arduino: Upload (active sketch)** → Uploads the compiled code to the Uno (you pick the serial port once).  
- **Arduino: Monitor (9600)** → Opens Serial Monitor at 9600 baud.

### How to Use
1. Open an `.ino` file in VS Code (e.g., `week02_dht_lcd.ino`).  
2. Press **Ctrl+Shift+B** → compiles that sketch.  
3. **Terminal → Run Task → Arduino: Upload (active sketch)** → uploads to Uno.  
4. **Terminal → Run Task → Arduino: Monitor (9600)** → opens Serial Monitor.  

---

## 🤖 Continuous Integration (CI) with GitHub Actions

This repo includes a workflow: `.github/workflows/build.yml`.  
It runs automatically on every **push** and **pull request**.

### What it does
1. Sets up Arduino CLI in a clean GitHub environment.  
2. Installs the AVR core and required libraries.  
3. Compiles every sketch in `src/`.  

### Why libraries are installed every run
- On **your local computer**: you install each library once, and Arduino CLI keeps them in `~/Arduino/libraries`.  
- On **GitHub Actions**: every workflow run uses a fresh virtual machine. Nothing is cached.  
  → That’s why `build.yml` must list **all libraries your sketches depend on**, so they are installed fresh each run.

### Rule of thumb
Whenever you add a new library to a sketch:
1. Install it locally:  
   ```bash
   arduino-cli lib install "LibraryName"
   ```
2. Add it to `build.yml` under `arduino-cli lib install` so CI also knows about it.

This ensures:
- Local builds succeed.  
- CI builds succeed.  
- Anyone else cloning your repo can see which libraries are required.

---

## 🧹 Git Ignore
`.gitignore` keeps the repo clean:
```
.vscode/*.db
.vscode/*.browse.VC.db
**/.pio/
**/.build/
*.hex
*.elf
*.bin
.DS_Store
```

---

## 📝 Adding a New Assignment
1. Make a new folder under `src/`:
   ```bash
   mkdir src/week03_servo
   ```
2. Create `src/week03_servo/week03_servo.ino`.  
3. Write your code.  
4. Open the `.ino` in VS Code.  
5. Press **Ctrl+Shift+B** to compile, then upload.  
6. Commit + push to GitHub.  
7. If you used new libraries → install them locally and add them to `build.yml`.

---

## 🚦 Example: Week02 (DHT + LCD)
- Folder: `src/week02_dht_lcd/`  
- File: `week02_dht_lcd.ino`  
- Libraries: `"LiquidCrystal"`, `"DHT sensor library"`, `"Adafruit Unified Sensor"`.  
- Upload port (on macOS): `/dev/cu.usbmodem21101`.  

---

✅ With this setup, you now have:
- **Organized weekly assignments**
- **One-click compile/upload in VS Code**
- **Auto-build on GitHub with library management**
