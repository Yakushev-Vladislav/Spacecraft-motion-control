from mathem import Mathem, Sys
# from math import cos, sin


class Newton:
    def __init__(self, a, c, x_list, y_for_rk, t_for_rk, h_for_rk,
                 new_delta, pars_konec):
        self.summarnaya = 0
        self.summarnaya_2 = 0
        self.key = 0
        self.vivod = ''
        # Присваиваем переменные, для использования их в методах класса
        self.a = a
        self.c = c
        self.xn = x_list
        self.konechnye = pars_konec.copy()
        self.y_n = y_for_rk.copy()
        self.t = t_for_rk
        self.h = h_for_rk.copy()

        self.n = 3
        # Задаем все списки, для дальнейшего их использования
        self.z1 = self.xn.copy()
        self.yy1 = [0.0] * 4
        # Зададим матрицу коэффициентов
        self.y1 = new_delta.copy()
        self.fi = [0.0] * 2
        # Зададим матрицу
        self.a1 = []
        for __ in range(self.n):
            self.a1.append([0.0] * (self.n+1))
        self.aa1 = [0.0] * self.n

        # Задаем оставшиеся переменные
        self.ExitResult = 1
        self.b = 1
        self.k = 0
        self.m = 2
        for i in range(self.n):
            self.z1[i] = self.xn[i]
        self.measure()

        if self.ExitResult == 0:
            # Успешный выход
            print(f'{self.ExitResult}: Успешный выход! Поздравляем!')
            return

        # Большой цикл {1}
        while self.ExitResult == 1:
            fake_deviation = self.deviation()
            system_result = Sys(fake_deviation).get_gauss()
            if system_result[1] == 1:
                self.ExitResult = 2
                print(f'{self.ExitResult}: решение не найдено :(')
                return
            for i in range(self.n):
                self.aa1[i] = self.a1[i][-1]
            self.yy1[3] = 0
            for i in range(self.n):
                while abs(self.b * self.aa1[i]) > self.y1[i][3]:
                    self.b = self.b / 2
            for i in range(self.n):
                self.xn[i] = self.z1[i] + self.b * self.aa1[i]
            self.k = 1
            self.measure()
            if self.ExitResult == 0:
                print(f'{self.ExitResult}: Успешный выход! Поздравляем!')
                return

            # ДРОБЛЕНИЕ ШАГА

            while self.fi[1] >= self.fi[0]:
                self.b = self.b / 2
                self.yy1[3] = self.yy1[3] + 1

                if self.yy1[3] > 20.5:  # Выход по дроблению
                    # print("Breaaaak")
                    self.ExitResult = 3
                    for i in range(self.n):
                        self.xn[i] = self.z1[i]
                    self.measure()
                    # self.exit()
                    print(f'{self.ExitResult}: выход по дроблению.')
                    return

                for i in range(self.n):
                    self.xn[i] = self.z1[i] + self.b * self.aa1[i]
                self.k = 1
                self.measure()
                if self.ExitResult == 0:
                    # self.exit()
                    print(f'{self.ExitResult}: Успешный выход! Поздравляем!')
                    return

            self.change()  # ЗДЕСЬ goto 1

    def measure(self):
        self.fn = Mathem(self.a, self.c).fyn(self.xn, self.y_n, self.t,
                                             self.h, self.konechnye)
        ii = 0
        n = self.n
        for i in range(n):
            if abs(self.fn[i]) > self.y1[i][2]:
                ii += 1
        if ii == 0:
            self.ExitResult = 0  # выход
        self.fi[self.k] = 0
        for i in range(n):
            self.fi[self.k] = self.fi[self.k] + self.y1[i][0] * abs(self.fn[i])
        return [self.fi, self.ExitResult]

    def deviation(self):

        n = self.n
        for i in range(n):
            self.a1[i][-1] = -self.fn[i]

        for j in range(n):
            self.xn[j] = self.z1[j] + self.y1[j][1]
            self.fn = Mathem(self.a, self.c).fyn(self.xn, self.y_n, self.t,
                                                 self.h, self.konechnye)
            for i in range(n):
                self.a1[i][j] = (self.fn[i] + self.a1[i][-1]) / self.y1[j][1]
            ii = 0
            for i in range(n):
                if abs(self.fn[i]) > self.y1[i][2]:
                    ii += 1
            if ii == 0:
                self.ExitResult = 0  # выход
            self.xn[j] = self.z1[j]
        return self.a1

    def change(self):
        n = self.n
        for i in range(n):
            self.z1[i] = self.xn[i]
        self.yy1[0] = self.yy1[0] + 1
        self.yy1[1] = self.fi[0]
        self.yy1[2] = self.fi[1]
        self.b = 1
        self.k = 1
        self.fi[0] = self.fi[1]
        self.fout()
        if self.m == 0:
            self.ExitResult = 0

    def fout(self):
        self.key += 1
        self.summarnaya = 0

        for i in range(len(self.fn)):
            self.summarnaya += abs(self.fn[i])
        if self.key == 1:
            self.summarnaya_2 = self.summarnaya
        # вывод промежуточных результатов
        print(f"fout:"
              f"  summ = {self.summarnaya}, x = {self.xn}, fn = {self.fn}")
        # вывод крайних результатов при выходе из Ньютона
        self.vivod = (f"P_r={self.xn[0]:.8f}, "
                      f"B={self.xn[1]:.8f}, "
                      f"λ={self.xn[2]:.5f}; "
                      f" Невязки = [a:{self.fn[0]:.8f},"
                      f" e:{self.fn[1]:.8f},"
                      f" P:{self.fn[2]:.8f}]")
