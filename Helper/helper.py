from Helper import bot, notes, sort, classes
from pathlib import Path
from Helper.bot import ABSOLUTE_CONTACT_PATH, CONTACT_SERIALIZATION_PATH
from Helper.notes import ABSOLUTE_NOTE_PATH, NOTEBOOK_SERIALIZATION_PATH


def main():
    while True:
        work_with = input(
            "With what part of helper you want to work? (contacts / notes / files) ")
        if work_with.lower() == "contacts":
            if CONTACT_SERIALIZATION_PATH.exists():
                bot.ADDRESS_BOOK.deserialize(ABSOLUTE_CONTACT_PATH)
            bot.main()
            bot.ADDRESS_BOOK.serialize(ABSOLUTE_CONTACT_PATH)
        elif work_with.lower() == "notes":
            if NOTEBOOK_SERIALIZATION_PATH.exists():
                notes.NOTES_BOOK.deserialize(ABSOLUTE_NOTE_PATH)
            notes.main()
            notes.NOTES_BOOK.serialize(ABSOLUTE_NOTE_PATH)
        elif work_with.lower() == "files":
            sort.clean()
            sort.DIR_PATH = ""
        elif work_with.lower() in ["cancel", "close", "exit", "good bye"]:
            print("Bye")
            break
        else:
            print("Wrong command")


if __name__ == "__main__":
    main()
