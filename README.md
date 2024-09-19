## How to Use

1. Ensure you have compatible Python and PIP versions to setup Mediapipe.<br>
   1.1) Python version 3.8 - 3.11. You can download python 3.11.0 from official website: [Python Downloads](https://www.python.org/downloads/release/python-3110/)

   1.2) PIP version: 20.3+, upgrade it if needed:
```bash
python3 -m pip install --upgrade pip
```
2. Clone repository, move to the directory and install requirements.txt file:
```bash
git clone <repo-url>
cd <repo-directory>
pip3 install -r requirements.txt
```
3. Install mediapipe and necessary tools:
```bash
python3 -m pip install mediapipe
xcode-select --install  # Installs Xcode command line tools
brew install gcc  # Installs GCC compiler
```
4. Run the application:
```bash
python3 app.py
```


## Features (macOS)
Uses hand gesture recognition to control various window management actions on a Mac:
- Close Window.
- Minimize window.
- Enter Full Screen.
- Drag and Drop window.


## Key Benefits
- Fatigue reduction associated with prolonged mouse or touchpad usage.
- Potentially prevents musculoskeletal issues.
- Increased productivity, saving about 5 days per year.
- Worldwide impact on ergonomic computer interaction.
- Potential for a groundbreaking development and adoption.


 ## Project Directory Structure
 ```
 MAC-CONTROL-GESTURES/
│
│── app.py                                              # Entry point of the application
│── README.md                                           # Project documentation
│── requirements.txt                                    # Required Python packages  
│
│── controller/                                         # Controller folder
│    │── __init__.py                                    # Recognize the directory as a package
│    └── gesture_controller.py                          # Process gestures and coordinate between model and view
│
│── utils/                                              # Utils folder                            
│    │── __init__.py                                    # Recognize the directory as a package
│    └── gesture_checks.py                              # Additional checks for gesture inputs
│
│── model/                                              # Model folder
│    │── __init__.py                                    # Recognize the directory as a package
│    │── hand_detector.py                               # Defines hand detection data models
│    └── window_manager.py                              # Defines window manager data models
│
└── view/                                               # View folder                                           
     │── __init__.py                                     # Recognize the directory as a package
     └── main_view.py                                    # Handles displaying video feed with landmarks
```

## License
This project is licensed under the MIT License - see the [LICENSE](license) file for details.
