import curses
import random
import time
import subprocess

def matrix_effect(stdscr, duration=5):
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    # Get screen dimensions
    height, width = stdscr.getmaxyx()
    
    # Create a list of columns to represent the falling characters
    columns = [0] * width
    
    start_time = time.time()
    while time.time() - start_time < duration:
        stdscr.clear()
        for i in range(width):
            if random.random() > 0.9:
                columns[i] = 0
            else:
                columns[i] = min(columns[i] + 1, height - 1)  # Prevent overflowing vertically
            
            for j in range(columns[i]):
                if j < height:  # Ensure we don't print outside the screen height
                    char = chr(random.randint(33, 126))
                    stdscr.addstr(j, i, char, curses.color_pair(1))
        
        stdscr.refresh()
        time.sleep(0.05)

def display_ascii_art(stdscr):
    ascii_art = [
        "  VECERT SETUP ",
        " vecert.io"
    ]
    height, width = stdscr.getmaxyx()
    start_y = height // 2 - len(ascii_art) // 2
    start_x = width // 2 - max(len(line) for line in ascii_art) // 2

    for i, line in enumerate(ascii_art):
        if start_y + i < height:
            stdscr.addstr(start_y + i, start_x, line, curses.A_BOLD)

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    display_ascii_art(stdscr)
    stdscr.refresh()
    time.sleep(2)  # Display ASCII art for 2 seconds
    matrix_effect(stdscr, duration=5)  # Run matrix effect for 5 seconds
    stdscr.clear()

    # Request API key input
    stdscr.addstr(0, 0, "Please enter your API key: ")
    stdscr.refresh()

    # Capture user input for the API key
    curses.echo()  # Enable echoing of characters as they are typed
    api_key = stdscr.getstr(1, 0, 60).decode('utf-8')  # Read user input, max length of 60
    curses.noecho()  # Disable echoing

    # Save the API key to a file
    with open("api_key.txt", "w") as file:
        file.write(api_key)

    stdscr.addstr(3, 0, "API key successfully saved in 'api_key.txt'.")
    stdscr.refresh()
    time.sleep(2)  # Wait for 2 seconds to show the message

    curses.endwin()  # End curses window to switch back to normal terminal

    # Execute the external script leakex_run.py
    subprocess.run(["python", "leakex_run.py"])

if __name__ == "__main__":
    curses.wrapper(main)
