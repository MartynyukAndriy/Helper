from collections import UserDict
from datetime import datetime
import pickle
from pathlib import Path


import classes

CONTACT_FILE_NAME = "addressbook.bin"
CONTACT_SERIALIZATION_PATH = Path(CONTACT_FILE_NAME)

ADDRESS_BOOK = classes.AddressBook()


def hello():
    return "How can I help you?"


def add():
    name = input("Type a contact name: ")
    if name.lower() == "cancel":
        return "Adding a new contact has been canceled"
    else:
        name = classes.Name(name)
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
        else:
            print("Please choose correct answer")
    record = classes.Record(name, phone, address, email, birthday)
    ADDRESS_BOOK.add_record(record)
    return f"Contact '{name.value}' has been saved"


def birthdays():
    days = int(input("How many days? "))
    if ADDRESS_BOOK.show_contacts_by_birthday(days):
        return ADDRESS_BOOK.show_contacts_by_birthday(days)
    else:
        return f"Nothing is match"


def search():
    while True:
        result = input("Choose what you want to find (name / phone): ")
        if result.lower() == "name":
            result = input("What you want to find: ")
            return ADDRESS_BOOK.find_info_by_name(result)
        elif result.lower() == "phone":
            result = input("What you want to find: ")
            return ADDRESS_BOOK.find_info_by_phone(result)
        elif result.lower() == "cancel":
            return "Serching has been canceled"
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
                        new_phone = classes.Phone(
                            input(f"Type a new phone for contact {contact}: "))
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
                    pass
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
                return f"Address for contact {contact} changed to {new_name}"
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
                answer = input(
                    "You have such options: (name / phone / address / email / birthday). Would you like to try one more time? (y/n)")
                if answer.lower() == "y":
                    continue
                else:
                    break
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
    return ADDRESS_BOOK.show_records()


def end_work():
    return "Good bye"


COMMANDS = {"hello": hello,
            "add": add,
            "birthdays": birthdays,
            "search": search,
            "change": change,
            "show": show_all,
            "del": del_record,
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
    if command.split()[0].lower() == "birthdays":
        return "birthdays"
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

