"""
Wellz Input Handler - Keyboard input processing
"""

import sys
import os
import termios
import tty
import select
from typing import Optional, Callable, Dict, Any
from enum import Enum, auto


class Action(Enum):
    """Available user actions"""
    NONE = auto()
    QUIT = auto()
    UP = auto()
    DOWN = auto()
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()
    SELECT = auto()
    SEARCH = auto()
    CANCEL = auto()
    KILL_PROCESS = auto()
    SIGNAL_MENU = auto()
    TOGGLE_CPU = auto()
    TOGGLE_MEMORY = auto()
    TOGGLE_NETWORK = auto()
    TOGGLE_DISK = auto()
    TOGGLE_GPU = auto()
    TOGGLE_PROCESSES = auto()
    TOGGLE_TREE = auto()
    TOGGLE_HELP = auto()
    THEME_NEXT = auto()
    THEME_PREV = auto()
    REFRESH_UP = auto()
    REFRESH_DOWN = auto()
    RESET_VIEW = auto()
    PAGE_UP = auto()
    PAGE_DOWN = auto()


class InputHandler:
    """Handles keyboard input in raw mode"""

    # Default key bindings
    DEFAULT_BINDINGS: Dict[str, Action] = {
        # Quit
        'q': Action.QUIT,

        # Navigation (vim-style)
        'j': Action.DOWN,
        'k': Action.UP,
        'h': Action.LEFT,
        'l': Action.RIGHT,
        'g': Action.TOP,
        'G': Action.BOTTOM,

        # Arrow keys are handled separately

        # Selection
        '\r': Action.SELECT,      # Enter
        '\n': Action.SELECT,

        # Search
        '/': Action.SEARCH,

        # Cancel/Escape handled separately
        # '\x1b': Action.CANCEL,

        # Process control
        'K': Action.KILL_PROCESS,
        's': Action.SIGNAL_MENU,

        # Panel toggles
        '1': Action.TOGGLE_CPU,
        '2': Action.TOGGLE_MEMORY,
        '3': Action.TOGGLE_NETWORK,
        '4': Action.TOGGLE_DISK,
        '5': Action.TOGGLE_GPU,
        'p': Action.TOGGLE_PROCESSES,
        't': Action.TOGGLE_TREE,

        # Display
        '?': Action.TOGGLE_HELP,
        'c': Action.THEME_NEXT,
        'C': Action.THEME_PREV,
        '+': Action.REFRESH_UP,
        '=': Action.REFRESH_UP,  # Shift not needed alternative
        '-': Action.REFRESH_DOWN,
        'r': Action.RESET_VIEW,
    }

    def __init__(self, vim_mode: bool = True):
        """
        Initialize input handler.

        Args:
            vim_mode: Enable vim-style navigation
        """
        self.vim_mode = vim_mode
        self.bindings = self.DEFAULT_BINDINGS.copy()
        self.old_settings = None
        self.in_raw_mode = False

    def enter_raw_mode(self) -> None:
        """Enter terminal raw mode for character-by-character input"""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            self.in_raw_mode = True

    def exit_raw_mode(self) -> None:
        """Exit terminal raw mode"""
        if self.old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            self.in_raw_mode = False
            self.old_settings = None

    def read_key(self, timeout: float = 0.1) -> Optional[str]:
        """
        Read a single keypress with timeout.

        Args:
            timeout: Timeout in seconds

        Returns:
            Key string or None if timeout
        """
        if not sys.stdin.isatty():
            return None

        # Check if input is available
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return None

        # Read first character
        char = sys.stdin.read(1)
        if not char:
            return None

        # Handle escape sequences
        if char == '\x1b':
            # Check for more characters (arrow keys, etc.)
            ready, _, _ = select.select([sys.stdin], [], [], 0.01)
            if ready:
                char += sys.stdin.read(1)
                if char == '\x1b[':
                    ready, _, _ = select.select([sys.stdin], [], [], 0.01)
                    if ready:
                        char += sys.stdin.read(1)

        return char

    def get_action(self, key: Optional[str]) -> Action:
        """
        Convert key to action.

        Args:
            key: Key string from read_key()

        Returns:
            Corresponding Action enum value
        """
        if key is None:
            return Action.NONE

        # Handle escape sequences
        if key == '\x1b' or key == '\x1b\x1b':
            return Action.CANCEL

        # Arrow keys
        if key == '\x1b[A':  # Up arrow
            return Action.UP
        if key == '\x1b[B':  # Down arrow
            return Action.DOWN
        if key == '\x1b[C':  # Right arrow
            return Action.RIGHT
        if key == '\x1b[D':  # Left arrow
            return Action.LEFT

        # Page up/down
        if key == '\x1b[5~':
            return Action.PAGE_UP
        if key == '\x1b[6~':
            return Action.PAGE_DOWN

        # Home/End
        if key == '\x1b[H' or key == '\x1b[1~':
            return Action.TOP
        if key == '\x1b[F' or key == '\x1b[4~':
            return Action.BOTTOM

        # Ctrl+C
        if key == '\x03':
            return Action.QUIT

        # Look up in bindings
        return self.bindings.get(key, Action.NONE)

    def read_line(self, prompt: str = "", max_len: int = 50) -> Optional[str]:
        """
        Read a line of text input (for search).
        Must be in raw mode.

        Args:
            prompt: Prompt to display
            max_len: Maximum input length

        Returns:
            Input string or None if cancelled
        """
        if not self.in_raw_mode:
            return None

        buffer = ""
        cursor = 0

        # Show prompt
        sys.stdout.write(f"\r{prompt}")
        sys.stdout.flush()

        while True:
            key = self.read_key(timeout=None)  # Block for input

            if key is None:
                continue

            # Enter - submit
            if key in ['\r', '\n']:
                return buffer

            # Escape - cancel
            if key == '\x1b':
                return None

            # Ctrl+C - cancel
            if key == '\x03':
                return None

            # Backspace
            if key in ['\x7f', '\x08']:
                if buffer and cursor > 0:
                    buffer = buffer[:cursor-1] + buffer[cursor:]
                    cursor -= 1
                    # Redraw
                    sys.stdout.write(f"\r{prompt}{buffer} ")
                    sys.stdout.write(f"\r{prompt}{buffer[:cursor]}")
                    sys.stdout.flush()
                continue

            # Delete
            if key == '\x1b[3~':
                if cursor < len(buffer):
                    buffer = buffer[:cursor] + buffer[cursor+1:]
                    sys.stdout.write(f"\r{prompt}{buffer} ")
                    sys.stdout.write(f"\r{prompt}{buffer[:cursor]}")
                    sys.stdout.flush()
                continue

            # Arrow keys for cursor movement
            if key == '\x1b[D':  # Left
                if cursor > 0:
                    cursor -= 1
                    sys.stdout.write('\x1b[D')
                    sys.stdout.flush()
                continue
            if key == '\x1b[C':  # Right
                if cursor < len(buffer):
                    cursor += 1
                    sys.stdout.write('\x1b[C')
                    sys.stdout.flush()
                continue

            # Regular character
            if len(key) == 1 and key.isprintable() and len(buffer) < max_len:
                buffer = buffer[:cursor] + key + buffer[cursor:]
                cursor += 1
                sys.stdout.write(f"\r{prompt}{buffer}")
                if cursor < len(buffer):
                    sys.stdout.write(f"\r{prompt}{buffer[:cursor]}")
                sys.stdout.flush()

        return buffer

    def set_binding(self, key: str, action: Action) -> None:
        """Set custom key binding"""
        self.bindings[key] = action

    def remove_binding(self, key: str) -> None:
        """Remove a key binding"""
        if key in self.bindings:
            del self.bindings[key]


class NonBlockingInput:
    """Context manager for non-blocking terminal input"""

    def __init__(self):
        self.handler = InputHandler()

    def __enter__(self):
        self.handler.enter_raw_mode()
        return self.handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handler.exit_raw_mode()
        return False
