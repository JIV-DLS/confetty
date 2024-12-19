import subprocess
import threading
import time
from pynput.keyboard import Controller

class KeyboardSimulator:
    def __init__(self, command, interval=1, duration=10):
        """
        Initialize the KeyboardSimulator class.

        Args:
            command (list): The command (binary) to launch as a subprocess.
            interval (int): Interval in seconds between key presses.
            duration (int): Total time to simulate key presses.
        """
        self.command = command
        self.interval = interval
        self.duration = duration
        self.process = None
        self.keypress_thread = None

    def start(self):
        """Launch the process and start the keypress simulation."""
        # Run the process
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Start a thread to simulate keypresses
        self.keypress_thread = threading.Thread(target=self.send_keypress)
        self.keypress_thread.start()

    def send_keypress(self):
        """Simulate keypresses (e.g., pressing Enter) periodically."""
        keyboard = Controller()
        end_time = time.time() + self.duration
        while time.time() < end_time:
            # Simulate pressing the Enter key
            keyboard.press('\n')  # Simulate the Enter key
            keyboard.release('\n')  # Release the Enter key
            time.sleep(self.interval)

    def wait_for_completion(self):
        """Wait for the process to complete and capture its output."""
        if self.process:
            self.process.wait()
            # Optionally wait for the keypress simulation thread to finish
            if self.keypress_thread:
                self.keypress_thread.join()

            # Capture output if needed
            stdout, stderr = self.process.communicate()
            return stdout, stderr
        return None, None

# Example usage:
if __name__ == "__main__":
    simulator = KeyboardSimulator(
        command=['your_binary'],  # Replace with your command or binary
        interval=1,  # Simulate keypress every second
        duration=10  # Simulate for 10 seconds
    )

    simulator.start()  # Launch the binary and start simulating keypresses
    stdout, stderr = simulator.wait_for_completion()  # Wait for completion and capture output

    # Optionally print the output
    print(stdout)
    print(stderr)