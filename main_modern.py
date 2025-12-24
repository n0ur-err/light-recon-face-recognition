"""
L1GHT REC0N - Modern Face Recognition System
Featuring PyQt6-based modern UI with glassmorphism effects
"""

import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect,
                              QComboBox)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect, QPoint
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QLinearGradient, QFont, QPainterPath
from person_profiles import get_profile, ProfileManager
from settings_manager import settings
from settings_dialog import SettingsDialog
import os
from datetime import datetime


class ModernVideoWidget(QWidget):
    """Modern video display widget with rounded corners and effects"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = None
        self.setMinimumSize(800, 600)
        
        # Set up styling
        self.setStyleSheet("""
            ModernVideoWidget {
                background: transparent;
                border-radius: 20px;
            }
        """)
        
    def setImage(self, image):
        """Update the displayed image"""
        self.image = image
        self.update()
        
    def paintEvent(self, event):
        """Custom paint event for rounded corners and effects"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.image:
            # Create rounded rectangle path
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
            painter.setClipPath(path)
            
            # Draw the image
            painter.drawPixmap(self.rect(), QPixmap.fromImage(self.image))
            
            # Add subtle border
            painter.setPen(QColor(100, 150, 255, 100))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 20, 20)
        else:
            # Draw placeholder
            painter.fillRect(self.rect(), QColor(30, 33, 41))


class GlassPanel(QWidget):
    """Glassmorphism panel widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 0.9
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)
        
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
        
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
        
    def paintEvent(self, event):
        """Paint glassmorphism effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        
        # Glass background with gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 255, 255, int(25 * self._opacity)))
        gradient.setColorAt(1, QColor(255, 255, 255, int(10 * self._opacity)))
        
        painter.fillPath(path, gradient)
        
        # Border
        painter.setPen(QColor(255, 255, 255, int(40 * self._opacity)))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 20, 20)


class ProfileCard(GlassPanel):
    """Modern profile card with animated entrance"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile = None
        self.setFixedSize(420, 650)
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Header
        self.header_label = QLabel("SUBJECT PROFILE")
        self.header_label.setStyleSheet("""
            QLabel {
                color: rgba(100, 150, 255, 255);
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 2px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        layout.addWidget(self.header_label)
        
        # Name
        self.name_label = QLabel("---")
        self.name_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 255);
                font-size: 32px;
                font-weight: 700;
                font-family: 'Segoe UI', Arial;
            }
        """)
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)
        
        # Status badge
        self.status_container = QWidget()
        status_layout = QHBoxLayout(self.status_container)
        status_layout.setContentsMargins(0, 10, 0, 10)
        
        self.status_badge = QLabel("CIVILIAN")
        self.status_badge.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
                padding: 8px 16px;
                background: rgba(0, 230, 118, 255);
                border-radius: 15px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        status_layout.addWidget(self.status_badge)
        status_layout.addStretch()
        layout.addWidget(self.status_container)
        
        # Divider
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(255, 255, 255, 0.1);")
        layout.addWidget(divider)
        
        # Info section
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(12)
        
        self.info_labels = {}
        info_fields = [
            ("AGE", "age"),
            ("GENDER", "gender"),
            ("OCCUPATION", "occupation"),
            ("NATIONALITY", "nationality"),
            ("THREAT LEVEL", "threat_level"),
            ("SIGHTINGS", "sightings"),
            ("LAST SEEN", "last_seen")
        ]
        
        for label_text, field_name in info_fields:
            field_widget = self._create_info_field(label_text, "---")
            info_layout.addWidget(field_widget)
            self.info_labels[field_name] = field_widget.findChild(QLabel, "value")
        
        layout.addWidget(info_widget)
        layout.addStretch()
        
        # Notes section
        notes_header = QLabel("NOTES")
        notes_header.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
                margin-top: 10px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        layout.addWidget(notes_header)
        
        self.notes_label = QLabel("No information available.")
        self.notes_label.setStyleSheet("""
            QLabel {
                color: rgba(200, 200, 200, 255);
                font-size: 13px;
                line-height: 1.5;
                font-family: 'Segoe UI', Arial;
            }
        """)
        self.notes_label.setWordWrap(True)
        layout.addWidget(self.notes_label)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def _create_info_field(self, label_text, value_text):
        """Create an info field with label and value"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
                min-width: 130px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        
        value = QLabel(value_text)
        value.setObjectName("value")
        value.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 255);
                font-size: 14px;
                font-weight: 500;
                font-family: 'Segoe UI', Arial;
            }
        """)
        
        layout.addWidget(label)
        layout.addWidget(value)
        layout.addStretch()
        
        return widget
        
    def updateProfile(self, profile):
        """Update the profile card with new data"""
        if profile:
            print(f"DEBUG ProfileCard: Updating with {profile.name}")
            self.profile = profile
            
            # Animate entrance
            self.animation.setStartValue(0.0)
            self.animation.setEndValue(0.9)
            self.animation.start()
            
            # Update name
            self.name_label.setText(profile.name)
            
            # Update status badge with dynamic colors from settings
            self.status_badge.setText(profile.status)
            
            # Get color from settings (with fallback logic)
            if profile.status == "SCANNING":
                badge_color = "rgba(100, 150, 255, 255)"
            elif profile.status == "UNIDENTIFIED":
                badge_color = "rgba(255, 152, 0, 255)"
            else:
                # Try to get custom color from settings
                status_color = settings.get_status_color(profile.status)
                if status_color:
                    # Convert hex to rgba
                    badge_color = self._hex_to_rgba(status_color)
                elif profile.threat_level:
                    # Fallback to threat level color
                    threat_color = settings.get_threat_level_color(profile.threat_level)
                    if threat_color:
                        badge_color = self._hex_to_rgba(threat_color)
                    else:
                        badge_color = "rgba(120, 144, 156, 255)"
                else:
                    badge_color = "rgba(120, 144, 156, 255)"
                
            self.status_badge.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    font-size: 11px;
                    font-weight: 600;
                    letter-spacing: 1px;
                    padding: 8px 16px;
                    background: {badge_color};
                    border-radius: 15px;
                    font-family: 'Segoe UI', Arial;
                }}
            """)
            
            # Update info fields
            print(f"DEBUG: Setting age to: {str(profile.age)}")
            self.info_labels["age"].setText(str(profile.age))
            self.info_labels["gender"].setText(str(profile.gender))
            self.info_labels["occupation"].setText(str(profile.occupation))
            self.info_labels["nationality"].setText(str(profile.nationality))
            self.info_labels["threat_level"].setText(str(profile.threat_level))
            self.info_labels["sightings"].setText(str(profile.sightings))
            self.info_labels["last_seen"].setText(str(profile.last_seen))
            print(f"DEBUG: Profile fields updated")
            
            # Update notes
            self.notes_label.setText(profile.notes)
    
    def _hex_to_rgba(self, hex_color):
        """Convert hex color to RGBA string"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, 255)"


class ModernMainWindow(QMainWindow):
    """Modern main window with gradient background"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("L1GHT REC0N - Advanced Face Recognition")
        self.setMinimumSize(1600, 900)
        
        # Detect available cameras
        self.available_cameras = self.detect_cameras()
        self.current_camera_index = 0
        
        # Face recognition setup
        self.setup_face_recognition()
        
        # Profile manager
        self.profile_manager = ProfileManager()
        self.current_profile = None
        
        # Setup UI
        self.setup_ui()
        
        # Video timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # ~30 FPS
        
        # Frame counter for animations
        self.frame_count = 0
        self.process_this_frame = True
        
    def detect_cameras(self):
        """Detect available cameras"""
        cameras = []
        for i in range(10):  # Check first 10 indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
                cap.release()
        return cameras if cameras else [0]  # Default to 0 if none found
        
    def setup_face_recognition(self):
        """Initialize face recognition models"""
        # Load face detection model
        self.face_detector = cv2.dnn.readNetFromCaffe(
            "deploy.prototxt",
            "res10_300x300_ssd_iter_140000.caffemodel"
        )
        
        # Load face recognition model
        self.face_recognizer = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7")
        
        # Check for CUDA support
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            self.face_detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.face_detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            self.face_recognizer.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.face_recognizer.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            print("✓ CUDA acceleration enabled")
        else:
            print("○ Running on CPU")
        
        # Load known faces
        self.load_known_faces()
        
        # Open webcam
        self.video_capture = cv2.VideoCapture(self.current_camera_index)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
    def load_known_faces(self):
        """Load all known face encodings"""
        self.known_face_encodings = []
        self.known_face_names = []
        
        dataset_dir = "dataset"
        if not os.path.exists(dataset_dir):
            print("⚠ Dataset directory not found")
            return
            
        for person_name in os.listdir(dataset_dir):
            person_dir = os.path.join(dataset_dir, person_name)
            if not os.path.isdir(person_dir):
                continue
            
            print(f"Loading faces for: {person_name}")
            person_encodings_loaded = 0
            
            for image_file in os.listdir(person_dir):
                if image_file.endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(person_dir, image_file)
                    image = cv2.imread(image_path)
                    
                    if image is not None:
                        # Detect face in the image first
                        h, w = image.shape[:2]
                        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
                                                    (104.0, 177.0, 123.0))
                        self.face_detector.setInput(blob)
                        detections = self.face_detector.forward()
                        
                        # Find the largest face
                        best_detection = None
                        best_confidence = 0
                        
                        for i in range(detections.shape[2]):
                            confidence = detections[0, 0, i, 2]
                            if confidence > 0.5 and confidence > best_confidence:
                                best_confidence = confidence
                                best_detection = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        
                        if best_detection is not None:
                            # Extract face region
                            (x1, y1, x2, y2) = best_detection.astype("int")
                            x1, y1 = max(0, x1), max(0, y1)
                            x2, y2 = min(w, x2), min(h, y2)
                            
                            face_image = image[y1:y2, x1:x2]
                            
                            if face_image.size > 0:
                                # Get face encoding from the detected face
                                face_blob = cv2.dnn.blobFromImage(
                                    face_image, 1.0/255, (96, 96),
                                    (0, 0, 0), swapRB=True, crop=False
                                )
                                self.face_recognizer.setInput(face_blob)
                                encoding = self.face_recognizer.forward()[0]
                                
                                self.known_face_encodings.append(encoding)
                                self.known_face_names.append(person_name)
                                person_encodings_loaded += 1
                                print(f"  ✓ Loaded encoding from {image_file} (confidence: {best_confidence:.2f})")
                        else:
                            print(f"  ✗ No face detected in {image_file}")
            
            if person_encodings_loaded == 0:
                print(f"  ⚠ No valid face encodings loaded for {person_name}")
        
        print(f"\n✓ Total: Loaded {len(self.known_face_encodings)} face encodings")
        if len(self.known_face_encodings) > 0:
            print(f"  Known people: {', '.join(set(self.known_face_names))}")
        else:
            print("  ⚠ No faces in database. Use Face Scanner to add people.")
        
    def setup_ui(self):
        """Setup the modern UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        # Left side - Video feed
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(20)
        
        # Header
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("L1GHT REC0N")
        title.setStyleSheet("""
            QLabel {
                color: rgba(100, 150, 255, 255);
                font-size: 36px;
                font-weight: 700;
                letter-spacing: 3px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Advanced Face Recognition System")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 14px;
                letter-spacing: 1px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        header_layout.addWidget(subtitle)
        
        left_layout.addWidget(header_widget)
        
        # Video widget
        self.video_widget = ModernVideoWidget()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 15)
        self.video_widget.setGraphicsEffect(shadow)
        left_layout.addWidget(self.video_widget, 1)
        
        # Status bar
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_label = QLabel("● ACTIVE")
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 230, 118, 255);
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 1px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        # Camera selector
        camera_label = QLabel("Camera:")
        camera_label.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 12px;
                font-family: 'Segoe UI', Arial;
                margin-left: 20px;
            }
        """)
        status_layout.addWidget(camera_label)
        
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
                padding: 5px 10px;
                font-size: 12px;
                min-width: 100px;
                font-family: 'Segoe UI', Arial;
            }
            QComboBox:hover {
                border: 1px solid rgba(100, 150, 255, 0.5);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
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
        status_layout.addWidget(self.camera_selector)
        
        # Add Face Scanner button
        scanner_btn = QPushButton("📸 Add Person")
        scanner_btn.clicked.connect(self.open_face_scanner)
        scanner_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        scanner_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(0, 200, 100),
                    stop:1 rgb(0, 230, 118)
                );
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 15px;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(0, 210, 110),
                    stop:1 rgb(0, 240, 128)
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(0, 180, 90),
                    stop:1 rgb(0, 210, 108)
                );
            }
        """)
        status_layout.addWidget(scanner_btn)
        
        # Settings button
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.open_settings)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(100, 150, 255),
                    stop:1 rgb(120, 170, 255)
                );
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 10px;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(110, 160, 255),
                    stop:1 rgb(130, 180, 255)
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(90, 140, 245),
                    stop:1 rgb(110, 160, 245)
                );
            }
        """)
        status_layout.addWidget(settings_btn)
        
        self.fps_label = QLabel("FPS: 0")
        self.fps_label.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 12px;
                font-family: 'Segoe UI', Arial;
                margin-left: 20px;
            }
        """)
        status_layout.addStretch()
        status_layout.addWidget(self.fps_label)
        
        left_layout.addWidget(status_widget)
        
        main_layout.addWidget(left_container, 2)
        
        # Right side - Profile card
        self.profile_card = ProfileCard()
        
        # Initialize with scanning state
        from person_profiles import PersonProfile
        scanning_profile = PersonProfile(
            "No Face Detected",
            age="---",
            gender="---",
            occupation="Scanning...",
            nationality="---",
            status="SCANNING",
            threat_level="UNKNOWN",
            notes="Position a face in the camera view to begin recognition."
        )
        self.profile_card.updateProfile(scanning_profile)
        
        main_layout.addWidget(self.profile_card, 0)
        
        # Set window style
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
    
    def open_face_scanner(self):
        """Open the face scanner window"""
        from face_scanner_modern import FaceScannerWindow
        
        # Pause the main video timer
        self.timer.stop()
        
        # Create and show scanner window
        self.scanner_window = FaceScannerWindow()
        self.scanner_window.finished.connect(self.on_scanner_closed)
        self.scanner_window.show()
    
    def on_scanner_closed(self):
        """Handle scanner window close"""
        # Reload known faces in case new ones were added
        self.load_known_faces()
        
        # Resume video timer
        self.timer.start(30)
        
        print("✓ Face scanner closed, database reloaded")
    
    def open_settings(self):
        """Open settings dialog"""
        # Pause video timer
        self.timer.stop()
        
        # Create and show settings dialog
        dialog = SettingsDialog(self)
        dialog.settings_changed.connect(self.apply_settings)
        
        if dialog.exec():
            print("✓ Settings saved successfully")
        
        # Resume video timer
        self.timer.start(30)
    
    def apply_settings(self):
        """Apply updated settings to the application"""
        print("⚙️ Applying new settings...")
        
        # Update FPS display visibility
        self.fps_label.setVisible(settings.get("show_fps", True))
        
        # Reload profile card to apply new colors
        if hasattr(self, 'current_profile') and self.current_profile:
            self.profile_card.updateProfile(self.current_profile)
        
        print("✓ Settings applied (some changes require restart)")
    
        
    def update_frame(self):
        """Update video frame and process faces"""
        ret, frame = self.video_capture.read()
        if not ret:
            return
            
        self.frame_count += 1
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Process faces every other frame for performance
        if self.process_this_frame:
            # Detect faces
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            blob = cv2.dnn.blobFromImage(small_frame, 1.0, (300, 300),
                                        (104.0, 177.0, 123.0))
            self.face_detector.setInput(blob)
            detections = self.face_detector.forward()
            
            face_locations = []
            face_names = []
            
            h, w = small_frame.shape[:2]
            
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                
                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (x1, y1, x2, y2) = box.astype("int")
                    
                    # Scale back up
                    x1, y1, x2, y2 = x1*2, y1*2, x2*2, y2*2
                    
                    # Ensure coordinates are within frame
                    x1 = max(0, x1)
                    y1 = max(0, y1)
                    x2 = min(frame.shape[1], x2)
                    y2 = min(frame.shape[0], y2)
                    
                    face_locations.append((x1, y1, x2, y2))
                    
                    # Get face encoding
                    face_image = frame[y1:y2, x1:x2]
                    
                    if face_image.size > 0:
                        try:
                            blob = cv2.dnn.blobFromImage(
                                face_image, 1.0/255, (96, 96),
                                (0, 0, 0), swapRB=True, crop=False
                            )
                            self.face_recognizer.setInput(blob)
                            encoding = self.face_recognizer.forward()[0]
                            
                            # Match with known faces
                            name = "Unknown"
                            if len(self.known_face_encodings) > 0:
                                distances = np.linalg.norm(
                                    self.known_face_encodings - encoding,
                                    axis=1
                                )
                                best_match_idx = np.argmin(distances)
                                min_distance = distances[best_match_idx]
                                
                                print(f"DEBUG: Best match distance: {min_distance:.3f} for {self.known_face_names[best_match_idx]}")
                                
                                # More lenient threshold
                                if min_distance < 0.8:
                                    name = self.known_face_names[best_match_idx]
                                    print(f"✓ Recognized: {name} (distance: {min_distance:.3f})")
                                else:
                                    print(f"✗ No match found (closest was {self.known_face_names[best_match_idx]} at {min_distance:.3f})")
                            
                            face_names.append(name)
                        except:
                            face_names.append("Unknown")
                    else:
                        face_names.append("Unknown")
            
            # Update profile for first detected face
            if len(face_names) > 0:
                print(f"DEBUG: Detected faces: {face_names}")
                if face_names[0] != "Unknown":
                    profile = get_profile(face_names[0])
                    print(f"DEBUG: Loaded profile - Name: {profile.name}, Age: {profile.age}, Status: {profile.status}")
                    # Always update to ensure fresh data
                    self.profile_card.updateProfile(profile)
                    self.current_profile = profile
                else:
                    # Show unknown profile
                    from person_profiles import PersonProfile
                    unknown_profile = PersonProfile(
                        "Unknown Person",
                        age="?",
                        gender="Unknown",
                        occupation="Unknown",
                        nationality="Unknown",
                        status="UNIDENTIFIED",
                        threat_level="UNKNOWN",
                        notes="Face detected but not in database. Use Face Scanner to register."
                    )
                    self.profile_card.updateProfile(unknown_profile)
            else:
                # No faces detected - show scanning state
                if self.frame_count % 100 == 0:  # Update every ~3 seconds
                    from person_profiles import PersonProfile
                    scanning_profile = PersonProfile(
                        "Scanning",
                        age="---",
                        gender="---",
                        occupation="Searching for faces...",
                        nationality="---",
                        status="SCANNING",
                        threat_level="UNKNOWN",
                        notes="Position a face in the camera view to begin recognition."
                    )
                    self.profile_card.updateProfile(scanning_profile)
            
            # Draw face boxes
            for (x1, y1, x2, y2), name in zip(face_locations, face_names):
                # Modern face box with glowing effect
                color = (100, 150, 255)
                
                # Main rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 100), 2)
                
                # Corner accents
                corner_length = 25
                thickness = 3
                
                # Animated pulse
                pulse = abs(np.sin(self.frame_count * 0.1))
                animated_color = tuple(int((0.6 + 0.4 * pulse) * c) for c in color)
                
                # Top-left
                cv2.line(frame, (x1, y1), (x1 + corner_length, y1), animated_color, thickness)
                cv2.line(frame, (x1, y1), (x1, y1 + corner_length), animated_color, thickness)
                
                # Top-right
                cv2.line(frame, (x2, y1), (x2 - corner_length, y1), animated_color, thickness)
                cv2.line(frame, (x2, y1), (x2, y1 + corner_length), animated_color, thickness)
                
                # Bottom-left
                cv2.line(frame, (x1, y2), (x1 + corner_length, y2), animated_color, thickness)
                cv2.line(frame, (x1, y2), (x1, y2 - corner_length), animated_color, thickness)
                
                # Bottom-right
                cv2.line(frame, (x2, y2), (x2 - corner_length, y2), animated_color, thickness)
                cv2.line(frame, (x2, y2), (x2, y2 - corner_length), animated_color, thickness)
                
                # Name label with background
                if name != "Unknown":
                    label = name
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.7
                    thickness = 2
                    
                    (text_width, text_height), baseline = cv2.getTextSize(
                        label, font, font_scale, thickness
                    )
                    
                    # Background
                    cv2.rectangle(frame, 
                                (x1, y2 + 5), 
                                (x1 + text_width + 10, y2 + text_height + baseline + 10),
                                (30, 33, 41), -1)
                    
                    # Text
                    cv2.putText(frame, label, 
                              (x1 + 5, y2 + text_height + 10),
                              font, font_scale, (255, 255, 255), thickness)
        
        self.process_this_frame = not self.process_this_frame
        
        # Convert to QImage and display
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        self.video_widget.setImage(qt_image)
        
        # Update FPS
        if self.frame_count % 30 == 0:
            self.fps_label.setText(f"FPS: {30}")
            
    def closeEvent(self, event):
        """Clean up on close"""
        self.video_capture.release()
        event.accept()


def main():
    """Launch the modern application"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = ModernMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
