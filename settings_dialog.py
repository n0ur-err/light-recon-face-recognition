"""
Settings Dialog for L1GHT REC0N
Modern PyQt6-based settings interface with customizable options
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QTabWidget, QWidget, QSpinBox, 
                              QDoubleSpinBox, QCheckBox, QComboBox, QSlider,
                              QGroupBox, QGraphicsDropShadowEffect, QListWidget,
                              QListWidgetItem, QLineEdit, QColorDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QPainterPath
from settings_manager import settings


class ModernGroupBox(QGroupBox):
    """Modern styled group box with glassmorphism"""
    
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 30),
                    stop:1 rgba(255, 255, 255, 15)
                );
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 14px;
                font-weight: 600;
                color: rgb(100, 150, 255);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: rgb(100, 150, 255);
            }
        """)


class ColoredListItem(QWidget):
    """List item with color preview"""
    
    def __init__(self, name, color, parent=None):
        super().__init__(parent)
        self.name = name
        self.color = color
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Color preview
        self.color_label = QLabel()
        self.color_label.setFixedSize(20, 20)
        self.color_label.setStyleSheet(f"""
            QLabel {{
                background: {color};
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.color_label)
        
        # Name label
        name_label = QLabel(name)
        name_label.setStyleSheet("color: white; font-size: 12px;")
        layout.addWidget(name_label)
        layout.addStretch()
    
    def update_color(self, color):
        """Update the color preview"""
        self.color = color
        self.color_label.setStyleSheet(f"""
            QLabel {{
                background: {color};
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
            }}
        """)


class SettingsDialog(QDialog):
    """Modern settings dialog with customizable options"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Settings - L1GHT REC0N")
        self.setModal(True)
        self.setMinimumSize(800, 700)
        
        # Store temporary settings
        self.temp_settings = settings.settings.copy()
        
        self.setup_ui()
        self.load_current_settings()
        
        # Apply glassmorphism effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 15)
        self.setGraphicsEffect(shadow)
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("⚙️ Application Settings")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                background: rgba(20, 25, 35, 200);
            }
            QTabBar::tab {
                background: rgba(30, 35, 45, 150);
                color: rgba(255, 255, 255, 180);
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(100, 150, 255),
                    stop:1 rgb(120, 170, 255)
                );
                color: white;
            }
            QTabBar::tab:hover {
                background: rgba(50, 55, 65, 200);
            }
        """)
        
        # Create tabs
        self.tabs.addTab(self.create_threat_levels_tab(), "⚠️ Threat Levels")
        self.tabs.addTab(self.create_status_types_tab(), "📋 Status Types")
        self.tabs.addTab(self.create_other_options_tab(), "🔧 Other Options")
        self.tabs.addTab(self.create_scanner_tab(), "📸 Face Scanner")
        self.tabs.addTab(self.create_recognition_tab(), "🎯 Recognition")
        self.tabs.addTab(self.create_video_tab(), "🎥 Video")
        self.tabs.addTab(self.create_ui_tab(), "🎨 Interface")
        
        layout.addWidget(self.tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self.reset_to_defaults)
        reset_btn.setStyleSheet(self.get_button_style("#FF6B6B"))
        button_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(self.get_button_style("#6C757D"))
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet(self.get_button_style("#00C864"))
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        # Dialog style
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgb(15, 18, 25),
                    stop:0.5 rgb(20, 25, 35),
                    stop:1 rgb(25, 30, 40)
                );
            }
            QLabel {
                color: rgba(255, 255, 255, 200);
                font-size: 13px;
            }
            QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {
                background: rgba(30, 35, 45, 200);
                border: 1px solid rgba(100, 150, 255, 100);
                border-radius: 6px;
                padding: 6px 10px;
                color: white;
                font-size: 12px;
                min-width: 100px;
            }
            QListWidget {
                background: rgba(30, 35, 45, 200);
                border: 1px solid rgba(100, 150, 255, 100);
                border-radius: 6px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: rgba(100, 150, 255, 100);
            }
            QCheckBox {
                color: white;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(100, 150, 255, 150);
                border-radius: 4px;
                background: rgba(30, 35, 45, 200);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(100, 150, 255),
                    stop:1 rgb(120, 170, 255)
                );
                border-color: rgb(100, 150, 255);
            }
        """)
    
    def create_threat_levels_tab(self):
        """Create threat levels customization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        info = QLabel("⚠️ Customize threat levels with your own options and colors")
        info.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 12px; margin-bottom: 10px;")
        layout.addWidget(info)
        
        # List of threat levels
        group = ModernGroupBox("Current Threat Levels")
        group_layout = QVBoxLayout()
        
        self.threat_list = QListWidget()
        self.threat_list.setMinimumHeight(200)
        group_layout.addWidget(self.threat_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add New")
        add_btn.clicked.connect(self.add_threat_level)
        add_btn.setStyleSheet(self.get_small_button_style("#00C864"))
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit Selected")
        edit_btn.clicked.connect(self.edit_threat_level)
        edit_btn.setStyleSheet(self.get_small_button_style("#0096FF"))
        btn_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("🗑️ Remove Selected")
        remove_btn.clicked.connect(self.remove_threat_level)
        remove_btn.setStyleSheet(self.get_small_button_style("#FF6B6B"))
        btn_layout.addWidget(remove_btn)
        
        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return tab
    
    def create_status_types_tab(self):
        """Create status types customization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        info = QLabel("📋 Customize status types with your own options and colors")
        info.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 12px; margin-bottom: 10px;")
        layout.addWidget(info)
        
        # List of status types
        group = ModernGroupBox("Current Status Types")
        group_layout = QVBoxLayout()
        
        self.status_list = QListWidget()
        self.status_list.setMinimumHeight(250)
        group_layout.addWidget(self.status_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add New")
        add_btn.clicked.connect(self.add_status_type)
        add_btn.setStyleSheet(self.get_small_button_style("#00C864"))
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit Selected")
        edit_btn.clicked.connect(self.edit_status_type)
        edit_btn.setStyleSheet(self.get_small_button_style("#0096FF"))
        btn_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton("🗑️ Remove Selected")
        remove_btn.clicked.connect(self.remove_status_type)
        remove_btn.setStyleSheet(self.get_small_button_style("#FF6B6B"))
        btn_layout.addWidget(remove_btn)
        
        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return tab
    
    def create_other_options_tab(self):
        """Create other customizable options tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Gender options
        group = ModernGroupBox("Gender Options")
        group_layout = QVBoxLayout()
        
        self.gender_list = QListWidget()
        self.gender_list.setMinimumHeight(150)
        group_layout.addWidget(self.gender_list)
        
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Option")
        add_btn.clicked.connect(self.add_gender_option)
        add_btn.setStyleSheet(self.get_small_button_style("#00C864"))
        btn_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("🗑️ Remove Selected")
        remove_btn.clicked.connect(self.remove_gender_option)
        remove_btn.setStyleSheet(self.get_small_button_style("#FF6B6B"))
        btn_layout.addWidget(remove_btn)
        
        group_layout.addLayout(btn_layout)
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return tab
    
    def create_scanner_tab(self):
        """Create face scanner settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Auto Capture Settings
        group = ModernGroupBox("🤖 Auto Capture")
        group_layout = QVBoxLayout()
        
        self.auto_capture_cb = QCheckBox("Enable Auto Capture Mode by Default")
        group_layout.addWidget(self.auto_capture_cb)
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Auto Capture Interval (seconds):"))
        self.auto_interval_spin = QDoubleSpinBox()
        self.auto_interval_spin.setRange(0.5, 10.0)
        self.auto_interval_spin.setSingleStep(0.5)
        self.auto_interval_spin.setDecimals(1)
        row.addWidget(self.auto_interval_spin)
        row.addStretch()
        group_layout.addLayout(row)
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Target Number of Captures:"))
        self.capture_count_spin = QSpinBox()
        self.capture_count_spin.setRange(1, 20)
        row.addWidget(self.capture_count_spin)
        row.addStretch()
        group_layout.addLayout(row)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Default Values
        group = ModernGroupBox("📋 Default Profile Values")
        group_layout = QVBoxLayout()
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Default Status:"))
        self.default_status_combo = QComboBox()
        row.addWidget(self.default_status_combo)
        row.addStretch()
        group_layout.addLayout(row)
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Default Threat Level:"))
        self.default_threat_combo = QComboBox()
        row.addWidget(self.default_threat_combo)
        row.addStretch()
        group_layout.addLayout(row)
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Default Gender:"))
        self.default_gender_combo = QComboBox()
        row.addWidget(self.default_gender_combo)
        row.addStretch()
        group_layout.addLayout(row)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return tab
    
    def create_recognition_tab(self):
        """Create recognition settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        group = ModernGroupBox("🎯 Recognition Accuracy")
        group_layout = QVBoxLayout()
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Recognition Threshold:"))
        self.recognition_threshold_spin = QDoubleSpinBox()
        self.recognition_threshold_spin.setRange(0.1, 1.5)
        self.recognition_threshold_spin.setSingleStep(0.05)
        self.recognition_threshold_spin.setDecimals(2)
        row.addWidget(self.recognition_threshold_spin)
        self.recognition_threshold_label = QLabel("0.80")
        self.recognition_threshold_label.setStyleSheet("color: rgb(100, 150, 255);")
        row.addWidget(self.recognition_threshold_label)
        row.addStretch()
        group_layout.addLayout(row)
        self.recognition_threshold_spin.valueChanged.connect(
            lambda v: self.recognition_threshold_label.setText(f"{v:.2f}")
        )
        
        info = QLabel("ℹ️ Lower = stricter | Higher = more lenient")
        info.setStyleSheet("color: rgba(255, 255, 255, 120); font-size: 11px;")
        group_layout.addWidget(info)
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Face Detection Confidence:"))
        self.confidence_threshold_spin = QDoubleSpinBox()
        self.confidence_threshold_spin.setRange(0.1, 1.0)
        self.confidence_threshold_spin.setSingleStep(0.05)
        self.confidence_threshold_spin.setDecimals(2)
        row.addWidget(self.confidence_threshold_spin)
        row.addStretch()
        group_layout.addLayout(row)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        group = ModernGroupBox("⚡ Performance")
        group_layout = QVBoxLayout()
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Process Every N Frames:"))
        self.process_frames_spin = QSpinBox()
        self.process_frames_spin.setRange(1, 10)
        row.addWidget(self.process_frames_spin)
        row.addStretch()
        group_layout.addLayout(row)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return tab
    
    def create_video_tab(self):
        """Create video settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        group = ModernGroupBox("📹 Camera Configuration")
        group_layout = QVBoxLayout()
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Default Camera Index:"))
        self.camera_index_spin = QSpinBox()
        self.camera_index_spin.setRange(0, 9)
        row.addWidget(self.camera_index_spin)
        row.addStretch()
        group_layout.addLayout(row)
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Width:"))
        self.camera_width_spin = QSpinBox()
        self.camera_width_spin.setRange(320, 1920)
        self.camera_width_spin.setSingleStep(160)
        row.addWidget(self.camera_width_spin)
        row.addWidget(QLabel("Height:"))
        self.camera_height_spin = QSpinBox()
        self.camera_height_spin.setRange(240, 1080)
        self.camera_height_spin.setSingleStep(120)
        row.addWidget(self.camera_height_spin)
        row.addStretch()
        group_layout.addLayout(row)
        
        self.mirror_mode_cb = QCheckBox("Mirror Video Feed")
        group_layout.addWidget(self.mirror_mode_cb)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return tab
    
    def create_ui_tab(self):
        """Create UI settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        group = ModernGroupBox("🖥️ Display Options")
        group_layout = QVBoxLayout()
        
        self.show_fps_cb = QCheckBox("Show FPS Counter")
        group_layout.addWidget(self.show_fps_cb)
        
        self.show_confidence_cb = QCheckBox("Show Detection Confidence")
        group_layout.addWidget(self.show_confidence_cb)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        group = ModernGroupBox("✨ Animation")
        group_layout = QVBoxLayout()
        
        row = QHBoxLayout()
        row.addWidget(QLabel("Animation Speed:"))
        self.animation_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.animation_speed_slider.setRange(5, 20)
        self.animation_speed_slider.setValue(10)
        self.animation_speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(50, 55, 65, 200);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(100, 150, 255),
                    stop:1 rgb(120, 170, 255)
                );
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
        """)
        row.addWidget(self.animation_speed_slider)
        self.animation_speed_label = QLabel("1.0x")
        self.animation_speed_label.setStyleSheet("color: rgb(100, 150, 255); min-width: 40px;")
        row.addWidget(self.animation_speed_label)
        group_layout.addLayout(row)
        
        self.animation_speed_slider.valueChanged.connect(
            lambda v: self.animation_speed_label.setText(f"{v/10:.1f}x")
        )
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return tab
    
    def load_current_settings(self):
        """Load current settings into controls"""
        # Load threat levels
        self.threat_list.clear()
        for item in self.temp_settings.get("threat_levels", []):
            list_item = QListWidgetItem(self.threat_list)
            widget = ColoredListItem(item["name"], item["color"])
            list_item.setSizeHint(widget.sizeHint())
            self.threat_list.setItemWidget(list_item, widget)
        
        # Load status types
        self.status_list.clear()
        for item in self.temp_settings.get("status_types", []):
            list_item = QListWidgetItem(self.status_list)
            widget = ColoredListItem(item["name"], item["color"])
            list_item.setSizeHint(widget.sizeHint())
            self.status_list.setItemWidget(list_item, widget)
        
        # Load gender options
        self.gender_list.clear()
        for option in self.temp_settings.get("gender_options", []):
            self.gender_list.addItem(option)
        
        # Populate dropdowns with current options
        self.default_status_combo.clear()
        self.default_status_combo.addItems([item["name"] for item in self.temp_settings.get("status_types", [])])
        
        self.default_threat_combo.clear()
        self.default_threat_combo.addItems([item["name"] for item in self.temp_settings.get("threat_levels", [])])
        
        self.default_gender_combo.clear()
        self.default_gender_combo.addItems(self.temp_settings.get("gender_options", []))
        
        # Scanner tab
        self.auto_capture_cb.setChecked(self.temp_settings.get("auto_capture_enabled", False))
        self.auto_interval_spin.setValue(self.temp_settings.get("auto_capture_interval", 2.0))
        self.capture_count_spin.setValue(self.temp_settings.get("capture_count_target", 5))
        
        # Set defaults
        default_status = self.temp_settings.get("default_status", "CIVILIAN")
        index = self.default_status_combo.findText(default_status)
        if index >= 0:
            self.default_status_combo.setCurrentIndex(index)
        
        default_threat = self.temp_settings.get("default_threat_level", "LOW")
        index = self.default_threat_combo.findText(default_threat)
        if index >= 0:
            self.default_threat_combo.setCurrentIndex(index)
        
        default_gender = self.temp_settings.get("default_gender", "Male")
        index = self.default_gender_combo.findText(default_gender)
        if index >= 0:
            self.default_gender_combo.setCurrentIndex(index)
        
        # Recognition tab
        self.recognition_threshold_spin.setValue(self.temp_settings.get("recognition_threshold", 0.8))
        self.confidence_threshold_spin.setValue(self.temp_settings.get("confidence_threshold", 0.5))
        self.process_frames_spin.setValue(self.temp_settings.get("process_every_n_frames", 2))
        
        # Video tab
        self.camera_index_spin.setValue(self.temp_settings.get("camera_index", 0))
        self.camera_width_spin.setValue(self.temp_settings.get("camera_width", 1280))
        self.camera_height_spin.setValue(self.temp_settings.get("camera_height", 720))
        self.mirror_mode_cb.setChecked(self.temp_settings.get("mirror_mode", True))
        
        # UI tab
        self.show_fps_cb.setChecked(self.temp_settings.get("show_fps", True))
        self.show_confidence_cb.setChecked(self.temp_settings.get("show_confidence", False))
        self.animation_speed_slider.setValue(int(self.temp_settings.get("animation_speed", 1.0) * 10))
    
    def add_threat_level(self):
        """Add a new threat level"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Add Threat Level", "Enter threat level name:")
        if ok and name:
            name = name.upper().strip()
            
            # Check if already exists
            if any(item["name"] == name for item in self.temp_settings.get("threat_levels", [])):
                QMessageBox.warning(self, "Error", f"Threat level '{name}' already exists!")
                return
            
            # Pick color
            color = QColorDialog.getColor(QColor("#FF0000"), self, "Choose Color")
            if color.isValid():
                threat_levels = self.temp_settings.get("threat_levels", [])
                threat_levels.append({"name": name, "color": color.name()})
                self.temp_settings["threat_levels"] = threat_levels
                
                # Refresh list
                list_item = QListWidgetItem(self.threat_list)
                widget = ColoredListItem(name, color.name())
                list_item.setSizeHint(widget.sizeHint())
                self.threat_list.setItemWidget(list_item, widget)
    
    def edit_threat_level(self):
        """Edit selected threat level"""
        current_item = self.threat_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a threat level to edit!")
            return
        
        widget = self.threat_list.itemWidget(current_item)
        old_name = widget.name
        
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Edit Threat Level", "Enter new name:", text=old_name)
        if ok and name:
            name = name.upper().strip()
            
            # Pick new color
            color = QColorDialog.getColor(QColor(widget.color), self, "Choose Color")
            if color.isValid():
                # Update in temp settings
                threat_levels = self.temp_settings.get("threat_levels", [])
                for item in threat_levels:
                    if item["name"] == old_name:
                        item["name"] = name
                        item["color"] = color.name()
                        break
                
                # Update widget
                widget.name = name
                widget.update_color(color.name())
    
    def remove_threat_level(self):
        """Remove selected threat level"""
        current_item = self.threat_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a threat level to remove!")
            return
        
        widget = self.threat_list.itemWidget(current_item)
        name = widget.name
        
        reply = QMessageBox.question(self, "Confirm", f"Remove threat level '{name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Remove from temp settings
            threat_levels = self.temp_settings.get("threat_levels", [])
            self.temp_settings["threat_levels"] = [item for item in threat_levels if item["name"] != name]
            
            # Remove from list
            self.threat_list.takeItem(self.threat_list.row(current_item))
    
    def add_status_type(self):
        """Add a new status type"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Add Status Type", "Enter status type name:")
        if ok and name:
            name = name.upper().strip()
            
            # Check if already exists
            if any(item["name"] == name for item in self.temp_settings.get("status_types", [])):
                QMessageBox.warning(self, "Error", f"Status type '{name}' already exists!")
                return
            
            # Pick color
            color = QColorDialog.getColor(QColor("#0096FF"), self, "Choose Color")
            if color.isValid():
                status_types = self.temp_settings.get("status_types", [])
                status_types.append({"name": name, "color": color.name()})
                self.temp_settings["status_types"] = status_types
                
                # Refresh list
                list_item = QListWidgetItem(self.status_list)
                widget = ColoredListItem(name, color.name())
                list_item.setSizeHint(widget.sizeHint())
                self.status_list.setItemWidget(list_item, widget)
    
    def edit_status_type(self):
        """Edit selected status type"""
        current_item = self.status_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a status type to edit!")
            return
        
        widget = self.status_list.itemWidget(current_item)
        old_name = widget.name
        
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Edit Status Type", "Enter new name:", text=old_name)
        if ok and name:
            name = name.upper().strip()
            
            # Pick new color
            color = QColorDialog.getColor(QColor(widget.color), self, "Choose Color")
            if color.isValid():
                # Update in temp settings
                status_types = self.temp_settings.get("status_types", [])
                for item in status_types:
                    if item["name"] == old_name:
                        item["name"] = name
                        item["color"] = color.name()
                        break
                
                # Update widget
                widget.name = name
                widget.update_color(color.name())
    
    def remove_status_type(self):
        """Remove selected status type"""
        current_item = self.status_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a status type to remove!")
            return
        
        widget = self.status_list.itemWidget(current_item)
        name = widget.name
        
        reply = QMessageBox.question(self, "Confirm", f"Remove status type '{name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Remove from temp settings
            status_types = self.temp_settings.get("status_types", [])
            self.temp_settings["status_types"] = [item for item in status_types if item["name"] != name]
            
            # Remove from list
            self.status_list.takeItem(self.status_list.row(current_item))
    
    def add_gender_option(self):
        """Add a new gender option"""
        from PyQt6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Add Gender Option", "Enter gender option:")
        if ok and name:
            name = name.strip()
            
            gender_options = self.temp_settings.get("gender_options", [])
            if name not in gender_options:
                gender_options.append(name)
                self.temp_settings["gender_options"] = gender_options
                self.gender_list.addItem(name)
            else:
                QMessageBox.warning(self, "Error", f"Gender option '{name}' already exists!")
    
    def remove_gender_option(self):
        """Remove selected gender option"""
        current_item = self.gender_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a gender option to remove!")
            return
        
        name = current_item.text()
        
        reply = QMessageBox.question(self, "Confirm", f"Remove gender option '{name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            gender_options = self.temp_settings.get("gender_options", [])
            self.temp_settings["gender_options"] = [item for item in gender_options if item != name]
            
            self.gender_list.takeItem(self.gender_list.row(current_item))
    
    def save_settings(self):
        """Save settings and close dialog"""
        # Update from controls
        self.temp_settings["auto_capture_enabled"] = self.auto_capture_cb.isChecked()
        self.temp_settings["auto_capture_interval"] = self.auto_interval_spin.value()
        self.temp_settings["capture_count_target"] = self.capture_count_spin.value()
        self.temp_settings["default_status"] = self.default_status_combo.currentText()
        self.temp_settings["default_threat_level"] = self.default_threat_combo.currentText()
        self.temp_settings["default_gender"] = self.default_gender_combo.currentText()
        
        self.temp_settings["recognition_threshold"] = self.recognition_threshold_spin.value()
        self.temp_settings["confidence_threshold"] = self.confidence_threshold_spin.value()
        self.temp_settings["process_every_n_frames"] = self.process_frames_spin.value()
        
        self.temp_settings["camera_index"] = self.camera_index_spin.value()
        self.temp_settings["camera_width"] = self.camera_width_spin.value()
        self.temp_settings["camera_height"] = self.camera_height_spin.value()
        self.temp_settings["mirror_mode"] = self.mirror_mode_cb.isChecked()
        
        self.temp_settings["show_fps"] = self.show_fps_cb.isChecked()
        self.temp_settings["show_confidence"] = self.show_confidence_cb.isChecked()
        self.temp_settings["animation_speed"] = self.animation_speed_slider.value() / 10.0
        
        # Save to settings manager
        settings.settings = self.temp_settings.copy()
        if settings.save_settings():
            self.settings_changed.emit()
            self.accept()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(self, "Confirm Reset", 
                                     "Reset all settings to defaults?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.temp_settings = settings.DEFAULT_SETTINGS.copy()
            self.load_current_settings()
    
    def get_button_style(self, color):
        """Get button stylesheet"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                min-width: 120px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """
    
    def get_small_button_style(self, color):
        """Get small button stylesheet"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """
