VOWELS = list('aeiou')


def get_word():
    return input('What is our word? ')


def count_vowels(string):
    count = 0
    for char in string:
        if char.lower() in VOWELS:
            count += 1
    return count


def count_vowels_oneline(string):
    return sum(1 for char in string if char.lower() in VOWELS)


def test():
    tests = dict((
        ('bob', 1), ('vowel', 2), ('house', 3),
        ('HOUSe', 3), ('pybit.ES', 2),
        ('how is it going MATE?', 7),
    ))
    for s, result in tests.items():
        assert count_vowels(s) == result
        assert count_vowels_oneline(s) == result


if __name__ == "__main__":
    test()
    print('This program will count the number of vowels in that word. ')
    word = get_word()
    print(word)
    count = count_vowels(word)
    print('The number of vowels in {} is: {}'.format(word, count))
