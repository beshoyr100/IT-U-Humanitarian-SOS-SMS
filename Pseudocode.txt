========================================
CLASS MessageStorage
Handles saving and loading data to a JSON file on disk.
========================================
DEFINE METHOD init(filename defaults to "messages.json"):
    SET self.filename = filename

DEFINE METHOD load():
    IF self.filename exists on the operating system:
        OPEN self.filename in read mode
        READ content and parse JSON into a list
        RETURN the list of messages
    ELSE:
        RETURN an empty list []

DEFINE METHOD save(messages_list):
    OPEN self.filename in write mode
    SERIALIZE messages_list into JSON format with indentation
    WRITE JSON data to file

========================================
CLASS MessageWindow (Inherits structure from Toplevel window)
The pop-up dialog for entering text.
========================================
DEFINE METHOD init(parent_window, on_send_callback_function):
    SET parent = parent_window
    SET callback = on_send_callback_function
    SET max_chars = 50

DEFINE METHOD create_window():
    CREATE new Toplevel window
    CONFIGURE window geometry (350x630), title, and set as topmost
    CALL _setup_ui()

DEFINE METHOD _setup_ui():
    TRY to load "phone background.png" image:
        RESIZE image to 350x630
        CREATE a Canvas widget placing the image as background
        CREATE a Text entry widget positioned over the image's "screen" area
        CREATE a Label widget below the Text widget for character counting
        BIND KeyPress event to self._on_keypress
        BIND KeyRelease event to self._update_count
        BIND Paste event (Ctrl+V) to self._on_paste
        BIND Return key event to self._on_return_pressed
        SET focus to the Text widget
    CATCH exception (if image missing or load fails):
        CALL _setup_fallback_ui()

DEFINE METHOD _setup_fallback_ui():
    CONFIGURE window background to gray
    CREATE a simple Frame with a green background
    CREATE Text entry widget and counter Label inside this frame
    BIND same events (KeyPress, KeyRelease, Paste, Return) as above

DEFINE METHOD _send_message():
    GET text content from Text widget AND strip leading/trailing whitespace
    IF text content is NOT empty:
        CALL self.callback with the text content
        DESTROY this pop-up window

DEFINE METHOD _on_keypress(event):
    IF the pressed key is a navigation key (e.g., Backspace, Arrows, Delete):
        ALLOW input (return None)
    CALCULATE prospective length = current length - selected text length + new char length
    IF prospective length > self.max_chars:
        PLAY system bell sound
        BLOCK input (return "break")

DEFINE METHOD _on_return_pressed(event):
    CALL self._enforce_char_limit() (trims excess if necessary)
    CALL self._send_message()
    BLOCK the default newline insertion (return "break")

# (Other helper methods like _enforce_char_limit, _update_count, _on_paste 
# perform string manipulation to ensure text stays within max_chars limit)

========================================
CLASS MessageFeed
The main application window.
========================================
DEFINE METHOD init(root_window):
    INITIALIZE a MessageStorage instance
    CONFIGURE root window title and geometry
    CALL _setup_ui()

DEFINE METHOD _setup_ui():
    CREATE top Frame
    ADD title Label "Your Feed" to top Frame
    ADD "+" Button to top Frame configured to CALL self._open_message_window when clicked
    CREATE a Listbox widget with a Scrollbar to display messages
    CALL self.refresh_feed()

DEFINE METHOD _open_message_window():
    INITIALIZE a new MessageWindow instance, passing self._on_message_sent as the callback
    CALL message_window.create_window()

DEFINE METHOD _on_message_sent(new_message_text):
    # This is executed when the user hits enter in the pop-up
    CALL self.storage.load() into messages_list
    GENERATE random latitude between 9.0 and 22.0 (approx Sudan)
    GENERATE random longitude between 21.0 and 38.0 (approx Sudan)
    GET current timestamp string ("YYYY-MM-DD HH:MM:SS")
    CREATE new message dictionary: {
        "text": new_message_text,
        "timestamp": current timestamp,
        "lat": latitude,
        "lon": longitude
    }
    APPEND new message dictionary to messages_list
    CALL self.storage.save(messages_list)
    CALL self.refresh_feed()

DEFINE METHOD refresh_feed():
    CLEAR all items currently in the Listbox
    CALL self.storage.load() into messages_list
    FOR EACH message IN messages_list REVERSED (newest first):
        FORMAT display string as "timestamp - text"
        INSERT display string into Listbox

========================================
MAIN PROGRAM FLOW
========================================
IF running as main script:
    INITIALIZE Tk root window
    INITIALIZE MessageFeed(root) # This sets up UI and loads initial data
    START Tk main event loop (app.run())
