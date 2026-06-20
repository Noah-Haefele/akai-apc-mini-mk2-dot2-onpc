# APC mini mk2 to dot2 onPC Bridge

This utility creates a bi-directional MIDI connection between the AKAI APC mini mk2 controller and MA Lighting dot2 onPC. It allows the APC mini mk2 to trigger buttons, executors, and adjust faders on dot2 onPC, while sending LED status feedback from dot2 back to the controller's LED grid.

---

## Prerequisites

Ensure the following components are installed on the system:

| Component | Requirement |
| :--- | :--- |
| **Operating System** | Windows PC running **MA Lighting dot2 onPC** |
| **Hardware** | **AKAI APC mini mk2** controller |
| **Environment** | **Python 3.x** (with "Add Python to PATH" selected during installation) |
| **MIDI Router** | **loopMIDI** |

---

## Step 1: loopMIDI Configuration

Windows does not natively route MIDI signals between applications. Use loopMIDI to create virtual connections.

1. Open **loopMIDI**.
2. Add the following two virtual ports (case-sensitive):
   * `dot2_to_python`
   * `python_to_dot2`

### Signal Flow

**Button and Fader Routing:**
```text
APC mini mk2 ➔ main.py ➔ python_to_dot2 ➔ dot2 onPC (MIDI In)
```

**LED Control Routing:**
```text
dot2 onPC (MIDI Out) ➔ dot2_to_python ➔ main.py ➔ APC mini mk2
```

---

## Step 2: Installation

1. Clone the repository with:
   ```text
   git clone https://github.com/Noah-Haefele/akai-apc-mini-mk2-dot2-onpc.git
   ```
2. Navigate to the project directory.
3. Verify that `requirements.txt` contains the following dependencies:
   ```text
   mido
   python-rtmidi
   ```
4. Open a command prompt or terminal in the project directory and install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Step 3: Script Configuration

Open main.py in a text editor to verify or edit the MIDI port variables to match your system configuration:

| Variable | Target Port | Function |
| :--- | :--- | :--- |
| `input_port_led` | `"dot2_to_python"` | Input port for LED triggers from dot2 |
| `output_port_led` | `"APC mini mk2 1"` | Output port to send LED states to physical grid |
| `input_port_button` | `"APC mini mk2 0"` | Input port receiving physical control triggers |
| `output_port_button` | `"python_to_dot2"` | Output port forwarding control triggers to dot2 |

> [!WARNING]
> **Port Name Differences:**  
> Windows dynamically assigns numbers to MIDI devices. Depending on your USB port, your APC mini might show up as `APC mini mk2 2` or `0` instead of `1`.  
>  
> **How to fix it if the script crashes:**  
> If the script cannot connect, look at the console window. The script will automatically print a list of all **"available inputs"** and **"available outputs"** detected on your PC. Simply copy the exact name shown there and paste it into your `main.py` variables.

### Color Customization
You can modify the default velocity color values defined in main.py:
```python
OFF = 0
RED = 5
YELLOW = 13
WHITE = 3
```

---

## Step 4: dot2 onPC Setup

### Software Settings
Open **dot2 onPC** and configure the MIDI settings:
* **MIDI In:** Set to `python_to_dot2`
* **MIDI Out:** Set to `dot2_to_python`

### LED Control Syntax
To trigger an LED on the APC mini grid from dot2, use the following dot2 command-line syntax:

```text
MidiNote 12 60
```

* **`12`**: Represents the physical pad number (Note) on the APC mini mk2 grid.
* **`60`**: Represents the color of the LED

---

## Running and Stopping the Tool

### Execution
Run the script using the command:
```bash
python main.py
```

### Safe Termination
To stop the utility, press `Ctrl + C` in the console. 