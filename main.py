import mido
import time
import traceback


# Config
input_port_led = "dot2_to_Python 3"
output_port_led = "APC mini mk2 1"

input_port_button = "APC mini mk2 0"
output_port_button = "loopThruAPC 3"

MIDI_CHANNEL = 6
# Colors
OFF = 0
RED = 5
YELLOW = 13
WHITE = 3

# Animation
ANIMATION_DELAY = 0.15
LAST_PAD_DELAY = 0.05

animation_sequence = [10, 14, 13, 12, 20, 29, 38, 46, 53, 44]


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


# Led
def set_all_pads(midi_out, velocity):
    for pad in range(64):
        midi_out.send(mido.Message("note_on", channel=MIDI_CHANNEL, note=pad, velocity=velocity))

def startup_animation(midi_out):
    set_all_pads(midi_out, WHITE)
    time.sleep(1)
    midi_out.send(mido.Message("note_on", channel=MIDI_CHANNEL, note=10, velocity=YELLOW))
    time.sleep(1)
    for pad in animation_sequence[1:-1]:
        midi_out.send(mido.Message("note_on", channel=MIDI_CHANNEL, note=pad, velocity=RED))
        time.sleep(ANIMATION_DELAY)
        midi_out.send(mido.Message("note_on", channel=MIDI_CHANNEL, note=pad, velocity=YELLOW))
    time.sleep(LAST_PAD_DELAY)
    midi_out.send(mido.Message("note_on", channel=MIDI_CHANNEL, note=animation_sequence[-1], velocity=YELLOW))
    time.sleep(2)
    set_all_pads(midi_out, OFF)


# Main
def main():
    midi_in_led, midi_out_led, midi_in_button, midi_out_button = open_ports()
    startup_animation(midi_out_led)

    print("system running (idle)...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram stopped...")

if __name__ == "__main__":
    main()