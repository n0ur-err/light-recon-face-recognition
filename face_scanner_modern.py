"""
L1GHT REC0N - Modern Face Scanner
Register new subjects with an elegant, modern interface
"""

import sys
import cv2
import numpy as np
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QLineEdit,
                              QComboBox, QTextEdit, QMessageBox, QGraphicsDropShadowEffect,
                              QFrame, QSpinBox, QGroupBox)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QLinearGradient, QFont, QPainterPath
import json
from datetime import datetime
from settings_manager import settings


class ModernButton(QPushButton):
    """Styled button with hover effects"""
    
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.primary = primary
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(66, 165, 245),
                        stop:1 rgb(100, 150, 255)
                    );
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px 24px;
                    letter-spacing: 1px;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(76, 175, 255),
                        stop:1 rgb(110, 160, 255)
                    );
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(56, 155, 235),
                        stop:1 rgb(90, 140, 245)
                    );
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.08);
                    color: rgba(255, 255, 255, 0.9);
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.05);
                }
            """)


class ModernInput(QLineEdit):
    """Styled input field"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: white;
                padding: 10px 15px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QLineEdit:focus {
                border: 2px solid rgba(100, 150, 255, 0.8);
                background: rgba(255, 255, 255, 0.08);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.3);
            }
        """)


class ModernComboBox(QComboBox):
    """Styled combo box"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: white;
                padding: 10px 15px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QComboBox:focus {
                border: 2px solid rgba(100, 150, 255, 0.8);
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background: rgb(30, 33, 41);
                border: 1px solid rgba(100, 150, 255, 0.3);
                selection-background-color: rgba(100, 150, 255, 0.3);
                color: white;
                padding: 5px;
            }
        """)


class ModernSpinBox(QSpinBox):
    """Styled spin box"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QSpinBox {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: white;
                padding: 10px 15px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QSpinBox:focus {
                border: 2px solid rgba(100, 150, 255, 0.8);
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: rgba(100, 150, 255, 0.2);
                border: none;
                width: 25px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: rgba(100, 150, 255, 0.4);
            }
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid white;
            }
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid white;
            }
        """)


class VideoPreview(QWidget):
    """Video preview widget for face scanner"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.setMinimumSize(640, 480)
        
    def setImage(self, image):
        self.image = image
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.image:
            # Rounded corners
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
            painter.setClipPath(path)
            
            painter.drawPixmap(self.rect(), QPixmap.fromImage(self.image))
            
            # Border
            painter.setPen(QColor(100, 150, 255, 80))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 15, 15)
        else:
            painter.fillRect(self.rect(), QColor(30, 33, 41))


class FaceScannerWindow(QMainWindow):
    """Modern face scanner interface"""
    
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("L1GHT REC0N - Face Scanner")
        self.setMinimumSize(1400, 800)
        
        self.captured_images = []
        self.auto_capture = False
        self.capture_count = 0
        
        # Detect available cameras
        self.available_cameras = self.detect_cameras()
        self.current_camera_index = 0
        
        # Setup camera
        self.video_capture = cv2.VideoCapture(self.current_camera_index)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Load face detector
        self.face_detector = cv2.dnn.readNetFromCaffe(
            "deploy.prototxt",
            "res10_300x300_ssd_iter_140000.caffemodel"
        )
        
        self.setup_ui()
        
        # Video timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
        self.frame_count = 0
        
    def detect_cameras(self):
        """Detect available cameras"""
        cameras = []
        for i in range(10):  # Check first 10 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
        return cameras if cameras else [0]  # Default to 0 if none found
        
    def setup_ui(self):
        """Setup the UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        # Left side - Video preview
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(20)
        
        # Header
        title = QLabel("Face Scanner")
        title.setStyleSheet("""
            QLabel {
                color: rgba(100, 150, 255, 255);
                font-size: 32px;
                font-weight: 700;
                letter-spacing: 2px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        left_layout.addWidget(title)
        
        subtitle = QLabel("Position your face in the frame")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        left_layout.addWidget(subtitle)
        
        # Camera selector
        camera_widget = QWidget()
        camera_layout = QHBoxLayout(camera_widget)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        
        camera_label = QLabel("Camera:")
        camera_label.setStyleSheet("""
            QLabel {
                color: rgba(200, 200, 200, 255);
                font-size: 13px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial;
            }
        """)
        camera_layout.addWidget(camera_label)
        
        self.camera_selector = QComboBox()
        for i, cam_idx in enumerate(self.available_cameras):
            self.camera_selector.addItem(f"Camera {cam_idx}", cam_idx)
        self.camera_selector.setCurrentIndex(0)
        self.camera_selector.currentIndexChanged.connect(self.change_camera)
        self.camera_selector.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                padding: 8px 12px;
                font-size: 13px;
                min-width: 120px;
                font-family: 'Segoe UI', Arial;
            }
            QComboBox:hover {
                border: 1px solid rgba(100, 150, 255, 0.5);
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: rgb(30, 33, 41);
                border: 1px solid rgba(100, 150, 255, 0.3);
                selection-background-color: rgba(100, 150, 255, 0.3);
                color: white;
                padding: 5px;
            }
        """)
        camera_layout.addWidget(self.camera_selector)
        camera_layout.addStretch()
        
        left_layout.addWidget(camera_widget)
        
        # Video preview
        self.video_preview = VideoPreview()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 10)
        self.video_preview.setGraphicsEffect(shadow)
        left_layout.addWidget(self.video_preview, 1)
        
        # Capture controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        self.capture_btn = ModernButton("Capture Image", primary=True)
        self.capture_btn.clicked.connect(self.capture_image)
        controls_layout.addWidget(self.capture_btn)
        
        self.auto_btn = ModernButton("Auto Capture: OFF")
        self.auto_btn.clicked.connect(self.toggle_auto_capture)
        controls_layout.addWidget(self.auto_btn)
        
        left_layout.addLayout(controls_layout)
        
        # Status
        self.status_label = QLabel(f"Images captured: {len(self.captured_images)}")
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 13px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        left_layout.addWidget(self.status_label)
        
        main_layout.addWidget(left_container, 2)
        
        # Right side - Profile form
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(20)
        
        form_title = QLabel("Subject Profile")
        form_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 700;
                font-family: 'Segoe UI', Arial;
            }
        """)
        right_layout.addWidget(form_title)
        
        # Form fields
        self.form_fields = {}
        
        # Name
        right_layout.addWidget(self.create_label("Name*"))
        self.form_fields["name"] = ModernInput("Enter full name")
        right_layout.addWidget(self.form_fields["name"])
        
        # Age
        right_layout.addWidget(self.create_label("Age"))
        self.form_fields["age"] = ModernSpinBox()
        self.form_fields["age"].setRange(1, 120)
        self.form_fields["age"].setValue(30)
        right_layout.addWidget(self.form_fields["age"])
        
        # Gender - populated from settings
        right_layout.addWidget(self.create_label("Gender"))
        self.form_fields["gender"] = ModernComboBox()
        self.form_fields["gender"].addItems(settings.get("gender_options", ["Male", "Female", "Other"]))
        # Set default
        default_gender = settings.get("default_gender", "Male")
        index = self.form_fields["gender"].findText(default_gender)
        if index >= 0:
            self.form_fields["gender"].setCurrentIndex(index)
        right_layout.addWidget(self.form_fields["gender"])
        
        # Occupation
        right_layout.addWidget(self.create_label("Occupation"))
        self.form_fields["occupation"] = ModernInput("Enter occupation")
        right_layout.addWidget(self.form_fields["occupation"])
        
        # Nationality
        right_layout.addWidget(self.create_label("Nationality"))
        self.form_fields["nationality"] = ModernInput("Enter nationality")
        right_layout.addWidget(self.form_fields["nationality"])
        
        # Status - populated from settings
        right_layout.addWidget(self.create_label("Status"))
        self.form_fields["status"] = ModernComboBox()
        self.form_fields["status"].addItems(settings.get_status_types())
        # Set default
        default_status = settings.get("default_status", "CIVILIAN")
        index = self.form_fields["status"].findText(default_status)
        if index >= 0:
            self.form_fields["status"].setCurrentIndex(index)
        right_layout.addWidget(self.form_fields["status"])
        
        # Threat Level - populated from settings
        right_layout.addWidget(self.create_label("Threat Level"))
        self.form_fields["threat_level"] = ModernComboBox()
        self.form_fields["threat_level"].addItems(settings.get_threat_levels())
        # Set default
        default_threat = settings.get("default_threat_level", "LOW")
        index = self.form_fields["threat_level"].findText(default_threat)
        if index >= 0:
            self.form_fields["threat_level"].setCurrentIndex(index)
        right_layout.addWidget(self.form_fields["threat_level"])
        
        # Notes
        right_layout.addWidget(self.create_label("Notes"))
        self.form_fields["notes"] = QTextEdit()
        self.form_fields["notes"].setPlaceholderText("Additional information...")
        self.form_fields["notes"].setMaximumHeight(100)
        self.form_fields["notes"].setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QTextEdit:focus {
                border: 2px solid rgba(100, 150, 255, 0.8);
            }
        """)
        right_layout.addWidget(self.form_fields["notes"])
        
        right_layout.addStretch()
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        save_btn = ModernButton("Save Profile", primary=True)
        save_btn.clicked.connect(self.save_profile)
        action_layout.addWidget(save_btn)
        
        clear_btn = ModernButton("Clear")
        clear_btn.clicked.connect(self.clear_form)
        action_layout.addWidget(clear_btn)
        
        right_layout.addLayout(action_layout)
        
        main_layout.addWidget(right_container, 1)
        
        # Window style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgb(15, 18, 25),
                    stop:0.5 rgb(20, 25, 35),
                    stop:1 rgb(25, 30, 40)
                );
            }
        """)
        
    def create_label(self, text):
        """Create a styled label"""
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                color: rgba(200, 200, 200, 255);
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 1px;
                font-family: 'Segoe UI', Arial;
                margin-top: 5px;
            }
        """)
        return label
        
    def change_camera(self, index):
        """Change the active camera"""
        if index < 0:
            return
            
        new_camera_index = self.camera_selector.itemData(index)
        
        if new_camera_index != self.current_camera_index:
            # Release current camera
            if hasattr(self, 'video_capture'):
                self.video_capture.release()
            
            # Open new camera
            self.current_camera_index = new_camera_index
            self.video_capture = cv2.VideoCapture(self.current_camera_index)
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            print(f"✓ Switched to Camera {self.current_camera_index}")
        
    def update_frame(self):
        """Update video frame"""
        ret, frame = self.video_capture.read()
        if not ret:
            return
            
        self.frame_count += 1
        frame = cv2.flip(frame, 1)
        
        # Detect faces
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                     (104.0, 177.0, 123.0))
        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()
        
        face_detected = False
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > 0.5:
                face_detected = True
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(w, x2)
                y2 = min(h, y2)
                
                # Draw face box
                color = (100, 150, 255)
                pulse = abs(np.sin(self.frame_count * 0.1))
                animated_color = tuple(int((0.6 + 0.4 * pulse) * c) for c in color)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 100), 2)
                
                # Corner accents
                corner_length = 30
                thickness = 3
                
                cv2.line(frame, (x1, y1), (x1 + corner_length, y1), animated_color, thickness)
                cv2.line(frame, (x1, y1), (x1, y1 + corner_length), animated_color, thickness)
                
                cv2.line(frame, (x2, y1), (x2 - corner_length, y1), animated_color, thickness)
                cv2.line(frame, (x2, y1), (x2, y1 + corner_length), animated_color, thickness)
                
                cv2.line(frame, (x1, y2), (x1 + corner_length, y2), animated_color, thickness)
                cv2.line(frame, (x1, y2), (x1, y2 - corner_length), animated_color, thickness)
                
                cv2.line(frame, (x2, y2), (x2 - corner_length, y2), animated_color, thickness)
                cv2.line(frame, (x2, y2), (x2, y2 - corner_length), animated_color, thickness)
        
        # Auto capture
        if self.auto_capture and face_detected and self.frame_count % 60 == 0:
            if len(self.captured_images) < 10:
                self.capture_image()
        
        # Convert to QImage
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        self.video_preview.setImage(qt_image)
        
    def capture_image(self):
        """Capture current frame"""
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.captured_images.append(frame)
            self.status_label.setText(f"Images captured: {len(self.captured_images)}")
            
    def toggle_auto_capture(self):
        """Toggle auto capture mode"""
        self.auto_capture = not self.auto_capture
        if self.auto_capture:
            self.auto_btn.setText("Auto Capture: ON")
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 230, 118, 0.2);
                    color: rgba(0, 230, 118, 1);
                    border: 1px solid rgba(0, 230, 118, 0.3);
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 12px 24px;
                }
            """)
        else:
            self.auto_btn.setText("Auto Capture: OFF")
            self.auto_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.08);
                    color: rgba(255, 255, 255, 0.9);
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 12px 24px;
                }
            """)
            
    def save_profile(self):
        """Save profile and captured images"""
        name = self.form_fields["name"].text().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a name")
            return
            
        if len(self.captured_images) < 3:
            QMessageBox.warning(self, "Error", "Please capture at least 3 images")
            return
        
        # Create person directory
        dataset_dir = "dataset"
        os.makedirs(dataset_dir, exist_ok=True)
        
        person_dir = os.path.join(dataset_dir, name)
        os.makedirs(person_dir, exist_ok=True)
        
        # Save images
        for i, img in enumerate(self.captured_images):
            img_path = os.path.join(person_dir, f"{name}_{i+1}.jpg")
            cv2.imwrite(img_path, img)
        
        # Save profile
        profile_data = {
            "name": name,
            "age": self.form_fields["age"].value(),
            "gender": self.form_fields["gender"].currentText(),
            "occupation": self.form_fields["occupation"].text() or "Unknown",
            "nationality": self.form_fields["nationality"].text() or "Unknown",
            "status": self.form_fields["status"].currentText(),
            "threat_level": self.form_fields["threat_level"].currentText(),
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": self.form_fields["notes"].toPlainText() or "No additional information.",
            "sightings": 0
        }
        
        profile_path = os.path.join(person_dir, "profile.json")
        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=4)
        
        QMessageBox.information(self, "Success", 
                               f"Profile for {name} saved successfully!\n"
                               f"{len(self.captured_images)} images saved.")
        
        self.clear_form()
        
    def clear_form(self):
        """Clear form and captured images"""
        self.form_fields["name"].clear()
        self.form_fields["age"].setValue(30)
        self.form_fields["gender"].setCurrentIndex(0)
        self.form_fields["occupation"].clear()
        self.form_fields["nationality"].clear()
        self.form_fields["status"].setCurrentIndex(0)
        self.form_fields["threat_level"].setCurrentIndex(0)
        self.form_fields["notes"].clear()
        
        self.captured_images = []
        self.status_label.setText(f"Images captured: {len(self.captured_images)}")
        
    def closeEvent(self, event):
        """Clean up on close"""
        self.video_capture.release()
        self.finished.emit()
        event.accept()


def main():
    """Launch the face scanner"""
    app = QApplication(sys.argv)
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = FaceScannerWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
