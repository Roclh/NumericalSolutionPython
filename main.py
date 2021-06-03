import math
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)


class Core:
    type_equations = 0
    a = 0
    b = 0
    accuracy = 0
    type_of_input = 0

    def __init__(self):
        self.choose_equation()
        self.choose_boundaries()
        self.choose_accuracy()
        self.start_of_calculation()

    def choose_equation(self):
        while 1:
            try:
                print("\nВыберите уравнение для решения: \n"
                      "\t1. x^3 - x + 4 = 0\n"
                      "\t2. e^2x - 2 = 0\n"
                      "\t3. -2.7x^(3) - 1.48x^(2) + 19.23x + 6.35 = 0\n")
                answer = int(input("Вариант: ").strip())
                if answer == 1:
                    self.type_equations = 1
                    break
                elif answer == 2:
                    self.type_equations = 2
                    break
                elif answer == 3:
                    self.type_equations = 3
                    break
                else:
                    get_answer(1)
                    continue
            except TypeError:
                get_answer(1)
                continue

    def choose_boundaries(self):
        while 1:
            try:
                print("Введите границы ввода (Пример: -10 10):.\n")
                limits = list(input("Границы сегмента: ").strip().split(" "))
                if len(limits) == 2 and (float(limits[0].strip()) < float(limits[1].strip())):
                    self.a = float(limits[0].strip())
                    self.b = float(limits[1].strip())
                    break
                else:
                    get_answer(1)
                    continue
            except ValueError:
                get_answer(1)
            except TypeError:
                get_answer(1)

    def choose_accuracy(self):
        while 1:
            try:
                print("\nВведите погрешность вычисления.\n")
                accuracy = float(input("Погрешность: ").strip())
                if accuracy <= 0:
                    get_answer(1)
                    continue
                else:
                    self.accuracy = accuracy
                    break
            except ValueError:
                get_answer(1)
            except TypeError:
                get_answer(1)

    def start_of_calculation(self):
        while 1:
            try:
                math_logic = MathCore(self.type_equations, self.a, self.b, self.accuracy)
                print("Выберите метод:\n"
                      "\t1. Метод половинного деления\n"
                      "\t2. Метод сечений\n"
                      "\t3. Метод простых итераций")
                type_of_method = int(input("Выбранный метод: ").strip())
                if type_of_method == 1:
                    math_logic.calculate_method_halves()
                    math_logic.print_table(1)
                elif type_of_method == 2:
                    math_logic.calculate_method_secant()
                    math_logic.print_table(2)
                elif type_of_method == 3:
                    math_logic.calculate_method_iter()
                    math_logic.print_table(3)
                print_result(math_logic)
                del math_logic
                break
            except TypeError:
                get_answer(1)
            except ValueError:
                get_answer(1)


class MathCore:
    param_1 = 1
    param_2 = 1
    param_3 = 1
    param_4 = 1
    param_lambda = 1
    status = 0
    solvable = 1
    type_equations = 0
    x = 0
    a = 0
    b = 0
    steps = 0
    previous_count = 0
    x0 = 0
    x1 = 0
    accuracy = 0
    result = 0
    segments = []
    halves_table = []
    secant_table = []
    iter_table = []

    def __init__(self, type_equations, a, b, accuracy):
        self.type_equations = type_equations
        self.a = a
        self.x = 0
        self.segments = []
        self.steps = 0
        self.solvable = 1
        self.status = 0
        self.previous_count = 0
        self.result = 0
        self.b = b
        self.accuracy = accuracy
        self.x0 = a
        self.x1 = b

    def calculate_method_halves(self):
        self.halves_table = []
        self.steps = 1
        self.x = (self.x0 + self.x1) / 2
        self.halves_table.append(
            [self.steps, self.x0, self.x1, self.x, self.function(self.x0), self.function(self.x1),
             self.function(self.x), abs(self.x1 - self.x0)])
        while not (abs(self.x0 - self.x1) >= self.accuracy and self.accuracy >= abs(self.function(self.x))):
            if self.function(self.x0) * self.function(self.x) <= 0:
                self.x1 = self.x
            else:
                self.x0 = self.x
            self.x = (self.x0 + self.x1) / 2
            self.steps += 1
            self.halves_table.append(
                [self.steps, self.x0, self.x1, self.x, self.function(self.x0), self.function(self.x1),
                 self.function(self.x), abs(self.x1 - self.x0)])
        self.result = self.x

    def calculate_method_secant(self):
        self.secant_table = []
        self.steps = 0
        if abs(self.x1 - self.x0) > self.accuracy:
            while 1:
                try:
                    self.previous_count = self.x1
                    self.x1 = self.x1 - (self.x1 - self.x0) * self.function(self.x1) / (
                            self.function(self.x1) - self.function(self.x0))
                    self.secant_table.append(
                        [self.steps, self.x0, self.previous_count, self.x1, self.function(self.x1),
                         abs(self.x1 - self.previous_count)])
                    self.steps += 1
                    self.x0 = self.previous_count
                    if abs(self.x1 - self.x0) <= self.accuracy:
                        break
                except ZeroDivisionError:
                    self.x1 = self.x1 - (self.x1 - self.x0) * self.function(self.x1) / (
                            self.function(self.x1) - self.function(self.x0) + 1e-8)
        else:
            self.status = 2
            print_result(self)
        self.result = self.x1

    def calculate_method_iter(self):
        self.iter_table = []
        self.param_lambda = - 1 / max(self.derivative_of_function(self.a), self.derivative_of_function(self.b))
        self.previous_count = self.a
        self.result = self.param_function(self.previous_count)
        self.steps = 0
        if abs(self.result - self.previous_count) > self.accuracy:
            while 1:
                self.result = self.param_function(self.previous_count)
                self.iter_table.append(
                    [self.steps, self.previous_count, self.result, self.param_function(self.result),
                     self.function(self.result), abs(self.result - self.previous_count)])
                self.steps += 1
                if abs(self.result - self.previous_count) <= self.accuracy:
                    break
                self.previous_count = self.result
        else:
            get_answer(3)

    def function(self, x):
        try:
            if self.type_equations == 1:
                return math.pow(x, 3) - x + 4
            elif self.type_equations == 2:
                return math.pow(math.e, 2 * x) - 2
            elif self.type_equations == 3:
                return -2.7 * x * x * x - 1.48 * x * x + 19.23 * x + 6.35
        except ZeroDivisionError:
            return self.function(x + 1e-8)
        except OverflowError:
            self.status = 3

    def derivative_of_function(self, x):
        try:
            if self.type_equations == 1:
                return 3 * math.pow(x, 2) - 1
            elif self.type_equations == 2:
                return 2 * math.pow(math.e, 2 * x)
            elif self.type_equations == 3:
                return -8.1 * x * x - 2.96 * x + 19.23
        except ZeroDivisionError:
            return self.derivative_of_function(x + 1e-8)
        except OverflowError:
            self.status = 3

    def param_function(self, x):
        try:
            if self.type_equations == 1:
                return self.param_lambda * math.pow(x, 3) - self.param_lambda * x + x + 4 * self.param_lambda
            elif self.type_equations == 2:
                return self.param_lambda * math.pow(math.e, 2 * x) - self.param_lambda * 2 + x
            elif self.type_equations == 3:
                return -self.param_lambda * 2.7 * x * x * x - self.param_lambda * 1.48 * math.pow(x,
                                                                                                  2) + self.param_lambda * 19.23 * x - self.param_lambda * 6.35 + x
        except ZeroDivisionError:
            return self.param_function(x + 1e-8)
        except OverflowError:
            self.status = 3

    def print_table(self, type_of_table):
        if type_of_table == 1:
            print('Метод половинного деления:')
            print(tabulate(self.halves_table, headers=["№", "a", "b", "x", "f(a)", "f(b)", "f(x)", "|a-b|"],
                           tablefmt="fancy_grid", floatfmt="5.3f"))
        elif type_of_table == 2:
            print('Метод сечений:')
            print(tabulate(self.secant_table, headers=["№", "x(i-1)", "x(i)", "x(i+1)", "f(x(i+1))", "|x(i+1)-x(i)|"],
                           tablefmt="fancy_grid", floatfmt="5.3f"))
        elif type_of_table == 3:
            print('Метод простых итераций:')
            print(tabulate(self.iter_table, headers=["№", "x(i)", "x(i+1)", "fi(i+1)", "f(x(i+1))", "|x(i+1)-x(i)|"],
                           tablefmt="fancy_grid", floatfmt="5.3f"))


def print_result(math_logic):
    if math_logic.solvable == 1:
        if math_logic.status == 0:
            print("\nКорень уровнения: " + str(math_logic.result) + "\n" +
                  "Значение функции в корне: " + str(math_logic.function(math_logic.x))+"\n"+
                  "Количество итераций: " + str(math_logic.steps) + "\n" +
                  "Погрешность вычислений: " + str(math_logic.accuracy) + "\n")
            draw_graph(math_logic)
        elif math_logic.status == 1:
            get_answer(3)
        elif math_logic.status == 2:
            get_answer(4)
        elif math_logic.status == 3:
            get_answer(5)
        elif math_logic.status == 4:
            get_answer(6)
        elif math_logic.status == 5:
            get_answer(3)
    else:
        get_answer(2)


def draw_graph(math_logic):
    try:
        ax = plt.gca()
        plt.grid()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        minimum = math_logic.a
        maximum = math_logic.b
        for segment in math_logic.segments:
            if segment[0] < minimum:
                minimum = segment[0]
            elif segment[1] > maximum:
                maximum = segment[1]
        x = np.linspace(minimum, maximum, 100)
        equations = {1: ["f(x) = x^3 - x + 4", [(math.pow(i, 3) - x + 4) for i in x]],
                     2: ["f(x) = e^2x - 2", [(math.pow(math.e, 2 * i) - 2) for i in x]],
                     3: ["f(x) = -2.7x^3 - 1.48x^2 + 19.23x + 6.35",
                         [(-2.7 * i * i * i - 1.48 * i * i + 19.23 * i + 6.35) for i in x]]}
        plt.title("Функция: " + equations[math_logic.type_equations][0])
        plt.plot(x, equations[math_logic.type_equations][1], color="b", linewidth=2)
        plt.plot(x, 0 * x, color="black", linewidth=1)
        plt.scatter(math_logic.result, 0, color="r", s=80)
        plt.show()
        del x
    except ValueError:
        return
    except ZeroDivisionError:
        return
    except OverflowError:
        return


def get_answer(type_answer):
    if type_answer == 1:
        print("Неверный ввод.\n")
    elif type_answer == 2:
        print("Нет решения.\n")
    elif type_answer == 3:
        print("Нет конкретного решения или корни не существуют.\n")
    elif type_answer == 4:
        print("Количество итераций превысело 2.5 миллиона , решение не найдено.\n")
    elif type_answer == 5:
        print("Плохо выбрано начальное приближение, решение не найдено.\n")
    elif type_answer == 6:
        print("Количество итераций достигло 250 тысяч, решение не найдено.\n")


while 1:
    new_core = Core()
    del new_core
    continue
