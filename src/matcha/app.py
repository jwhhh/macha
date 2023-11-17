"""Metronome and tuner combined - hybrid app
"""
import time
import threading
import simpleaudio as sa
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class Matcha(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)

        self.tempo_input = toga.NumberInput(min_value=1, max_value=300, step=1)
        self.start_button = toga.Button('Start', on_press=self.start_metronome)

        box = toga.Box(
            children=[
                self.tempo_input,
                self.start_button
            ],
            style=Pack(direction=COLUMN, padding=10)
        )

        self.main_window.content = box
        self.main_window.show()

    def start_metronome(self, widget):
        tempo = int(self.tempo_input.value)
        interval = 60.0 / tempo

        # Load a wave file to be played as the metronome sound
        wave_obj = sa.WaveObject.from_wave_file("/path/to/sound.wav")

        def metronome():
            while True:
                wave_obj.play()
                time.sleep(interval)

        # Start a new thread for the metronome
        threading.Thread(target=metronome).start()


def main():
    return Matcha()
