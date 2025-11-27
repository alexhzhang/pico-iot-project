# 📡 **IoT Sensor Data Pipeline — Raspberry Pi Pico W, MicroPython, Flask, MySQL**

This project implements a full end-to-end IoT system where a **Raspberry Pi Pico W** collects sensor readings, transmits JSON via HTTP, and interfaces with a **Flask API** connected to a **MySQL database** for persistent storage.
Built collaboratively using a modular architecture that cleanly separates **firmware**, **backend ingestion routes**, and **database logic** into a unified data pipeline.

---

# 🏗️ **System Architecture**

```
[Pico W – MicroPython Firmware]
        │  (JSON over HTTP POST)
        ▼
[Flask API Server – Python]
        │  (SQL INSERT)
        ▼
[MySQL Database – Persistent Storage]
        ▼
[Optional Dashboard / Visualization Layer]
```

### **Embedded (Pico) Layer**

* Firmware modules: `boot.py`, `main.py`, `sensors.py`, `send.py`
* Handles Wi-Fi configuration, WebREPL access, timed sensor acquisition, and HTTP POST uploads

### **Server Layer**

* Flask API exposes `/upload` ingestion endpoint
* Validates incoming JSON packets
* Passes structured data to the database connector (`db.py`)

### **Database Layer**

* MySQL schema defined in `database/init.sql`
* Stores sensor readings, timestamps, and associated metadata

---

# 📁 **Repository Structure**

```
pico-iot-project/
│
├── pico/               # MicroPython firmware
│   ├── boot.py
│   ├── main.py
│   ├── sensors.py
│   └── send.py
│
├── server/             # Flask backend + DB interface
│   ├── server.py
│   ├── db.py
│   ├── config.py
│   └── requirements.txt
│
├── database/           # SQL schema + notes
│   ├── init.sql
│   └── schema_notes.md
│
├── dashboard/          # Future visualization layer
│   ├── app.py
│   ├── templates/
│   └── static/
│
├── .gitignore
└── README.md
```

---

# ⚙️ **Setup Instructions**

## **1. Install Dependencies (PC Backend)**

```
cd server
pip install -r requirements.txt
```

## **2. Initialize MySQL Database**

Configure MySQL, then run:

```
mysql -u root -p < database/init.sql
```

Update your local credentials in `config.py`.

## **3. Run the Flask API Server**

```
python server/server.py
```

The server will begin accepting JSON POSTs at:

```
http://<your-pc-ip>:5000/upload
```

## **4. Deploy MicroPython Files to the Pico W**

Using WebREPL or Thonny, upload:

* `pico/boot.py`
* `pico/main.py`
* Supporting modules

Reboot the device to start the firmware.

---

# 🧪 **Testing the Upload Route**

Use the VS Code REST Client or `curl`:

```
POST http://<your-pc-ip>:5000/upload
Content-Type: application/json

{
  "temp": 24.3,
  "humidity": 40,
  "timestamp": "2025-02-10T18:30:00"
}
```

You should see:

* A `200 OK` from Flask
* A new record inside your MySQL table

---

# 🤝 **Collaboration Workflow (GitHub)**

This project is developed collaboratively using a lightweight Git workflow:

### **Daily Workflow**

```
git pull                     # get teammate’s changes
git add .
git commit -m "feat: add sensor acquisition loop"
git push                     # publish your changes
```

### **Guidelines**

* Pull before editing
* Communicate when modifying shared files
* Keep commit messages clean and descriptive
* Push only working code to `main`

---

# 👥 **Contributors**

* **Alex Zhang**
* **vincent Mascia**

