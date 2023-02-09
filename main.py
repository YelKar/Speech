from typing import Any, Generator

from app import Main, Filter
from util.config import name, load_bar
from datetime import datetime
from util.int2word import int2word, count_word
from util.jokes import jokes
from random import sample, choice
from colorama import Fore, Style
from util.translate import translate

main = Main()


def run():
    main.add_handler(Filter.text("Повтори", 70), repeat_after_me)
    main.add_handler(Filter.text("Переведи", 60), translate_en)
    main.add_handler(Filter.text(["привет", "здоров", "здравствуйте"], 80), "Доброго времени суток")
    main.add_handler(Filter.text("как дела?", 70), "Лучше всех!!!")
    main.add_handler(Filter.text(["сколько времени", "который час"], 80), what_time)
    main.add_handler(Filter.text(["расскажи анекдот", "расскажи шутку"], 70), tell_joke)
    main.add_handler(Filter.text("смени голос", 80), change_voice)

    main.loop(
        name,
        Filter.text(["перестать слушать", "пока", "до свидания"], 60),
        main.create_audio(Style.BRIGHT + choice(["Отключаюсь. До свидания", "Удачи, я пошел спать", "До встречи"])),
    )


def what_time(_):
    time = datetime.now()
    main.play_text(f"{int2word(time.hour)} {count_word('час', time.hour)} "
                   f"{int2word(time.minute, 'Ж')} {count_word('минут', time.minute, 'Ж')}")


def change_voice(_):
    if main.speaker == "baya":
        main.speaker = "aidar"
    else:
        main.speaker = "baya"
    main.play_text("Так?")


def tell_joke(_):
    main.play_text("Сейчас вспомню")
    global joke_sample
    try:
        joke: str = next(joke_sample)
        chunks = joke.split("\n")
        audios = []
        length = len(chunks)
        for num, text in enumerate(chunks, 1):
            load_bar(int(num / length * 100), style=f"{Style.BRIGHT}{Fore.BLUE}",
                     length=20, complete=f"{Style.BRIGHT + Fore.GREEN}Вспомнил!")
            audio = main.create_audio(text.replace("!", "").replace("- ", ""))
            audio.text = text
            audios.append(audio)
        main.play_text(choice(["Вспомнил!", "Короче...", "Итак, слушай...", "Короче... Шуточка..."]))
        # for audio in audios:
        for audio in audios:
            main.play_audio(audio)
        return audios

    except StopIteration:
        joke_sample = gen(sample(jokes, 2))
        tell_joke(_)


def gen(s: Any) -> Generator:
    for i in s:
        yield i


joke_sample = gen(sample(jokes, len(jokes)))


def translate_en(text: str):
    text = main.wait(Filter.text('', 0))
    print(f"Перевод: {translate(text).text}")


def repeat_after_me(_):
    repeat = main.wait(filt=Filter.text("", 0))
    main.play_text(repeat)


if __name__ == '__main__':
    run()
