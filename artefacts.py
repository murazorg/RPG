from tabulate import tabulate


class Artefact:
    artefacts = {'Гномий щит': ['Левая рука', False, False, None],
                 'Кулон смерти': ['Шея', False, False, None],
                 'Кулон жизни': ['Шея', False, False, None],
                 'Магический жезл': ['Правая рука', False, False, None],
                 'Кистень иглоспина': ['Правая рука', False, False, None],
                 # 'Шлем Хаоса': ['Голова', False, False, None],
                 # 'Сандали святого': ['Ноги', False, False, None],
                 'Рёбра кентавра': ['Торс', False, False, None],
                 'Шкура зверя': ['Накидка', False, False, None],
                 # 'Кольцо жизненной силы': ['Кольцо', False, False, None],
                 'Зеркальное копьё': ['Левая рука', False, False, None],
                 # 'Тиара душ': ['Голова', False, False, None],
                 'Резец гоблина': ['Карман', False, False, None],
                 'Капюшон расторопного вора': ['Голова', False, False, None],
                 'Дубина огра': ['Правая рука', False, False, None],
                 'Папаха победителя': ['Голова', False, False, None],
                 'Вороний глиф': ['Карман', False, False, None]
                 }  # Слот, Подобран, Одет, ID
    artefact_skill = {}
    count = 0

    def get_artefact(self, name):
        self.artefacts[name][1] = True
        self.count += 1
        self.artefacts[name][3] = self.count
        print('Предмет {0} подобран в рюкзак'.format(name))

    def wear(self, id, person):
        for key, value in self.artefacts.items():
            if value[3] == id and value[2]:  # Он одет
                value[2] = False  # Снимаем
                print('Предмет {0} убран в рюкзак'.format(key))
                self.effect_off(key, person)  # Убираем эффекты
                return True
            elif value[3] == id and (value[2] is False):  # Он не одет
                for k, v in self.artefacts.items():
                    if v[0] == value[0] and v[2]:  # Если такой же слот уже занят
                        print("Слот занят")
                        return True
                value[2] = True  # Одеваем
                print('Предмет {0} экипирован'.format(key))
                self.effect_on(key, person)  # Добавляем эффекты
                return True
        else:
            print('Такого предмета нет!')
            return True

    def print_artefact_skill(self):
        for k, v in self.artefact_skill.items():
            if v[0]:
                for key, value in self.artefacts.items():
                    if v[1] == value[3]:
                        print(v[1], key)
        return input()

    def enter_artefact_skill(self, input, person):
        for k, v in self.artefact_skill.items():
            if int(input) == v[1]:
                match k:
                    case 'Мираж':
                        print('Вы мерцнули копьём и создали иллюзию-двойника')
                        person.effects['Мираж'] = True
                        self.artefact_skill[k][0] = False
                        return True
                    case 'Жертва':
                        print('Камень в центре тиары зловеще загорелся и поглотил ваши жизненные силы')
                        person.mp += 50
                        person.hp -= 100
                        self.artefact_skill[k][0] = False
                        return True
                    case 'Трансформация':
                        print('Прочитав надпись на глифе, вы превратились в большого ворона и, уклоняясь от атак, взмыли в небо')
                        person.effects['Трансформация'] = 3
                        self.artefact_skill[k][0] = False
                        return True
        print('Неверный ввод')
        return False

    def update(self):
        for k, v in self.artefact_skill.items():
            v[0] = True

    def effect_on(self, name, person):
        match name:
            case 'Гномий щит':
                person.armor += 4
            case 'Кулон смерти':
                person.effects['Кулон смерти'] = True
            case 'Кулон жизни':
                person.max_hp += 45
                person.restoration()
            case 'Магический жезл':
                person.change_attribute('intellect', 5)
                person.amp_mag_dmg += 5
                person.restoration()
            case 'Кистень иглоспина':
                person.change_attribute('strength', 4)
                person.dmg += 5
                person.restoration()
            case 'Шлем Хаоса':
                person.armor += 3
                person.change_attribute('intellect', 3)
                person.amp_mag_dmg += 6
                person.restoration()
            case 'Сандали святого':
                person.change_attribute('strength', 7)
                person.change_attribute('agility', 7)
                person.change_attribute('intellect', 7)
                person.restoration()
            case 'Рёбра кентавра':
                person.armor += 2
                person.change_attribute('strength', 2)
                person.restoration()
            case 'Шкура зверя':
                person.mag_resist += 0.1
                person.armor += 3
            case 'Кольцо жизненной силы':
                person.effects['Кольцо жизненной силы'] = True
                person.change_attribute('strength', 5)
                person.restoration()
            case 'Зеркальное копьё':
                self.artefact_skill['Мираж'] = [True, self.artefacts['Зеркальное копьё'][3]]
                person.change_attribute('agility', 22)
                person.restoration()
            case 'Тиара душ':
                self.artefact_skill['Жертва'] = [True, self.artefacts['Тиара душ'][3]]
            case 'Резец гоблина':
                person.dmg += 3
            case 'Капюшон расторопного вора':
                person.change_attribute('agility', 2)
                person.dmg += 4
                person.restoration()
            case 'Дубина огра':
                person.dmg += 16
            case 'Папаха победителя':
                person.change_attribute('strength', 10)
                person.restoration()
            case 'Вороний глиф':
                self.artefact_skill['Трансформация'] = [True, self.artefacts['Вороний глиф'][3]]

    def effect_off(self, name, person):
        match name:
            case 'Гномий щит':
                person.armor -= 4
            case 'Кулон смерти':
                del person.effects['Кулон смерти']
            case 'Кулон жизни':
                person.max_hp -= 45
                person.restoration()
            case 'Магический жезл':
                person.change_attribute('intellect', -5)
                person.amp_mag_dmg -= 5
                person.restoration()
            case 'Кистень иглоспина':
                person.change_attribute('strength', -4)
                person.dmg -= 5
                person.restoration()
            case 'Шлем Хаоса':
                person.armor -= 3
                person.change_attribute('intellect', -3)
                person.amp_mag_dmg -= 6
                person.restoration()
            case 'Сандали святого':
                person.change_attribute('strength', -7)
                person.change_attribute('agility', -7)
                person.change_attribute('intellect', -7)
                person.restoration()
            case 'Рёбра кентавра':
                person.armor -= 2
                person.change_attribute('strength', -2)
                person.restoration()
            case 'Шкура зверя':
                person.mag_resist -= 0.1
                person.armor -= 3
            case 'Кольцо жизненной силы':
                del person.effects['Кольцо жизненной силы']
                person.change_attribute('strength', -5)
                person.restoration()
            case 'Зеркальное копьё':
                del self.artefact_skill['Мираж']
                person.change_attribute('agility', -22)
                person.restoration()
            case 'Тиара душ':
                del self.artefact_skill['Жертва']
            case 'Резец гоблина':
                person.dmg -= 3
            case 'Капюшон расторопного вора':
                person.change_attribute('agility', -2)
                person.dmg -= 4
                person.restoration()
            case 'Дубина огра':
                person.dmg -= 16
            case 'Папаха победителя':
                person.change_attribute('strength', -10)
                person.restoration()
            case 'Вороний глиф':
                del self.artefact_skill['Трансформация']

    def not_equipment(self):
        table = []
        for key, value in self.artefacts.items():
            if value[1] and (value[2] is False):
                table.append(value[3])
                table.append(':')
                table.append(key)
                table.append(':')
                table.append(value[0])
                table.append('    ')
        if table:
            return table
        else:
            return "Рюкзак пуст"

    def equipment(self):
        table_A = [None, None, None]
        table_B = [None, None, None]
        table_C = [None, None, None]
        table_D = [None, None, None]
        table = [table_A, table_B, table_C, table_D]
        for key, value in self.artefacts.items():
            if value[1] and value[2]:
                match value[0]:
                    case 'Голова':
                        table_A[1] = '{0}.{1}'.format(value[3], key)
                    case 'Кольцо':
                        table_B[0] = '{0}.{1}'.format(value[3], key)
                    case 'Шея':
                        table_B[1] = '{0}.{1}'.format(value[3], key)
                    case 'Перчатка':
                        table_B[2] = '{0}.{1}'.format(value[3], key)
                    case 'Правая рука':
                        table_C[0] = '{0}.{1}'.format(value[3], key)
                    case 'Торс':
                        table_C[1] = '{0}.{1}'.format(value[3], key)
                    case 'Левая рука':
                        table_C[2] = '{0}.{1}'.format(value[3], key)
                    case 'Карман':
                        table_D[0] = '{0}.{1}'.format(value[3], key)
                    case 'Ноги':
                        table_D[1] = '{0}.{1}'.format(value[3], key)
                    case 'Накидка':
                        table_D[2] = '{0}.{1}'.format(value[3], key)
        if table:
            return print(tabulate(table, tablefmt="simple_grid", missingval=''))
        else:
            return "Ничего не экипировано"
