class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть сообщение о выполненной тренировке."""
        round_duration: float = f'{self.duration:.3f}'
        round_distance: float = f'{self.distance:.3f}'
        round_speed: float = f'{self.speed:.3f}'
        round_calories: float = f'{self.calories:.3f}'
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {round_duration} ч.; '
                f'Дистанция: {round_distance} км; '
                f'Ср. скорость: {round_speed} км/ч; '
                f'Потрачено ккал: {round_calories}.'
                )


class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_MIN: int = 60

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_mult_speed: int = 18
        coeff_diff_speed: int = 20
        return ((coeff_mult_speed * self.get_mean_speed() - coeff_diff_speed)
               * self.weight / self.M_IN_KM * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_mult_weight: float = 0.035
        coeff_square_speed: int = 2
        coeff_mult_div: float = 0.029
        return ((coeff_mult_weight * self.weight
                 + (self.get_mean_speed() ** coeff_square_speed // self.height)
                 * coeff_mult_div * self.weight) * self.duration
                 * self.H_IN_MIN
                )


class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
              / self.M_IN_KM / self.duration
                )
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_add_speed: float = 1.1
        coeff_mult_weight: int = 2
        return ((self.get_mean_speed() + coeff_add_speed)
                 * coeff_mult_weight * self.weight
                )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_workout = {'RUN': Running,
                        'WLK': SportsWalking,
                        'SWM': Swimming
                        }
    return types_of_workout[workout_type](*data)

def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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

