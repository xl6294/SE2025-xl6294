#include <LiquidCrystal.h>
#include <DHT.h>

// ----- DHT11 setup -----
#define DHTPIN   8
#define DHTTYPE  DHT11
DHT dht(DHTPIN, DHTTYPE);

// ----- LCD setup (RS, E, D4, D5, D6, D7) -----
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

// ----- Timing controls -----
const unsigned long SAMPLE_MS = 60000;  // <--- Change this to set sensor read interval
unsigned long lastSample = 0;

// ----- CSV header string -----
const char* CSV_HEADER = "t_s,temperature_C,humidity_pct";
bool headerSent = false;

void setup() {
  Serial.begin(115200);   // serial logging
  dht.begin();

  lcd.begin(16, 2);
  lcd.print("DHT11 + LCD");
  delay(1500);
  lcd.clear();

  // Print header at startup
  Serial.println(CSV_HEADER);
  headerSent = true;
}

void loop() {
  unsigned long now = millis();

  // Check if user typed something in Serial
  if (Serial.available()) {
    char c = toupper(Serial.read());   // read a character, uppercase
    if (c == 'H') {
      Serial.println(CSV_HEADER);      // on-demand header print
    }
  }

  // ----- Time-based sampling -----
  if (now - lastSample < SAMPLE_MS) return;
  lastSample = now;

  // Read sensor
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) return;

  // ----- LCD output -----
  lcd.setCursor(0,0);
  lcd.print("Temp: ");
  lcd.print(t,1);
  lcd.print("C   ");

  lcd.setCursor(0,1);
  lcd.print("Humidity: ");
  lcd.print(h,1);
  lcd.print("%  ");

  // ----- Serial CSV output -----
  Serial.print(now/1000.0, 1); Serial.print(',');
  Serial.print(t, 1);          Serial.print(',');
  Serial.println(h, 1);
}