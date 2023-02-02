class Artefact():
    artefacts = {'Гномий щит': ['Левая рука', False, False, None], 'Aboba': ['Левая рука', False, False, None]}
    count = 0

    def get_artefact(self, name):
        self.artefacts[name][1] = True
        self.count += 1
        self.artefacts[name][3] = self.count
        print('Предмет {0} подобран в рюкзак'.format(name))

    def wear(self, id):
        for key, value, in self.artefacts.items():
            if value[3] == id:
                if value[2]:
                    value[2] = False
                    print('Предмет {0} убран в рюкзак'.format(key))
                    return True
                else:
                    value[2] = True
                    print('Предмет {0} экипирован'.format(key))
                    self.effects(key)
                    return True
        else:
            print('Такого предмета нет!')

    def effects(self, name):
        match name:
            case 'Гномий щит':
                pass

    def not_equipment(self):
        a = []
        for key, value in self.artefacts.items():
            if value[1] and (value[2] is False):
                a.append(value[3])
                a.append(':')
                a.append(key)
                a.append('  ')
        if a:
            return a
        else:
            return "[Рюкзак пуст]"

    def equipment(self):
        a = []
        for key, value in self.artefacts.items():
            if value[1] and value[2]:
                a.append(value[3])
                a.append(':')
                a.append(key)
                a.append('  ')
        if a:
            return a
        else:
            return "[Ничего не экипировано]"

