class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_tupe = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_tupe}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIES_1 = 18
        COEFF_CALORIES_2 = 20
        min_in_hour = 60
        speed_weight = ((COEFF_CALORIES_1 * self.get_mean_speed()
                         - COEFF_CALORIES_2) * self.weight)
        return (speed_weight / self.M_IN_KM * (self.duration * min_in_hour))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        COEFF_CALORIES_1 = 0.035
        COEFF_CALORIES_2 = 2
        COEFF_CALORIES_3 = 0.029
        min_in_hour = 60
        calorie_1 = COEFF_CALORIES_1 * self.weight
        calorie_2 = self.get_mean_speed()**COEFF_CALORIES_2 // self.height
        calorie_3 = COEFF_CALORIES_3 * self.weight
        return ((calorie_1 + calorie_2 * calorie_3) *
                (self.duration * min_in_hour))
        # более подробное название привысит 
        # рекомендованное значение 79  знаков в строке
        # ругаються автотесты 


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        pool = self.length_pool * self.count_pool
        return pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        COEFF_CALORIES_1 = 1.1
        COEFF_CALORIES_2 = 2
        calorie_1 = self.get_mean_speed() + COEFF_CALORIES_1
        return (calorie_1 * COEFF_CALORIES_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TYPE_TO_CLASS = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in TYPE_TO_CLASS:
        return TYPE_TO_CLASS[workout_type](*data)
    else:
        raise Exception('Вид тренировки не найден')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
