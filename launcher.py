"""
L1GHT REC0N Launcher
Choose between modern PyQt6 UI or classic OpenCV interface
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette


class LauncherButton(QPushButton):
    """Custom styled button for launcher"""
    
    def __init__(self, text, description, primary=False):
        super().__init__()
        self.text_label = text
        self.description = description
        self.setMinimumHeight(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        title = QLabel(text)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: 700;
                font-family: 'Segoe UI', Arial;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel(description)
        desc.setStyleSheet("""
            QLabel {
                color: rgba(200, 200, 200, 255);
                font-size: 13px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(66, 165, 245),
                        stop:1 rgb(100, 150, 255)
                    );
                    border: none;
                    border-radius: 15px;
                    padding: 20px;
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
                    border: 2px solid rgba(255, 255, 255, 0.15);
                    border-radius: 15px;
                    padding: 20px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.12);
                    border: 2px solid rgba(255, 255, 255, 0.25);
                }
                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.05);
                }
            """)


class LauncherWindow(QMainWindow):
    """Main launcher window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("L1GHT REC0N Launcher")
        self.setFixedSize(700, 600)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Logo/Title
        title = QLabel("L1GHT REC0N")
        title.setStyleSheet("""
            QLabel {
                color: rgba(100, 150, 255, 255);
                font-size: 48px;
                font-weight: 700;
                letter-spacing: 4px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Advanced Face Recognition System")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 255);
                font-size: 16px;
                letter-spacing: 2px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Mode selection
        mode_label = QLabel("Select Interface")
        mode_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial;
            }
        """)
        layout.addWidget(mode_label)
        
        # Modern UI button
        modern_btn = LauncherButton(
            "🚀 Modern Interface",
            "PyQt6-based UI with glassmorphism effects and smooth animations",
            primary=True
        )
        modern_btn.clicked.connect(self.launch_modern)
        layout.addWidget(modern_btn)
        
        # Classic UI button
        classic_btn = LauncherButton(
            "⚡ Classic Interface",
            "OpenCV-based interface with sci-fi themed overlay",
            primary=False
        )
        classic_btn.clicked.connect(self.launch_classic)
        layout.addWidget(classic_btn)
        
        layout.addSpacing(20)
        
        # Scanner button
        scanner_label = QLabel("Face Registration")
        scanner_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial;
            }
        """)
        layout.addWidget(scanner_label)
        
        scanner_btn = LauncherButton(
            "📸 Face Scanner",
            "Register new subjects to the database",
            primary=False
        )
        scanner_btn.clicked.connect(self.launch_scanner)
        layout.addWidget(scanner_btn)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel("Press ESC or Q to exit any interface")
        footer.setStyleSheet("""
            QLabel {
                color: rgba(120, 120, 120, 255);
                font-size: 12px;
                font-family: 'Segoe UI', Arial;
            }
        """)
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)
        
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
        
    def launch_modern(self):
        """Launch modern PyQt6 interface"""
        self.close()
        try:
            import main_modern
            main_modern.main()
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to launch modern interface:\n{str(e)}\n\n"
                               f"Make sure PyQt6 is installed:\npip install PyQt6")
            sys.exit(1)
            
    def launch_classic(self):
        """Launch classic OpenCV interface"""
        self.close()
        try:
            from person_profiles import main as classic_main
            classic_main()
        except Exception as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to launch classic interface:\n{str(e)}")
            sys.exit(1)
            
    def launch_scanner(self):
        """Launch face scanner"""
        self.close()
        try:
            import face_scanner_modern
            face_scanner_modern.main()
        except Exception as e:
            # Try classic scanner as fallback
            try:
                import face_scanner
                face_scanner.main()
            except:
                QMessageBox.critical(self, "Error",
                                   f"Failed to launch face scanner:\n{str(e)}")
                sys.exit(1)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Check for required files
    import os
    required_files = [
        "deploy.prototxt",
        "res10_300x300_ssd_iter_140000.caffemodel",
        "openface_nn4.small2.v1.t7"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Missing Model Files")
        msg.setText("Some required model files are missing.")
        msg.setInformativeText(
            "The following files will be downloaded automatically:\n\n" +
            "\n".join(missing_files) +
            "\n\nThis may take a few moments..."
        )
        msg.exec()
        
        # Download models
        try:
            from main import download_models
            download_models()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Download Failed")
            msg.setText(f"Failed to download model files:\n{str(e)}")
            msg.exec()
            sys.exit(1)
    
    window = LauncherWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
