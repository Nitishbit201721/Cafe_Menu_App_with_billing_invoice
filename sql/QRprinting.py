import serial
import serial.tools.list_ports
import qrcode
from PIL import Image, ImageTk
import win32print
import os
import tempfile
import threading
import tkinter as tk
from tkinter import messagebox
import time


def generate_qr_image(data, filename):
    """Generate QR code image and save."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


def print_image(filename):
    """Send image to default Windows printer."""
    try:
        printer_name = win32print.GetDefaultPrinter()
        os.startfile(filename, "print")
        return f"Printed to {printer_name}"
    except Exception as e:
        return f"Print error: {e}"


def auto_detect_scanner():
    """Try to auto-detect a QR scanner from serial ports."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, 9600, timeout=1)
            ser.close()
            return port.device
        except Exception:
            continue
    return None


class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Scanner & Printer")
        self.root.geometry("500x600")

        self.label = tk.Label(root, text="QR Scanner & Printer", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Scanning", font=("Arial", 12),
                                      command=self.start_scanning, bg="green", fg="white")
        self.start_button.pack(pady=10)

        # Show scanned QR text
        self.scanned_label = tk.Label(root, text="Scanned QR Data:", font=("Arial", 12))
        self.scanned_label.pack(pady=5)

        self.scanned_text = tk.StringVar()
        self.scanned_entry = tk.Entry(root, textvariable=self.scanned_text, font=("Arial", 12), width=50, state="readonly")
        self.scanned_entry.pack(pady=5)

        # Status log
        self.textbox = tk.Text(root, height=10, width=60, state="disabled")
        self.textbox.pack(pady=10)

        # QR preview
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.running = False
        self.scanner_port = None

    def start_scanning(self):
        """Start scanning after button click."""
        self.scanner_port = auto_detect_scanner()
        if not self.scanner_port:
            messagebox.showerror("Error", "No QR scanner detected.")
            return

        self.start_button.config(state="disabled", text="Scanning...")
        self.running = True
        self.thread = threading.Thread(target=self.listen_scanner, daemon=True)
        self.thread.start()
        self.update_status(f"Listening on {self.scanner_port}...")

    def listen_scanner(self):
        try:
            ser = serial.Serial(self.scanner_port, 9600, timeout=1)
            buffer = ""

            while self.running:
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting).decode("utf-8", errors="ignore").strip()
                    if data:
                        buffer += data
                        if "\n" in buffer or "\r" in buffer:
                            qr_data = buffer.splitlines()[0].strip()
                            if qr_data:
                                self.process_qr(qr_data)
                            buffer = ""
                time.sleep(0.1)

            ser.close()
        except Exception as e:
            self.update_status(f"Scanner error: {e}")

    def process_qr(self, qr_data):
        """Generate, display, print QR code and show scanned text."""
        # Show raw data in text field
        self.scanned_text.set(qr_data)

        self.update_status(f"Scanned: {qr_data}")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            filename = tmp_file.name

        generate_qr_image(qr_data, filename)

        # Show QR in GUI
        img = Image.open(filename).resize((150, 150))
        tk_img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img

        # Print
        result = print_image(filename)
        self.update_status(result)

        os.unlink(filename)

    def update_status(self, msg):
        self.textbox.config(state="normal")
        self.textbox.insert("end", msg + "\n")
        self.textbox.see("end")
        self.textbox.config(state="disabled")

    def on_close(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
