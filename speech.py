# imports for play
import torch
import sounddevice as sd
import time

# imports for record
import vosk
import queue
import sys

from colorama import Fore, Style


class Speech:
    def __init__(self, speaker: str = "aidar"):
        self.speaker = speaker
        self.sample_rate = 48000
        self.put_accent = True
        self.put_yo = True

        language = "ru"
        model_id = "ru_v3"
        device = torch.device("cpu")

        self.record_model = vosk.Model("model")
        self.record_sample_rate = 16000

        self.model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language=language,
            speaker=model_id
        )
        self.model.to(device)

        self.q = queue.Queue()

    def play_text(self, text: str = "Привет, мир!"):
        audio = self.create_audio(text)
        self.play_audio(audio)

    def create_audio(self, text: str = "Привет, мир!") -> torch.Tensor:
        audio = self.model.apply_tts(
            text=text,
            speaker=self.speaker,
            sample_rate=self.sample_rate,
            put_accent=self.put_accent,
            put_yo=self.put_yo
        )
        audio.text = text
        audio.play = lambda *x: self.play_audio(audio)
        return audio

    def play_audio(self, audio: torch.Tensor):
        sd.play(audio, self.sample_rate)
        try:
            print(f"{Fore.LIGHTBLUE_EX}Ответ: {audio.text.replace('+', '')}{Style.RESET_ALL}")
        except AttributeError:
            pass
        time.sleep(len(audio) / self.sample_rate + .3)
        sd.stop()

    def _callback(self, indata, _, __, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def input(self):
        return sd.RawInputStream(
            samplerate=self.record_sample_rate,
            device=1,
            callback=self._callback,
            blocksize=8000,
            dtype="int16",
            channels=1
        )
