<div align="center">

# 🔷 L1GHT REC0N

### Next-Generation Face Recognition System

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0-brightgreen)](https://opencv.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6.0%2B-41cd52)](https://www.riverbankcomputing.com/software/pyqt/)
[![CUDA](https://img.shields.io/badge/CUDA-Compatible-orange)](https://developer.nvidia.com/cuda-toolkit)

**A cutting-edge face recognition system featuring a stunning 2026-style modern UI with glassmorphism effects, real-time detection, and comprehensive profile management.**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Documentation](#-documentation)

---

![L1GHT REC0N Interface Preview](img.jpg)

</div>

## ✨ Features

### 🎨 **Modern Interface**
- **Glassmorphism Design**: Translucent panels with beautiful blur effects
- **Smooth Animations**: Fluid transitions, pulsing effects, and animated entrance
- **Gradient Backgrounds**: Multi-color gradients that create depth
- **Responsive Layout**: Adapts seamlessly to any screen size
- **Dark Theme**: Easy on the eyes with modern color palette
- **⚙️ Customizable Settings**: Comprehensive settings dialog with personalization options

### 🚀 **Dual Interface System**
Choose your experience:
- **🔷 Modern Interface**: PyQt6-based desktop app with 2026-style design
- **⚡ Classic Interface**: OpenCV-based sci-fi themed overlay (legacy)

### 📸 **Integrated Face Scanner**
- **Built-in Registration**: Click "📸 Add Person" button without leaving the app
- **Auto-Capture Mode**: Automatically capture multiple angles
- **Manual Control**: Precise control over image capture
- **Live Preview**: Real-time face detection feedback
- **Instant Recognition**: Newly added faces recognized immediately

### 🎯 **Advanced Recognition**
- **Real-time Detection**: Fast and accurate face detection using OpenCV DNN
- **Deep Learning**: OpenFace neural network for 128-dimensional embeddings
- **Multi-Face Support**: Detects and tracks multiple faces simultaneously
- **GPU Acceleration**: CUDA support for enhanced performance
- **Adjustable Threshold**: Configurable recognition sensitivity

### 📊 **Profile Management**
- **Comprehensive Profiles**: Name, age, gender, occupation, nationality
- **Status Tracking**: Civilian, VIP, Employee, Visitor, Wanted
- **Threat Levels**: Low, Moderate, High with color coding
- **Sighting Counter**: Automatic tracking of encounters
- **Notes System**: Additional information storage
- **JSON Storage**: Easy to edit and backup

### 🎥 **Camera Features**
- **Multi-Camera Support**: Automatically detects all available cameras
- **Hot-Swap Cameras**: Switch between cameras without restarting
- **High Resolution**: Supports up to 1280x720 video feed
- **Mirror Mode**: Flipped view for natural interaction

### ⚙️ **Fully Customizable Options**
- **Custom Threat Levels**: Add your own threat levels (e.g., EXTREME, CRITICAL) with custom colors
- **Custom Status Types**: Create unlimited status types (e.g., SUSPECT, ALLY, CONTRACTOR) with custom colors
- **Custom Gender Options**: Add any gender options you need
- **Profile Defaults**: Set default values for new profiles
- **Recognition Tuning**: Adjust thresholds via GUI without code editing
- **Performance Options**: Configure frame processing and camera settings
- **Persistent Storage**: All customizations saved automatically

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Webcam**: Any USB or built-in camera

### Software Dependencies
- **PyQt6** 6.6.0+ - Modern UI framework
- **OpenCV** 4.11.0+ - Computer vision library
### Quick Install

```bash
# Clone the repository
git clone https://github.com/nour23019870/light-recon-face-recognition.git
cd light-recon-face-recognition

# Install dependencies
pip install -r requirements.txt
```

### Model Files
**Automatic Download**: Model files are downloaded automatically on first run.

**Manual Download** (optional):
- [deploy.prototxt](https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt) - Face detection config
- [res10_300x300_ssd_iter_140000.caffemodel](https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel) - Face detection weights
- [openface_nn4.small2.v1.t7](https://github.com/pyannote/pyannote-data/raw/master/openface.nn4.small2.v1.t7) - Face recognition model
🎯 Quick Start

### First Time Setup

**Step 1: Launch the App**
```bash
python launcher.py
```

**Step 2: Choose Modern Interface**
Click **🚀 Modern Interface** from the launcher

**Step 3: Add Your First Profile**
1. Click **📸 Add Person** button (bottom of screen)
2. Position your face in the camera view
3. Click **Capture Image** or enable **Auto Capture**
4. Take 5-10 images from different angles
5. Fill in your name and details
6. Click **Save Profile**

**Step 4: Test Recognition**
Close the scanner and show your face to the camera. Your profile should appear on the right!

---

## 📖 Usage

### Launcher (Recommended)

### Modern Interface

**Direct Launch:**
```bash
python main_modern.py
```

**Features:**
- 🎨 Glassmorphism profile cards with animations
- 🖼️ Hardware-accelerated video rendering
- 🎯 Real-time face detection with animated corners
- 🌈 Gradient backgrounds and modern typography
- 📷 Camera selector - switch cameras on-the-fly
- ➕ Built-in face scanner - click "📸 Add Person"

**Controls:**
- Click **Camera dropdown** to switch cameras
- Click **📸 Add Person** to register new faces
- Click **⚙️ Settings** to customize options (threat levels, status types, colors, etc.)
- Profile updates automatically when face is recognized

---

### Classic Interface

**Direct Launch:**
```bash
python main.py
```

**Controls:**
- `F` - Toggle fullscreen mode
- `D` - Toggle detailed profile view
- `Q` or `ESC` - Quit

---

### Face Scanner

**Integrated:** Click **📸 Add Person** in modern interface

**Standalone:**
```bash
python face_scanner_modern.py
```

**Workflow:**
1. Position face in camera view
2. Capture 3-10 images (different angles recommended)
3. Fill in profile information
4. Save profile

**Tips:**
- Use **Auto Capture** mode for hands-free operation
- Capture from multiple angles for better recognition
- Ensure good lighting for best results
- Look directly at camera for at least one image
```bash
python main.py
```

Controls:
- Press `F` to toggle fullscreen mode
---

## 📖 Documentation

### How It Works

**Multi-Stage Recognition Pipeline:**

1. **Face Detection**
   - Pre-trained Caffe SSD model (300x300)
   - Detects faces in video stream at 30 FPS
   - Confidence threshold: 50%

2. **Face Extraction**
   - Crops detected face region
   - Resizes to 96x96 for recognition model
   - Normalizes pixel values (0-1 range)

3. **Feature Extraction**
   - OpenFace neural network (nn4.small2.v1)
   - Generates 128-dimensional embedding vector
   - Represents unique facial features

4. **Face Matching**
   - Calculates Euclidean distance to known faces
   - Threshold: 0.8 (configurable)
   - Returns closest match if within threshold

5. **Profile Display**
   - Loads profile data from JSON
   - Updates UI with smooth animations
   - Increments sighting counter

### Profile System

**Storage Format:** JSON files in `dataset/[name]/profile.json`

**Profile Fields:**
```json
{
  "name": "Person Name",
  "age": 30,
  "gender": "Male/Female/Other",
---

## 🎨 Customization

### ⚙️ Using the Settings Dialog (Recommended)

Click **⚙️ Settings** in the modern interface to access the comprehensive settings system:

#### ⚠️ **Threat Levels Tab**
Add, edit, or remove custom threat levels with colors:
- **Add New**: Click "➕ Add New", enter name (e.g., "EXTREME"), pick a color (e.g., purple)
- **Edit**: Select a threat level, click "✏️ Edit Selected", change name/color
- **Remove**: Select and click "🗑️ Remove Selected"
- **Built-in defaults**: LOW (green), MODERATE (orange), HIGH (red), CRITICAL (dark red)

**Example Custom Threat Levels:**
- EXTREME - Purple (#8B00FF)
- MINIMAL - Light Blue (#87CEEB)
- UNKNOWN - Gray (#808080)

#### 📋 **Status Types Tab**
Create unlimited custom status types with colors:
- **Add New**: Click "➕ Add New", enter name (e.g., "SUSPECT", "ALLY"), pick a color
- **Edit/Remove**: Same as threat levels
- **Built-in defaults**: CIVILIAN (gray), VIP (gold), EMPLOYEE (blue), VISITOR (purple), WANTED (red), UNKNOWN (gray)

**Example Custom Status Types:**
- CONTRACTOR - Orange (#FF8C00)
- FAMILY - Pink (#FF69B4)
- SECURITY - Navy (#000080)
- SUSPECT - Dark Red (#8B0000)

#### 🔧 **Other Options Tab**
- **Gender Options**: Add custom gender options (e.g., "Non-binary", "Prefer not to say")
- Click "➕ Add Option" to add new options
- Built-in defaults: Male, Female, Other, Prefer not to say

#### 📸 **Face Scanner Tab**
- **Auto Capture**: Enable/disable auto-capture mode by default
- **Capture Interval**: Time between auto-captures (0.5-10 seconds)
- **Target Captures**: How many images to capture automatically (1-20)
- **Default Values**: Set default status, threat level, and gender for new profiles

#### 🎯 **Recognition Tab**
- **Recognition Threshold**: Adjust face matching sensitivity (0.1-1.5)
  - Lower = stricter matching (fewer false positives)
  - Higher = more lenient (better for varied lighting)
  - Default: 0.80
- **Detection Confidence**: Minimum confidence to detect a face (0.1-1.0)
- **Performance**: Process every N frames (1-10) for performance tuning

#### 🎥 **Video Tab**
- **Default Camera**: Choose startup camera (0-9)
- **Resolution**: Set camera width and height
  - Common resolutions: 640x480, 1280x720, 1920x1080
- **Mirror Mode**: Enable/disable horizontal video flip

#### 🎨 **Interface Tab**
- **Show FPS Counter**: Toggle FPS display
- **Show Confidence**: Display detection confidence values
- **Animation Speed**: Adjust UI animation speed (0.5x - 2.0x)

### 💾 Settings Storage

All settings are automatically saved to `settings.json` in the project root:

```json
{
    "threat_levels": [
        {"name": "LOW", "color": "#00C864"},
        {"name": "HIGH", "color": "#FF4444"},
        {"name": "EXTREME", "color": "#8B00FF"}
    ],
    "status_types": [
        {"name": "CIVILIAN", "color": "#6C757D"},
        {"name": "SUSPECT", "color": "#DC143C"}
    ],
    "gender_options": ["Male", "Female", "Other", "Non-binary"],
    "recognition_threshold": 0.8,
    "camera_width": 1280,
    "camera_height": 720
}
```

**Manual Editing**: You can edit `settings.json` directly, but using the Settings dialog is recommended for ease of use.

### 🔧 Advanced Code Customization

#### Modify Profile Fields

Edit [person_profiles.py](person_profiles.py), `PersonProfile` class:
```python
---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🎨 Improve UI/UX design
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features

### Development Setup
```bash
git clone https://github.com/nour23019870/light-recon-face-recognition.git
cd light-recon-face-recognition
pip install -r requirements.txt
# Make your changes
# Test thoroughly
# Submit pull request
```

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Update README for new features

---

## 📄 License

This project is licensed under the **MIT License**.

**You are free to:**
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Sublicense

**Conditions:**
- Include original license
- Include copyright notice

See [LICENSE](LICENSE) file for full details.

---

## ⚠️ Legal & Privacy

### Disclaimer
This software is provided **"AS IS"** for **educational and research purposes only**.

### Important Notes
- ⚠️ Use responsibly and ethically
- 🔒 Comply with privacy laws (GDPR, CCPA, etc.)
- 👤 Obtain consent before capturing faces
- 🚫 Do not use for surveillance without authorization
- 📋 Follow local regulations on biometric data

### Liability
The developers assume **NO LIABILITY** for:
- Misuse or abuse of this software
- Damages or legal issues arising from use
- Privacy violations by users
- Accuracy of face recognition results

**Users are solely responsible for compliance with applicable laws.**

---

## 🌟 Acknowledgments

### Technologies Used
- **OpenCV** - Computer vision library
- **PyQt6** - Modern UI framework  
- **OpenFace** - Face recognition model
- **NumPy** - Numerical computing

### Inspired By
- Modern UI/UX trends of 2026
- Glassmorphism design principles
- Sci-fi interface aesthetics

---

## 📬 Support & Contact

### Get Help
- 📖 Read the [Documentation](#-documentation)
- 🐛 [Report Issues](https://github.com/nour23019870/light-recon-face-recognition/issues)
- 💬 [Discussions](https://github.com/nour23019870/light-recon-face-recognition/discussions)

### Stay Updated
- ⭐ Star this repository
- 👁️ Watch for updates
- 🔔 Enable notifications

---

<div align="center">

### Made with ❤️ by L1ght

**If you find this project useful, please consider giving it a ⭐!**

[⬆ Back to Top](#-l1ght-rec0n)

</div>()`:
```python
self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Width
self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Height
```

---

## 🐛 Troubleshooting

### Camera Not Detected
**Solution:**
- Check camera permissions in system settings
- Try different camera indices (0, 1, 2...)
- Restart the application
- Check if camera works in other apps

### Face Not Recognized
**Solution:**
- Ensure good lighting (avoid backlighting)
- Capture 5-10 training images
- Include different angles and expressions
- Increase recognition threshold to 0.9
- Check debug output for distance values

### Low FPS / Laggy
**Solution:**
- Reduce camera resolution to 640x480
- Process every 3rd frame instead of every other
- Close other camera applications
- Enable GPU acceleration (CUDA)

### Profile Data Not Showing
**Solution:**
- Check console for debug messages
- Verify profile.json exists in dataset folder
- Ensure JSON format is valid
- Restart app to reload database

### Scanner Won't Save
**Solution:**
- Capture at least 3 images
- Fill in the name field (required)
- Check write permissions in dataset folder
- Look for error messages in console
### Project Structure

```
light-recon-face-recognition/
│
├── 🚀 launcher.py                    # Main launcher (START HERE!)
├── 🎨 main_modern.py                 # Modern PyQt6 interface
├── 📸 face_scanner_modern.py         # Modern registration tool
├── ⚙️ settings_dialog.py             # Settings customization dialog
├── 💾 settings_manager.py            # Settings persistence manager
│
├── ⚡ main.py                        # Classic interface (legacy)
├── 📋 person_profiles.py             # Classic UI + profile logic
├── 🔧 face_scanner.py                # Classic scanner (legacy)
│
├── 🧠 Models/
│   ├── deploy.prototxt              # Face detection config
│   ├── res10_300x300...caffemodel   # Detection weights
│   └── openface_nn4.small2.v1.t7    # Recognition model
│
├── 📊 dataset/                       # Face database
│   └── [person_name]/
│       ├── [name]_1.jpg             # Face image 1
│       ├── [name]_2.jpg             # Face image 2
│       └── profile.json             # Profile data
│
├── ⚙️ settings.json                  # User settings & customizations
├── 📦 requirements.txt               # Python dependencies
└── 📖 README.md                      # This file
```

### Performance Optimization

**CPU Mode:**
- ~15-25 FPS on modern CPU
- Processes every other frame
- Adequate for single-camera setups

**GPU Mode (CUDA):**
- ~30+ FPS with NVIDIA GPU
- Real-time processing
- Recommended for production use

**Optimization Tips:**
- Reduce camera resolution if laggy
- Process every 3rd frame for slower systems
- Use GPU acceleration when available
- Close other applications using camera 128-dimensional feature vectors from each detected face
3. **Face Recognition**: Compares extracted feature vectors with known faces using cosine similarity
4. **Profile Display**: Shows detailed profile information with dynamic visual elements for recognized individuals

The system stores profile information in individual JSON files, making it easy to manage and update details for each person.

## 📷 Face Scanning Process

The face registration system allows you to:
1. Create a new profile for a person with customizable attributes
2. Capture multiple images of the person's face from different angles
3. Automatically detect and extract faces from captured images
4. Save profile information and face images for future recognition

## 💻 GPU Acceleration

L1GHT REC0N supports GPU acceleration through CUDA when available. To use GPU acceleration:

1. Install OpenCV with CUDA support:
   ```bash
   pip uninstall opencv-python
   pip install opencv-contrib-python-cuda
   ```

2. Make sure you have NVIDIA CUDA Toolkit installed
3. The application will automatically detect and use CUDA if available

## 👥 Profile System

Each profile contains detailed information about an individual:

- Basic information (name, age, gender)
- Demographic data (nationality, occupation)
- System-specific data (status, threat level, sighting count)
- Notes and additional information
- Last seen timestamp

## 🛠️ Customization

L1GHT REC0N can be customized in several ways:

- Modify profile attributes in the `PersonProfile` class
- Adjust detection parameters for improved performance
- Customize the visual interface by modifying the draw functions
- Add new profile fields by updating the profile schema

## 🤝 Contributing

Contributions to L1GHT REC0N are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This software is provided for educational and research purposes only. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

## 📬 Contact

For questions or suggestions, please open an issue in the GitHub repository.

---

Developed with ❤️ by L1ght
