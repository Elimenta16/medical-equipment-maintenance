# Medical Equipment Maintenance Tracker 🛠️🏥

A clean, practical Streamlit app built to automate medical equipment maintenance schedules and countdowns for hospital Clinical Engineering departments.

## 🚀 Live Demo
🔗 [Check out the live app here!](PASTE_YOUR_STREAMLIT_URL_HERE)

## 🛠️ What this app does
Instead of tracking calibration dates in a massive, confusing spreadsheet that everyone forgets to check, this app takes a standard inventory list and automates the scheduling:
* **Automatic 6-Month Cycle:** It instantly calculates the next mandatory maintenance window (+180 days) from the last service date.
* **Smart Status Alerts:** Evaluates remaining days and flags equipment status into immediate action items: `🟢 Al Corriente` (Safe), `🟡 Próximo` (Under 15 days), or `🔴 Vencido` (Overdue / Out of Compliance).
* **Workload by Area:** Generates interactive Plotly charts that show hospital management exactly which areas (ER, OR, ICU) have the highest density of overdue equipment.
* **Risk Mitigator:** Helps biomedical teams stay audit-ready and prevents critical medical devices from failing on patients.

## 🧰 Tech Stack
* **Language:** Python
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, Datetime & OpenPyXL
* **Charts:** Plotly Express

## 📋 How to test it
Upload an Excel file with these exact column headers: `ID_Equipo`, `Equipo`, `Marca_Modelo`, `Area_Hospital`, and `Ultimo_Mantenimiento` (format: YYYY-MM-DD).
