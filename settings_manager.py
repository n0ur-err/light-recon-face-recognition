"""
Settings Manager for L1GHT REC0N
Handles app settings persistence and customizable options
"""

import json
import os
from pathlib import Path


class SettingsManager:
    """Manages application settings and customizable options"""
    
    DEFAULT_SETTINGS = {
        # Add Person / Face Scanner Settings
        "auto_capture_enabled": False,
        "auto_capture_interval": 2.0,
        "capture_count_target": 5,
        "scanner_camera_index": 0,
        
        # Recognition Settings
        "recognition_threshold": 0.8,
        "confidence_threshold": 0.5,
        "process_every_n_frames": 2,
        
        # Video Settings
        "camera_index": 0,
        "camera_width": 1280,
        "camera_height": 720,
        "mirror_mode": True,
        
        # UI Settings
        "show_fps": True,
        "show_confidence": False,
        "animation_speed": 1.0,
        
        # Customizable Options - Users can add/remove/edit these
        "threat_levels": [
            {"name": "LOW", "color": "#00C864"},
            {"name": "MODERATE", "color": "#FFA500"},
            {"name": "HIGH", "color": "#FF4444"},
            {"name": "CRITICAL", "color": "#8B0000"},
        ],
        
        "status_types": [
            {"name": "CIVILIAN", "color": "#6C757D"},
            {"name": "VIP", "color": "#FFD700"},
            {"name": "EMPLOYEE", "color": "#0096FF"},
            {"name": "VISITOR", "color": "#9370DB"},
            {"name": "WANTED", "color": "#DC143C"},
            {"name": "UNKNOWN", "color": "#808080"},
        ],
        
        "gender_options": [
            "Male",
            "Female", 
            "Other",
            "Prefer not to say"
        ],
        
        # Default values
        "default_status": "CIVILIAN",
        "default_threat_level": "LOW",
        "default_gender": "Male",
    }
    
    def __init__(self):
        self.settings_file = Path(__file__).parent / "settings.json"
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or return defaults"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to handle new settings
                    merged = self.DEFAULT_SETTINGS.copy()
                    merged.update(loaded_settings)
                    return merged
            except Exception as e:
                print(f"⚠ Error loading settings: {e}")
                return self.DEFAULT_SETTINGS.copy()
        return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            print("✓ Settings saved successfully")
            return True
        except Exception as e:
            print(f"✗ Error saving settings: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save_settings()
    
    # Helper methods for customizable options
    
    def get_threat_levels(self):
        """Get list of threat level names"""
        return [item["name"] for item in self.settings.get("threat_levels", [])]
    
    def get_threat_level_color(self, name):
        """Get color for a specific threat level"""
        for item in self.settings.get("threat_levels", []):
            if item["name"] == name:
                return item["color"]
        return "#808080"  # Default gray
    
    def get_status_types(self):
        """Get list of status type names"""
        return [item["name"] for item in self.settings.get("status_types", [])]
    
    def get_status_color(self, name):
        """Get color for a specific status type"""
        for item in self.settings.get("status_types", []):
            if item["name"] == name:
                return item["color"]
        return "#808080"  # Default gray
    
    def add_threat_level(self, name, color):
        """Add a new threat level"""
        threat_levels = self.settings.get("threat_levels", [])
        if not any(item["name"] == name for item in threat_levels):
            threat_levels.append({"name": name, "color": color})
            self.settings["threat_levels"] = threat_levels
            return True
        return False
    
    def remove_threat_level(self, name):
        """Remove a threat level"""
        threat_levels = self.settings.get("threat_levels", [])
        self.settings["threat_levels"] = [
            item for item in threat_levels if item["name"] != name
        ]
    
    def update_threat_level(self, old_name, new_name, color):
        """Update a threat level"""
        threat_levels = self.settings.get("threat_levels", [])
        for item in threat_levels:
            if item["name"] == old_name:
                item["name"] = new_name
                item["color"] = color
                break
        self.settings["threat_levels"] = threat_levels
    
    def add_status_type(self, name, color):
        """Add a new status type"""
        status_types = self.settings.get("status_types", [])
        if not any(item["name"] == name for item in status_types):
            status_types.append({"name": name, "color": color})
            self.settings["status_types"] = status_types
            return True
        return False
    
    def remove_status_type(self, name):
        """Remove a status type"""
        status_types = self.settings.get("status_types", [])
        self.settings["status_types"] = [
            item for item in status_types if item["name"] != name
        ]
    
    def update_status_type(self, old_name, new_name, color):
        """Update a status type"""
        status_types = self.settings.get("status_types", [])
        for item in status_types:
            if item["name"] == old_name:
                item["name"] = new_name
                item["color"] = color
                break
        self.settings["status_types"] = status_types
    
    def add_gender_option(self, name):
        """Add a new gender option"""
        gender_options = self.settings.get("gender_options", [])
        if name not in gender_options:
            gender_options.append(name)
            self.settings["gender_options"] = gender_options
            return True
        return False
    
    def remove_gender_option(self, name):
        """Remove a gender option"""
        gender_options = self.settings.get("gender_options", [])
        self.settings["gender_options"] = [
            item for item in gender_options if item != name
        ]


# Global settings instance
settings = SettingsManager()
