from src.work import DBManager
from src.utils import creat_tables
from src.utils import greet_function


if __name__ == '__main__':
    qwestion = DBManager()
    creat_tables()
    countries = [
        "Germany",
        "France",
        "Poland",
        "Norway"
    ]
    greet_function(countries)
    print("Здравствуйте. Вам представляется программа работы с базами данных.")
    print("В ней реализована отражение положения воздушных судов (самолетов) над странами европы.")
    print("В данном случае над Германией, Францией, Польшей и Норвегией")
    print("Выдор стран пользователем пока не реализован.")
    print("Реализовано получение название страны и количество воздушных судов в ее воздушном пространстве:")
    state = qwestion.get_all_aeroplanes()
    print(state)
    #print(qwestion.get_all_aeroplanes())
    input('Нажмите ввод')
    print("Реализовано получение перечня воздушных судов в базе данных:")
    print(qwestion.get_all_aeroplanes())
    input('Нажмите ввод')
    print("Реализовано получение значения скорости воздушных судов в м/с:")
    print(qwestion.get_avg_speed())
    input('Нажмите ввод')
    print("Реализовано получение перечня воздушных судов скорость которых больше средней:")
    print(qwestion.get_aeroplanes_with_higher_speed())
    input('Нажмите ввод')
    print("Реализовано получение перечня воздушных судов с выбраным пользователем сочетании букв в позывном:")
    key = input('Введите необходимое сочетание символов латинскими буквами')
    key.upper()
    set = key.isalpha()
    if set:
        print(qwestion.get_aeroplanes_with_keyword(key))
    else:
        print("Вы ввели не символы")
