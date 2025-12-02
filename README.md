# Humanitarian SOS SMS

As part of the design and data labs to design a shelter; we had a lot of problems with data. Also we learned a lot about peoples suffering with different humanitarian crisis.
We designed a simple Python GUI application where people can add their SOS messages to a main feed annonymosly reporting to everyone about anything happening in their surroundings.

## Features

- **Main Feed**: Displays messages with timestamps which represents a call for help or defining a danger somewhere to everyone else.
- **"+" Button**: Opens a message input window to add new messages #annonymosly#.
- **Dataset**: Messages are saved to a JSON file (`messages.json`) *A sort of a simple database just for now*.
- **Auto-close**: The input window closes automatically after sending a message.

## Prerequisites

- **Python 3.x** (Python 3.6 or higher)
- **tkinter** (usually comes with Python by default)

## File Structure
```
c:\Users\-\Humanitarian SOS SMS\
├── main.py           # The main app
├── messages.json     # Created automatically with your messages
└── README.md         # This file
```

## How to Run

1. Open PowerShell and navigate to this folder:
```powershell
cd "c:\Users\-\Humanitarian SOS SMS"
```

2. Run the app:
```powershell
python main.py
```

3. The app window will open. Use it like this:
   - Click the **"+"** button to open the message input window
   - Type your message in the text field
   - Press **Ctrl+Enter** or click "Send" to submit ################ Check this line
   - The window closes and your message appears in the feed


## Troubleshooting

**Problem**: "Python is not recognized"
- Make sure Python is installed from https://www.python.org
- During installation, check "Add Python to PATH"

**Problem**: tkinter window won't open
- Try: `python -m pip install tk`

**Problem**: Messages aren't saving
- Make sure you have write permissions in the folder
- Check if `messages.json` file appears after adding a message



Enjoy Our APP! 🚀
Greta & Bishoy


**TO DO LIST**: for capstone project

├── Idea/
│   ├── Definition                  # 
│   └── Presentation                # 
├── Design/                         # (Diagrams)
│   ├── Usage                       # (e.g., class, activity)
│   │   └── Flowchart.png           #
│   └── Coverage                    #
└── Code/                           # 
    ├── IO                          # 
    ├── OOP                         # 
    ├── Functionality               # (NO bug)
    ├── Testing/                    # 
    │   └── Test_Scripts.py
    └── Readability                 # Done (type hints, naming, clean code)
