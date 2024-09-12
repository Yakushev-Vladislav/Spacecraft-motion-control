from math import pi, sqrt, atan, cos, sin


class Mathem:
    def __init__(self, a_, c_):
        self.file0 = None
        self.delta = 0
        self.a = a_
        self.c = c_
        self.sin_lam = 1
        self.cos_lam = 0
        self.betta = self.a / self.c

    def prav(self, y):

        delta_big = (y[9] / self.c) + (
                sqrt((y[7] ** 2) + (y[8] ** 2)) / (1 - y[4]))
        self.delta = 0
        self.delta = self.ssign(delta_big)

        self.sin_lam = y[8] / sqrt((y[7] ** 2) + (y[8] ** 2))
        self.cos_lam = y[7] / sqrt((y[7] ** 2) + (y[8] ** 2))
        # Вектор левых частей
        d = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Основная система уравнений
        '''
        Нумерация параметров:
        0-r
        1-fi
        2-V_r
        3-V_fi
        4-m
        5-P_r
        6-P_fi
        7-P_Vr
        8-P_Vfi
        9-P_m
        10_t
        '''
        d[0] = y[2]
        d[1] = y[3] / y[0]
        d[2] = (y[3] ** 2) / y[0] - (1 / (y[0] ** 2)) + (
                (self.a * self.delta) * self.cos_lam) / (1 - y[4])
        d[3] = (- (y[2] * y[3]) / y[0]) + (
                (self.a * self.delta) * self.sin_lam) / (1 - y[4])
        d[4] = self.betta * self.delta

        # Сопряженные
        d[5] = y[7] * ((y[3] ** 2 / y[0] ** 2) - (2 / y[0] ** 3)) - (
                y[8] * y[2] * y[3]) / (y[0] ** 2)
        d[6] = 0
        d[7] = - y[5] + y[8] * (y[3] / y[0])
        d[8] = ((y[8] * y[2]) - (2 * y[7] * y[3])) / y[0]
        d[9] = - ((self.a * self.delta * sqrt(
            (y[7] ** 2) + (y[8] ** 2))) / ((1 - y[4]) ** 2))
        d[10] = 1  # Время

        return d

    def rk_db(self, y_rk, t_rk, h, save_result=True):
        # Открытие файлов, если необходимо записать результаты
        if save_result is True:
            file0 = open('results/r=f(t).txt', 'w', encoding='utf-8')
            file1 = open('results/fi=f(t).txt', 'w', encoding='utf-8')
            file2 = open('results/V_r=f(t).txt', 'w', encoding='utf-8')
            file3 = open('results/V_fi=f(t).txt', 'w', encoding='utf-8')
            file4 = open('results/m=f(t).txt', 'w', encoding='utf-8')
            file5 = open('results/P_r=f(t).txt', 'w', encoding='utf-8')
            file6 = open('results/P_fi=f(t).txt', 'w', encoding='utf-8')
            file7 = open('results/P_Vr=f(t).txt', 'w', encoding='utf-8')
            file8 = open('results/P_Vfi=f(t).txt', 'w', encoding='utf-8')
            file9 = open('results/P_m=f(t).txt', 'w', encoding='utf-8')
            file10 = open('results/t.txt', 'w', encoding='utf-8')
            file11 = open('results/lam=f(t).txt', 'w', encoding='utf-8')
            file12 = open('results/delta=f(t).txt', 'w', encoding='utf-8')
            file13 = open('results/a=f(t).txt', 'w', encoding='utf-8')
            file14 = open('results/e=f(t).txt', 'w', encoding='utf-8')
            file15 = open('results/for_table.txt', 'w', encoding='utf-8')
        else:  # Если сохранять результаты не требуется
            file0 = file1 = file2 = file3 = file4 = file5 = file6 = file7 = \
                file8 = file9 = file10 = file11 = file12 = file13 = file14 = \
                file15 = None
        # Коэффициенты Рунге-Кутта
        y1 = y_rk.copy()
        c1 = (0, 1 / 6, 1 / 3, 1 / 3, 1 / 6)
        c2 = (0, 1 / 2, 1 / 2, 1, 1)
        # Принимаем первый шаг и записываем его в дублирующие переменные
        hrk = h[0]
        hrk1 = hrk
        # Ключ проверки дробленый ли шаг
        key = True
        flag = True  # Для выхода из интегрирования
        # Начинаем основной цикл программы.
        # Определяем длину массивов.
        n = len(self.prav(y1))
        m = 1
        z1 = []
        for _ in range(2 * n + m):
            z1.append(0)

        while flag is True:
            for j in range(1, 5):
                d1 = self.prav(y1)
                if j == 1:
                    f1 = self.get_sf(y1, t_rk)

                    # Запись в текстовые файлы всех результатов
                    if save_result is True:
                        file0.write(f'{y1[0]} \n')
                        file1.write(f'{y1[1]} \n')
                        file2.write(f'{y1[2]} \n')
                        file3.write(f'{y1[3]} \n')
                        file4.write(f'{y1[4]} \n')
                        file5.write(f'{y1[5]} \n')
                        file6.write(f'{y1[6]} \n')
                        file7.write(f'{y1[7]} \n')
                        file8.write(f'{y1[8]} \n')
                        file9.write(f'{y1[9]} \n')
                        file10.write(f'{y1[-1]} \n')
                        ugol_ = self.get_ugol(
                            self.sin_lam, self.cos_lam) * 180 / pi
                        file11.write(
                            f'{ugol_} \n')
                        file12.write(f'{self.delta} \n')

                        e_for_result = sqrt(
                            (y1[0] * y1[3] * y1[3] - 1) ** 2 +
                            (y1[0] * y1[2] * y1[3]) ** 2)
                        a_for_result = ((y1[0] ** 2) * (y1[3] ** 2)) * (
                                1 - (e_for_result ** 2))
                        file13.write(f'{a_for_result} \n')
                        file14.write(f'{e_for_result} \n')
                        file15.write(f'{y1[10]}, {y1[0]}, {y1[1]}, {y1[2]},'
                                     f' {y1[3]}, {y1[4]}, {y1[5]}, {y1[7]},'
                                     f' {y1[8]}, {e_for_result},'
                                     f' {a_for_result} \n')

                    else:
                        pass

                    if abs(f1) <= h[-1]:
                        # !!!___Сработала функция выхода___!!!
                        flag = False
                        break
                    else:
                        if (key is False) and (z1[2 * n] * f1 < 0):
                            hrk = (z1[2 * n] * hrk1) / (z1[2 * n] - f1)
                            hrk1 = hrk
                            for ir in range(n):
                                y1[ir] = z1[ir]

                        # Здесь надо начинать все сначала
                        else:
                            z1[2 * n] = f1

                # Непосредственно Рунге-Кутта
                if j > 4:
                    break
                for i in range(n):
                    if j != 1:
                        z1[n + i] = z1[n + i] + hrk1 * d1[i] * c1[j]
                        y1[i] = z1[i] + hrk1 * d1[i] * c2[j]

                    else:
                        z1[i] = y1[i]
                        z1[n + i] = y1[i]
                        z1[n + i] = z1[n + i] + hrk1 * d1[i] * c1[j]
                        y1[i] = z1[i] + hrk1 * d1[i] * c2[j]

            key = False
            for ii in range(n):
                y1[ii] = z1[n + ii]

        if save_result is True:
            file0.close()
            file1.close()
            file2.close()
            file3.close()
            file4.close()
            file5.close()
            file6.close()
            file7.close()
            file8.close()
            file9.close()
            file10.close()
            file11.close()
            file12.close()
            file13.close()
            file14.close()
            file15.close()
        else:
            pass
        return y1

    def get_sf(self, y_sf, t_sfk):
        self.is_not_used()
        sf = y_sf[10] - t_sfk
        # sf_2 = y_sf[9]
        return sf

    def ssign(self, some):
        self.is_not_used()
        res = 0
        if some > 0:
            res = 1
        elif some < 0:
            res = 0
        return res

    def get_ugol(self, s, ccos):
        if ccos == 0:
            at = 0.5 * pi * self.ssign(s)
        else:
            at = atan(s / ccos)

        if ccos < 0:
            at = at + pi
        else:
            if s < 0:
                at = at + 2 * pi
        return at

    def is_not_used(self):
        pass

    def fyn(self, x_list, y_for_rk, t_for_rk, h_for_rk, param):
        """
        param = [a_k, e_k]
        x_list = [P_r, B, lam]
        0-r; 1-fi; 2-V_r; 3-V_fi; 4-m;
        5-P_r; 6-P_fi; 7-P_Vr; 8-P_Vfi; 9-P_m; 10_t
        """
        y_fyn = y_for_rk.copy()
        y_fyn[7] = x_list[1] * sin(x_list[2])  # P_Vr
        y_fyn[8] = x_list[1] * cos(x_list[2])  # P_Vfi
        y_fyn[5] = x_list[0]  # P_r
        y_k = self.rk_db(y_fyn, t_for_rk, h_for_rk, False)
        result = []
        e_ot_t = sqrt((y_k[0] * y_k[3] * y_k[3] - 1) ** 2 +
                      (y_k[0] * y_k[2] * y_k[3]) ** 2)
        a_ot_t = ((y_k[0] ** 2) * (y_k[3] ** 2)) * (1 - (e_ot_t ** 2))
        p_n1_n2 = (- y_k[5] * y_k[0] * y_k[0] * y_k[2] +
                   y_k[7] * (1 - y_k[0] * y_k[3] * y_k[3]) +
                   y_k[8] * y_k[0] * y_k[2] * y_k[3])
        f_1 = a_ot_t - param[0]  # a
        result.append(f_1)
        f_2 = e_ot_t - param[1]  # e
        result.append(f_2)
        f_3 = p_n1_n2  # трансверсальность
        result.append(f_3)
        return result


class Sys:
    def __init__(self, matrix):
        self.ExitSystem = 0
        self.len = len(matrix)
        self.m = self.len + 1
        for j in range(self.len):
            i = 0
            self.b = 0
            for k in range(j, self.len):
                if abs(matrix[k][j]) > abs(self.b):
                    i = k
                    self.b = matrix[k][j]
                else:
                    if self.b == 0:
                        self.ExitSystem = 1
                        break
            if self.ExitSystem == 1:
                break
            for k in range(self.m):
                self.c = matrix[i][k] / self.b
                matrix[i][k] = matrix[j][k]
                matrix[j][k] = self.c

            for k in range(self.len):
                self.b = matrix[k][j]
                if k != j:
                    for ks in range(self.m):
                        matrix[k][ks] = matrix[k][ks] - matrix[j][ks] * self.b
        self.M = matrix

    def get_gauss(self):
        return self.M, self.ExitSystem
