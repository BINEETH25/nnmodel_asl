from pynput import keyboard

# Flag to track key press
key_pressed = False

def on_press(key):
    global key_pressed
    try:
        if key.char == 'b' and not key_pressed:
            key_pressed = True
            print("Hi")  # Print "Hi" when 'b' is pressed
    except AttributeError:
        pass

def on_release(key):
    global key_pressed
    if key.char == 'b':
        key_pressed = False  # Reset the flag when 'b' is released

    # Stop listener when ESC is pressed
    if key == keyboard.Key.esc:
        return False

# Start listening to key presses
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

print("Press 'b' to print 'Hi'. Press ESC to exit.")

# Keep the program running
try:
    listener.join()
except KeyboardInterrupt:
    print("Exiting program.")
