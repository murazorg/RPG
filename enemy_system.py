import random


def random_enemy(person, difficulty):
    enemy_lvl = {'Гоблин': [1, 2], 'Орк': [2, 5], 'Огр': [7, 10], 'Циклоп': [9, 13],
                 'Малый энт': [1, 2], 'Гигантский паук': [2, 4], 'Сатир': [4, 8], 'Беорн': [8, 12], 'Большой энт': [10, 14]}
    pull = []
    match difficulty:
        case 'easy':
            for key, value in enemy_lvl.items():
                if (person.lvl >= value[0]) and (person.lvl <= value[1]):
                    pull.append(key)
            # print(pull)  # Для откладки пулла
            return random.choice(pull)
        case 'normal':
            for key, value in enemy_lvl.items():
                if (person.lvl >= (value[0] - 1)) and (person.lvl <= (value[1] - 1)):
                    pull.append(key)
            # print(pull)  # Для откладки пулла
            return random.choice(pull)
        case 'hard':
            for key, value in enemy_lvl.items():
                if (person.lvl >= (value[0] - 2)) and (person.lvl <= (value[1] - 2)):
                    pull.append(key)
            # print(pull)  # Для откладки пулла
            return random.choice(pull)
