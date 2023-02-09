import numpy as np
import simpleaudio as sa
from speech import Speech
import soundfile as sf


s = Speech()


frequency = 440  # Наша сыгранная нота будет 440 Гц
fs = 44100  # 44100 выборок в секунду
seconds = 3  # Примечание длительность 3 секунды
# Генерировать массив с секундами * сэмплированием шагов, в диапазоне от 0 до 3 секунд
t = np.linspace(0, seconds, seconds * fs, False)
# Генерация синусоидальной волны 440 Гц
note = np.array(s.create_audio("Привет"))

sf.write("audio.wav", note, s.sample_rate)

print(type(note))
# Убедитесь, что максимальное значение находится в 16-битном диапазоне
audio = note * (2**15 - 1) / np.max(np.abs(note))
# Конвертировать в 16-битные данные
audio = audio.astype(np.int16)

# Начать воспроизведение
play_obj = sa.play_buffer(audio, 1, 2, fs)
# Дождитесь окончания воспроизведения перед выходом
play_obj.wait_done()