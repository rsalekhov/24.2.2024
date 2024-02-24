from pprint import pprint
import csv
import re

# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Пройдемся по списку и обработаем каждый контакт
for i, contact in enumerate(contacts_list[1:], start=1):  # Используем enumerate для получения нумерации, начинающейся с 1
    # Шаг 1: Записываем Имя, Фамилию, Отчество в соответствующие столбцы
    parts = contact[0].split()
    if len(parts) >= 3:
        contact[:3] = parts[:3]
    elif len(parts) == 2:
        contact[:3] = parts + [""]  # Если нет отчества, добавляем пустую строку

merged_contacts = {}
original_phones_list = []  # Создаем список для сохранения оригинальных номеров телефонов

for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    if key not in merged_contacts:
        merged_contacts[key] = contact[2:]  # Создаем новую запись
    else:
        # Обновляем значения, оставляя только уникальные элементы в столбцах "surname" и "organization"
        merged_contacts[key] = [
            x[0] if isinstance(x[0], str) and x[0] else x[1] for x in zip(merged_contacts[key], contact[2:])
        ]

    # Сохраняем оригинальные номера телефонов
    original_phones = contact[6]  # Номера телефонов теперь находятся в столбце с индексом 6
    if original_phones:
        original_phones_list.extend(original_phones.split(", "))

# Создаем новый список с объединенными контактами
merged_contacts_list = [[str(i)] + list(key) + merged_contacts[key] for i, key in enumerate(merged_contacts, start=1)]

# Вставляем заголовок
merged_contacts_list.insert(0, ["", "lastname", "firstname", "surname", "organization", "position", "phone", "email"])

# Выводим оригинальные номера телефонов
print("Original Phones (Before):")
for original_phone in original_phones_list:
    print(original_phone)

for contact in merged_contacts_list[1:]:
    phones = re.findall(r"(\+7|8)?\s*\(*(\d{3})\)*[\s\(\)\-]*\s*(\d{2,3})[\s\(\)\-]*(\d{2})[\s\(\)\-]*(\d{2})\s*(?:\(*доб\.\s?(\d+)\)?)?", contact[6])
    formatted_phones = []
    for phone in phones:
        country_code = "+7" if phone[0] and phone[0] != " 8" else ""  # Определение кода страны

        extension = f" доб.{phone[5]}" if phone[5] else ""  # Формирование добавочного номера, если он есть
        formatted_phone = f"{country_code}({phone[1]}){phone[2]}-{phone[3]}-{phone[4]}{extension}"
        formatted_phones.append(formatted_phone)

    # Обновляем контакт с отформатированными номерами телефонов
    contact[6] = ", ".join(formatted_phones)

# Выводим оригинальные номера телефонов после изменений
print("\nOriginal Phones (After):")
for original_phone in original_phones_list:
    print(original_phone)

# Выводим получившиеся данные для проверки
pprint(merged_contacts_list)

# TODO 2: Сохраняем получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(merged_contacts_list)
