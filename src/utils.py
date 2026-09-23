


def filter_state(air_boards: list[object], name_state: str) -> list:
    '''
    Фуекция фильтрации самолетов по стране регистрации
    :param air_boards: список объектов Airplane
    :param name_state: выбранная пользователем страна регистрации для фильтрации
    :return: список бортов зарегистрированных в стране выбранной пользователем
    '''
    state_key = name_state
    plane_state = (x for x in air_boards if x.state == state_key)
    return list(plane_state)