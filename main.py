from time import sleep
from random import randint
from artefacts import Artefact
from enemy_system import random_enemy
from tabulate import tabulate


class Character:
    def __init__(self):
        print('Введите имя для своего персонажа')
        self.name = input()
        self.strength = 0
        self.agility = 0
        self.intellect = 0
        self.hp = 120
        self.max_hp = 120
        self.shield = 0
        self.dmg = 20
        self.mp = 50
        self.max_mp = 50
        self.amp_mag_dmg = 0
        self.armor = 2
        self.mag_resist = 0.1
        self.lvl = 1
        self.points = 0
        self.exp = 0
        self.name_list = [False, False, False, False, False, False, False, False, False, False,
                          False, False, False, False, False, False, False,
                          False, False, False, False, False, False, False]
        self.effects = {}
        self.duration = [False, False, False, False, False, False, False, False, False, False,
                         False, False, False, False, False, False, False,
                         False, False, False, False, False, False, False]
        self.advice = 1

    def menu(self):
        a = False
        print('')
        print('МЕНЮ')
        print('Информация о персонаже:       1')
        print('Отправиться в путь:           2')
        print('Пойти в колизей:              3')
        print('Отдохнуть:                    4')
        if self.points > 0:
            a = True
            print('Поднять уровень:              5')
        choose = input()
        match choose:
            case '1':
                self.info()
            case '2':
                print('Минимальный рекомендуемый уровень: {0}. Желаете отправиться в путь?'.format(self.advice))
                print('Да:                           1')
                print('Нет:                          0')
                if input() == '1':
                    return True
                else:
                    self.menu()
            case '3':
                self.arena()
                self.menu()
            case '4':
                self.chill()
            case '5':
                if a:
                    self.lvl_up()
                else:
                    self.menu()
            case _:
                print('Неопознанная команда, возвращение в меню...')
                sleep(1)
                self.menu()

    def print_skills(self):
        a = []
        for item in reversed(self.name_list[0:3]):
            if item:
                a.append(item)
                break
        for item in reversed(self.name_list[3:6]):
            if item:
                a.append(item)
                break
        for item in reversed(self.name_list[6:9]):
            if item:
                a.append(item)
                break
        if self.name_list[9]:
            a.append(self.name_list[9])
        for item in reversed(self.name_list[10:13]):
            if item:
                a.append(item)
                break
        for item in reversed(self.name_list[13:16]):
            if item:
                a.append(item)
                break
        if self.name_list[16]:
            a.append(self.name_list[16])
        for item in reversed(self.name_list[17:20]):
            if item:
                a.append(item)
                break
        for item in reversed(self.name_list[20:23]):
            if item:
                a.append(item)
                break
        if self.name_list[23]:
            a.append(self.name_list[23])
        return a

    def print_effects(self):
        a = []
        for keys in self.effects:
            if self.effects.get(keys):
                a.append(keys)
        return a

    def info(self):
        print('')
        table_1 = ['Имя', self.name, 'Уровень', self.lvl, 'Очки', self.points]
        table_2 = ['Сила', self.strength, 'Здоровье', self.hp, 'Сопр.магии', '{0}%'.format(round((self.mag_resist * 100), 1)) ]
        table_3 = ['Ловкость', self.agility, 'Урон', self.dmg, 'Броня', round(self.armor, 1)]
        table_4 = ['Интеллект', self.intellect, 'Мана', self.mp, 'Колдовство', '{0}%'.format(self.amp_mag_dmg)]
        table_all = [table_1, table_2, table_3, table_4]
        print(tabulate(table_all, tablefmt="simple_grid"))
        print('Умения:           ', self.print_skills())
        print('Рюкзак:            [', *art.not_equipment(), ']', sep='')
        print('Экипировано:')
        art.equipment()
        print('Экипировать/снять: 1')
        # print('LOGO:              2')
        print('Назад:             0')
        choose = input()
        match choose:
            case '1':
                print('\nВведите номер предмета, который хотите экипировать...')
                id = input()
                art.wear(int(id), person)
                self.info()
            # case '2':
            #     print(art.artefacts)
            #     self.info()
            case '0':
                self.menu()
            case _:
                print('Неопознанная команда, возвращение в меню...')
                sleep(1)
                self.menu()

    def battle_info(self):
        print('')
        print(self.name)
        table_1 = ['Здоровье', self.hp, 'Сопр.магии', '{0}%'.format(round((self.mag_resist * 100), 1))]
        table_2 = ['Урон', self.dmg, 'Броня', '{0}({1}%)'.format(round(self.armor, 1), format(round(self.armor_impact() * 100)))]
        table_3 = ['Мана', self.mp, 'Щит', self.shield]
        table_all = [table_1, table_2, table_3]
        print(tabulate(table_all, tablefmt="simple_grid"))
        print('Активные эффекты:', self.print_effects(), '\n')

    def armor_impact(self):
        damage_reduction = ((0.05 * self.armor) / (1 + 0.05 * self.armor))
        # print('Physical damage reduction: ', damage_reduction, '%', sep='')  #- Для проверки формулы брони в бою
        return round(damage_reduction, 2)

    def change_attribute(self, attribute_name, value):
        match attribute_name:
            case 'strength':
                self.strength += value
                self.max_hp += 10 * value
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
                self.mag_resist += round((0.001 * value), 3)
            case 'agility':
                self.agility += value
                self.dmg += 1 * value
                self.armor += 0.2 * value
            case 'intellect':
                self.intellect += value
                self.max_mp += 5 * value
                if self.mp > self.max_mp:
                    self.mp = self.max_mp
                self.amp_mag_dmg += 0.25 * value

    def restoration(self):
        art.update()
        self.hp = self.max_hp
        self.mp = self.max_mp

    def heal(self, value):
        if self.hp < self.max_hp:
            heal = value * (1 + (self.amp_mag_dmg / 100))
            self.hp += round(heal)
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            return heal
        return 0

    def chill(self):
        if self.hp == self.max_hp and self.mp == self.max_mp:
            print('\nВы чувствуете себя хорошо')
            self.menu()
        else:
            print('Вы решили немного покимарить', end='')
            for i in range(5):
                i += 1
                sleep(1)
                print('.', end='')
            self.restoration()
            print('\nВы проснулись и чувствуете что хорошо отдохнули')
            self.menu()

    def give_exp(self, value):
        self.exp += value
        exp_for_lvl = round(((self.lvl + 1) * 100) * (0.4 + (0.1 * self.lvl)))
        if self.exp >= exp_for_lvl:
            self.points += 1
            self.exp -= exp_for_lvl

    def arena(self):
        print('Вы пошли в местный колизей')
        input()
        print('Здешний распорядитель предложил вам два варианта:\n'
              '1. Выйти первым номером и развеселить публику, став звездой этого дня\n'
              '2. Выйти вторым номером и заполнить пустое время\n'
              'Что выберете вы?')
        choice = input()
        match choice:
            case '1':
                print('Дождавшись своего часа, вы вышли на арену. На противоположной стороне вас поджидал')
                x = random_enemy(self, 'normal')
                enemy = Enemy(x)
                if battle(enemy, True) is False: return False
                print('Прикончив первого соперника, под возгласы публики, на арену вышел второй')
                x = random_enemy(self, 'normal')
                enemy = Enemy(x)
                if battle(enemy, True) is False: return False
                print('Когда вы расправились со вторым, арена задрожала от множества криков. \n'
                      'Но было рано придаваться славе, перед вами был выпущен последний соперник')
                x = random_enemy(self, 'hard')
                enemy = Enemy(x)
                if battle(enemy, True) is False: return False
                print('Все зрители были в восторге, а вы, окончив грандиозное представление и взяв награду, ушли домой...')
                if art.artefacts['Папаха победителя'][1] is False:
                    art.get_artefact('Папаха победителя')
                return True
            case '2':
                print('Дождавшись своего часа, вы вышли на арену. На противоположной стороне вас поджидал')
                x = random_enemy(self, 'easy')
                enemy = Enemy(x)
                if battle(enemy, True) is False: return False
                print('Прикончив первого соперника, на арену вышел второй')
                x = random_enemy(self, 'easy')
                enemy = Enemy(x)
                if battle(enemy, True) is False: return False
                print('Когда вы расправились со вторым, перед вами был выпущен последний соперник')
                x = random_enemy(self, 'normal')
                enemy = Enemy(x)
                if battle(enemy, True) is False: return False
                print('Под аплодисменты зрителей вы, окончив эту схватку победой, ушли домой...')
                return True
            case _:
                print('Неопознанная команда, возвращение в колизей...')
                self.arena()



    def lvl_up(self):
        increase = 5
        print('Какой атрибут вы желаете увеличить на {0} единиц?'.format(increase))
        print('                              1    Силу')
        print('                              2    Ловкость')
        print('                              3    Интеллект')
        print('                              4    ИНФО')
        choose = input()
        match choose:
            case '1':
                self.change_attribute('strength', increase)
                print('Сила увеличена на {0}!'.format(increase))
                self.points -= 1
                self.lvl += 1
                self.restoration()
            case '2':
                self.change_attribute('agility', increase)
                print('Ловкость увеличена на {0}!'.format(increase))
                self.points -= 1
                self.lvl += 1
                self.restoration()
            case '3':
                self.change_attribute('intellect', increase)
                print('Интеллект увеличен на {0}!'.format(increase))
                self.points -= 1
                self.lvl += 1
                self.restoration()
            case '4':
                print('Cила увеличивает живучесть и устойчивость к магии')
                print('Ловкость оттачивает ваши атаки и смягчает получаемые удары')
                print('Интеллект увеличивает запас маны и силу заклинаний')
                print('\nВведите что-нибудь для продолжения...')
                input()
                self.lvl_up()
            case _:
                print('Неопознанная команда, возвращение в меню...')
                sleep(1)
                self.menu()
        self.change_attribute('strength', 1)
        self.change_attribute('agility', 1)
        self.change_attribute('intellect', 1)
        self.restoration()
        skill.new()
        self.menu()

    def take_attack(self, enemy, attack):
        if 'Гипоцентр' in enemy.effects:
            if randint(0, 100) <= 25:
                print('Противник промахнулся')
                return False
        if 'Мираж' in self.effects:
            if randint(0, 100) <= 30:
                print('Противник попал по иллюзии и та растворилась')
                del self.effects['Мираж']
                return False
        if 'Гнев орка' in enemy.effects:
            if randint(0, 100) <= 20:
                attack = attack * 1.5
                print(enemy.name, 'совершил критическую атаку!')
        if 'Ядовитые жвалы' in enemy.effects:
            if 'Яд гигантского паука' not in self.effects:
                self.effects['Яд гигантского паука'] = True
            else:
                print('Яд нанёс', self.take_mag_attack(10), 'урона')
        if 'Глубокие раны' in enemy.effects:
            if 'Глубокие раны' in person.effects:
                person.effects['Глубокие раны'] += 6
            else:
                person.effects['Глубокие раны'] = 6
            attack += person.effects['Глубокие раны']
        attack -= skill.inertial_damping(attack)  # Attack reduced block
        impact = attack - (attack * self.armor_impact())
        if 'Трансформация' in self.effects:
            impact *= 0.1
        if 'Демоническая кровь' in enemy.effects:
            if randint(0, 100) <= 20:
                enemy.hp += round(impact * 0.33)
                print(enemy.name, 'в ярости наполнил оружие демонической энергией и восстановил {0} здоровья!'.format(round(impact * 0.2)))
        self.hp -= round(impact)
        return round(impact)

    def take_mag_attack(self, mag_attack):
        if 'Мираж' in self.effects:
            if randint(0, 100) <= 30:
                print('Противник попал по иллюзии и та растворилась')
                del self.effects['Мираж']
                return False
        if self.shield > 0:
            dmg_on_shield = self.shield - mag_attack
            if dmg_on_shield <= 0:
                dmg_on_shield = self.shield
            mag_attack -= self.shield
            if mag_attack > 0:
                print('Магический щит поглотил {0} магического урона и разрушился'.format(dmg_on_shield))
            elif mag_attack <= 0:
                print('Магический щит поглотил {0} магического урона'.format(dmg_on_shield))
                mag_attack = 0
        impact = mag_attack - (mag_attack * self.mag_resist)
        if 'Трансформация' in self.effects:
            impact *= 0.1
        self.hp -= round(impact)
        return round(impact)

    def dispelling(self):
        if 'Мираж' in self.effects:
            if randint(0, 100) <= 30:
                print('Противник попал по иллюзии и та растворилась')
                del self.effects['Мираж']
                return False
        if 'Каменная кожа. 1ур' in self.effects:
            del self.effects['Каменная кожа. 1ур']
            person.armor -= 4
            self.duration[0][0] = 0
        if 'Каменная кожа. 2ур' in self.effects:
            del self.effects['Каменная кожа. 2ур']
            person.armor -= 8
            self.duration[1][0] = 0
        if 'Каменная кожа. 3ур' in self.effects:
            del self.effects['Каменная кожа. 3ур']
            person.armor -= 12
            self.duration[2][0] = 0
        if 'Водный щит. 1ур' in self.effects:
            del self.effects['Водный щит. 1ур']
            person.shield = 0
            self.duration[10][0] = 0
        if 'Водный щит. 2ур' in self.effects:
            del self.effects['Водный щит. 2ур']
            person.shield = 0
            self.duration[11][0] = 0
        if 'Водный щит. 3ур' in self.effects:
            del self.effects['Водный щит. 3ур']
            person.shield = 0
            self.duration[12][0] = 0
        if 'Трансформация' in self.effects:
            del self.effects['Трансформация']
        print('Вам развеяли положительные эффекты')


class Enemy:
    hp = 0
    dmg = 0
    mp = 0
    armor = 0
    mag_resist = 0
    effects = {}

    def __init__(self, name):
        self.name = name
        match self.name:
            case 'Гоблин':
                self.hp = 70
                self.dmg = 8
                self.mp = 0
                self.armor = 2
                self.mag_resist = 0.1
                self.effects = {}
                self.exp = 50
            case 'Орк':
                self.hp = 150
                self.dmg = 14
                self.mp = 0
                self.armor = 8
                self.mag_resist = 0.15
                self.effects = {'Гнев орка': True}
                self.exp = 120
            case 'Огр':
                self.hp = 200
                self.max_hp = 200
                self.dmg = 24
                self.mp = 80
                self.armor = 7
                self.mag_resist = 0.05
                self.effects = {'Регенерация': True}
                self.exp = 350
            case 'Циклоп':
                self.hp = 400
                self.dmg = 56
                self.mp = 0
                self.armor = 15
                self.mag_resist = 0.15
                self.effects = {'Ярость': False, 'Крепкая кожа': True}
                self.exp = 720
            case 'Урук-хай':
                self.hp = 500
                self.dmg = 65
                self.mp = 0
                self.armor = 16
                self.mag_resist = 0.15
                self.effects = {'Гнев орка': True, 'Демоническая кровь': True, 'Мираж': True}
                self.exp = 1000
            case 'Малый энт':
                self.hp = 90
                self.max_hp = 90
                self.dmg = 7
                self.mp = 0
                self.armor = 4
                self.mag_resist = 0.1
                self.effects = {'Малое заживление': True}
                self.exp = 60
            case 'Гигантский паук':
                self.hp = 110
                self.dmg = 8
                self.mp = 0
                self.armor = 4
                self.mag_resist = 0.1
                self.effects = {'Ядовитые жвалы': True}
                self.exp = 100
            case 'Сатир':
                self.hp = 190
                self.dmg = 12
                self.mp = 200
                self.armor = 6
                self.mag_resist = 0.25
                self.effects = {'Порождение магии': True, 'Ослепление': True,
                                'Восстановление': True, 'Движение маны': True}
                self.exp = 220
            case 'Беорн':
                self.hp = 330
                self.dmg = 20
                self.mp = 0
                self.armor = 12
                self.mag_resist = 0.1
                self.effects = {'Глубокие раны': True, 'Обновление': 3}
                self.exp = 500
            case 'Большой энт':
                self.hp = 500
                self.max_hp = 500
                self.dmg = 70
                self.mp = 120
                self.armor = 16
                self.mag_resist = 0.1
                self.effects = {'Большое заживление': True, 'Шипы': True, 'Цветение': True, 'Развеивание': True}
                self.exp = 800

    def enemy_move(self):
        match self.name:
            case 'Гоблин' | 'Орк' | 'Огр' | 'Циклоп' | 'Малый энт' | 'Гигантский паук' | 'Урук-хай':
                dmg = person.take_attack(self, self.dmg)
                if dmg: print('Вы получили {0} урона'.format(dmg))
                if 'Мираж' in self.effects:
                    dmg = person.take_attack(self, self.dmg)
                    if dmg: print('Второй Вожак атаковал и вы получили {0} урона'.format(dmg))
                return True
            case 'Сатир':
                if self.effects['Ослепление']:
                    person.effects['Ослепление'] = True
                    print('Вы ослеплены!')
                    self.effects['Ослепление'] = False
                    self.mp -= 30
                    return True
                if self.hp <= 80 and self.effects['Восстановление'] and self.mp >= 50:
                    self.hp += 100
                    self.mp -= 50
                    print('Сатир применил шаманскую магию и исцелил себя')
                    self.effects['Восстановление'] = False
                    return True
                if self.mp >= 20:
                    self.mp -= 20
                    if 'Воодушевление' not in person.effects:
                        if 'Движение маны' in person.effects:
                            person.effects['Движение маны'] += 2
                        else:
                            person.effects['Движение маны'] = 2
                        self.hp += person.take_mag_attack(person.effects['Движение маны'])
                        if person.mp > 0:
                            self.mp += person.effects['Движение маны']
                            person.mp -= person.effects['Движение маны']
                            if person.mp < 0:
                                person.mp = 0
                        print('Сатир расшатал внутренние потоки и выжег', person.effects['Движение маны'], 'здоровья и маны')
                        return True
                    else:
                        print('Папаха победителя защитила вас от колдунства')
                        return True
                dmg = person.take_attack(self, self.dmg)
                if dmg: print('Вы получили {0} урона'.format(dmg))
                return True
            case 'Беорн':
                if self.hp <= 300 and self.effects['Обновление'] == 3:
                    self.dispelling()
                    self.effects['Обновление'] -= 1
                if self.hp <= 200 and self.effects['Обновление'] == 2:
                    self.dispelling()
                    self.effects['Обновление'] -= 1
                if self.hp <= 100 and self.effects['Обновление'] == 1:
                    self.dispelling()
                    self.effects['Обновление'] -= 1
                dmg = person.take_attack(self, self.dmg)
                if dmg: print('Вы получили {0} урона'.format(dmg))
                return True
            case 'Большой энт':
                if ('Каменная кожа. 1ур' or 'Каменная кожа. 2ур' or 'Каменная кожа. 3ур' or 'Водный щит. 1ур' or
                        'Водный щит. 2ур' or 'Водный щит. 3ур' or 'Трансформация') in person.effects and self.mp >= 30:
                    self.mp -= 30
                    person.dispelling()
                    return True
                if self.mp >= 30 and randint(0, 100) <= 33:
                    self.mp -= 30
                    if 'Воодушевление' not in person.effects:
                        print(self.name, 'попытался внедрить в вас побег и нанёс {0} урона'.format(person.take_mag_attack(50)))
                        return True
                    else:
                        print('Папаха победителя защитила вас от колдунства')
                        return True
                else:
                    dmg = person.take_attack(self, self.dmg)
                    if dmg: print('Вы получили {0} урона'.format(dmg))
                    return True

    def dispelling(self):
        if 'Поджиг. 1ур' in self.effects:
            del self.effects['Поджиг. 1ур']
            person.duration[20][0] = 0
        if 'Поджиг. 2ур' in self.effects:
            del self.effects['Поджиг. 2ур']
            person.duration[21][0] = 0
        if 'Поджиг. 3ур' in self.effects:
            del self.effects['Поджиг. 3ур']
            person.duration[22][0] = 0
        print(self.name, 'развеял отрицательные эффекты')

    def print_effects(self):
        a = []
        for keys in self.effects:
            if self.effects.get(keys):
                a.append(keys)
        return a

    def battle_info(self):
        print(self.name)
        table_1 = ['Здоровье', self.hp, 'Сопр.магии', '{0}%'.format(round((self.mag_resist * 100), 1))]
        table_2 = ['Урон', self.dmg, 'Броня',
                   '{0}({1}%)'.format(round(self.armor, 1), format(round(self.armor_impact() * 100)))]
        table_3 = ['Мана', self.mp]
        table_all = [table_1, table_2, table_3]
        print(tabulate(table_all, tablefmt="simple_grid"))
        print('Активные эффекты:            ', self.print_effects())

    def armor_impact(self):
        damage_reduction = ((0.05 * self.armor) / (1 + 0.05 * self.armor))
        return round(damage_reduction, 2)

    def take_attack(self, attack):
        if 'Ослепление' in person.effects:
            if randint(0, 100) <= 25:
                print('Критический промах!')
                return False
        if 'Мираж' in self.effects:
            if randint(0, 100) <= 30:
                print('Ваша атака попала по иллюзии и развеяла её')
                del self.effects['Мираж']
                return False
        if 'Крепкая кожа' in self.effects:
            attack - 10
            print('Крепкая кожа выдержала часть урона')
        if 'Кулон смерти' in person.effects:
            if 'Кулон смерти' not in self.effects:
                self.effects['Кулон смерти'] = True
                self.armor -= 2
        if 'Шипы' in self.effects:
            dmg = person.take_attack(self, 10)
            if dmg:
                print('Шипы нанесли {0} урона'.format(dmg))
        skill.fusion(self)
        impact = attack - (attack * self.armor_impact())
        if 'Трансформация' in person.effects:
            impact *= 0.1
        self.hp -= round(impact)
        if self.hp > 0:
            if 'Ярость' in self.effects:
                if self.effects['Ярость'] is False:
                    if self.hp <= 160:
                        self.effects['Ярость'] = True
                        print(self.name, 'вошёл в состояние ярости')
                        self.mag_resist += 0.15
                        self.dmg += 10
        return round(impact)

    def take_mag_attack(self, mag_attack: int):
        if 'Мираж' in self.effects:
            if randint(0, 100) <= 30:
                print('Ваша атака попала по иллюзии и развеяла её')
                del self.effects['Мираж']
                return 0
        impact = (mag_attack * (1 + (person.amp_mag_dmg / 100))) * (1 - self.mag_resist)
        if 'Трансформация' in person.effects:
            impact *= 0.1
        self.hp -= round(impact)
        if self.hp > 0:
            if 'Ярость' in self.effects:
                if self.effects['Ярость'] is False:
                    if self.hp <= 160:
                        self.effects['Ярость'] = True
                        print(self.name, 'вошёл в состояние ярости')
                        self.mag_resist += 0.15
                        self.dmg += 10
        return round(impact)


class Skill:
    def __init__(self):
        self.time_list = \
            [
                [3, 6], [4, 6], [5, 6], [0, 1], [0, 1], [0, 1], [None], [None], [None], [3, 6],
                [7, 3], [7, 3], [7, 3], [None], [None], [None], [None],
                [None], [None], [None], [2, 5], [3, 5], [4, 5], [5, 5]
            ]
        self.cost = 0

    # type = []
    # earth_list = []
    # water_list = []
    # fire_list = []
    # wind_list = []
    # lightning_list = []
    # life_list = []
    # matter_list = []
    # ice_list = []
    # destruction_list = []
    # light_list = []
    # dark_list = []
    # pure_list = []

    def new(self):
        print('\nВыберете аспект:')
        false_count = person.name_list[0:10].count(False)
        if false_count > 0:
            print('1                 Аспект Земли')
        false_count = person.name_list[10:16].count(False)
        if false_count > 0 and person.name_list[9]:
            print('2                 Аспект Воды')
        false_count = person.name_list[17:24].count(False)
        if false_count > 0 and person.name_list[9]:
            print('3                 Аспект Огня')
        match input():
            case '1':
                print('\nВыберете способность для изучения:')
                false_count = person.name_list[0:3].count(False)
                match false_count:
                    case 3:
                        print('1 - Каменная кожа. 1ур')
                    case 2:
                        print('1 - Каменная кожа. 2ур')
                    case 1:
                        print('1 - Каменная кожа. 3ур')
                    case 0:
                        pass
                false_count = person.name_list[3:6].count(False)
                match false_count:
                    case 3:
                        print('2 - Земляные шипы. 1ур')
                    case 2:
                        print('2 - Земляные шипы. 2ур')
                    case 1:
                        print('2 - Земляные шипы. 3ур')
                    case 0:
                        pass
                false_count = person.name_list[6:9].count(False)
                match false_count:
                    case 3:
                        print('3 - Инерционное гашение*. 1ур')
                    case 2:
                        print('3 - Инерционное гашение*. 2ур')
                    case 1:
                        print('3 - Инерционное гашение*. 3ур')
                    case 0:
                        pass
                if (person.name_list[0:9].count(False) <= 6) and (person.name_list[9] is False):
                    print('4 - !Гипоцентр')
                print('5 - ИНФО')
                print('0 - Назад')
                self.choose_skill('earth')
            case '2':
                print('\nВыберете способность для изучения:')
                false_count = person.name_list[10:13].count(False)
                match false_count:
                    case 3:
                        print('1 - Водный щит. 1ур')
                    case 2:
                        print('1 - Водный щит. 2ур')
                    case 1:
                        print('1 - Водный щит. 3ур')
                    case 0:
                        pass
                false_count = person.name_list[13:16].count(False)
                match false_count:
                    case 3:
                        print('2 - Конденсат*. 1ур')
                    case 2:
                        print('2 - Конденсат*. 2ур')
                    case 1:
                        print('2 - Конденсат*. 3ур')
                    case 0:
                        pass
                if (person.name_list[10:16].count(False) <= 3) and (person.name_list[16] is False):
                    print('3 - !Морские змеи*')
                print('5 - ИНФО')
                print('0 - Назад')
                self.choose_skill('water')
            case '3':
                print('\nВыберете способность для изучения:')
                false_count = person.name_list[17:20].count(False)
                match false_count:
                    case 3:
                        print('1 - Плавление*. 1ур')
                    case 2:
                        print('1 - Плавление*. 2ур')
                    case 1:
                        print('1 - Плавление*. 3ур')
                    case 0:
                        pass
                false_count = person.name_list[20:23].count(False)
                match false_count:
                    case 3:
                        print('2 - Поджиг. 1ур')
                    case 2:
                        print('2 - Поджиг. 2ур')
                    case 1:
                        print('2 - Поджиг. 3ур')
                    case 0:
                        pass
                if (person.name_list[17:23].count(False) <= 3) and (person.name_list[23] is False):
                    print('3 - !Огненный Аркан')
                print('5 - ИНФО')
                print('0 - Назад')
                self.choose_skill('fire')

    def choose_skill(self, aspect):
        choice = input()
        match aspect:
            case 'earth':
                match choice:
                    case '1':
                        false_count = person.name_list[0:3].count(False)
                        match false_count:
                            case 3:
                                person.name_list[0] = 'Каменная кожа. 1ур'
                            case 2:
                                person.name_list[1] = 'Каменная кожа. 2ур'
                            case 1:
                                person.name_list[2] = 'Каменная кожа. 3ур'
                            case 0:
                                pass
                    case '2':
                        false_count = person.name_list[3:6].count(False)
                        match false_count:
                            case 3:
                                person.name_list[3] = 'Земляные шипы. 1ур'
                            case 2:
                                person.name_list[4] = 'Земляные шипы. 2ур'
                            case 1:
                                person.name_list[5] = 'Земляные шипы. 3ур'
                            case 0:
                                pass
                    case '3':
                        false_count = person.name_list[6:9].count(False)
                        match false_count:
                            case 3:
                                person.name_list[6] = 'Инерционное гашение. 1ур'
                            case 2:
                                person.name_list[7] = 'Инерционное гашение. 2ур'
                            case 1:
                                person.name_list[8] = 'Инерционное гашение. 3ур'
                            case 0:
                                pass
                    case '4':
                        false_count = person.name_list[9:10].count(False)
                        match false_count:
                            case 1:
                                person.name_list[9] = 'Гипоцентр'
                            case 0:
                                pass
                    case '5':
                        print('\nКаменная кожа - одно из самых известных заклинаний, покрывающее вашу плоть камнем. '
                              '\nПрекрасно подходит как для слабозащищенных магов, так и для крепких воинов')
                        print('\nЗемляные шипы - девиант философии данного аспекта. Создает шипы прямо под противником '
                              'и пронзает его ими. \nБыстропроизносимое и не требующее особого мастерства. '
                              'Несмотря на свою простоту может стать хорошим подспорьем в схватке')
                        print('\nИнерционное гашение - древнее зачарование, призванное поглотить вражеские удары '
                              'многослойными песчаными структурами. \nНе требует маны для поддержания и '
                              'существует до тех пор, пока жив сам зачарователь')
                        if person.name_list[2] or person.name_list[5] or person.name_list[8]:
                            print('\nГипоцентр - Один из сильнейших представителей аспекта, воплощающее суть Земли.\n'
                                  'Приводя в движение земные породы, вы буквально выбиваете землю из под ног противника'
                                  ', отчего они начинают промахиваться и терпят урон')
                        print('\nВведите что-нибудь для возврата...')
                        input()
                        self.new()
                    case '0':
                        self.new()
            case 'water':
                match choice:
                    case '1':
                        false_count = person.name_list[10:13].count(False)
                        match false_count:
                            case 3:
                                person.name_list[10] = 'Водный щит. 1ур'
                            case 2:
                                person.name_list[11] = 'Водный щит. 2ур'
                            case 1:
                                person.name_list[12] = 'Водный щит. 3ур'
                            case 0:
                                pass
                    case '2':
                        false_count = person.name_list[13:16].count(False)
                        match false_count:
                            case 3:
                                person.name_list[13] = 'Конденсат. 1ур'
                            case 2:
                                person.name_list[14] = 'Конденсат. 2ур'
                            case 1:
                                person.name_list[15] = 'Конденсат. 3ур'
                            case 0:
                                pass
                    case '3':
                        false_count = person.name_list[16:17].count(False)
                        match false_count:
                            case 1:
                                person.name_list[16] = 'Морские змеи'
                            case 0:
                                pass
                    case '5':
                        print('\nВодный щит - заклинание, которым изначально пользовались инструктора \n'
                              'на магических дуэлях, чтобы соперники не сожгли друг-друга. \n'
                              'Но на Шестой войне ему нашли другое применение')
                        print('\nКонденсат - техника обратных потоков маны в теле, позволяющая использовать \n'
                              'отработанную ману повторно. Освоившие эту технику считаются гениями')
                        if person.name_list[12] or person.name_list[15]:
                            print('\nМорские змеи - вершина искусства аспекта Воды, проявляющая полноту манипуляции \n'
                                  'в призыве ручного морского змея. Хоть они и не сильны, но обладают разумом и \n'
                                  'набросятся на вас как только вы потеряете должную концентрацию')
                        print('\nВведите что-нибудь для возврата...')
                        input()
                        self.new()
                    case '0':
                        self.new()
            case 'fire':
                match choice:
                    case '1':
                        false_count = person.name_list[17:20].count(False)
                        match false_count:
                            case 3:
                                person.name_list[17] = 'Плавление. 1ур'
                            case 2:
                                person.name_list[18] = 'Плавление. 2ур'
                            case 1:
                                person.name_list[19] = 'Плавление. 3ур'
                            case 0:
                                pass
                    case '2':
                        false_count = person.name_list[20:23].count(False)
                        match false_count:
                            case 3:
                                person.name_list[20] = 'Поджиг. 1ур'
                            case 2:
                                person.name_list[21] = 'Поджиг. 2ур'
                            case 1:
                                person.name_list[22] = 'Поджиг. 3ур'
                            case 0:
                                pass
                    case '3':
                        false_count = person.name_list[23:24].count(False)
                        match false_count:
                            case 1:
                                person.name_list[23] = 'Огненный Аркан'
                            case 0:
                                pass
                    case '5':
                        print('\nПлавление - наполняет оружие термальной энергией, отчего оно начинает \n'
                              'разрушать броню соперника с каждым последующим ударом. Говорят, именно с помощью этого\n'
                              'заклинания Парлакс и расплавил Великие Врата крепости Дымогор')
                        print('\nПоджиг - пламенная ярость охватывает того, кого вы коснетесь своим оружием. \n'
                              'Во времена Седьмой войны этим заклинанием неизвестный убийца сжег дотла Короля Земли')
                        if person.name_list[19] or person.name_list[22]:
                            print('\nОгненный Аркан - очень мощное и опасное заклинание, взывающее к\n'
                                  'древнему Духу Огня, питающимся жизненными силами противника \n'
                                  'Кодекс Магов запрещает применять это заклинания')
                        print('\nВведите что-нибудь для возврата...')
                        input()
                        self.new()
                    case '0':
                        self.new()

    def mana_check(self, id_skill):
        match id_skill:
            case 0:
                self.cost = 20
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 1:
                self.cost = 30
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 2:
                self.cost = 40
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 3:
                self.cost = 15
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 4:
                self.cost = 30
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 5:
                self.cost = 45
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 9:
                self.cost = 120
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 10:
                self.cost = 80
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 11:
                self.cost = 80
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 12:
                self.cost = 80
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 20:
                self.cost = 30
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 21:
                self.cost = 30
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 22:
                self.cost = 30
                if person.mp >= self.cost:
                    return True
                else:
                    return False
            case 23:
                self.cost = 90
                if person.mp >= self.cost:
                    return True
                else:
                    return False

    def stone_skin(self):
        false_count = person.name_list[0:3].count(False)
        match false_count:
            case 2:
                if self.mana_check(0):
                    person.mp -= self.cost
                    person.effects['Каменная кожа. 1ур'] = True
                    person.armor += 4
                    print('Вы покрыли себя камнем и затратили на это {0} маны'.format(self.cost))
                    return self.time_list[0]
                else:
                    print('Не получилось прочесть заклинание')
                    return False
            case 1:
                if self.mana_check(1):
                    person.mp -= self.cost
                    person.effects['Каменная кожа. 2ур'] = True
                    person.armor += 8
                    print('Вы покрыли себя камнем и затратили на это {0} маны'.format(self.cost))
                    return self.time_list[1]
                else:
                    print('Не получилось прочесть заклинание')
                    return False
            case 0:
                if self.mana_check(2):
                    person.mp -= self.cost
                    person.effects['Каменная кожа. 3ур'] = True
                    person.armor += 12
                    print('Вы покрыли себя камнем и затратили на это {0} маны'.format(self.cost))
                    return self.time_list[2]
                else:
                    print('Не получилось прочесть заклинание')
                    return False

    def earth_spike(self, enemy):
        false_count = person.name_list[3:6].count(False)
        match false_count:
            case 2:
                if self.mana_check(3):
                    person.mp -= self.cost
                    dmg = enemy.take_mag_attack(25)
                    print('Земляные пики разверзлись под противником и нанесли ему {1} урона. '
                          'Вы затратили на это {0} маны'.format(self.cost, dmg))
                    return self.time_list[3]
                else:
                    print('Не получилось прочесть заклинание')
                    return False
            case 1:
                if self.mana_check(4):
                    person.mp -= self.cost
                    dmg = enemy.take_mag_attack(40)
                    print('Земляные пики разверзлись под противником и нанесли ему {1} урона. '
                          'Вы затратили на это {0} маны'.format(self.cost, dmg))
                    return self.time_list[4]
                else:
                    print('Не получилось прочесть заклинание')
                    return False
            case 0:
                if self.mana_check(5):
                    person.mp -= self.cost
                    dmg = enemy.take_mag_attack(55)
                    print('Земляные пики разверзлись под противником и нанесли ему {1} урона. '
                          'Вы затратили на это {0} маны'.format(self.cost, dmg))
                    return self.time_list[5]
                else:
                    print('Не получилось прочесть заклинание')
                    return False

    def inertial_damping(self, attack):
        block = 0
        false_count = person.name_list[6:9].count(False)
        match false_count:
            case 2:
                if randint(0, 100) <= 30:
                    block = 8
                    print('Слои песка заблокировали {0} урона'.format(block))
            case 1:
                if randint(0, 100) <= 40:
                    block = 16
                    if attack > block:
                        print('Слои песка заблокировали {0} урона'.format(block))
                    else:
                        block = attack
                        print('Слои песка заблокировали все {0} урона'.format(block))
            case 0:
                if randint(0, 100) <= 50:
                    block = 24
                    if attack > block:
                        print('Слои песка заблокировали {0} урона'.format(block))
                    else:
                        block = attack
                        print('Слои песка заблокировали все {0} урона'.format(block))
        return block

    def gipocent(self, enemy):
        if person.name_list[9]:
            if self.mana_check(9):
                person.mp -= self.cost
                enemy.effects['Гипоцентр'] = True
                print('Земля вокруг задрожала и противник начал терять равновесие. '
                      'Вы затратили на это {0} маны'.format(self.cost))
                return self.time_list[9]
            else:
                print('Не получилось прочесть заклинание')
                return False

    def water_shield(self):
        false_count = person.name_list[10:13].count(False)
        match false_count:
            case 2:
                if self.mana_check(10):
                    person.mp -= self.cost
                    person.effects['Водный щит. 1ур'] = True
                    person.shield = 50 * (1 + person.amp_mag_dmg / 100)
                    print('Вы создали вокруг себя водную сферу и затратили на это {0} маны'.format(self.cost))
                    return self.time_list[10]
            case 1:
                if self.mana_check(11):
                    person.mp -= self.cost
                    person.effects['Водный щит. 2ур'] = True
                    person.shield = 100 * (1 + person.amp_mag_dmg / 100)
                    print('Вы создали вокруг себя водную сферу и затратили на это {0} маны'.format(self.cost))
                    return self.time_list[11]
            case 0:
                if self.mana_check(12):
                    person.mp -= self.cost
                    person.effects['Водный щит. 3ур'] = True
                    person.shield = 150 * (1 + person.amp_mag_dmg / 100)
                    print('Вы создали вокруг себя водную сферу и затратили на это {0} маны'.format(self.cost))
                    return self.time_list[12]

    def condensate(self):
        false_count = person.name_list[13:16].count(False)
        match false_count:
            case 2:
                if person.mp < person.max_mp:
                    condensate = person.max_mp * 0.05
                    if condensate > 100:
                        condensate = 100
                    person.mp += round(condensate)
                    if person.mp > person.max_mp:
                        person.mp = person.max_mp
                    print('Вы сконденсировали {0} маны'.format(round(condensate)))
            case 1:
                if person.mp < person.max_mp:
                    condensate = person.max_mp * 0.075
                    if condensate > 100:
                        condensate = 100
                    person.mp += round(condensate)
                    if person.mp > person.max_mp:
                        person.mp = person.max_mp
                    print('Вы сконденсировали {0} маны'.format(round(condensate)))
            case 0:
                if person.mp < person.max_mp:
                    condensate = person.max_mp * 0.1
                    if condensate > 100:
                        condensate = 100
                    person.mp += round(condensate)
                    if person.mp > person.max_mp:
                        person.mp = person.max_mp
                    print('Вы сконденсировали {0} маны'.format(round(condensate)))

    def sea_snakes(self, enemy):
        if person.name_list[16]:
            dmg = enemy.take_mag_attack(person.intellect * 0.5)
            enemy.mag_resist -= 0.01
            print('Морские змеи нанесли {0} урона. {1} стал чувствительнее к мане'.format(dmg, enemy.name))

    def fusion(self, enemy):
        false_count = person.name_list[17:20].count(False)
        match false_count:
            case 2:
                enemy.armor -= 0.5
            case 1:
                enemy.armor -= 1
            case 0:
                enemy.armor -= 1.5

    def burning(self, enemy):
        false_count = person.name_list[20:23].count(False)
        match false_count:
            case 2:
                if self.mana_check(20):
                    person.mp -= self.cost
                    print('Вы окутали своё оружие пламенной яростью и атаковали противника. '
                          'Вы затратили на это {0} маны'.format(self.cost))
                    print(enemy.name, 'получил', enemy.take_attack(person.dmg), 'урона')
                    enemy.effects['Поджиг. 1ур'] = True
                    return self.time_list[20]
            case 1:
                if self.mana_check(21):
                    person.mp -= self.cost
                    print('Вы окутали своё оружие пламенной яростью и атаковали противника. '
                          'Вы затратили на это {0} маны'.format(self.cost))
                    print(enemy.name, 'получил', enemy.take_attack(person.dmg), 'урона')
                    enemy.effects['Поджиг. 2ур'] = True
                    return self.time_list[21]
            case 0:
                if self.mana_check(22):
                    person.mp -= self.cost
                    print('Вы окутали своё оружие пламенной яростью и атаковали противника. '
                          'Вы затратили на это {0} маны'.format(self.cost))
                    print(enemy.name, 'получил', enemy.take_attack(person.dmg), 'урона')
                    enemy.effects['Поджиг. 3ур'] = True
                    return self.time_list[22]

    def fire_arcan(self, enemy):
        if self.mana_check(23):
            person.mp -= self.cost
            enemy.effects['Огненный Аркан'] = True
            print('Вы воззвали к древнему Духу Огня и {1}а пожрал живой огонь. '
                  'Дух забрал {0} маны'.format(self.cost, enemy.name))
            return self.time_list[23]

    def disspell(self, person, enemy, skill_id):
        match skill_id:
            case 0:
                del person.effects['Каменная кожа. 1ур']
                person.armor -= 4
            case 1:
                del person.effects['Каменная кожа. 2ур']
                person.armor -= 8
            case 2:
                del person.effects['Каменная кожа. 3ур']
                person.armor -= 12
            case 9:
                del enemy.effects['Гипоцентр']
            case 10:
                del person.effects['Водный щит. 1ур']
                person.shield = 0
            case 11:
                del person.effects['Водный щит. 2ур']
                person.shield = 0
            case 12:
                del person.effects['Водный щит. 3ур']
                person.shield = 0
            case 20:
                del enemy.effects['Поджиг. 1ур']
            case 21:
                del enemy.effects['Поджиг. 2ур']
            case 22:
                del enemy.effects['Поджиг. 3ур']
            case 23:
                del enemy.effects['Огненный Аркан']


def skill_id(skill_id):
    name = 'YOU ARE ABOBA'
    match skill_id:
        case 0 | 1 | 2:
            name = 'Каменная кожа'
        case 3 | 4 | 5:
            name = 'Земляные шипы'
        case 9:
            name = 'Гипоцентр'
        case 10 | 11 | 12:
            name = 'Водный щит'
        case 20 | 21 | 22:
            name = 'Поджиг'
        case 23:
            name = 'Огненный Аркан'
    return name


def check(timer, enemy):
    for i in timer:
        if i:
            i[0] -= 1
            i[1] -= 1
            if i[0] > 0:
                print('Оставшаяся длительность {0}: {1}'.format(skill_id(timer.index(i)), i[0]))
            elif i[0] == 0:
                print('Умение {0} перестало действовать'.format(skill_id(timer.index(i))))
                skill.disspell(person, enemy, timer.index(i))
            elif i[1] <= 0:
                print('Умение {0} снова доступно'.format(skill_id(timer.index(i))))
                index = timer.index(i)
                timer[index] = False
        continue


def skill_number():
    print('Выберите аспект:')
    if person.name_list[0:10].count(False) < len(person.name_list[0:10]):
        print('                              1  Аспект Земли')
    if person.name_list[10:13].count(False) < len(person.name_list[10:13]):
        print('                              2  Аспект Воды')
    if person.name_list[20:24].count(False) < len(person.name_list[20:24]):
        print('                              3  Аспект Огня')
    print('                              0  Назад')
    choice = input()
    match choice:
        case '1':
            for item in reversed(person.name_list[0:3]):
                if item:  # Скилл изучен
                    if person.duration[person.name_list.index(item)] is False:  # Его метод не применялся
                        if skill.mana_check(person.name_list.index(item)):
                            print('                              1    {0}'.format(item))
                        else:
                            print('Недостаточно маны!            1    {0}'.format(item))
                        break
            for item in reversed(person.name_list[3:6]):
                if item:
                    if person.duration[person.name_list.index(item)] is False:
                        if skill.mana_check(person.name_list.index(item)):
                            print('                              2    {0}'.format(item))
                        else:
                            print('Недостаточно маны!            2    {0}'.format(item))
                        break
            for item in reversed(person.name_list[9:10]):
                if item:
                    if person.duration[person.name_list.index(item)] is False:
                        if skill.mana_check(person.name_list.index(item)):
                            print('                              4    {0}'.format(item))
                        else:
                            print('Недостаточно маны!            4    {0}'.format(item))
                        break
            print('                              0    Назад')
            return 'earth'
        case '2':
            for item in reversed(person.name_list[10:13]):
                if item:
                    if person.duration[person.name_list.index(item)] is False:
                        if skill.mana_check(person.name_list.index(item)):
                            print('                              1    {0}'.format(item))
                        else:
                            print('Недостаточно маны!            1    {0}'.format(item))
                        break
            print('                              0    Назад')
            return 'water'
        case '3':
            for item in reversed(person.name_list[20:23]):
                if item:
                    if person.duration[person.name_list.index(item)] is False:
                        if skill.mana_check(person.name_list.index(item)):
                            print('                              2    {0}'.format(item))
                        else:
                            print('Недостаточно маны!            2    {0}'.format(item))
                        break
            for item in reversed(person.name_list[23:24]):
                if item:
                    if person.duration[person.name_list.index(item)] is False:
                        if skill.mana_check(person.name_list.index(item)):
                            print('                              3    {0}'.format(item))
                        else:
                            print('Недостаточно маны!            3    {0}'.format(item))
                        break
            print('                              0    Назад')
            return 'fire'
        case '0':
            return 'pass'


def select_skill(enemy):
    aspect = skill_number()
    if aspect == 'pass':
        return False
    choose = input()
    match aspect:
        case 'earth':
            match choose:
                case '1':
                    person_move = skill.stone_skin()
                    for item in reversed(person.name_list[0:3]):
                        if item:
                            person.duration[person.name_list.index(item)] = person_move
                            break
                    return True
                case '2':
                    person_move = skill.earth_spike(enemy)
                    for item in reversed(person.name_list[3:6]):
                        if item:
                            person.duration[person.name_list.index(item)] = person_move
                            break
                    return True
                case '4':
                    person_move = skill.gipocent(enemy)
                    person.duration[9] = person_move
                    return True
                case '0':
                    select_skill(enemy)
                case _:
                    select_skill(enemy)
        case 'water':
            match choose:
                case '1':
                    person_move = skill.water_shield()
                    for item in reversed(person.name_list[10:13]):
                        if item:
                            person.duration[person.name_list.index(item)] = person_move
                            break
                    return True
                case '0':
                    select_skill(enemy)
                case _:
                    select_skill(enemy)
        case 'fire':
            match choose:
                case '2':
                    person_move = skill.burning(enemy)
                    for item in reversed(person.name_list[20:23]):
                        if item:
                            person.duration[person.name_list.index(item)] = person_move
                            break
                    return True
                case '3':
                    person_move = skill.fire_arcan(enemy)
                    person.duration[23] = person_move
                    return True
                case '0':
                    select_skill(enemy)
                case _:
                    select_skill(enemy)


def enemy_effects(enemy):
    if 'Регенерация' in enemy.effects:
        percent = enemy.hp / enemy.max_hp
        if 0.9 <= percent < 1:
            enemy.hp += enemy.max_hp * 0.02
        if 0.7 <= percent < 0.9:
            enemy.hp += enemy.max_hp * 0.04
        if 0.5 <= percent < 0.7:
            enemy.hp += enemy.max_hp * 0.06
        if 0.3 <= percent < 0.5:
            enemy.hp += enemy.max_hp * 0.08
        if percent < 0.3:
            enemy.hp += enemy.max_hp * 0.1
        enemy.hp = round(enemy.hp)
        print(enemy.name, 'восстановил часть здоровья')
    if 'Малое заживление' in enemy.effects:
        if enemy.hp < enemy.max_hp:
            enemy.hp += 5
            print(enemy.name, 'восстановил часть здоровья')
    if 'Большое заживление' in enemy.effects:
        if enemy.hp < enemy.max_hp:
            enemy.hp += 12
            print(enemy.name, 'восстановил часть здоровья')


def debuff(enemy):
    if 'Огненный Аркан' in enemy.effects:
        dmg = enemy.take_mag_attack(enemy.hp * 0.1)
        print('Огненный Дух нанес {0} урона'.format(dmg))
    if 'Гипоцентр' in enemy.effects:
        dmg = enemy.take_mag_attack(50)
        print('Гипоцентр нанёс {0} урона'.format(dmg))
    if 'Поджиг. 1ур' in enemy.effects:
        dmg = enemy.take_mag_attack(person.agility * 0.25)
        print('Поджиг нанёс {0} урона'.format(dmg))
    if 'Поджиг. 2ур' in enemy.effects:
        dmg = enemy.take_mag_attack(person.agility * 0.5)
        print('Поджиг нанёс {0} урона'.format(dmg))
    if 'Поджиг. 3ур' in enemy.effects:
        dmg = enemy.take_mag_attack(person.agility * 0.75)
        print('Поджиг нанёс {0} урона'.format(dmg))


def person_effects(enemy):
    if 'Кольцо жизненной силы' in person.effects:
        print('Кольцо жизненной силы восстановило', round(person.heal(5)), 'здоровья')
    skill.condensate()
    skill.sea_snakes(enemy)


def other_buff(already_used):
    if art.artefacts['Папаха победителя'][2]:
        if 'Воодушевление' in person.effects:
            if person.effects['Воодушевление'] > 1:
                person.effects['Воодушевление'] -= 1
                print('Оставшаяся длительность Воодушевления:', person.effects['Воодушевление'])
            else:
                print('\nВоодушевление от Папахи победителя перестало действовать')
                del person.effects['Воодушевление']
        if ('Воодушевление' not in person.effects) and (already_used[1] is False):
            print('\nПапаха победителя воодушевила вас, теперь вы чувствуете себя непобедимым')
            person.effects['Воодушевление'] = 3
            already_used[1] = True
    if 'Трансформация' in person.effects:
        if person.effects['Трансформация'] > 1:
            person.effects['Трансформация'] -= 1
            print('Оставшаяся длительность Трансформации:', person.effects['Трансформация'])
        else:
            print('\nСила трансформации иссякла и вы приземлились на землю')
            del person.effects['Трансформация']
    return already_used


def battle(enemy, arena=False):
    already_used = ['Папаха победителя', False]
    count = 1
    person.duration = [False, False, False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False]
    while enemy.hp > 0 and person.hp > 0:
        already_used = other_buff(already_used)
        skill.time_list = \
            [
                [4, 6], [5, 6], [6, 6], [0, 1], [0, 1], [0, 1], [None], [None], [None], [3, 6],
                [7, 3], [7, 3], [7, 3], [None], [None], [None], [None],
                [None], [None], [None], [2, 5], [3, 5], [4, 5], [5, 5]
            ]
        check(person.duration, enemy)
        sleep(1)
        enemy.battle_info()
        person.battle_info()
        while True:
            print('\nХод {0} как вы поступите?'.format(count))
            print('                              1    Атаковать')
            if person.name_list.count(False) < len(person.name_list):
                print('                              2    Использовать способность')
            # print(art.artefact_skill)  #  Для лого предметов
            number_true = 0
            for v in art.artefact_skill.values():
                if v[0]: number_true += 1
            if number_true > 0:
                print('                              3    Использовать предмет')
            choose = input()
            match choose:
                case '1':
                    person_move = enemy.take_attack(person.dmg)
                    if 'Мираж' in person.effects:
                        print('Двойник атаковал')
                        double_move = enemy.take_attack(person.agility / 2)
                        if double_move:
                            print('Двойник нанёс', double_move, 'урона')
                    if person_move:
                        print(enemy.name, 'получил', person_move, 'урона')
                    break
                case '2':
                    if select_skill(enemy):
                        break
                    else:
                        continue
                case '3':
                    if art.enter_artefact_skill(art.print_artefact_skill(), person):
                        break
                    else:
                        continue
                case _:
                    continue
        sleep(0.5)
        person_effects(enemy)
        sleep(0.5)
        debuff(enemy)
        if enemy.hp <= 0:
            person.give_exp(enemy.exp)
            if 'Каменная кожа. 1ур' in person.effects:
                del person.effects['Каменная кожа. 1ур']
                person.armor -= 4
            if 'Каменная кожа. 2ур' in person.effects:
                del person.effects['Каменная кожа. 2ур']
                person.armor -= 8
            if 'Каменная кожа. 3ур' in person.effects:
                del person.effects['Каменная кожа. 3ур']
                person.armor -= 12
            if 'Водный щит. 1ур' in person.effects:
                del person.effects['Водный щит. 1ур']
                person.shield = 0
            if 'Водный щит. 2ур' in person.effects:
                del person.effects['Водный щит. 2ур']
                person.shield = 0
            if 'Водный щит. 3ур' in person.effects:
                del person.effects['Водный щит. 3ур']
                person.shield = 0
            if 'Движение маны' in person.effects:
                del person.effects['Движение маны']
            if 'Ослепление' in person.effects:
                del person.effects['Ослепление']
            if 'Яд гигантского паука' in person.effects:
                del person.effects['Яд гигантского паука']
            if 'Глубокие раны' in person.effects:
                del person.effects['Глубокие раны']
            if 'Мираж' in person.effects:
                del person.effects['Мираж']
            if 'Воодушевление' in person.effects:
                del person.effects['Воодушевление']
            if 'Трансформация' in person.effects:
                del person.effects['Трансформация']
            print('\nВы победили!\n')
            continue
        sleep(0.5)
        enemy_effects(enemy)
        enemy.enemy_move()
        count += 1
        # if len(person.duration) > 0:  # Для откладки duration
        #     print(person.duration)
        #     print(skill.time_list)
    if person.hp <= 0:
        if arena:
            print('\nВас избили до полусмерти, но милостивый распорядитель велел спасти вас. '
                  'За такой позор вы потеряли часть опыта')
            if 'Каменная кожа. 1ур' in person.effects:
                del person.effects['Каменная кожа. 1ур']
                person.armor -= 4
            if 'Каменная кожа. 2ур' in person.effects:
                del person.effects['Каменная кожа. 2ур']
                person.armor -= 8
            if 'Каменная кожа. 3ур' in person.effects:
                del person.effects['Каменная кожа. 3ур']
                person.armor -= 12
            if 'Водный щит. 1ур' in person.effects:
                del person.effects['Водный щит. 1ур']
                person.shield = 0
            if 'Водный щит. 2ур' in person.effects:
                del person.effects['Водный щит. 2ур']
                person.shield = 0
            if 'Водный щит. 3ур' in person.effects:
                del person.effects['Водный щит. 3ур']
                person.shield = 0
            if 'Движение маны' in person.effects:
                del person.effects['Движение маны']
            if 'Ослепление' in person.effects:
                del person.effects['Ослепление']
            if 'Яд гигантского паука' in person.effects:
                del person.effects['Яд гигантского паука']
            if 'Глубокие раны' in person.effects:
                del person.effects['Глубокие раны']
            if 'Мираж' in person.effects:
                del person.effects['Мираж']
            if 'Воодушевление' in person.effects:
                del person.effects['Воодушевление']
            if 'Трансформация' in person.effects:
                del person.effects['Трансформация']
            person.exp = 0
            person.hp = 10
            return False
        else:
            print('\nВы проиграли, игра окончена...')
            sleep(5)
            exit()
    return True


def scenario_1():
    print("В диких лесах...")
    sleep(1)
    print('Вы, как обычно, готовили жаркое из оленины.')
    input()
    print('Однако, когда пришло время закидывать мясо, вы заметили что его нет! Вы решили исправить эту проблему')
    input()
    print('Выйдя на охоту за дичью, вы так ничего и не смогли найти, однако вместо дичи...')
    input()
    print('Вам повстречался гоблин!')
    enemy = Enemy('Гоблин')
    battle(enemy)
    print('Пока вы забирали трофейный зуб павшего противника, вам, исподтишка, в спину ударил ещё один гоблин')
    art.get_artefact('Резец гоблина')
    # Здесь должна быть динамическая функция награды за противника
    print('Вы получили 14 урона!')
    person.hp -= 14
    enemy = Enemy('Гоблин')
    battle(enemy)
    print('После небольшой охоты вы возвращаетесь домой', end='')
    for i in range(3):
        i += 1
        sleep(1)
        print('.', end='')
    print("\nКогда вы развешивали на деревьях уши убитых гоблинов, "
          "вам на глаза попался рваный капюшон, что свисал с одной из веток. Вы, недолго думая, прихватили и его")
    art.get_artefact('Капюшон расторопного вора')
    person.advice = 2
    person.menu()


def scenario_2():
    print('Узнав что в ваших лесах бродят гоблины, вы решили разведать территорию')
    input()
    print('Зайдя достаточно далеко, вы так и не повстречали ни одного гоблина. \n'
          'Однако вы встретили иглоспина, что зашиб себя собственным кистнем. Зная, что вы более опытны в обращении'
          ' с этим оружием, вы незаметно берёте этот прекрасный кистень из рук погибшего.')
    input()
    art.get_artefact('Кистень иглоспина')
    input()
    print('После ещё нескольких часов поиска вы наткнулись на Энта!')
    input()
    enemy = Enemy('Малый энт')
    battle(enemy)
    print('Совершив решающий удар по, и без того, слабому противнику, из кустов вышел ещё один Энт!')
    sleep(1)
    enemy = Enemy('Малый энт')
    battle(enemy)
    print('На шум прибежал Орк. У него был орочий тесак и небольшой круглый щит')
    enemy = Enemy('Орк')
    battle(enemy)
    art.get_artefact('Гномий щит')
    print('С охапкой хвороста, кистнем и новым трофейным щитом, что носил орк, вы возвратились домой', end='')
    for i in range(3):
        i += 1
        sleep(1)
        print('.', end='')
    person.advice = 4
    person.menu()


def scenario_3():
    print('Хорошо отдохнув, вы решили завершить дело до конца. На этот раз вы не стали идти в том же направлении')
    input()
    print('Удача! После нескольких часов пути, вы увидели дым, поднимающийся из пещеры')
    input()
    print("Тихонько зайдя в пещеру и услышав голоса, вы прислушались")
    input()
    print("В старых песнях поётся: орков создали, чтобы бить демонов!")
    input()
    print("Старые песни правильные – демоны зло! - прозвучал более глупый голос")
    input()
    print('Решив подсмотреть, вы невольно задели старую опору, и она с грохотом обрушилась, \n'
          'оставив вас лежать перед Орком и Огром')
    input()
    enemy = Enemy('Орк')
    battle(enemy)
    print('После смерти своего собрата, до Огра дошло что никто больше не приготовит ему еду. Он взревел!')
    enemy = Enemy('Огр')
    battle(enemy)
    art.get_artefact('Дубина огра')
    print('Из последних сил срубив Огру голову, вы не стали испытывать удачу и продвигаться вглубь пещеры\n'
          'Забрав его огромную дубину, вы выбрались на поверхность и пошли домой', end='')
    for i in range(3):
        i += 1
        sleep(1)
        print('.', end='')
    print("Засолив голову и подвесив её возле входа, вы сложили второй трофейный меч")
    person.advice = 7
    person.menu()


def scenario_4():
    print('На другой день, возвращаясь в хижину с новоприобретенным магическим жезлом, что вручил вам ваш давний друг,\n'
          'вы, заприметив неладное, остановились')
    input()
    print('Дверь в дом была выломана, а вместо засоленной головы огра вы увидели разорванную сетку')
    input()
    print('Заранее подготовившись, вы аккуратно вошли домой, но треснувшая щепа под ногами раскрыла ваше присутствие')
    input()
    print('В это мгновение из угла выбежал огромный медведь. Мощным ударом он выкинул вас из избы')
    print('Вы получили 23 урона!')
    person.hp -= 23
    input()
    print('Поспешно встав, вы увидели что это был не обычный медведь, это был могучий беорн!')
    enemy = Enemy('Беорн')
    battle(enemy)
    print('Одержав победу над лесным зверем, вы решили в будущем перестать вывешивать еду на веранду')
    input()
    print('Вы подобрали оброненный жезл и занялись разделкой туши')
    for i in range(3):
        i += 1
        sleep(1)
        print('.', end='')
    print('После нескольких часов возьни вы получили хорошую шкуру, из которой сделали себе накидку.\n'
          'А все мясо хорошо спрятали')
    art.get_artefact('Шкура зверя')
    art.get_artefact('Магический жезл')
    person.advice = 8
    person.menu()


def scenario_5():
    print('Собравшись с силами и взяв все необходимое снаряжение, вы отправились исследовать глубины той пещеры')
    input()
    print("После нескольких часов пути, вы снова пробрались в неё и стали углубляться")
    input()
    print("На достаточной глубине оказалось большое подземное озеро, домик и большие ворота в скалу")
    input()
    print("Возле ворот стояло два Орка. Заприметив вас, они вступили в бой")
    enemy = Enemy('Орк')
    battle(enemy)
    enemy = Enemy('Орк')
    battle(enemy)
    print("Расправившись с Орками, вы исследовали домик на берегу озера. В нем вы нашли большой черный ключ\n"
          "Решив, что он от тех ворот, вы поспешили им воспользоваться")
    input()
    print("Отворив врата, внутри вас ждал дикий Циклоп!")
    enemy = Enemy('Циклоп')
    battle(enemy)
    print('После серьезной схватки и пронзенного глаза чудища, в загоне вы наткнулись на грудную клетку крупного животного. \n'
          'Рассмотрев в ней нечто большее чем останки, вы зацепили её к себе на спину и пошли домой')
    art.get_artefact('Рёбра кентавра')
    for i in range(3):
        i += 1
        sleep(1)
        print('.', end='')
    print("Окончив все свои опасные путешествия, вы устроили большой званый ужин из печени Циклопа")
    input()
    print("Среди присутствующих гостей был причудливый монах в красной рясе. \n"
          "Он был так восхищён рассказом, что захотел подарить вам один из своих памятных кулонов\n"
          "1. Кулон жизни, напоминающий ему о рождении сына\n"
          "2. Кулон смерти, напоминающий ему о смерти сына\n"
          "0. Ничего не брать\n")
    a = input()
    match a:
        case '1':
            print('Вы выбрали кулон Жизни, олицетворяющий надежду монаха. После этого монах удалился')
            art.get_artefact('Кулон жизни')
        case '2':
            print('Вы выбрали кулон Смерти, олицетворяющий скорбь монаха. После этого монах удалился')
            art.get_artefact('Кулон смерти')
        case _:
            print('Вы решили не принимать таких подарков, чем огорчили монаха, и тот удалился')
    input()
    person.advice = 10
    person.menu()


def scenario_6():
    print('Спустя несколько дней, ранним утром, вас разбудил громкий стук в дверь')
    input()
    print('Собравшись и выйдя на веранду, вы увидели множество орков и гоблинов. Все они окружили вашу избу')
    input()
    print('Окинув всех взглядом, вы приметили что среди них один выделялся')
    input()
    print('Он был трех метров, весь в боевых трофеях и с зеркальным копьём, его взгляд источал спокойствие и ужас')
    input()
    print('Чужеземец, выходи, я буду говорить с тобой!')
    input()
    print('Понимая что вам не справиться с такой оравой, вы поступили как он велел, войдя в их среду')
    input()
    print('Я Урук-хай, вождь и шаман клана Черные Уруки, давший клятву защищать эти земли')
    input()
    print('Я чую дух безродного оскверняет его! Чтобы жить в наших лесах, одолей меня в битве!\n'
          'Оставь коварные уловки колдунам и безродным. Один на один, меч против меча!\n'
          'Чья сила больше! Чья душа чище?')
    input()
    print('Даю слово чести, если победишь, они тебя не тронут и мы уйдём из этих земель')
    input()
    print('Он мерцнул копьём и в отражении вы увидели бугая, мчащегося на вас...')
    enemy = Enemy('Урук-хай')
    battle(enemy)
    print('Выйдя победителем из этой кровожадной битвы, все наблюдавшие орки закричали:\n'
          'Урук-хай честь, Урук-хай держит слово!')
    input()
    print('Забрав тело вожака они все ушли, а вы остались с новым копьём, отражающим ваше израненное лицо')
    input()
    art.get_artefact('Зеркальное копьё')
    sleep(3)
    print('Конец первого акта. Ввод для завершения программы')
    input()
    exit()


art = Artefact()
enemy = Enemy('None')
skill = Skill()
person = Character()
person.menu()
scenario_1()
scenario_2()
scenario_3()
scenario_4()
scenario_5()
scenario_6()
