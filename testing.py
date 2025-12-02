import pdb
import os
import json
from datetime import datetime

# Import classes from your main file
# Assuming your main file is named 'main.py' - adjust if different
from main import MessageStorage, MessageWindow
import tkinter as tk

def test_message_storage():
    """Test MessageStorage save and load functionality"""
    
    # Create a test storage instance with a test file
    test_file = "test_messages.json"
    storage = MessageStorage(test_file)
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("Testing MessageStorage...")
    
    # Test 1: Load from non-existent file (should return empty list)
    messages = storage.load()
    pdb.set_trace()  # Breakpoint 1: Check that messages is []
    assert messages == [], "Expected empty list for non-existent file"
    print("✓ Test 1 passed: Load from non-existent file returns []")
    
    # Test 2: Save some messages
    test_messages = [
        {
            "text": "Hello Robert & Shaily",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lat": 15.5,
            "lon": 32.5
        },
        {
            "text": "This is a test message",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lat": 12.3,
            "lon": 30.1
        }
    ]
    storage.save(test_messages)
    pdb.set_trace()  # Breakpoint 2: Check file was created
    assert os.path.exists(test_file), "Expected file to be created"
    print("✓ Test 2 passed: Messages saved successfully")
    
    # Test 3: Load saved messages
    loaded_messages = storage.load()
    pdb.set_trace()  # Breakpoint 3: Inspect loaded messages
    assert len(loaded_messages) == 2, "Expected 2 messages"
    assert loaded_messages[0]["text"] == "Hello Robert & Shaily", "Expected correct message text"
    print("✓ Test 3 passed: Messages loaded correctly")
    
    # Cleanup
    os.remove(test_file)
    print("\n✓ All MessageStorage tests passed!\n")


def test_message_window():
    """Test MessageWindow character limit functionality"""
    
    print("Testing MessageWindow character limit...")
    
    # Create a root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Track if callback was called
    callback_data = {"called": False, "message": ""}
    
    def mock_callback(message):
        callback_data["called"] = True
        callback_data["message"] = message
    
    # Create MessageWindow instance
    msg_window = MessageWindow(root, mock_callback)
    
    # Test 1: Check max_chars is set correctly
    pdb.set_trace()  # Breakpoint 4: Check msg_window.max_chars
    assert msg_window.max_chars == 50, "Expected max_chars to be 50"
    print("✓ Test 1 passed: max_chars is 50")
    
    # Test 2: Create window and check text field exists
    msg_window.create_window()
    pdb.set_trace()  # Breakpoint 5: Check msg_window.text_field exists
    assert msg_window.text_field is not None, "Expected text_field to be created"
    print("✓ Test 2 passed: text_field created")
    
    # Test 3: Simulate entering text and check enforcement
    test_text = "This is a test message that is under the limit"
    msg_window.text_field.insert("1.0", test_text)
    msg_window._enforce_char_limit()
    content = msg_window.text_field.get("1.0", "end-1c")
    pdb.set_trace()  # Breakpoint 6: Check content length
    assert len(content) <= 50, f"Expected content <= 50 chars, got {len(content)}"
    print(f"✓ Test 3 passed: Content length is {len(content)} (within limit)")
    
    # Cleanup
    msg_window.window.destroy()
    root.destroy()
    
    print("\n✓ All MessageWindow tests passed!\n")


if __name__ == "__main__":
    test_message_storage()
    test_message_window()
    print("=" * 50)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 50)
