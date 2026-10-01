from src.utils import DBManager
from src.utils import creat_tables
from src.utils import greet_function


if __name__ == '__main__':

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
    st_planes = DBManager.get_countries_and_aeroplanes_count()
    print(st_planes)
    input('Нажмите ввод')
    print("Реализовано получение перечня воздушных судов в базе данных:")
    planes = DBManager.get_all_aeroplanes()
    print(planes)
    input('Нажмите ввод')
    print("Реализовано получение значения скорости воздушных судов в м/с:")
    avg_speed = DBManager.get_avg_speed()
    print(avg_speed)
    input('Нажмите ввод')
    print("Реализовано получение перечня воздушных судов скорость которых больше средней:")
    sup_avgspeed = DBManager.get_aeroplanes_with_higher_speed()
    print(sup_avgspeed)
    input('Нажмите ввод')
    print("Реализовано получение перечня воздушных судов с выбраным пользователем сочетании букв в позывном:")
    key = input('Введите необходимое сочетание символов латинскими буквами: ')
    key.upper()
    set = key.isalpha()
    if set == True:
        answer = DBManager.get_aeroplanes_with_keyword(key)
        print(answer)
    else:
        print("Вы ввели не символы")
