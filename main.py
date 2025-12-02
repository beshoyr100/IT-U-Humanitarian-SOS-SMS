import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Callable, Any

class MessageStorage:
    """Handles loading and saving messages to JSON file"""
    
    def __init__(self, filename: str = "messages.json") -> None:
        self.filename: str = filename
    
    def load(self) -> List[Dict[str, Any]]:
        """Load messages from file"""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []
    
    def save(self, messages: List[Dict[str, Any]]) -> None:
        """Save messages to file"""
        with open(self.filename, "w") as f:
            json.dump(messages, f, indent=2)


class MessageWindow:
    """Pop-up window for entering new messages"""
    
    def __init__(self, parent: tk.Tk, on_send_callback: Callable[[str], None]) -> None:
        self.parent: tk.Tk = parent
        self.on_send_callback: Callable[[str], None] = on_send_callback
        self.window: Optional[tk.Toplevel] = None
        self.text_field: Optional[tk.Text] = None
        self.counter_label: Optional[tk.Label] = None
        self.max_chars: int = 50
    
    def create_window(self) -> None:
        """Create and display the message input window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("New Message")
        self.window.geometry("350x630")
        self.window.resizable(False, False)
        self.window.attributes('-topmost', True)
        self.window.config(bg="white")
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the UI with phone background and text field"""
        try:
            # Load and display the phone background image
            if os.path.exists("phone background.png"):
                phone_image: Image.Image = Image.open("phone background.png")
                
                # Resize to fit window
                phone_image = phone_image.resize((350, 630), Image.Resampling.LANCZOS)
                phone_photo: ImageTk.PhotoImage = ImageTk.PhotoImage(phone_image)
                
                # Create canvas to display image
                canvas: tk.Canvas = tk.Canvas(self.window, width=350, height=630, highlightthickness=0)
                canvas.pack()
                canvas.create_image(0, 0, image=phone_photo, anchor="nw")
                canvas.image = phone_photo  # Keep a reference
                
                # Text field positioned over the green screen area
                self.text_field = tk.Text(
                    canvas,
                    height=5,
                    width=24,
                    font=("Courier", 11, "bold"),
                    bg="#cbe690",
                    fg="#000000",
                    relief=tk.FLAT,
                    wrap=tk.WORD,
                    insertbackground="#000000",
                    selectbackground="#00aa00",
                    bd=0,
                    highlightthickness=0,
                    borderwidth=0
                )
                
                # Position text field over the screen in the phone design
                canvas.create_window(175, 215, window=self.text_field, width=110, height=85)

                # Character counter label (placed just below the screen)
                self.counter_label = tk.Label(
                    canvas,
                    text=f"0/{self.max_chars}",
                    font=("Arial", 8),
                    bg="#cbe690",
                    fg="#000000"
                )
                # place counter below the text field (tweak Y as needed)
                canvas.create_window(175, 265, window=self.counter_label)

                # Bind events for character limit and sending
                self.text_field.bind("<KeyPress>", self._on_keypress)
                self.text_field.bind("<KeyRelease>", lambda e: self._update_count())
                self.text_field.bind("<Control-v>", self._on_paste)
                self.text_field.bind("<Control-V>", self._on_paste)
                self.text_field.bind("<Return>", self._on_return_pressed)
                self.text_field.focus()
            else:
                self._setup_fallback_ui()
        except Exception as e:
            print(f"Error loading phone image: {e}")
            self._setup_fallback_ui()
    
    def _setup_fallback_ui(self) -> None:
        """Fallback UI if phone image is not available"""
        self.window.config(bg="#a8a8a8")
        screen_frame: tk.Frame = tk.Frame(self.window, bg="#a8ff00", relief=tk.RIDGE, bd=3)
        screen_frame.pack(pady=15, fill=tk.BOTH, expand=False, padx=15)
        
        # Fallback text field (also made borderless to match the visual style)
        self.text_field = tk.Text(
            screen_frame,
            height=6,
            width=28,
            font=("Courier", 10, "bold"),
            bg="#cbe690",
            fg="#000000",
            relief=tk.FLAT,
            wrap=tk.WORD,
            insertbackground="#000000",
            selectbackground="#00aa00",
            bd=0,
            highlightthickness=0,
            borderwidth=0,
        )
        self.text_field.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        # Fallback counter under the screen
        self.counter_label = tk.Label(screen_frame, text=f"0/{self.max_chars}", font=("Arial", 8), bg="#cbe690", fg="#000000")
        self.counter_label.pack(pady=(2, 0))
        # Bind events for fallback text field as well
        self.text_field.bind("<KeyPress>", self._on_keypress)
        self.text_field.bind("<KeyRelease>", lambda e: self._update_count())
        self.text_field.bind("<Control-v>", self._on_paste)
        self.text_field.bind("<Control-V>", self._on_paste)
        self.text_field.bind("<Return>", self._on_return_pressed)
    
    def _send_message(self) -> None:
        """Send the message and close the window"""
        if not self.text_field:
            return
        message: str = self.text_field.get("1.0", tk.END).strip()
        
        if message:
            self.on_send_callback(message)
            if self.window:
                self.window.destroy()

    def _enforce_char_limit(self) -> None:
        """Trim the text field content to self.max_chars if needed."""
        if not self.text_field:
            return
        content: str = self.text_field.get("1.0", "end-1c")
        if len(content) > self.max_chars:
            # Trim excess characters and keep cursor at end (fallback)
            self.text_field.delete("1.0", tk.END)
            self.text_field.insert("1.0", content[: self.max_chars])
            try:
                # small audible feedback
                if self.window:
                    self.window.bell()
            except Exception:
                pass
        # Update counter label
        self._update_count()

    def _update_count(self) -> None:
        """Update remaining/total counter shown on the phone screen."""
        if not self.text_field:
            return
        content: str = self.text_field.get("1.0", "end-1c")
        remaining: int = max(0, self.max_chars - len(content))
        if hasattr(self, "counter_label") and self.counter_label:
            try:
                self.counter_label.config(text=f"{remaining}/{self.max_chars}")
            except Exception:
                pass

    def _on_keypress(self, event: tk.Event) -> Optional[str]:
        """Prevent typing when max chars reached. Allow navigation and control keys."""
        if not self.text_field:
            return None
        # Allow control/navigation keys
        allowed_keys = {
            "BackSpace",
            "Delete",
            "Left",
            "Right",
            "Up",
            "Down",
            "Home",
            "End",
            "Tab",
            "Return",
        }
        if event.keysym in allowed_keys:
            return None

        # Determine current content length and selection length
        content: str = self.text_field.get("1.0", "end-1c")
        sel_len: int = 0
        try:
            sel: str = self.text_field.get("sel.first", "sel.last")
            sel_len = len(sel)
        except tk.TclError:
            sel_len = 0

        # Characters that will be inserted by this keypress
        insert_len: int = len(event.char) if event.char is not None else 0
        # If no printable char and not in allowed set, let it through
        if insert_len == 0:
            return None

        prospective_len: int = len(content) - sel_len + insert_len
        if prospective_len > self.max_chars:
            try:
                if self.window:
                    self.window.bell()
            except Exception:
                pass
            return "break"

    def _on_paste(self, event: Optional[tk.Event] = None) -> str:
        """Handle Ctrl+V paste: insert only allowed portion from clipboard."""
        if not self.text_field or not self.window:
            return "break"
        try:
            clip: str = self.window.clipboard_get()
        except Exception:
            return "break"

        content: str = self.text_field.get("1.0", "end-1c")
        sel_len: int = 0
        try:
            sel: str = self.text_field.get("sel.first", "sel.last")
            sel_len = len(sel)
        except tk.TclError:
            sel_len = 0

        allowed: int = self.max_chars - (len(content) - sel_len)
        if allowed <= 0:
            try:
                if self.window:
                    self.window.bell()
            except Exception:
                pass
            return "break"

        to_insert: str = clip[:allowed]
        # Perform the insertion at current insert position
        self.text_field.insert(tk.INSERT, to_insert)
        # Update counter
        self._update_count()
        return "break"

    def _on_return_pressed(self, event: Optional[tk.Event] = None) -> str:
        """Handler for Return key: enforce limit then send; return 'break' to prevent newline."""
        # enforce limit first
        self._enforce_char_limit()
        # send
        self._send_message()
        return "break"


class MessageFeed:
    """Main application window displaying the message feed"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title("Message Feed")
        self.root.geometry("600x500")
        
        self.storage: MessageStorage = MessageStorage()
        self.feed_listbox: Optional[tk.Listbox] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the main feed UI"""
        # Top frame with title and + button
        top_frame: tk.Frame = tk.Frame(self.root, bg="#f0f0f0", height=60)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_label: tk.Label = tk.Label(top_frame, text="Your Feed", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, padx=10)
        
        # + Button
        add_button: tk.Button = tk.Button(top_frame, text="+", command=self._open_message_window, 
                              font=("Arial", 20, "bold"), width=3, height=1,
                              bg="#2196F3", fg="white")
        add_button.pack(side=tk.RIGHT, padx=10)
        
        # Feed display frame
        feed_frame: tk.Frame = tk.Frame(self.root)
        feed_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar: tk.Scrollbar = tk.Scrollbar(feed_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.feed_listbox = tk.Listbox(feed_frame, font=("Arial", 10), yscrollcommand=scrollbar.set)
        self.feed_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.feed_listbox.yview)
        
        # Initial load
        self.refresh_feed()
    
    def _open_message_window(self) -> None:
        """Open the message input window"""
        message_window: MessageWindow = MessageWindow(self.root, self._on_message_sent)
        message_window.create_window()
    
    def _on_message_sent(self, message: str) -> None:
        """Callback when a message is sent"""
        messages: List[Dict[str, Any]] = self.storage.load()
        # Generate a randomized coordinate within a bounding box for Sudan.
        lat: float = round(random.uniform(9.0, 22.0), 6)
        lon: float = round(random.uniform(21.0, 38.0), 6)
        messages.append({
            "text": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lat": lat,
            "lon": lon
        })
        self.storage.save(messages)
        self.refresh_feed()
    
    def refresh_feed(self) -> None:
        """Refresh the feed display"""
        if self.feed_listbox:
            self.feed_listbox.delete(0, tk.END)
        
        messages: List[Dict[str, Any]] = self.storage.load()
        
        # Display messages in reverse order (newest first)
        for msg in reversed(messages):
            display_text: str = f"{msg['timestamp']} - {msg['text']}"
            if self.feed_listbox:
                self.feed_listbox.insert(0, display_text)


class App:
    """Main application class"""
    
    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.feed: MessageFeed = MessageFeed(self.root)
    
    def run(self) -> None:
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app: App = App()
    app.run()