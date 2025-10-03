import sys
import json
import time
import pyautogui
import pyperclip
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

MAC_REGEX = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
CONFIG_FILE = 'sabreConfig.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)['click_coordinates']
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        # Default coordinates if JSON file is missing or invalid
        return {
            'random_click': [100, 100],
            'QR_single_click': [100, 100],
            'qr_double_click': [100, 100],
            'QR_ok_click': [100, 100],
            'select_region': [100, 100, 150, 150],
            'hatch_click': [100, 100],
            'final_ok': [100, 100],
            'Mark_Print': [100, 100],
            'delete_hatch': [100, 100],
            'sleep_time': 5
        }

def click(xy, delay=0.5):
    pyautogui.click(xy[0], xy[1])
    time.sleep(delay)

def double_click(xy, delay=0.5):
    pyautogui.doubleClick(xy[0], xy[1])
    time.sleep(delay)

def type_imei(imei):
    pyperclip.copy(imei)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

def select_region(region):
    start_x, start_y, end_x, end_y = region
    pyautogui.moveTo(start_x, start_y, duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.5)
    pyautogui.mouseUp()

def process_imei(imei, coords):
    try:
        click(coords['random_click'])
        double_click(coords['random_click'])
        click(coords['QR_single_click'])
        double_click(coords['qr_double_click'])
        type_imei(imei)
        click(coords['QR_ok_click'])
        select_region(coords['select_region'])
        click(coords['hatch_click'])
        click(coords['final_ok'])
        click(coords['Mark_Print'])
        for _ in range(int(coords['sleep_time'])):
            time.sleep(1)
        select_region(coords['select_region'])
        click(coords['delete_hatch'])
        return True, f"MAC {imei} processed successfully."
    except Exception as e:
        return False, f"Error processing MAC {imei}: {str(e)}"

class LaserPrintingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coords = load_config()
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        self.setWindowTitle("Sabre Automation Tool")
        self.setGeometry(100, 100, 450, 250)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # Always on top
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # QR Scanner Ready Label
        self.ready_label = QLabel("QR Scanner Ready")
        self.ready_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.ready_label)
        
        # Instruction Label
        self.instruction_label = QLabel("Scan QR Code")
        self.instruction_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.instruction_label)
        
        # MAC Address Input
        self.mac_entry = QLineEdit()
        self.mac_entry.setFont(QFont("Arial", 16))
        self.mac_entry.setPlaceholderText("Scan or enter MAC address")
        self.mac_entry.setAlignment(Qt.AlignCenter)
        self.mac_entry.setFixedWidth(300)
        layout.addWidget(self.mac_entry)
        
        # Status Label
        self.status_label = QLabel("Scan QR Code")
        self.status_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.status_label)
        
        # Instructions
        self.instructions = QLabel("• Scan QR Code with scanner\n• Press Enter to start automation")
        self.instructions.setFont(QFont("Arial", 9))
        self.instructions.setStyleSheet("color: gray")
        layout.addWidget(self.instructions)
        
        # Exit Button
        self.exit_button = QPushButton("Exit")
        self.exit_button.setFont(QFont("Arial", 10))
        self.exit_button.setStyleSheet("background-color: lightcoral")
        layout.addWidget(self.exit_button)
        
        # Focus on MAC entry
        self.mac_entry.setFocus()
    
    def setup_connections(self):
        self.mac_entry.returnPressed.connect(self.on_enter_pressed)
        self.mac_entry.textChanged.connect(self.on_text_changed)
        self.exit_button.clicked.connect(self.close)
    
    def on_enter_pressed(self):
        mac = self.mac_entry.text().strip()
        if MAC_REGEX.match(mac):
            self.mac_entry.clear()
            self.setVisible(False)  # Hide window during automation
            try:
                success, message = process_imei(mac, self.coords)
                if success:
                    QMessageBox.information(self, "Success", message)
                else:
                    QMessageBox.critical(self, "Error", message)
            finally:
                self.setVisible(True)  # Show window after automation
                self.mac_entry.setFocus()
        else:
            QMessageBox.warning(self, "Invalid MAC", "MAC must be in format xx:xx:xx:xx:xx:xx")
            self.mac_entry.clear()
            self.status_label.setText("Enter valid MAC format xx:xx:xx:xx:xx:xx")
    
    def on_text_changed(self, text):
        text = text.strip()
        if len(text) > 17:
            self.mac_entry.setText(text[:17])  # Truncate to 17 characters
        if MAC_REGEX.match(text):
            self.status_label.setText("Ready - Press Enter to start automation")
            self.status_label.setStyleSheet("color: green")
        elif text:
            self.status_label.setText("Enter valid MAC format xx:xx:xx:xx:xx:xx")
            self.status_label.setStyleSheet("color: orange")
        else:
            self.status_label.setText("Scan QR Code")
            self.status_label.setStyleSheet("color: black")

def main():
    app = QApplication(sys.argv)
    window = LaserPrintingApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()