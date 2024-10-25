from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    """Базовий клас для полів запису"""

    def __init__(self, value: str):
        self.value = value.strip()

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту"""

    def __init__(self, value: str):
        if len(value.strip()) == 0:
            raise ValueError("Name can not be empty!")
        super().__init__(value)


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією формату."""

    def __init__(self, value: str):
        if Phone.isValid(value):
            super().__init__(value)
        else:
            raise ValueError("Phone number must contain 10 digits")

    @staticmethod
    def isValid(phone) -> bool:
        """Валідація телефону - 10 цифр"""
        if re.fullmatch(r"\d{10}", phone):
            return True
        else:
            return False

    def __eq__(self, value: object) -> bool:
        """=="""
        return self.value == value.value

    def edit(self, new_value: str) -> None:
        """edit phone"""
        if Phone.isValid(new_value):
            self.value = new_value.strip()
        else:
            raise ValueError("Phone number must contain 10 digits")


class Birthday(Field):
    """Клас для зберігання дня народження."""

    def __init__(self, value: str):
        try:
            # Перетворюємо рядок на об'єкт datetime
            birthday = datetime.strptime(value.strip(), "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        # перевірка на коректність дати
        if birthday > datetime.today().date():
            raise ValueError("Birthday from the future is not allowed!")
        self.value = birthday

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Клас для зберігання інформації про контакт."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        """Додавання номера телефону."""
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> str:
        """Пошук телефону у записі."""
        find_phone = Phone(phone)
        for p in self.phones:
            if p == find_phone:
                return p
        raise ValueError(f"Phone number {phone} not found")

    def remove_phone(self, phone: str) -> None:
        """Видалення номера телефону."""
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Редагування телефону."""
        self.find_phone(old_phone).edit(new_phone)

    def add_birthday(self, birthday: str) -> None:
        """Додавання дня народження."""
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами в адресній книзі."""

    def add_record(self, record: Record) -> None:
        """Додавання запису до книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """Пошук запису за ім'ям."""
        if name in self.data:
            return self.data[name]
        raise KeyError(f"Record with name {name} not found")

    def delete(self, name: str) -> None:
        """Видалення запису за ім'ям."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record with name {name} not found")

    def get_upcoming_birthdays(self) -> list:
        """Отримання списку користувачів, яких потрібно привітати на наступному тижні."""
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= today + timedelta(days=7):
                    upcoming_birthdays.append(
                        {
                            "name": str(record.name),
                            "congratulation_date": birthday_this_year.strftime(
                                "%d.%m.%Y"
                            ),
                        }
                    )

        return upcoming_birthdays
