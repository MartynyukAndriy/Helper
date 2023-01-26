import bot
import sort

if __name__ == "__main__":
    while True:
        work_with = input(
            "With part of helper you want to work? (contacts / notes / files) ")
        if work_with.lower() == "contacts":
            if bot.CONTACT_SERIALIZATION_PATH.exists():
                bot.ADDRESS_BOOK.deserialize(bot.CONTACT_FILE_NAME)
            bot.main()
            bot.ADDRESS_BOOK.serialize()
        elif work_with.lower() == "notes":
            pass
        elif work_with.lower() == "files":
            sort.clean()
        elif work_with.lower() in ["cancel", "close", "exit", "good bye"]:
            print("Bye")
            break
        else:
            print("Wrong command")
