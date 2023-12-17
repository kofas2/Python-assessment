import json
import os
from datetime import datetime

class NotesManager:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.notes = json.load(file)

    def save_notes(self):
        with open(self.filename, "w") as file:
            json.dump(self.notes, file, indent=2)

    def add_note(self, title, message):
        note = {
            "id": len(self.notes) + 1,
            "title": title,
            "message": message,
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        self.notes.append(note)
        self.save_notes()
        print(f"Заметка успешно добавлена. ID: {note['id']}")

    def list_notes(self, filter_date=None):
        if filter_date:
            try:
                datetime.strptime(filter_date, "%d-%m-%Y")
            except ValueError:
                print("Некорректный формат даты. Используйте формат: дд-мм-гггг")
                return

            filtered_notes = [note for note in self.notes if note["timestamp"].startswith(filter_date)]
            if not filtered_notes:
                print("На указанную дату нет заметок.")
                return

            notes_to_display = filtered_notes
        else:
            notes_to_display = self.notes

        for note in notes_to_display:
            print(f"{note['id']}. {note['title']} ({note['timestamp']})")
            print(note['message'])
            print()

    def edit_note(self, note_id, title, message):
        note = self.get_note_by_id(note_id)
        if note:
            note["title"] = title
            note["message"] = message
            note["timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print("Заметка успешно отредактирована.")
        else:
            print("Заметка с указанным ID не найдена.")

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print("Заметка успешно удалена.")
        else:
            print("Заметка с указанным ID не найдена.")

    def get_note_by_id(self, note_id):
        return next((note for note in self.notes if note["id"] == note_id), None)


def main():
    notes_manager = NotesManager()

    while True:
        print("\nВыберите команду:")
        print("1. Добавить заметку")
        print("2. Список заметок")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Выход")

        choice = input()

        if choice == "1":
            title = input("Введите заголовок заметки: ")
            message = input("Введите текст заметки: ")
            notes_manager.add_note(title, message)
        elif choice == "2":
            filter_date = input("Введите дату для фильтрации (дд-мм-гггг): ")
            notes_manager.list_notes(filter_date)
        elif choice == "3":
            note_id = int(input("Введите ID заметки для редактирования: "))
            title = input("Введите новый заголовок заметки: ")
            message = input("Введите новый текст заметки: ")
            notes_manager.edit_note(note_id, title, message)
        elif choice == "4":
            note_id = int(input("Введите ID заметки для удаления: "))
            notes_manager.delete_note(note_id)
        elif choice == "5":
            break
        else:
            print("Неверная команда. Пожалуйста, выберите существующую команду.")


if __name__ == "__main__":
    main()
