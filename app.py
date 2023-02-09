import json

from fuzzywuzzy import fuzz
from speech import Speech
import vosk
import torch
from colorama import Style, Fore


class Filter(object):
    @staticmethod
    def text(f_text: str or list, percent: int):
        def g(g_text: str):
            if not f_text:
                return True
            if type(f_text) is list:
                for t in f_text:
                    if fuzz.WRatio(t, g_text) > percent:
                        return True
                return False
            return fuzz.WRatio(f_text, g_text) > percent
        return g


class Main(Speech):
    def __init__(self, speaker: str or list = "aidar"):
        super().__init__(speaker)
        self.handlers = Handlers()
        self.else_answer = self.create_audio("Да да, я вас внимательно слушаю")
        self.rec = None

    def add_handler(self, filt, ans):
        if type(ans) is torch.Tensor:
            self.handlers[filt] = ans.play
        elif type(ans) is str:
            audio = self.create_audio(ans)
            self.handlers[filt] = audio.play
        else:
            self.handlers[filt] = ans

    def called(self, call, text):
        for name in call:
            if name in text:
                return True
        return False

    def wait(self, filt: callable or list, stop=None, stop_audio=None):
        if callable(filt):
            filt = [filt]
        stop = stop or Filter.text("Стоп", 60)
        if stop_audio is None:
            stop_audio = self.create_audio("Отключаюсь")
        while True:
            data = self.q.get()
            if self.rec.AcceptWaveform(data):
                text = json.loads(self.rec.Result())["text"]
                if text:
                    print(Fore.LIGHTYELLOW_EX, f"Получено: {text}", sep="", end=" ")
                    for f in filt:
                        if f(text):
                            print(f"{Fore.GREEN}-> Валидация прошла успешно")
                            return text
                    else:
                        print(f"{Fore.YELLOW}-> Не прошло валидацию")

    def loop(self, call=None, stop=None, stop_audio=None):
        call = call or ["Ассистент"]
        stop = stop or Filter.text("Стоп", 60)
        if stop_audio is None:
            stop_audio = self.create_audio("Отключаюсь")

        try:
            with self.input():
                self.rec = vosk.KaldiRecognizer(self.record_model, self.record_sample_rate)
                self.play_text(f"{Style.BRIGHT}Ассистент запущен")
                while True:
                    data = self.q.get()
                    if self.rec.AcceptWaveform(data):
                        text = json.loads(self.rec.Result())["text"]
                        if text:
                            print(Fore.LIGHTYELLOW_EX, f"Получено: {text}", sep="", end=" ")
                            answer = self.handlers.get(text)
                            if self.called(call, text):
                                print(Fore.GREEN, "-> Обнаружено обращение", Style.RESET_ALL, sep="")
                                if answer:
                                    answer(text)
                                elif stop(text):
                                    stop_audio.play()
                                    break
                                else:
                                    self.else_answer.play()
                            else:
                                print(Fore.RED, "-> Не обнаружены обращения", Style.RESET_ALL, sep="")
        except KeyboardInterrupt:
            self.play_audio(stop_audio)


class Handlers(dict):
    def get(self, key, default=None):
        for filt in self:
            if filt(key):
                return self[filt]
        return default
