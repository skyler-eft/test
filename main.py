from PIL import Image
import pyautogui
import keyboard
import threading

# Color to search for (RGB format)
target_color = (226, 99, 56)  # Hex color #E26338

# Coordinates of the box to crop
left, top, right, bottom = 664, 616, 2265, 1577

def find_color_position(image, target_color):
    
    pixels = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if pixels[x, y][:3] == target_color:  # Check RGB, ignore alpha if present
                return (x, y)
    return None

def script():
    print("Script started. Press 'q' to stop.")
    while running.is_set():
        # Take a screenshot
        screenshot = pyautogui.screenshot(region=(left, top, right-left, bottom-top))

        # Find the position of the target color
        position = find_color_position(screenshot, target_color)

        if position:
            # Adjust position to be relative to the entire screen
            click_position = (left + position[0], top + position[1])
            # Move the mouse and click
            pyautogui.click(click_position)
    

def start_script():
    global thread
    if not running.is_set():  # Only start if it's not already running
        running.set()
        thread = threading.Thread(target=script)
        thread.start()

def stop_script():
    running.clear()
    if thread.is_alive():  # Wait for the thread to finish if it's still running
        thread.join()
    print("Script stopped.")

if __name__ == "__main__":
    running = threading.Event()
    keyboard.add_hotkey('t', start_script)
    keyboard.add_hotkey('q', stop_script)
    print("Press 't' to start the script and 'q' to stop the script.")
    keyboard.wait()  # Keep the script running to listen for hotkeys
