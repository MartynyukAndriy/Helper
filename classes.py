from collections import UserDict
from datetime import date, datetime
import pickle
from pathlib import Path
import re
import copy
import os


FILE_NAME = "addressbook.bin"
SERIALIZATION_PATH = Path(FILE_NAME)


class AddressBook(UserDict):
    """Creating user's addressbooks"""

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record, None)

    def change_name(self, old_name, new_name):
        self.data[new_name] = copy.deepcopy(self.data[old_name])
        self.data[new_name].name.value = new_name
        self.remove_record(old_name)

    def change_address(self, record, new_address):
        self.data[record].address.value = new_address

    def change_email(self, record, new_email):
        self.data[record].email.value = new_email

    def change_birthday(self, record, new_birthday):
        self.data[record].birthday.value = new_birthday

    def edit_phone(self, record, new_phone):
        self.data[record].add_phone(new_phone)

    def clear_phones(self, record):
        self.data[record].phones = []

    def get_phones(self, record):
        return self.data[record].phones

    def set_phones(self, record, phone_list):
        self.data[record].phones = phone_list

    def show_records(self):
        return self.data

    def show_record(self, contact):
        try:
            return self.data[contact]
        except:
            return None

    def iterator(self, n=1):
        records = list(self.data.keys())
        records_num = len(records)
        if n > records_num:
            n = records_num
        for i in range(0, records_num, n):
            yield [self.data[records[i+j]].show_contact() for j in range(n) if i + j < records_num]

    def serialize(self, file_name="addressbook.bin"):
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def deserialize(self, file_name="addressbook.bin"):
        with open(file_name, "rb") as file:
            self.data = pickle.load(file)

    def find_info_by_name(self, name):
        users_search = []
        for user, info in self.data.items():
            if name.lower() in info.name.value.lower():
                users_search.append(self.data[user])
        if users_search:
            return users_search
        else:
            return "Nothing found"

    def find_info_by_phone(self, search_phone):
        users_search = []
        for user, info in self.data.items():
            if info.phones and info.phones[0].value != None:
                for phone in info.phones:
                    if str(search_phone) in phone.value:
                        users_search.append(self.data[user])
        if users_search:
            return users_search
        else:
            return "Nothing found"

    def show_contacts_by_birthday(self, days):
        result = [self.data[record] for record in self.data if self.data[record].birthday and self.data[record].days_to_birthday()
                  <= days]
        return result


class Record:
    """Creating user's contacts"""

    def __init__(self, name, phone=None, address=None, email=None, birthday=None):
        self.name = name
        self.phones = []
        if phone and phone.value != None:
            self.add_phone(phone)
        self.address = address
        self.email = email
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            self.birthday = None

    def __str__(self):
        return f"Name: {self.name.value} Phone: {self.phones} Address: {self.address.value} Email: {self.email.value} Birthday: {self.birthday}"

    def __repr__(self):
        return f"Name: {self.name.value} Phone: {self.phones} Address: {self.address.value} Email: {self.email.value} Birthday: {self.birthday}"

    def add_phone(self, phone):
        self.phones.append(phone)

    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            self.birthday = Birthday(birthday)

    def change_phone(self, phone):
        self.phones = phone

    def delete_phone(self):
        self.phones = []

    def show_contact(self):
        return {"name": self.name.value,
                "phone": [phone.value for phone in self.phones] if self.phones else [],
                "birthday": self.birthday.value if self.birthday else self.birthday}

    def days_to_birthday(self):
        birthday = datetime(year=int(datetime.now().year),
                            month=int(self.birthday.value[3:5]), day=int(self.birthday.value[:2])).date()
        time_now = datetime.now().date()
        delta = birthday - time_now
        if int(delta.days) >= 0:
            return delta.days
        else:
            birthday = datetime(year=int(datetime.now().year)+1,
                                month=int(self.birthday.value[3:5]), day=int(self.birthday.value[:2])).date()
            delta = birthday - time_now
            return delta.days


class Field:

    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Address(Field):
    pass


class Email(Field):
    def __init__(self, email):
        self.__value = None
        self.value = email

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

    def check_email(self, email):
        result = re.match(
            r"[a-zA-Z]{1}[a-zA-Z0-9._]+@{1}\w+\.{1}[a-zA-Z]{2,3}", email)
        if result:
            return email
        else:
            return None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_email):
        if new_email == None:
            self.__value = None
        elif self.check_email(new_email):
            self.__value = self.check_email(new_email)


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, phone):
        self.__value = None
        self.value = phone

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

    def check_phone(self, phone):
        new_phone = str(phone).strip().replace("+", "").replace(
            "(", "").replace(")", "").replace("-", "").replace(" ", "")
        try:
            new_phone = [str(int(i)) for i in new_phone]
        except ValueError:
            print("Phone number is incorrect!")

        else:
            new_phone = "".join(new_phone)
            if len(new_phone) == 12:
                return f"+{new_phone[0:2]}({new_phone[2:5]}){new_phone[5:7]}-{new_phone[7:9]}-{new_phone[9:]}"
            elif len(new_phone) == 10:
                return f"+38({new_phone[0:3]}){new_phone[3:6]}-{new_phone[6:8]}-{new_phone[8:]}"
            else:
                print("Length of phone's number is wrong")
                return None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_phone):
        if self.check_phone(new_phone):
            self.__value = self.check_phone(new_phone)


class Birthday(Field):

    def __init__(self, birthday):
        self.__value = None
        self.value = birthday

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_birthday):
        if new_birthday == None:
            self.__value = None
        elif self.check_birthday(new_birthday):
            self.__value = self.check_birthday(new_birthday)

    def check_birthday(self, birthday):
        try:
            year = int(birthday[6:])
            month = int(birthday[3:5])
            day = int(birthday[:2])
            test_date = date(year, month, day)
            delta = datetime.now().date() - test_date
            if len(str(year)) < 4:
                raise ValueError
            if delta.days < 0:
                raise TypeError
        except TypeError:
            print("No one can be born in the future :)")
        except ValueError:
            print("Wrong date, should be - dd.mm.yyyy, only numbers")
        else:
            return birthday

class Notes:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'{self.value}'

class Tags:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'{self.value}'

class RecordNote:
    def __init__(self, note: Notes, tag: Tags = None):
        self.note = note
        self.tags = []
        if tag:
            self.tags.append(tag)

    def __repr__(self):
        if len(self.tags) > 0:
            return f'Tags: {[i.value for i in self.tags]}\n{self.note.value}'
        return f'{self.note.value}'

    def add_tag(self):
        while True:
            tag_input = input('Please, add tag:')
            my_tag = Tags(tag_input)
            if tag_input == "":
                break
            if my_tag.value not in [i.value for i in self.tags]:
                self.tags.append(my_tag)


class Notebook(UserDict):
    def __init__(self):
        self.data = {}

    def __repr__(self):
        return f'{self.data}'

    def add_note(self, note: Note):
        my_note = Notes(note)
        rec = RecordNote(my_note)
        self.data[rec.note.value] = rec
        return rec.add_tag()

    def find_by_keyword(self, keyword):
        res = {
            keyword: []
        }
        for tag, notes in self.data.items():
            if keyword in tag.split(', '):
                if notes not in res[keyword]:
                    res[keyword].append(notes)
        return res

    def load_file(self):
        if os.path.isfile('addressbook.bin'):
            with open('addressbook.bin', 'rb') as file:
                addressbook = pickle.load(file)

        with open('addressbook.bin', 'wb') as file:
            pickle.dump(addressbook, file)



class Notebook(UserDict):
    def add_note(self,tags,notes):
        self.data[tags.value]=notes.note
    
    def find_by_keyword(self,keyword):
        res={
            keyword:[]
            }
        for tag, notes in self.data.items():
            if keyword in tag.split(', '):
                if  notes not in res[keyword]:
                    res[keyword].append(notes)
        return res

class Tags():
    def __init__(self,tags):
        self.value=tags

class Notes():
    def __init__(self,note):
        self.note=note

