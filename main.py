import mido
import time
import traceback


# Config
input_port_led = "dot2_to_Python 3"
output_port_led = "APC mini mk2 1"

input_port_button = "APC mini mk2 0"
output_port_button = "loopThruAPC 3"


# Midi
def print_available_ports():
    print("\navailable inputs:")
    for port in mido.get_input_names():
        print(" ->", port)
    print("\navailable output:")
    for port in mido.get_output_names():
        print(" ->", port)

def open_ports():
    try:
        midi_in_led = mido.open_input(input_port_led)
        midi_out_led = mido.open_output(output_port_led)
        midi_in_button = mido.open_input(input_port_button)
        midi_out_button = mido.open_output(output_port_button)
        print("midi-ports successfully opened")
        return midi_in_led, midi_out_led, midi_in_button, midi_out_button
    except Exception as e:
        print("error while opening midi-ports:", e)
        print_available_ports()
        raise


# Main
def main():
    midi_in_led, midi_out_led, midi_in_button, midi_out_button = open_ports()
    print("system running (idle)...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram stopped...")

if __name__ == "__main__":
    main()