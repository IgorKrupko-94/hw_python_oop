from dataclasses import dataclass, asdict

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    RESULT_TRAINING: str = ('Тип тренировки: {training_type}; '
                            'Длительность: {duration:.3f} ч.; '
                            'Дистанция: {distance:.3f} км; '
                            'Ср. скорость: {speed:.3f} км/ч; '
                            'Потрачено ккал: {calories:.3f}.'
                            )

    def get_message(self) -> str:
        """Вернуть сообщение о выполненной тренировке."""
        return self.RESULT_TRAINING.format(**asdict(self))


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
        raise NotImplementedError('Переопределите метод get_spent_calories в '
                                  + str(type(self).__name__)
                                  )

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
        COEFF_1_SPEED_RUN: int = 18
        COEFF_2_SPEED_RUN: int = 20
        return ((COEFF_1_SPEED_RUN * self.get_mean_speed() - COEFF_2_SPEED_RUN)
                * self.weight / self.M_IN_KM * self.duration * self.H_IN_MIN
                )


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
        COEFF_MULT_1_WALK: float = 0.035
        COEFF_SQUARE_WALK: int = 2
        COEFF_MULT_2_WALK: float = 0.029
        return ((COEFF_MULT_1_WALK * self.weight
                + (self.get_mean_speed() ** COEFF_SQUARE_WALK // self.height)
                * COEFF_MULT_2_WALK * self.weight) * self.duration
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
        COEFF_ADD_SWIM: float = 1.1
        COEFF_MULT_SWIM: int = 2
        return ((self.get_mean_speed() + COEFF_ADD_SWIM)
                * COEFF_MULT_SWIM * self.weight
                )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_workout = {'RUN': Running,
                        'WLK': SportsWalking,
                        'SWM': Swimming
                        }
    workout_get_type = types_of_workout.get(workout_type)
    if not workout_get_type:
        raise ValueError('Задайте корректный тип тренировки')
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