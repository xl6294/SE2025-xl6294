# Arduino DHT11 + LCD1602 Logging Project

This project uses an Elegoo Uno R3 with a DHT11 temperature/humidity sensor and a 1602 LCD display. Data is printed in CSV format over Serial for logging.

---

## Build and Upload
Use Arduino IDE or VS Code with Arduino CLI tasks to build/upload to the Uno.

---

## 📊 Logging DHT11 data to CSV

The sketch prints CSV like:
```
t_s,temperature_C,humidity_pct
0.0,24.6,48.0
2.0,24.7,48.0
```

### Quick start (VS Code)
1. Create and select the project venv the first time:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   .venv/bin/pip install pyserial
   ```
2. Upload the sketch.  
3. Close any Serial Monitor.
4. Run the VS Code task **“Logger: Run (CSV to Downloads)”**  
   – or –  
   In a terminal:
   ```bash
   python3 tools/log_serial_logger.py
   ```

### File rotation
Files are named by the start of their interval, e.g.:  
- `2025-09-23_14-00.csv` (if ROTATE_EVERY=3600 → hourly)  
- `2025-09-23_00-00.csv`, `2025-09-23_02-00.csv` (if ROTATE_EVERY=7200 → every 2 hours)

Change interval in `tools/log_serial_logger.py`:
```python
ROTATE_EVERY = 7200
```

### Tips
- Monitor at **115200** if you use the Serial Monitor.  
- Only one app can open the port at a time (close Serial Monitor before running the logger).  
- To change how often Arduino prints, edit `SAMPLE_MS` in the sketch.
