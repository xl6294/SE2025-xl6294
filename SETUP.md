# Project Setup

## Requirements
- Arduino IDE or VS Code with Arduino CLI
- Python 3.8+
- VS Code recommended with Python extension

---

## Arduino Development

### Build and Upload
Use Arduino IDE or VS Code tasks to build and upload the sketch to your Elegoo Uno R3.

### Serial Monitor
Default baud for logging is **115200** (but can be changed). Ensure Serial Monitor or logger matches the baud rate set in your `.ino` sketch.

---

## 📊 CSV Logging with Python (VS Code dropdown for baud)

We log sensor data by printing CSV from the sketch and capturing it with a Python script.

### Prereqs
Create a virtual environment and install pyserial:
```bash
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install pyserial
```

### Where logs go
By default logs are saved under `~/Downloads/arduino_logs`.  
Each file is named by the start of its interval, e.g. `2025-09-23_14-00.csv`.

### Order of operations
1. **Connect Uno via USB.**
2. **Upload sketch** (close any Serial Monitor afterwards).
3. **Activate venv if not already:**  
   ```bash
   source .venv/bin/activate
   ```
4. **Run the logger from VS Code:**  
   - Terminal → Run Task → **Logger: Run (CSV to Downloads, select baud)**
   - Choose the baud rate from the dropdown (must match `Serial.begin(...)` in your sketch).

Stop with `Ctrl+C` in terminal if running manually.

### Rotation frequency
Change this line in `tools/log_serial_logger.py` to control when new log files are created:
```python
ROTATE_EVERY = 7200  # seconds
```
Examples:
- `60` → new file every 1 min  
- `600` → every 10 min  
- `3600` → every 1 hour  
- `7200` → every 2 hours  
- `86400` → every 1 day  

### Notes
- Only one process can open the serial port at a time. Close Serial Monitor before running the logger.  
- Adjust sampling interval in your `.ino` sketch with `SAMPLE_MS`.  
