words = [
    "ноль",
    "один",
    "два",
    "три",
    "четыре",
    "пять",
    "шесть",
    "семь",
    "восемь",
    "девять",
    "десять",
    "одиннадцать",
    "двенадцать",
    "тринадцать"
]

numbers = {
    num: word for num, word in enumerate(words)
}

for num, word in list(numbers.items())[4:10]:
    numbers[num + 10] = word[:-1] + "надцать"

for num, word in enumerate(["двадцать", "тридцать", "сорок"], 2):
    numbers[num * 10] = word

for num, word in list(numbers.items())[5:9]:
    numbers[num * 10] = word + "десят"

numbers[90] = "девяносто"

for num, word in enumerate(["сто", "двести", "триста", "четыреста"], 1):
    numbers[num * 100] = word

for num, word in list(numbers.items())[5:10]:
    numbers[num * 100] = word + "сот"

numbers_w = numbers.copy()
numbers_w[1] = "одна"
numbers_w[2] = "две"


def int2word(num: int or str, sex: str = "М"):
    num = int(num)
    nums = numbers if sex == "М" else numbers_w
    if num in nums:
        return nums[num]
    else:
        s = str(num)
        n = int(s[0]) * 10 ** (len(s) - 1)
        return f"{int2word(n)} {int2word(int(s[1:]))}"


def count_word(word: str, num: int, sex: str = "М"):
    if sex == "М":
        if 10 < num < 20:
            return word + "ов"
        elif num % 10 == 1:
            return word
        elif num % 10 in [2, 3, 4]:
            return word + "а"
        return word + "ов"
    elif sex == "Ж":
        if 10 < num < 20:
            return word
        elif num % 10 == 1:
            return word + "а"
        elif num % 10 in [2, 3, 4]:
            return word + "ы"
        return word


def replace_num2word(line: str):
    sentence = line.split()
    for num, word in enumerate(sentence):
        if word.isnumeric():
            sentence[num] = int2word(word)
    return " ".join(sentence)


if __name__ == '__main__':
    print(*[f"{key}: {val}" for key, val in numbers.items()], sep="\n")
