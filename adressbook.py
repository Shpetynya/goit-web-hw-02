import pickle
from collections import UserDict
from datetime import datetime, timedelta
from models import Name, Phone, Birthday


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str):
        """Додає телефон до списку телефонів."""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number: str):
        """Видаляє телефон зі списку телефонів."""
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        """Редагує існуючий телефон."""
        old_phone = self.find_phone(old_phone_number)
        if old_phone:
            try:
                new_phone = Phone(new_phone_number)
                self.remove_phone(old_phone_number)
                self.add_phone(new_phone_number)
            except ValueError:
                raise ValueError(
                    f"New phone number {new_phone_number} is not valid. It must be 10 digits."
                )
        else:
            raise ValueError(f"Phone number {old_phone_number} not found.")

    def find_phone(self, phone_number: str):
        """Повертає телефон, якщо він є в списку."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для управління записами в адресній книзі."""

    def add_record(self, record: Record):
        """Додає запис до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Знаходить запис за ім'ям."""
        return self.data.get(name, None)

    def delete(self, name: str):
        """Видаляє запис з адресної книги за ім'ям."""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                # Перетворюємо рядок в дату
                birthday_date = datetime.strptime(
                    record.birthday.value, "%d.%m.%Y"
                ).date()
                next_birthday = birthday_date.replace(year=today.year)

                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)

                days_until_birthday = (next_birthday - today).days
                if 0 <= days_until_birthday <= 7:
                    # Перевірка на вихідні
                    if next_birthday.weekday() in (5, 6):
                        next_birthday += timedelta(days=(7 - next_birthday.weekday()))

                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "birthday": next_birthday.strftime(
                                "%d.%m.%Y"
                            ),  # Перетворюємо дату в рядок
                        }
                    )

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
