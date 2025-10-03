import pyautogui
import cv2
import numpy as np
from pyzbar import pyzbar
import time
import json
import logging
from typing import List, Tuple, Dict, Any
import re
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Disable pyautogui failsafe for automated operation (use with caution)
pyautogui.FAILSAFE = True  # Keep failsafe enabled for safety
pyautogui.PAUSE = 0.5  # Add small pause between actions

@dataclass
class Coordinate:
    x: int
    y: int
    action: str = "click"  # click, double_click, right_click
    delay: float = 1.0  # delay after action in seconds

class QRCodeValidator:
    """Validates QR code content and extracts coordinates"""
    
    @staticmethod
    def validate_qr_format(qr_data: str) -> bool:
        """
        Validate if QR code contains valid coordinate data
        Expected format: JSON with coordinates array
        """
        try:
            data = json.loads(qr_data)
            if 'coordinates' in data and isinstance(data['coordinates'], list):
                return True
            return False
        except (json.JSONDecodeError, KeyError):
            return False
    
    @staticmethod
    def extract_coordinates(qr_data: str) -> List[Coordinate]:
        """Extract coordinates from QR code data"""
        try:
            data = json.loads(qr_data)
            coordinates = []
            
            for coord_data in data['coordinates']:
                coord = Coordinate(
                    x=coord_data['x'],
                    y=coord_data['y'],
                    action=coord_data.get('action', 'click'),
                    delay=coord_data.get('delay', 1.0)
                )
                coordinates.append(coord)
            
            return coordinates
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Error extracting coordinates: {e}")
            return []

class QRCodeScanner:
    """Handles QR code scanning from camera or image file"""
    
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = None
    
    def initialize_camera(self) -> bool:
        """Initialize camera for QR code scanning"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                logger.error("Failed to open camera")
                return False
            return True
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            return False
    
    def scan_qr_from_camera(self, timeout: int = 30) -> str:
        """
        Scan QR code from camera with timeout
        Returns QR code data as string
        """
        if not self.initialize_camera():
            return ""
        
        start_time = time.time()
        logger.info("Starting QR code scan from camera...")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Decode QR codes in the frame
                qr_codes = pyzbar.decode(frame)
                
                if qr_codes:
                    for qr in qr_codes:
                        qr_data = qr.data.decode('utf-8')
                        logger.info(f"QR Code detected: {qr_data}")
                        self.cleanup_camera()
                        return qr_data
                
                # Show camera feed
                cv2.imshow('QR Code Scanner - Press Q to quit', frame)
                
                # Check for timeout or quit
                if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > timeout:
                    break
            
        except Exception as e:
            logger.error(f"Error during QR scanning: {e}")
        finally:
            self.cleanup_camera()
        
        return ""
    
    def scan_qr_from_image(self, image_path: str) -> str:
        """Scan QR code from image file"""
        try:
            image = cv2.imread(image_path)
            qr_codes = pyzbar.decode(image)
            
            if qr_codes:
                qr_data = qr_codes[0].data.decode('utf-8')
                logger.info(f"QR Code from image: {qr_data}")
                return qr_data
            else:
                logger.warning("No QR code found in image")
                return ""
                
        except Exception as e:
            logger.error(f"Error reading QR from image: {e}")
            return ""
    
    def cleanup_camera(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

class UIAutomator:
    """Handles UI automation for laser machine printing"""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        logger.info(f"Screen resolution: {self.screen_width}x{self.screen_height}")
    
    def validate_coordinates(self, coordinates: List[Coordinate]) -> bool:
        """Validate if coordinates are within screen bounds"""
        for coord in coordinates:
            if not (0 <= coord.x <= self.screen_width and 0 <= coord.y <= self.screen_height):
                logger.error(f"Coordinate ({coord.x}, {coord.y}) is outside screen bounds")
                return False
        return True
    
    def execute_automation_sequence(self, coordinates: List[Coordinate]) -> bool:
        """Execute the automation sequence"""
        try:
            logger.info(f"Starting automation sequence with {len(coordinates)} coordinates")
            
            for i, coord in enumerate(coordinates, 1):
                logger.info(f"Step {i}: {coord.action} at ({coord.x}, {coord.y})")
                
                # Move to coordinate
                pyautogui.moveTo(coord.x, coord.y, duration=0.3)
                
                # Perform action
                if coord.action == "click":
                    pyautogui.click()
                elif coord.action == "double_click":
                    pyautogui.doubleClick()
                elif coord.action == "right_click":
                    pyautogui.rightClick()
                else:
                    logger.warning(f"Unknown action: {coord.action}")
                    pyautogui.click()  # Default to click
                
                # Wait for specified delay
                time.sleep(coord.delay)
            
            logger.info("Automation sequence completed successfully")
            return True
            
        except pyautogui.FailSafeException:
            logger.error("PyAutoGUI failsafe triggered - mouse moved to corner")
            return False
        except Exception as e:
            logger.error(f"Error during automation: {e}")
            return False
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot for verification"""
        if not filename:
            filename = f"screenshot_{int(time.time())}.png"
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return ""

class LaserPrintingAutomation:
    """Main class for laser printing automation system"""
    
    def __init__(self, camera_index: int = 0):
        self.qr_scanner = QRCodeScanner(camera_index)
        self.qr_validator = QRCodeValidator()
        self.ui_automator = UIAutomator()
    
    def run_automation_from_camera(self) -> bool:
        """Run complete automation process using camera QR scan"""
        logger.info("=== Starting Laser Printing Automation ===")
        
        # Step 1: Scan QR code
        qr_data = self.qr_scanner.scan_qr_from_camera()
        if not qr_data:
            logger.error("No QR code detected or scanning failed")
            return False
        
        return self._process_qr_data(qr_data)
    
    def run_automation_from_image(self, image_path: str) -> bool:
        """Run automation process using QR code from image file"""
        logger.info(f"=== Starting Automation from Image: {image_path} ===")
        
        # Step 1: Scan QR from image
        qr_data = self.qr_scanner.scan_qr_from_image(image_path)
        if not qr_data:
            logger.error("No QR code found in image")
            return False
        
        return self._process_qr_data(qr_data)
    
    def run_automation_from_text(self, qr_text: str) -> bool:
        """Run automation process using QR code text directly"""
        logger.info("=== Starting Automation from Text Input ===")
        return self._process_qr_data(qr_text)
    
    def _process_qr_data(self, qr_data: str) -> bool:
        """Process QR data and execute automation"""
        # Step 2: Validate QR code format
        if not self.qr_validator.validate_qr_format(qr_data):
            logger.error("Invalid QR code format")
            return False
        
        # Step 3: Extract coordinates
        coordinates = self.qr_validator.extract_coordinates(qr_data)
        if not coordinates:
            logger.error("No valid coordinates found in QR code")
            return False
        
        # Step 4: Validate coordinates
        if not self.ui_automator.validate_coordinates(coordinates):
            logger.error("Invalid coordinates detected")
            return False
        
        # Step 5: Take screenshot before automation
        self.ui_automator.take_screenshot("before_automation.png")
        
        # Step 6: Execute automation
        success = self.ui_automator.execute_automation_sequence(coordinates)
        
        # Step 7: Take screenshot after automation
        self.ui_automator.take_screenshot("after_automation.png")
        
        if success:
            logger.info("=== Automation completed successfully ===")
        else:
            logger.error("=== Automation failed ===")
        
        return success

def create_sample_qr_data() -> str:
    """Create sample QR code data for testing"""
    sample_data = {
        "coordinates": [
            {"x": 100, "y": 100, "action": "click", "delay": 1.0},
            {"x": 200, "y": 150, "action": "click", "delay": 1.5},
            {"x": 300, "y": 200, "action": "double_click", "delay": 2.0},
            {"x": 400, "y": 250, "action": "right_click", "delay": 1.0}
        ],
        "description": "Sample laser printing coordinates",
        "timestamp": int(time.time())
    }
    return json.dumps(sample_data, indent=2)

# Example usage
if __name__ == "__main__":
    # Initialize the automation system
    automation = LaserPrintingAutomation(camera_index=0)
    
    # Example 1: Run automation from camera QR scan
    print("Choose an option:")
    print("1. Scan QR code from camera")
    print("2. Use sample QR data")
    print("3. Load QR from image file")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        automation.run_automation_from_camera()
    elif choice == "2":
        sample_qr = create_sample_qr_data()
        print(f"Using sample QR data:\n{sample_qr}")
        automation.run_automation_from_text(sample_qr)
    elif choice == "3":
        image_path = input("Enter image file path: ").strip()
        automation.run_automation_from_image(image_path)
    else:
        print("Invalid choice")

# Additional utility functions
def generate_qr_code_image(data: str, filename: str = "laser_printing_qr.png"):
    """Generate QR code image from data (requires qrcode library)"""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"QR code saved as: {filename}")
        return filename
    except ImportError:
        print("qrcode library not installed. Install with: pip install qrcode[pil]")
        return None

def test_coordinates_on_screen():
    """Test function to visualize coordinates on screen"""
    coordinates = [
        Coordinate(100, 100),
        Coordinate(200, 150),
        Coordinate(300, 200),
        Coordinate(400, 250)
    ]
    
    for coord in coordinates:
        pyautogui.moveTo(coord.x, coord.y, duration=1)
        time.sleep(1)
    
    print("Coordinate test completed")