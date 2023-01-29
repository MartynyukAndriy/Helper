import classes
from pathlib import Path

NOTEBOOK_FILE_NAME = "notebook.bin"
NOTEBOOK_SERIALIZATION_PATH = Path(NOTEBOOK_FILE_NAME)

NOTES_BOOK = classes.NoteBook()


def hello():
    return "How can I help you?"


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
    name = classes.NoteName(name)
    note = input(f"Type {name.value}'s note: ")
    if note.lower() == "cancel":
        return "Adding a new note has been canceled"
    else:
        note = classes.Notes(note)
    tag = input(f"Type {name.value}'s tags: ")
    if tag.lower() == "cancel":
        return "Adding a new tag has been canceled"
    else:
        tag = classes.Tags(tag)
    record = classes.RecordNote(name, note, tag)
    NOTES_BOOK.add_note(record)
    return f"Contact '{name.value}' has been saved"


def search():
    while True:
        result = input("Choose what you want to find (name / tag / status): ")
        if result.lower() == "name":
            result = input("What you want to find: ")
            if result == "cancel":
                return "Searching has been canceled"
            if NOTES_BOOK.find_info_by_name(result):
                return NOTES_BOOK.find_info_by_name(result)
            else:
                return "Nothing match to result"
        elif result.lower() == "tag":
            result = input("What you want to find: ")
            if result == "cancel":
                return "Searching has been canceled"
            if NOTES_BOOK.find_info_by_tag(result.lower()):
                return NOTES_BOOK.find_info_by_tag(result.lower())
            else:
                return "Nothing match to result"
        elif result.lower() == "status":
            result = input("What you want to find: ")
            if result == "cancel":
                return "Searching has been canceled"
            if NOTES_BOOK.find_info_by_status(result.lower()):
                return NOTES_BOOK.find_info_by_status(result.lower())
            else:
                return "Nothing match to result"
        elif result.lower() == "cancel":
            return "Serching has been canceled"
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
                            new_tag = classes.Tag(new_tag)
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
                        old_tag = classes.Tag(old_tag)
                        tags_list = [
                            tag.value for tag in NOTES_BOOK.get_tags(name)]
                        if old_tag.value in tags_list:
                            while True:
                                new_tag = input("Type a new tag: ")
                                if new_tag.lower() == "cancel":
                                    return "Changing has been canceled"
                                new_tag = classes.Tag(new_tag)
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
                                    tags = NOTES_BOOK.gat_tags(name)
                                    for i in range(len(tags)):
                                        if tags[i].value == old_tag.value:
                                            tags[i] = new_tag
                                    NOTES_BOOK.change_tags(name, tags)
                                    return f"Tag {old_tag.value} has been changed to {new_tag.value}"
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
            elif command.lower() == "dell":
                while True:
                    old_tag = input(
                        "Type tag you want to dellete: ")
                    if old_tag.lower() == "cancel":
                        return "Changing has been canceled"
                    old_tag = classes.Tag(old_tag)
                    tag_list = [
                        tag.value for tag in NOTES_BOOK.get_tags(name)]
                    if old_tag.value in tag_list:
                        NOTES_BOOK.dell_tag(name, old_tag)
                        return f"Tag {old_tag.value} has been dellated."
                    else:
                        answer = input(
                            "Tag is incorrect, would you like to try one more time? (y/n): ")
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
    command = input("Do you want to delete the note? (y/n) ")
    while True:
        if command.lower() == "y":
            note = input("What note do you want to delete? ")
            if note.lower() in NOTES_BOOK.data.keys():
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
                if answer.lower() in ["n", "cancel"]:
                    return "You have canceled deleting"
                if answer.lower() == "y":
                    NOTES_BOOK.dellete_notes()
                    return f"Notes with status Done has been deleted"
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


def show_all():
    return NOTES_BOOK.show_records()


def end_work():
    return "Good bye"


COMMANDS = {"hello": hello,
            "add": add,
            "search": search,
            "change": change,
            "show": show_all,
            "del": dellate_note,
            "end_work": end_work}


def parser(command):
    if command.lower() == "hello":
        return "hello"
    if command.lower() in ["good bye", "close", "exit"]:
        return "end_work"
    if command.split()[0].lower() == "add":
        return "add"
    if command.split()[0].lower() == "search":
        return "search"
    if command.split()[0].lower() == "change":
        return "change"
    if command.split()[0].lower() == "show":
        return "show"
    if command.split()[0].lower() == "del":
        return "del"
    else:
        return "wrong_command"


def main():
    while True:
        user_command = input(">> ")
        command = parser(user_command)
        if command == "end_work":
            print(COMMANDS["end_work"]())
            break
        if command == "hello":
            print(COMMANDS["hello"]())
            continue
        if command == "show":
            print(COMMANDS["show"]())
            continue
        if command == "wrong_command":
            print("Wrong command")
            continue
        print(COMMANDS[command]())


if __name__ == "__main__":
    if NOTEBOOK_SERIALIZATION_PATH.exists():
        NOTES_BOOK.deserialize(NOTEBOOK_SERIALIZATION_PATH)
    main()
    NOTES_BOOK.serialize()
