import random
import simpy
from termcolor import cprint

TOTAL_NUMBER_OF_CITIZENS = 10000
DAYS_BEFORE_HOSPITALIZATION = [3, 15]
RECOVERY_DAYS = [15, 45]  # Время проведенное в больнице
WEEKS = 1  # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24  # Simulation time in minutes
time_of_day = "day"  # night
count_days = 0
current_time = 0
time_now = 0


class Citizen:
    def __init__(self, number, env):
        self.number = number
        self.env = env
        # Вероятноть ношения маски = 50%:
        if random.randint(1, 2) == 1:
            self.wearing_mask = True
        else:
            self.wearing_mask = False
        self.health_status = "healthy"  # ill
        self.antibodies = 0  # Если переболел - больше 0, заболеть не может
        self.in_hospital = False
        self.location = "work"  # shop/fun_places/public_transport/hospital

    def going_to_work(self):
        """
        Находится на работе 9 часов
        :return:
        """
        print("-----------")
        print(f"Человек({self.number}) сейчас на работе, время симуляции-{self.env.now}")
        yield self.env.timeout(9)
        print(f"Человек({self.number}) закончил работать, время симуляции-{env.now}")
        print("+++++++++++")

    def use_public_transport(self):
        """
        Находится в общественном траснпорте от 30 минут то 1,5 часов
        :return:
        """
        print("-----------")
        print(f"Человек({self.number}) сейчас в общественном транспорте, время симуляции-{env.now}")
        # yield env.timeout(value=1.5)
        travel_time = random.uniform(0.5, 1.5)
        print(f"Время поездки человека({self.number}) = {travel_time}")
        yield self.env.timeout(travel_time)
        print(f"Человек({self.number}) вышел из общественного транспорта, время симуляции-{env.now}")
        print("+++++++++++")

    def go_to_shop(self):
        """
        Находится в магазине от 10 минут до полтора часа
        :return:
        """
        print("-----------")
        print(f"Человек({self.number}) сейчас в магазине, время-{env.now}")
        # yield env.timeout(value=1.5)
        time_for_shopping = random.uniform(0.16, 1.5)
        print(f"Человек({self.number}) провел в магазине время - {time_for_shopping}")
        yield self.env.timeout(time_for_shopping)
        print(f"Человек({self.number}) вышел из магазина, время-{env.now}")
        print("+++++++++++")

    def go_to_fun_places(self):
        """
        Находится в кинотеатре, ресторане итд
        от 1 до 2.5 часов
        :return:
        """
        print("-----------")
        print(f"Человек({self.number}) сейчас в торговом центре(кинотеатр итд), время-{env.now}")
        # yield env.timeout(value=1.5)
        time_for_shopping = random.uniform(1, 2.5)
        print(f"Человек({self.number}) провел в торговом центре время - {time_for_shopping}")
        yield self.env.timeout(time_for_shopping)
        print(f"Человек({self.number}) вышел из торгового центра, время-{env.now}")
        print("+++++++++++")

    def _get_infected(self):
        """
        Заразиться
        :return:
        """
        pass

    def chance_to_infected(self):
        """
        Если в помещении больной человек, есть вероятность заразиться
        :return:
        """
        probability = 40
        self.health_status = random.choices(["healthy", "ill"], weights=[100, 100 - probability])

    def run(self):
        global current_time
        while True:
            if time_now == 7:  # Сьездить на работу и вернутся с нее
                start_time = self.env.now
                print(f"start_time(время симуляции) человека№{self.number}=", start_time)
                yield self.env.process(self.use_public_transport())
                yield self.env.process(self.going_to_work())
                yield self.env.process(self.use_public_transport())
                end_time = self.env.now
                print(f"end_time(время симуляции) человека№({self.number})=", end_time)
                print(f"После возвращения с работы на часах человека({self.number})={time_now} часов")
                if 17 <= time_now <= 19:
                    yield self.env.process(self.go_to_fun_places())
                    if random.randint(1, 2) == 1:
                        yield self.env.process(self.go_to_shop())
                    yield self.env.process(self.use_public_transport())

                    print(f"После развлечений и магазина(возможно) на часах человека({self.number})={time_now} часов")

            yield self.env.timeout(0.0001)  # Для того чтобы можно было вызвать как генератор


class Building:
    """
    Базовый класс всех помещений
    """

    def __init__(self):
        self.amount_of_people = 0
        self.amount_of_sick_people = 0
        self.sick_human_in_room = 0


class Work(Building):
    """
    Базовый класс для видов работ(помещений)
    """

    def __init__(self, name_of_work: str):
        super().__init__()
        self.name_of_work = name_of_work


class Shop(Building):
    """
    Класс магазинов
    """

    def __init__(self):
        super().__init__()


class FunPlaces(Building):
    """
    Базовый класс развлекательных мест
    """

    def __init__(self):
        super().__init__()


class PublicTransport(Building):
    """
        Класс развлекательных мест
        """

    def __init__(self):
        super().__init__()


def calendar(env):
    global time_now
    global count_days
    while True:
        print("Сейчас 7утра, время симуляции=", env.now)
        time_now = 7
        while time_now < 22:
            yield env.timeout(1)
            time_now += 1
        if time_now >= 22:
            print("Наступила ночь, время симуляции =", env.now)
            yield env.timeout(9)
            count_days += 1
            cprint("=" * 25 + f"Следующий день №{count_days}" + "=" * 25, "green")


##########################
# env = simpy.Environment()
env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=0.001, strict=False)
human1 = Citizen(number=1, env=env)
env.process(human1.run())
human2 = Citizen(number=2, env=env)
env.process(human2.run())
env.process(calendar(env))

env.run(until=SIM_TIME)
