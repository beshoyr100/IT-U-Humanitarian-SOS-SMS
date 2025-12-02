# Humanitarian SOS SMS

As part of the design and data labs at IT:U to design a shelter for displaced people; we had a lot of problems with data. Also, we learned a lot about peoples' suffering with different humanitarian crises.

For our project, we designed a simple Python GUI application that allows people to anonymously submit SOS messages to a shared feed, enabling them to report anything happening in their surroundings to others immediately.

## Features

- **Main Feed**: Displays messages with timestamps that represent calls for help or warnings about dangers in the surroundings.
- **"+" Button**: Opens a message input window to add new messages #annonymosly#.
- **Dataset**: Messages are saved to a JSON file (`messages.json`) *A sort of a simple database just for now*.
- **Auto-close**: The input window closes automatically after sending a message.
- **coordinates**: Coordinates have been added for each message to help identify the location of the person requesting help. This feature is not fully implemented yet; the current values are generated placeholders to illustrate the concept.

## Prerequisites

- **Python 3.x** (Python 3.6 or higher)
- **tkinter** (usually comes with Python by default)

## File Structure
```
c:\Users\-\Humanitarian SOS SMS\
├── main.py                    # The main app
├── messages.json              # Created automatically with your messages
├── phone background.png       # In-APP pop-up window background
├── testing.py                 # Features testing script
└── README.md                  # This file
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

**Problem**: GUI Doesn't work properly 
- This can happen in the current version if you open only main.py using VScode.
- Open the project folder with VScode then run `main.py` and it should work fine.


## Testing
- run `testing.py` and continue through the breakpoint by clicking `c`
- You can see everything is working as intended.


Enjoy Our APP! 🚀
Greta & Bishoy


**TO DO LIST**: for capstone project
```
├── Idea/
│   ├── Definition                  # Done
│   └── Presentation                # Done
├── Design/                          
│   ├── Usage                       # Done
│   │   └── Flowchart.png           # Done
│   └── Coverage                    # Done
└── Code/                           
    ├── IO                          # Done
    ├── OOP                         # Done
    ├── Functionality               # Done
    ├── Testing/
    │   └── testing.py              # Done
    └── Readability                 # Done
```




