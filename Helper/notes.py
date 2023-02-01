from Helper import classes
from pathlib import Path
import os


NOTEBOOK_FILE_NAME = "notebook.bin"
CONTACT_DIR = "C:\Program Files\Helper"
os.makedirs(
    rf"{CONTACT_DIR}", exist_ok=True)
ABSOLUTE_NOTE_PATH = rf"{CONTACT_DIR}\{NOTEBOOK_FILE_NAME}"
NOTEBOOK_SERIALIZATION_PATH = Path(ABSOLUTE_NOTE_PATH)

NOTES_BOOK = classes.NoteBook()


def hello():
    return "How can I help you?"


def help():
    print(f"To start working with the assistant, write one of the commands.\nCommand. Description.\n", "-"*90)
    print(f"add:     Adds a note to the notebook.\n", "-"*90)
    print(f"search:  Searches for notes in the notebook by the following fields: name / tag / status.\n", "-"*90)
    print(f"change:  Changes the information in the note: name / note / tag / status.\n", "-"*90)
    print(f"shownote:Show note which the user want to see.\n", "-"*90)
    print(f"show:    Show all notes.\n", "-"*90)
    print(f"del:     Deleting a note, or deleting completed notes.\n", "-"*90)
    print(f"cancel:  An undo command anywhere in the assistant.\n", "-"*90)
    print(f"good bye, close, exit: Exit the program.\n", "-"*90)
    command = input("Press any key to return. ")
    if command.lower() == "cancel":
        return "Exit from the help menu. "
    else:
        main()


def add():
    name = input("Type a theme to your record: ")
    while name == "":
        print("Note name cannot be empty!")
        name = input("What do you want to record?: ")
        if name.lower() == "cancel":
            return "Adding a new record has been canceled"
        elif name == classes.NoteName(name):
            while True:
                answer = input(
                    "You have already such note, do you want to rewrite it? (y/n) ")
                if answer.lower() == "y":
                    name = classes.NoteName(name)
                    break
                elif answer.lower() == "cancel":
                    return "Adding a new note has been canceled"
                elif answer.lower() == "n":
                    break
            if answer.lower() == "y":
                break
            else:
                continue
        else:
            name = classes.NoteName(name)
            break
    if name == "cancel":
        return "Adding a new note has been canceled"
    name = classes.NoteName(name)
    note = input(f"Type {name.value}'s note: ")
    if note.lower() == "cancel":
        return "Adding a new note has been canceled"
    else:
        note = classes.Notes(note)
    tag = input(f"Type {name.value}'s tag: ")
    if tag.lower() == "cancel":
        return "Adding a new tag has been canceled"
    else:
        tag = classes.Tags(tag)
    record = classes.RecordNote(name, note, tag)
    NOTES_BOOK.add_note(record)
    return f"Note '{name.value}' has been saved"


def search():
    while True:
        result = input("Choose what you want to find (name / tag / status): ")
        if result.lower() == "name":
            result = input("What you want to find: ")
            if result == "cancel":
                print("Searching has been canceled")
            if NOTES_BOOK.find_info_by_name(result):
                showing_func(NOTES_BOOK.find_info_by_name(result))
            else:
                print("Nothing match to result")
        elif result.lower() == "tag":
            result = input("What you want to find: ")
            if result == "cancel":
                print("Searching has been canceled")
            if NOTES_BOOK.find_info_by_tag(result.lower()):
                showing_func(NOTES_BOOK.find_info_by_tag(result.lower()))
            else:
                print("Nothing match to result")
        elif result.lower() == "status":
            result = input("What you want to find: ")
            if result == "cancel":
                print("Searching has been canceled")
            if NOTES_BOOK.find_info_by_status(result):
                showing_func(NOTES_BOOK.find_info_by_status(result))
            else:
                print("Nothing match to result")
        elif result.lower() == "cancel":
            print("Serching has been canceled")
            break
        else:
            print("Wrong command")


def change():
    name = input("Which note do you want to change? ")
    if name.lower() == "cancel":
        return "Changing has been canceled"
    if NOTES_BOOK.show_record(name):
        while True:
            item = input(
                f"What do you want to change at {name}'s records: (name / note / tag / status)? ")
            if item.lower() == "name":
                new_name = input(f"Type a new name for note {name}: ")
                NOTES_BOOK.change_name(name, new_name)
                return f"Name for note {name} changed to {new_name}"
            elif item.lower() == "note":
                new_note = input(
                    f"Type a new text for note {name}: ")
                if new_note.lower() == "cancel":
                    return "Changing has been canceled"
                NOTES_BOOK.change_note(name, new_note)
                return f"Text for note {name} changed."
            elif item.lower() == "tag":
                command = input(
                    "Choose option: add (add one more tag) / change (replace tag to another) / dell (dell tag): ")
                if command.lower() == "add":
                    while True:
                        new_tag = input(
                            f"Type a new tag for note {name}: ")
                        if new_tag.lower() == "cancel":
                            return "Changing has been canceled"
                        else:
                            new_tag = classes.Tags(new_tag)
                        if new_tag.value:
                            NOTES_BOOK.add_tag(name, new_tag)
                            return f"Tag {new_tag.value} has been added"
                        else:
                            answer = input(
                                "Please, type the tag. Would you like to try one more time? (y/n): ")
                            if answer.lower() == "n":
                                break
                            elif answer.lower() == "y":
                                continue
                            elif answer.lower() == "cancel":
                                return "Changing has been canceled"
                            else:
                                break
                elif command.lower() == "change":
                    while True:
                        old_tag = input(
                            "Type tag you want to change: ")
                        if old_tag.lower() == "cancel":
                            return "Changing has been canceled"
                        if old_tag in [tag.value for tag in NOTES_BOOK.get_tags(name)]:
                            while True:
                                new_tag = input("Type a new tag: ")
                                if new_tag.lower() == "cancel":
                                    return "Changing has been canceled"
                                new_tag = classes.Tags(new_tag)
                                if new_tag.value == None:
                                    while True:
                                        answer = input(
                                            "Would you like try one more time? (y/n) ")
                                        if answer.lower() == "y":
                                            break
                                        elif answer.lower() in ["cancel", "n"]:
                                            return "Changing has been canceled"
                                        else:
                                            print("Wrong command")
                                else:
                                    old_tag = classes.Tags(old_tag)
                                    NOTES_BOOK.change_tag(
                                        name, old_tag, new_tag)
                                    return f"Tag {old_tag.value} has been changed to {new_tag.value}"
                elif command.lower() == "dell":
                    while True:
                        tag = input("Please type a tag you want to delete ")
                        if tag == "cancel":
                            return f"You canceled changing contact {name}"
                        if NOTES_BOOK.find_info_by_tag(tag):
                            NOTES_BOOK.delete_tag(name, tag)
                            return f"Tag {tag} has been deleted"
                        else:
                            while True:
                                answer = input(
                                    "Such tag didn't exist, would you like to try one more time? (y/n)")
                                if answer.lower() in ["cancel", "n"]:
                                    return "Deleting has been canceled"
                                if answer.lower() == "y":
                                    break
                                else:
                                    print("Wrong command")
                else:
                    answer = input(
                        "Please, type the tag. Would you like to try one more time? (y/n): ")
                    if answer.lower() == "n":
                        break
                    elif answer.lower() == "y":
                        continue
                    elif answer.lower() == "cancel":
                        return "Changing has been canceled"
                    else:
                        continue
            elif item.lower() == "status":
                while True:
                    new_status = input(
                        f"Type a new status for note {name}: (Done / In progress)? ")
                    if new_status.lower() == "cancel":
                        return "Changing has been canceled"
                    NOTES_BOOK.change_status(name, new_status)
                    return f"Status for note {name} changed to {new_status}"
            elif item.lower() == "cancel":
                return "Changing has been canceled"
            else:
                answer = input(
                    "You have such options: (name / note / tag / status). Would you like to try one more time? (y/n)")
                if answer.lower() == "y":
                    continue
                else:
                    break
    else:
        return f"{name} didn't exist"


def dellate_note():
    while True:
        command = input("Do you want to delete one note? (y/n) ")
        if command.lower() == "cancel":
            return "You have canceled deleting"
        if command.lower() == "y":
            note = input("Which note do you want to delete? ")
            if note in NOTES_BOOK.data.keys():
                NOTES_BOOK.data.pop(note)
                return f"Note {note} has been deleted"
            else:
                while True:
                    answer = input(
                        "No such note, do you want to try one more time? (y/n) ")
                    if answer.lower() == "y":
                        break
                    elif answer.lower() in ["n", "cancel"]:
                        return "You have canceled deleting"
                    else:
                        print("Wrong command")
        elif command.lower() == "n":
            while True:
                answer = input(
                    "Do you want to delete all completed notes? (y/n) ")
                if answer.lower() in ["cancel"]:
                    return "You have canceled deleting"
                if answer.lower() == "y":
                    NOTES_BOOK.dellete_notes_by_status("done")
                    return f"Notes with status 'done' has been deleted"
                elif command.lower() == "cancel":
                    return "You have canceled deleting"
                else:
                    while True:
                        answer = input(
                            "No such note, do you want to try one more time? (y/n) ")
                        if answer.lower() == "y":
                            break
                        elif answer.lower() == "n":
                            return "You have canceled deleting"
                        else:
                            print("Wrong command")
        else:
            print("Wrong command")


def show_note():
    name = input("Which note do you want to see? ")
    if name.lower() == "cancel":
        return "Showing has been canceled"
    if NOTES_BOOK.show_record(name):
        return NOTES_BOOK.show_record(name)
    else:
        return "Nothing match"


def show_all():
    counter = 1
    print(
        f"{'№':^2} | {'Name':^31} | {'Note':^67} | {'Tags':^26} | {'Status':^11} |\n", "-"*150)
    for info in NOTES_BOOK.show_records().values():
        name = info.name.value
        if len(info.tags) == 1:
            tags = info.tags[0].value
        elif len(info.tags) > 1:
            tags_l = []
            for tag in [tag.value for tag in info.tags]:
                tags_l.append(tag)
            tags = ", ".join(tags_l)
        tags = tags if len(tags) < 26 else tags[:23]+"..."
        note = info.note.value
        note = note if len(note) < 67 else note[:63]+"..."
        status = info.status.value
        print(
            f"{counter:<2} | {name:<31} | {note:<67} | {tags:<26} | {status:<11} |\n", "-"*150)
        counter += 1


def showing_func(lst):
    counter = 1
    print(
        f"{'№':^2} | {'Name':^31} | {'Note':^67} | {'Tags':^26} | {'Status':^11} |\n", "-"*150)
    for info in lst:
        name = info.name.value
        if len(info.tags) == 1:
            tags = info.tags[0].value
        elif len(info.tags) > 1:
            tags_l = []
            for tag in [tag.value for tag in info.tags]:
                tags_l.append(tag)
            tags = ", ".join(tags_l)
        tags = tags if len(tags) < 26 else tags[:23]+"..."
        note = info.note.value
        note = note if len(note) < 67 else note[:63]+"..."
        status = info.status.value
        print(
            f"{counter:<2} | {name:<31} | {note:<67} | {tags:<26} | {status:<11} |\n", "-"*150)
        counter += 1


def end_work():
    return "Good bye"


COMMANDS = {"hello": hello,
            "help": help,
            "add": add,
            "search": search,
            "change": change,
            "show": show_all,
            "shownote": show_note,
            "del": dellate_note,
            "end_work": end_work}


def parser(command):
    if command.lower() == "hello":
        return "hello"
    if command.lower() in ["good bye", "close", "exit"]:
        return "end_work"
    if command.lower() == "help":
        return "help"
    if command.split()[0].lower() == "add":
        return "add"
    if command.split()[0].lower() == "search":
        return "search"
    if command.split()[0].lower() == "change":
        return "change"
    if command.split()[0].lower() == "show":
        return "show"
    if command.split()[0].lower() == "shownote":
        return "shownote"
    if command.split()[0].lower() == "del":
        return "del"
    else:
        return "wrong_command"


def main():
    print("Hello. If you need help, write 'help'")
    while True:
        user_command = input(">>> ")
        command = parser(user_command)
        if command == "end_work":
            print(COMMANDS["end_work"]())
            break
        if command == "hello":
            print(COMMANDS["hello"]())
            continue
        if command == "help":
            print(COMMANDS["help"]())
            continue
        if command == "shownote":
            print(COMMANDS["shownote"]())
            continue
        if command == "show":
            COMMANDS["show"]()
            continue
        if command == "wrong_command":
            print("Wrong command")
            continue
        if command == "search":
            COMMANDS[command]()
            continue
        print(COMMANDS[command]())


if __name__ == "__main__":
    if NOTEBOOK_SERIALIZATION_PATH.exists():
        NOTES_BOOK.deserialize(NOTEBOOK_SERIALIZATION_PATH)
    main()
    NOTES_BOOK.serialize()
