"""
Metronome and Cadence Helper App
"""
import time
import threading
import toga
import playsound
import numpy
import simpleaudio


class Macha(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_window = toga.MainWindow(title=self.formal_name)

        self.bpm = toga.NumberInput(min_value=30, max_value=240, step=1)
        self.bpm.value = 60
        
        self.label = toga.Label('BPM:', style=toga.style.Pack(padding_top=5))
        self.start_button = toga.Button('Start', on_press=self.start_metronome, style=toga.style.Pack(padding=5))
        self.stop_button = toga.Button('Stop', on_press=self.stop_metronome, style=toga.style.Pack(padding=5))
        
        box = toga.Box(
            style=toga.style.Pack(direction=toga.style.pack.COLUMN, padding_top=10),
            children=[
                self.label,
                self.bpm,
                self.start_button,
                self.stop_button,
            ]
        )
        
        self.main_window.content = box
        self.main_window.show()
        
        self.metronome_thread = None
        self.metronome_running = False

    def start_metronome(self, widget):
        if self.metronome_thread is None or not self.metronome_thread.is_alive():
            self.metronome_running = True
            self.metronome_thread = threading.Thread(target=self.run_metronome)
            self.metronome_thread.start()

    def stop_metronome(self, widget):
        self.metronome_running = False

    def run_metronome(self):
        while self.metronome_running:
            # replace 'sound_file.wav' with your metronome tick sound file path
            play_beep(440, 1)
            time.sleep(60.0 / int(self.bpm.value))


def play_beep(frequency, duration):
    # Get the sample rate and the sample length
    sample_rate = 44100
    sample_len = duration * sample_rate

    # Generate the samples for a sine wave at the given frequency
    t = numpy.linspace(0, duration, sample_len, False)
    tone = numpy.sin(frequency * t * 2 * numpy.pi)

    # Ensure that highest value is in 16-bit range
    audio = tone * (2**15 - 1) / numpy.max(numpy.abs(tone))
    audio = audio.astype(numpy.int16)

    # Play the audio
    play_obj = simpleaudio.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()


def main():
    return Macha()
