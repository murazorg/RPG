class Artefact():
    artefacts = {'Гномий щит': ['Левая рука', False, False, None], 'Кулон смерти': ['Шея', False, False, None],
                 'Кулон жизни': ['Шея', False, False, None]}
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

    def effect_on(self, name, person):
        match name:
            case 'Гномий щит':
                person.armor += 4
            case 'Кулон смерти':
                person.effects['Кулон смерти'] = True
            case 'Кулон жизни':
                person.max_hp += 75
                person.restoration()

    def effect_off(self, name, person):
        match name:
            case 'Гномий щит':
                person.armor -= 4
            case 'Кулон смерти':
                del person.effects['Кулон смерти']
            case 'Кулон жизни':
                person.max_hp -= 75
                person.restoration()

    def not_equipment(self):
        a = []
        for key, value in self.artefacts.items():
            if value[1] and (value[2] is False):
                a.append(value[3])
                a.append(':')
                a.append(key)
                a.append(':')
                a.append(value[0])
                a.append(' ')
        if a:
            return a
        else:
            return "Рюкзак пуст"

    def equipment(self):
        a = []
        for key, value in self.artefacts.items():
            if value[1] and value[2]:
                a.append(value[3])
                a.append(':')
                a.append(key)
                a.append(':')
                a.append(value[0])
                a.append(' ')
        if a:
            return a
        else:
            return "Ничего не экипировано"

