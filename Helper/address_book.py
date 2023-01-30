from collections import UserDict
from datetime import datetime
import pickle
from pathlib import Path


FILE_NAME = "addressbook.bin"
SERIALIZATION_PATH = Path(FILE_NAME)


class AddressBook(UserDict):
    """Creating user's addressbooks"""

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def show_records(self):
        return self.data

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


class Record:
    """Creating user's contacts"""

    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        if phone:
            self.add_phone(phone)
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            self.birthday = None

    def __str__(self):
        return f"Name: {self.name.value} Phone: {self.phones} Birthday: {self.birthday}"

    def __repr__(self):
        return f"Name: {self.name.value} Phone: {self.phones} Birthday: {self.birthday}"

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
            return f"{delta.days} left to the birthaday"
        else:
            birthday = datetime(year=int(datetime.now().year)+1,
                                month=int(self.birthday.value[3:5]), day=int(self.birthday.value[:2])).date()
            delta = birthday - time_now
            return f"{delta.days} left to the birthaday"


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
            print("Phone number is wrong!")

        else:
            new_phone = "".join(new_phone)
            if len(new_phone) == 12:
                return f"+{new_phone[0:2]}({new_phone[2:5]}){new_phone[5:7]}-{new_phone[7:9]}-{new_phone[9:]}"
            elif len(new_phone) == 10:
                return f"+38({new_phone[0:3]}){new_phone[3:6]}-{new_phone[6:8]}-{new_phone[8:]}"
            else:
                print("Length of phone's number is wrong")

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
        if self.check_birthday(new_birthday):
            self.__value = self.check_birthday(new_birthday)

    def check_birthday(self, birthday):
        try:
            year = int(birthday[6:])
            month = int(birthday[3:5])
            day = int(birthday[:2])
        except ValueError:
            print(f"Wrong date, should be - dd.mm.yyyy, only numbers")
        else:
            return birthday


if __name__ == "__main__":
    address_book = AddressBook()
    if SERIALIZATION_PATH.exists():
        address_book.deserialize(FILE_NAME)
    else:
        name = Name("Bill")
        phone = Phone("111")
        print(f"Phone: {phone}")
        rec = Record(name, phone)
        rec.add_birthday("10.10.2002")
        address_book.add_record(rec)
        name1 = Name("John")
        phone1 = Phone("1111111")
        rec1 = Record(name1, phone1)
        address_book.add_record(rec1)
        name2 = Name("Andriy")
        phone2 = Phone("0909090909")
        rec2 = Record(name2, phone2)
        address_book.add_record(rec2)
        name3 = Name("Igor")
        phone3 = Phone("1144411221")
        birthday3 = Birthday("01.01.1991")
        print(birthday3)
        rec3 = Record(name3, phone3, birthday3)
        print(rec3.birthday.value)
        print(rec3.days_to_birthday())
        address_book.add_record(rec3)
        print(address_book.show_records())
        a = address_book.iterator(3)
        print(next(a))
        print(next(a))
    while True:
        search = input("Type what you want to find: ")
        if search.isnumeric():
            print(f"By phone - {address_book.find_info_by_phone(search)}")
        elif search in ["exit", "close", "end"]:
            break
        else:
            print(f"By name - {address_book.find_info_by_name(search)}")
    address_book.serialize()
