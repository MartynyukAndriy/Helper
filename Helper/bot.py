from collections import UserDict
from datetime import datetime
import pickle
from pathlib import Path
import os


from Helper import classes


CONTACT_FILE_NAME = "addressbook.bin"
CONTACT_DIR = "C:\Program Files\Helper"
os.makedirs(
    rf"{CONTACT_DIR}", exist_ok=True)
CONTACT_FILE_NAME = "addressbook.bin"
ABSOLUTE_CONTACT_PATH = rf"{CONTACT_DIR}\{CONTACT_FILE_NAME}"
CONTACT_SERIALIZATION_PATH = Path(ABSOLUTE_CONTACT_PATH)

ADDRESS_BOOK = classes.AddressBook()


def hello():
    return "How can I help you?"


def help():
    print(f"To start working with the assistant, write one of the commands.\nCommand. Description.\n", "-"*115)
    print(f"add:          Adds a contact to the addressbook. Fields for writing phone, address, email, birthday, are not mandatory.\n", "-"*115)
    print(f"search:       Searches for contacts in the address book by the following fields: name / phone.\n", "-"*115)
    print(f"change:       Changes the information in the contact: name / phone / address / email / birthday.\n", "-"*115)
    print(f"show:         Show contacts as much as the user specifies.\n", "-"*115)
    print(f"showcontact:  Show exact contact user specifies.\n", "-"*115)
    print(f"showall:      Show all notes.\n", "-"*115)
    print(f"del:          Deleting a contact, or deleting phone / address / email / birthday in contact.\n", "-"*115)
    print(f"cancel:       An undo command anywhere in the assistant.\n", "-"*115)
    print(f"birthdays:    Shows the number of days until someone's birthday.\n", "-"*115)
    print(f"good bye, close, exit: Exit the program.\n", "-"*115)
    command = input("Press any key to return. ")
    if command.lower() == "cancel":
        return "Exit from the help menu. "
    else:
        main()


def add():
    while True:
        name = input("Type a contact name: ")
        if name.lower() == "cancel":
            return "Adding a new contact has been canceled"
        elif name in ADDRESS_BOOK.data.keys():
            while True:
                answer = input(
                    "You have already such contact, do you want to rewrite it? (y/n) ")
                if answer.lower() == "y":
                    name = classes.Name(name)
                    break
                elif answer.lower() == "cancel":
                    return "Adding a new contact has been canceled"
                elif answer.lower() == "n":
                    break
                else:
                    print("Wrong command")
            if answer.lower() == "y":
                break
            else:
                continue
        else:
            name = classes.Name(name)
            break
    phone = input(f"Type {name.value}'s phone number: ")
    if phone.lower() == "cancel":
        return "Adding a new contact has been canceled"
    else:
        phone = classes.Phone(phone)
    while not phone.value:
        answer = input(
            "Would you like to try one more time? (y/n): ")
        if answer.lower() == "n":
            break
        elif answer.lower() == "cancel":
            return "Adding a new contact has been canceled"
        elif answer.lower() == "y":
            phone = classes.Phone(input(f"Type {name.value}'s phone number: "))
            if phone.value:
                break
        else:
            print("Please choose correct answer")
    address = input(f"Type {name.value}'s address: ")
    if address.lower() == "cancel":
        return "Adding a new contact has been canceled"
    else:
        address = classes.Address(address)
    email = input(f"Type {name.value}'s email: ")
    if email.lower() == "cancel":
        return "Adding a new contact has been canceled"
    else:
        email = classes.Email(email)
    while not email.value:
        answer = input(
            "Email is incorrect, would you like to try one more time? (y/n): ")
        if answer.lower() == "n":
            break
        elif answer.lower() == "cancel":
            return "Adding a new contact has been canceled"
        elif answer.lower() == "y":
            email = classes.Email(input(f"Type {name.value}'s email: "))
            if email.value:
                break
        else:
            print("Please choose correct answer")
    birthday = input(f"Type {name.value}'s birthday: ")
    if birthday.lower() == "cancel":
        return "Adding a new contact has been canceled"
    else:
        birthday = classes.Birthday(birthday)
    while not birthday.value:
        answer = input(
            "Would you like to try one more time? (y/n): ")
        if answer.lower() == "n":
            break
        elif answer.lower() == "cancel":
            return "Adding a new contact has been canceled"
        elif answer.lower() == "y":
            birthday = classes.Birthday(
                input(f"Type {name.value}'s birthday: "))
            if birthday.value:
                break
        else:
            print("Please choose correct answer")
    record = classes.Record(name, phone, address, email, birthday)
    ADDRESS_BOOK.add_record(record)
    return f"Contact '{name.value}' has been saved"


def birthdays():
    days = input("How many days? ")
    if days.isnumeric():
        if ADDRESS_BOOK.show_contacts_by_birthday(int(days)):
            showrecord(ADDRESS_BOOK.show_contacts_by_birthday(int(days)))
        else:
            print(f"Nothing is match")
    else:
        print("Days has to be a positive number")


def search():
    while True:
        result = input("Choose what you want to find (name / phone): ")
        if result.lower() == "name":
            result = input("What you want to find: ")
            if ADDRESS_BOOK.find_info_by_name(result) and ADDRESS_BOOK.find_info_by_name(result) != "Nothing found":
                showrecord(ADDRESS_BOOK.find_info_by_name(result))
            else:
                print(f"Nothing match with {result}")
        elif result.lower() == "phone":
            result = input("What you want to find: ")
            if ADDRESS_BOOK.find_info_by_phone(result) and ADDRESS_BOOK.find_info_by_phone(result) != "Nothing found":
                showrecord(ADDRESS_BOOK.find_info_by_phone(result))
            else:
                print(f"Nothing match with {result}")
        elif result.lower() == "cancel":
            print("Serching has been canceled")
            break
        else:
            print("Wrong command")


def change():
    contact = input("Which contact do you want to change? ")
    if contact.lower() == "cancel":
        return "Changing has been canceled"
    if ADDRESS_BOOK.show_record(contact):
        while True:
            item = input(
                f"What do you want to change at {contact}'s records? ")
            if item.lower() == "name":
                new_name = input(f"Type a new name for contact {contact}: ")
                ADDRESS_BOOK.change_name(contact, new_name)
                return f"Name for contact {contact} changed to {new_name}"
            elif item.lower() == "phone":
                command = input(
                    "Choose option: edit (add one more phone number) / change (del all numbers and add one) / replace (replace exact phone number to another): ")
                if command.lower() == "edit":
                    while True:
                        new_phone = input(
                            f"Type a new phone for contact {contact}: ")
                        if new_phone.lower() == "cancel":
                            return "Changing has been canceled"
                        else:
                            new_phone = classes.Phone(new_phone)
                        if new_phone.value:
                            ADDRESS_BOOK.edit_phone(contact, new_phone)
                            return f"Phone {new_phone.value} has been added"
                        else:
                            answer = input(
                                "Phone is incorrect, would you like to try one more time? (y/n): ")
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
                        old_phones = ADDRESS_BOOK.get_phones(contact)
                        ADDRESS_BOOK.clear_phones(contact)
                        new_phone = input(
                            f"Type a new phone for contact {contact}: ")
                        if new_phone.lower() == "cancel":
                            return "Changing has been canceled"
                        else:
                            new_phone = classes.Phone(new_phone)
                        if new_phone.value:
                            ADDRESS_BOOK.edit_phone(contact, new_phone)
                            return f"Phone {new_phone.value} has been added"
                        else:
                            answer = input(
                                "Phone is incorrect, would you like to try one more time? (y/n): ")
                            if answer.lower() == "n":
                                ADDRESS_BOOK.set_phones(contact, old_phones)
                                break
                            elif answer.lower() == "y":
                                continue
                            elif answer.lower() == "cancel":
                                return "Changing has been canceled"
                            else:
                                break
                elif command.lower() == "replace":
                    while True:
                        old_phone = input(
                            "Type phone number you want to change: ")
                        if old_phone.lower() == "cancel":
                            return "Changing has been canceled"
                        old_phone = classes.Phone(old_phone)
                        phones_list = [
                            phone.value for phone in ADDRESS_BOOK.get_phones(contact)]
                        if old_phone.value in phones_list:
                            while True:
                                new_phone = input("Type a new phone: ")
                                if new_phone.lower() == "cancel":
                                    return "Changing has been canceled"
                                new_phone = classes.Phone(new_phone)
                                if new_phone.value == None:
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
                                    phones = ADDRESS_BOOK.get_phones(contact)
                                    for i in range(len(phones)):
                                        if phones[i].value == old_phone.value:
                                            phones[i] = new_phone
                                    ADDRESS_BOOK.set_phones(contact, phones)
                                    return f"Phone {old_phone.value} has been changed to {new_phone.value}"
                else:
                    answer = input(
                        "Command is incorrect, would you like to try one more time? (y/n): ")
                    if answer.lower() == "n":
                        break
                    elif answer.lower() == "y":
                        continue
                    elif answer.lower() == "cancel":
                        return "Changing has been canceled"
                    else:
                        continue
            elif item.lower() == "address":
                new_address = input(
                    f"Type a new address for contact {contact}: ")
                if new_address.lower() == "cancel":
                    return "Changing has been canceled"
                ADDRESS_BOOK.change_address(contact, new_address)
                return f"Address for contact {contact} changed to {new_address}"
            elif item.lower() == "email":
                while True:
                    new_email = input(
                        f"Type a new email for contact {contact}: ")
                    if new_email.lower() == "cancel":
                        return "Changing has been canceled"
                    ADDRESS_BOOK.change_email(contact, new_email)
                    if ADDRESS_BOOK.data[contact].email.value == new_email:
                        return f"Email for contact {contact} changed to {new_email}"
                    else:
                        answer = input(
                            "Email is incorrect, would you like to try one more time? (y/n): ")
                        if answer.lower() == "n":
                            break
                        elif answer.lower() == "y":
                            continue
                        elif answer.lower() == "cancel":
                            return "Changing has been canceled"
                        else:
                            break
            elif item.lower() == "birthday":
                while True:
                    new_birthday = input(
                        f"Type a new birthday for contact {contact}: ")
                    if new_birthday.lower() == "cancel":
                        return "Changing has been canceled"
                    ADDRESS_BOOK.change_birthday(contact, new_birthday)
                    if ADDRESS_BOOK.data[contact].birthday.value == new_birthday:
                        return f"Birthday for contact {contact} changed to {new_birthday}"
                    else:
                        answer = input(
                            "Birthday is incorrect, would you like to try one more time? (y/n): ")
                        if answer.lower() == "n":
                            break
                        elif answer.lower() == "y":
                            continue
                        elif answer.lower() == "cancel":
                            return "Changing has been canceled"
                        else:
                            continue
            elif item.lower() == "cancel":
                return "Changing has been canceled"
            else:
                while True:
                    answer = input(
                        "You have such options: (name / phone / address / email / birthday). Would you like to try one more time? (y/n)")
                    if answer.lower() == "y":
                        break
                    elif answer.lower() in ["n", "cancel"]:
                        return "Changing has been canceled"
                    else:
                        print("Wrong command")
    else:
        return f"{contact} didn't exist"


def del_record():
    command = input("Do you want to delete whole contact? (y/n) ")
    while True:
        if command.lower() == "y":
            contact = input("What contact do you want to delete? ")
            if contact in ADDRESS_BOOK.data.keys():
                ADDRESS_BOOK.data.pop(contact)
                return f"Contact {contact} has been deleted"
            else:
                while True:
                    answer = input(
                        "No such contact, do you want to try one more time? (y/n) ")
                    if answer.lower() == "y":
                        break
                    elif answer.lower() in ["n", "cancel"]:
                        return "You have canceled deleting"
                    else:
                        print("Wrong command")
        elif command.lower() == "n":
            while True:
                contact = input(
                    "Type in which contact you want to delete something: ")
                if contact.lower() == "cancel":
                    return "You have canceled deleting"
                if contact in ADDRESS_BOOK.data.keys():
                    while True:
                        item = input("What exact you want to delete? ")
                        if item.lower() == "phone":
                            ADDRESS_BOOK.clear_phones(contact)
                        elif item.lower() == "address":
                            ADDRESS_BOOK.change_address(contact, None)
                        elif item.lower() == "email":
                            ADDRESS_BOOK.change_email(contact, None)
                        elif item.lower() == "birthday":
                            ADDRESS_BOOK.change_birthday(contact, None)
                        elif item.lower() == "cancel":
                            return "You have canceled deleting"
                        else:
                            print(
                                "You have to choose one of this command: (phone / address / email / birthday / cancel) ")
                            continue
                        return f"{item.title()} for contact {contact} has been deleted"
                elif contact.lower() == "cancel":
                    return "You have canceled deleting"
                else:
                    while True:
                        answer = input(
                            "No such contact, do you want to try one more time? (y/n) ")
                        if answer.lower() == "y":
                            break
                        elif answer.lower() == "n":
                            return "You have canceled deleting"
                        else:
                            print("Wrong command")


def show_all():
    counter = 1
    print(
        f"{'№':^2} | {'Name':^20} | {'Phones':^35} | {'Email':^35} | {'Address':^35} | {'Birthday':^10} |")
    for info in ADDRESS_BOOK.show_records().values():
        name = info.name.value if len(
            info.name.value) < 20 else name[:17]+'...'
        if len(info.phones) == 1:
            contacts = info.phones[0].value
        elif len(info.phones) > 1:
            contacts = [contact.value for contact in info.phones]
            contacts = ", ".join(contacts)
            contacts = contacts if len(
                contacts) < 34 else contacts[:32]+"..."
        else:
            contacts = "None"
        address = info.address.value if info.address.value else "None"
        address = address if len(address) < 35 else address[:32]+"..."
        email = info.email.value if info.email.value else "None"
        email = email if len(email) < 35 else email[:32]+"..."
        birthday = info.birthday.value if info.birthday.value else "None"
        print(
            f"{counter:<2} | {name:<20} | {contacts:<35} | {email:<35} | {address:<35} | {birthday:<10} |")
        counter += 1


def showcontact():
    while True:
        contact = input("Which contact yoou want to see? ")
        if contact.lower() == "cancel":
            return "You have canceled showing"
        if ADDRESS_BOOK.show_record(contact):
            return ADDRESS_BOOK.show_record(contact)
        else:
            return "Nothing match"


def show():
    while True:
        n = input("How many records you want to see? ")
        if n.isnumeric() and int(n) > 0 and int(n) <= len(ADDRESS_BOOK.show_records().values()):
            n = int(n)
            break
        elif n.isnumeric() and int(n) > 0 and int(n) > len(ADDRESS_BOOK.show_records().values()):
            n = len(ADDRESS_BOOK.show_records().values())
            break
        else:
            print("You have to type a number > 0")
    counter = 1
    print(
        f"{'№':^2} | {'Name':^20} | {'Phones':^35} | {'Email':^35} | {'Address':^35} | {'Birthday':^10} |")
    for info in ADDRESS_BOOK.show_records().values():
        name = info.name.value if len(
            info.name.value) < 20 else name[:17]+'...'
        if len(info.phones) == 1:
            contacts = info.phones[0].value
        elif len(info.phones) > 1:
            contacts = [contact.value for contact in info.phones]
            contacts = ", ".join(contacts)
            contacts = contacts if len(
                contacts) < 34 else contacts[:32]+"..."
        else:
            contacts = "None"
        address = info.address.value if info.address.value else "None"
        address = address if len(address) < 35 else address[:32]+"..."
        email = info.email.value if info.email.value else "None"
        email = email if len(email) < 35 else email[:32]+"..."
        birthday = info.birthday.value if info.birthday.value else "None"
        print(
            f"{counter:<2} | {name:<20} | {contacts:<35} | {email:<35} | {address:<35} | {birthday:<10} |")
        counter += 1
        if counter > n:
            break


def showrecord(lst):
    counter = 1
    print(
        f"{'№':^2} | {'Name':^20} | {'Phones':^35} | {'Email':^35} | {'Address':^35} | {'Birthday':^10} |")
    for info in lst:
        name = info.name.value if len(
            info.name.value) < 20 else name[:17]+'...'
        if len(info.phones) == 1:
            contacts = info.phones[0].value
        elif len(info.phones) > 1:
            contacts = [contact.value for contact in info.phones]
            contacts = ", ".join(contacts)
            contacts = contacts if len(
                contacts) < 34 else contacts[:32]+"..."
        else:
            contacts = "None"
        address = info.address.value if info.address.value else "None"
        address = address if len(address) < 35 else address[:32]+"..."
        email = info.email.value if info.email.value else "None"
        email = email if len(email) < 35 else email[:32]+"..."
        birthday = info.birthday.value if info.birthday.value else "None"
        print(
            f"{counter:<2} | {name:<20} | {contacts:<35} | {email:<35} | {address:<35} | {birthday:<10} |")
        counter += 1


def end_work():
    return "Good bye"


COMMANDS = {"hello": hello,
            "help": help,
            "add": add,
            "birthdays": birthdays,
            "search": search,
            "change": change,
            "showall": show_all,
            "show": show,
            "del": del_record,
            "end_work": end_work,
            "showcontact": showcontact}


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
    if command.split()[0].lower() == "showall":
        return "showall"
    if command.split()[0].lower() in ["show", "showcontact"]:
        return command.split()[0].lower()
    if command.split()[0].lower() == "birthdays":
        return "birthdays"
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
        if command in ["show", "showall"]:
            COMMANDS[command]()
            continue
        if command == "showcontact":
            print(COMMANDS[command]())
            continue
        if command == "birthdays":
            COMMANDS[command]()
            continue
        if command == "search":
            COMMANDS[command]()
            continue
        if command == "wrong_command":
            print("Wrong command")
            continue
        print(COMMANDS[command]())


if __name__ == "__main__":
    if CONTACT_SERIALIZATION_PATH.exists():
        ADDRESS_BOOK.deserialize(ABSOLUTE_CONTACT_PATH)
    main()
    ADDRESS_BOOK.serialize(ABSOLUTE_CONTACT_PATH)
