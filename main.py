import pickle
from collections import defaultdict

from abc import ABC, abstractmethod
from adressbook import AddressBook, Record


# Абстрактний інтерфейс для команд
class CommandHandler(ABC):
    @abstractmethod
    def handle(self, args, book: AddressBook):
        pass


# Конкретні команди
class AddContactCommand(CommandHandler):
    def handle(self, args, book: AddressBook):
        name, phone, *_ = args
        record = book.find(name)
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = f"Contact {name} added."
        else:
            message = f"Contact {name} updated."
        if phone:
            try:
                record.add_phone(phone)
            except ValueError as e:
                return str(e)
        return message


class ChangeContactCommand(CommandHandler):
    def handle(self, args, book: AddressBook):
        name, old_phone, new_phone = args
        record = book.find(name)
        if record:
            try:
                record.edit_phone(old_phone, new_phone)
                return (
                    f"Phone number for {name} changed from {old_phone} to {new_phone}."
                )
            except ValueError as e:
                return str(e)
        else:
            return f"Contact {name} not found."


class ShowPhoneCommand(CommandHandler):
    def handle(self, args, book: AddressBook):
        name = args[0]
        record = book.find(name)
        if record:
            return f"Phones for {name}: {', '.join(p.value for p in record.phones)}"
        else:
            return f"Contact {name} not found."


class ShowAllCommand(CommandHandler):
    def handle(self, args, book: AddressBook):
        return str(book)


class AddBirthdayCommand(CommandHandler):
    def handle(self, args, book: AddressBook):
        name = args[0]
        birthday = args[1]
        record = book.find(name)
        if record:
            try:
                record.add_birthday(birthday)
                return f"Birthday for {name} set to {birthday}."
            except ValueError as e:
                return str(e)
        else:
            return f"Contact {name} not found."


class ShowBirthdayCommand(CommandHandler):
    def handle(self, args, book: AddressBook):
        name = args[0]
        record = book.find(name)
        if record and record.birthday:
            return f"Birthday for {name}: {record.birthday.value}"
        else:
            return f"Birthday for {name} is not set or contact not found."


class BirthdaysCommand(CommandHandler):
    def handle(self, args, book: AddressBook):
        upcoming_birthdays = book.get_upcoming_birthdays()
        return "\n".join(
            [f"{bd['name']} - {bd['birthday']}" for bd in upcoming_birthdays]
        )


# Обробка помилок
def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Error: Not enough arguments provided."
        except KeyError as e:
            return f"Error: {e} not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return wrapper


# Обробник команд
class CommandProcessor:
    def __init__(self):
        self.commands = defaultdict(lambda: None)

    def register_command(self, name, handler: CommandHandler):
        self.commands[name] = handler

    @input_error
    def execute(self, command, args, book):
        handler = self.commands.get(command)
        if handler:
            return handler.handle(args, book)
        return "Invalid command."


# Збереження та завантаження даних
def save_data(book, filename="addressbook.pkl"):
    """Функція для збереження даних у файл"""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Функція для загрузки файлу"""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return (
            AddressBook()
        )  # Повертаємось до поточної адресної книги якщо файл ще не існує


# Головна програма
def main():
    book = load_data()  # Підгружаємо дані з файлу
    command_processor = CommandProcessor()  # Створюємо обробник команд

    # Реєстрація команд
    command_processor.register_command("add", AddContactCommand())
    command_processor.register_command("change", ChangeContactCommand())
    command_processor.register_command("phone", ShowPhoneCommand())
    command_processor.register_command("all", ShowAllCommand())
    command_processor.register_command("add-birthday", AddBirthdayCommand())
    command_processor.register_command("show-birthday", ShowBirthdayCommand())
    command_processor.register_command("birthdays", BirthdaysCommand())

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = user_input.split()[0], user_input.split()[1:]

        if command in ["close", "exit"]:
            save_data(book)  # Збереження перед виходом
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        else:
            result = command_processor.execute(command, args, book)
            print(result)


if __name__ == "__main__":
    main()
