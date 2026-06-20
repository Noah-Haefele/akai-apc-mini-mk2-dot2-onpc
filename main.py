import mido
import time
import traceback
from threading import Event, Thread


# Config
input_port_led = "dot2_to_Python" # Midi input for led control from dot2
output_port_led = "APC mini mk2 1" # Midi output for led control to APC mini mk2

input_port_button = "APC mini mk2 0" # Midi input for buttons and faders from APC mini mk2
output_port_button = "python_to_dot2" # Midi output for buttons and faders to dot2

MIDI_CHANNEL = 6
# Colors
OFF = 0
RED = 5
YELLOW = 13
WHITE = 3

ihex_ohex = {48: 99, 49: 100, 50: 101, 51: 102, 52: 103, 53: 104, 54: 105, 55: 106, 56: 107}
stop_event = Event()

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

def led_listener(midi_in, midi_out):
    try:
        while not stop_event.is_set():
            for msg in midi_in.iter_pending():
                if msg.type == "note_on":
                    midi_out.send(mido.Message("note_on", channel=MIDI_CHANNEL, note=msg.note, velocity=msg.velocity))
            time.sleep(0.005)
    except Exception:
        traceback.print_exc()


# Button
def button_translator(midi_in, midi_out, led):
    try:
        while not stop_event.is_set():
            for msg in midi_in.iter_pending():
                # Map control changes (faders) to specific notes if defined
                if msg.type == "control_change" and msg.control in ihex_ohex:
                    midi_out.send(mido.Message("note_on", note=ihex_ohex[msg.control], velocity=msg.value, channel=msg.channel))
                    print("Fader: " + str(msg))
                else:
                    if msg.type == "note_on":
                        midi_out.send(mido.Message("note_on", note=msg.note, velocity=msg.velocity, channel=msg.channel))
                        print(msg)
                    elif msg.type == "note_off":
                        midi_out.send(mido.Message("note_off", note=msg.note, velocity=msg.velocity, channel=msg.channel))
                        print(msg)
            time.sleep(0.005)
    except Exception:
        traceback.print_exc()


# Main
def main():
    midi_in_led, midi_out_led, midi_in_button, midi_out_button = open_ports()
    startup_animation(midi_out_led)

    t_btn = Thread(target=button_translator, args=(midi_in_button, midi_out_button, midi_out_led))
    t_led = Thread(target=led_listener, args=(midi_in_led, midi_out_led))
    t_btn.start()
    t_led.start()

    print("system running (idle)...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram stopped...")
        stop_event.set()                       # Signal threads to stop looping
        t_led.join()                           # Wait for LED thread to finish
        t_btn.join()                           # Wait for button thread to finish
        set_all_pads(midi_out_led, OFF)        # Turn off all pads on exit
        midi_in_led.close()                    # Safely release MIDI ports
        midi_out_led.close()
        midi_in_button.close()
        midi_out_button.close()
        print("midi-ports successfully closed")
        exit()

if __name__ == "__main__":
    main()