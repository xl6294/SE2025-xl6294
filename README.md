# Arduino Class Assignments (Uno R3)

[![Build all Uno sketches](https://github.com/xl6294/SE2025-xl6294/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/<user>/<repo>/actions/workflows/build.yml)

Weekly assignments for my Arduino course, built and tested with:
- **Arduino CLI**
- **VS Code tasks**
- **GitHub Actions CI**

---

## 🗂 Layout
```
src/
  week01_blink/week01_blink.ino
  week02_dht_lcd/week02_dht_lcd.ino
  weekNN_project/weekNN_project.ino
```

---

## ⚙️ Local Build

Install AVR core and required libraries (one time):
```bash
arduino-cli core install arduino:avr
arduino-cli lib install "LiquidCrystal" "DHT sensor library" "Adafruit Unified Sensor"
```

Compile a sketch:
```bash
arduino-cli compile --fqbn arduino:avr:uno src/week02_dht_lcd
```

Upload to Uno (replace port if needed):
```bash
arduino-cli upload -p /dev/cu.usbmodem21101 --fqbn arduino:avr:uno src/week02_dht_lcd
```

---

## 🖥️ VS Code tasks

This repo includes `.vscode/tasks.json` for automation:

- **Ctrl+Shift+B** → compile active sketch  
- **Terminal → Run Task → Arduino: Upload (active sketch)** → upload to Uno  
- **Terminal → Run Task → Arduino: Monitor (9600)** → open Serial Monitor  

---

## 🤖 GitHub Actions CI

GitHub builds all `.ino` sketches under `src/` automatically on every push and pull request.  
Badge above reflects the latest build status.

---

## 📝 Adding a New Assignment

1. Create a folder:
   ```bash
   mkdir src/week03_servo
   ```
2. Add a matching `.ino` file inside:
   ```
   src/week03_servo/week03_servo.ino
   ```
3. Write your code.  
4. Open `.ino` in VS Code → compile/upload.  
5. Commit and push.  
6. If new libraries are required:  
   - Install locally with `arduino-cli lib install "LibraryName"`  
   - Add to `.github/workflows/build.yml` under library installs.  

---

✅ With this setup:
- Each assignment lives in its own folder.  
- You can build/upload easily in VS Code.  
- GitHub ensures every sketch compiles via CI.  
