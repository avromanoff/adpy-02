from pprint import pprint
import re
import csv


def get_raw_list():
    # читаем адресную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        # pprint(contacts_list)
        print('открыли файл, получили сырой список')
    return contacts_list


def get_correct_name_list():
    correct_name_list = []
    for row in get_raw_list():
        full_name = row[0] + ' ' + row[1] + ' ' + row[2]  # Получили ФИО
        full_name = full_name.strip()  # убрали пробелы в начале и в конце
        full_name = re.sub(r'( \s)+', ' ', full_name)  # убрали лишние пробелы между словами
        new_full_name = full_name.split()  # разбили на Ф, И, О
        new_lastname = new_full_name[0]
        new_fistname = new_full_name[1]
        if len(new_full_name) == 3:
            new_surname = new_full_name[2]
        else:
            new_surname = ''
        new_row = [new_lastname, new_fistname, new_surname] + row[3:]  # Ф И О на месте
        correct_name_list.append(new_row)
    print('получили список (correct_name_list) с правильными ФИО')
    return correct_name_list


def get_correct_phone_list():
    correct_phone_list = []
    for name_row in get_correct_name_list():
        pattern = r"(\+7|8)(\s?)\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d*)[\s-]?\(?([д][\D]*)?(\d*)\)?"
        subst = r"+7(\3)\4-\5-\6 доб.\8"
        new_phone = ''
        if name_row[5] != '':
            new_phone = re.sub(pattern, subst, str(name_row[5]))
            if new_phone[-1] == '.':
                new_phone = new_phone.replace(' доб.', '')
        name_row[5] = new_phone
        correct_phone_list.append(name_row)
    print('получили список (correct_phone_list) с правильными ФИО и телефонами')
    # получили список (correct_phone_list) с правильными ФИО и телефонами
    return correct_phone_list


def no_double_list():
    correct_phone_list = get_correct_phone_list()
    no_double_dict = {}
    for row in correct_phone_list:
        key_name = row[0] + row[1]
        no_double_dict[key_name] = row
    print('получили словарь (no_double_dict), ключи -- уникальные ФИ')
    # получили словарь (no_double_dict), ключи -- уникальные ФИ, значения -- какие-то строки
    # дальше нужно объединить значения из неуникальных строк
    long_list = []
    for long_key in no_double_dict:
        for row in correct_phone_list:
            list_key = row[0] + row[1]
            if long_key == list_key:
                dict_row = no_double_dict.get(long_key)
                len_row = len(row)
                for i in range(0, len_row):
                    if row[i] != dict_row[i]:
                        dict_row[i] = dict_row[i] + row[i]  # дописываем то, чего нет
                long_list.append(dict_row)
    # получили список (long_list) с полными значениями в строках
    for row in long_list:
        if long_list.count(row) != 1:
            long_list.remove(row)
    # удалили дубликаты
    return long_list


def get_my_phonebook():
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(no_double_list())


if __name__ == '__main__':
    get_my_phonebook()

