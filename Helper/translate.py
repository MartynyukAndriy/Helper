CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")


TRANS = {}


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name):
    """
    This function normalize file's name
    """
    result = ""
    try:
        for letter in name.split(".")[0]:
            if letter.lower() not in CYRILLIC_SYMBOLS and letter.lower() not in TRANSLATION and letter not in "1234567890cwxWXC":
                result += "_"
            elif letter.lower() not in CYRILLIC_SYMBOLS:
                result += letter
            else:
                result += TRANS[ord(letter)]
    except:
        return name
    result += "." + name.split(".")[1]
    return result
