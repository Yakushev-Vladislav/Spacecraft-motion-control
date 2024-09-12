#  Импорт необходимых библиотек
from tkinter import *
from tkinter.ttk import Notebook, Treeview, Style, Progressbar
from tkinter.messagebox import showinfo
from matplotlib import pyplot as plt
from math import cos, sin, sqrt, pi
from mathem import Mathem
from newton import Newton


# Создание класса основного окна интерфейса
class Window:
    def __init__(self, width, height, title='Расчет перелета КА.',
                 resizable=(False, False), icon=None):
        self.koef_for_time = 1  # Объявление переменной для перевода
        # время графиков

        # Параметры основного окна
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f'{width}x{height}+350+150')
        self.root.resizable(resizable[0], resizable[1])
        self.root.iconbitmap(icon)
        self.tabs_control = Notebook(self.root)
        # Прорисовка всех вкладок окна (интегрирование, результаты, Ньютон)
        self.tab_1 = Frame(self.tabs_control)
        self.tabs_control.add(self.tab_1, text="Интегрирование")
        self.tab_2 = Frame(self.tabs_control)
        self.tabs_control.add(self.tab_2, text="Результаты")
        self.tab_3 = Frame(self.tabs_control)
        self.tabs_control.add(self.tab_3, text="Оптимизация")
        # Зададим основные управляющие виджеты (кнопки)
        self.btn_get_rk = Button(self.tab_1, width=15, height=2,
                                 text='Интегрирование',
                                 font='Verdana 11',
                                 fg='dark green',
                                 bg='light grey',
                                 command=self.get_integrate)
        self.btn_destroy = Button(self.tab_1, width=15, height=2,
                                  text='Выход',
                                  font='Verdana 11',
                                  fg='dark red',
                                  bg='light grey',
                                  command=self.get_down)
        self.btn_back = Button(self.tab_2, width=15, height=2,
                               text='Назад',
                               font='Verdana 11',
                               fg='dark red',
                               bg='light grey',
                               command=self.get_back)
        self.btn_plot = Button(self.tab_2, width=15, height=2,
                               text='Построить',
                               font='Verdana 11',
                               fg='dark green',
                               bg='light grey',
                               command=self.get_plot)
        self.btn_back2 = Button(self.tab_3, width=15, height=2,
                                text='Назад',
                                font='Verdana 11',
                                fg='dark red',
                                bg='light grey',
                                command=self.get_back2)
        self.btn_newton = Button(self.tab_3, width=15, height=2,
                                 text='Рассчитать',
                                 font='Verdana 11',
                                 fg='dark green',
                                 bg='light grey',
                                 command=self.get_newton)
        self.btn_stop_newton = Button(self.tab_3, width=15, height=2,
                                      text='Остановка',
                                      font='Verdana 11',
                                      fg='dark blue',
                                      bg='light grey',
                                      command=self.stop_newton)

        # ___Первая вкладка___
        # Параметры начальной орбиты
        begin_pericenter = StringVar(self.tab_1, value="100")
        self.ent_begin_pericenter = Entry(
            self.tab_1, fg='blue', width=25, textvariable=begin_pericenter)
        begin_exc = StringVar(self.tab_1, value="0")
        self.ent_begin_exc = Entry(self.tab_1, fg='blue', width=25,
                                   textvariable=begin_exc)
        begin_poluos = StringVar(self.tab_1, value="6871")
        self.ent_begin_poluos = Entry(self.tab_1, fg='blue', width=25,
                                      textvariable=begin_poluos)
        begin_shyrota = StringVar(self.tab_1, value="0")
        self.ent_begin_shyrota = Entry(self.tab_1, fg='blue', width=25,
                                       textvariable=begin_shyrota)
        # Параметры целевой орбиты
        end_pericenter = StringVar(self.tab_1, value="0")
        self.ent_end_pericenter = Entry(self.tab_1, fg='blue', width=25,
                                        textvariable=end_pericenter)
        end_exc = StringVar(self.tab_1, value="0.05")
        self.ent_end_exc = Entry(self.tab_1, fg='blue', width=25,
                                 textvariable=end_exc)
        end_poluos = StringVar(self.tab_1, value="6921")
        self.ent_end_poluos = Entry(self.tab_1, fg='blue', width=25,
                                    textvariable=end_poluos)
        end_shyrota = StringVar(self.tab_1, value="270")
        self.ent_end_shyrota = Entry(self.tab_1, fg='blue', width=25,
                                     textvariable=end_shyrota)
        # Сопряженные вектор-функции
        var_p_r = StringVar(self.tab_1, value="1.2")
        self.ent_sopryazh_P_r = Entry(self.tab_1, fg='blue', width=25,
                                      textvariable=var_p_r)
        var_b = StringVar(self.tab_1, value="0.45")
        self.ent_sopryazh_B = Entry(self.tab_1, fg='blue', width=25,
                                    textvariable=var_b)
        var_lam = StringVar(self.tab_1, value="120")
        self.ent_sopryazh_lam = Entry(self.tab_1, fg='blue', width=25,
                                      textvariable=var_lam)
        # Время и параметры КА
        var_time = StringVar(self.tab_1, value="5")
        self.ent_time = Entry(self.tab_1, fg='blue', width=25,
                              textvariable=var_time)
        var_mass = StringVar(self.tab_1, value="100")
        self.ent_KA_mass = Entry(self.tab_1, fg='blue', width=25,
                                 textvariable=var_mass)
        var_p = StringVar(self.tab_1, value="0.5")
        self.ent_KA_P = Entry(self.tab_1, fg='blue', width=25,
                              textvariable=var_p)
        var_c = StringVar(self.tab_1, value="20000")
        self.ent_KA_c = Entry(self.tab_1, fg='blue', width=25,
                              textvariable=var_c)
        # Параметры расчета
        var_shag = StringVar(self.tab_1, value="0.01")
        self.shag = Entry(self.tab_1, fg='blue', width=25,
                          textvariable=var_shag)
        var_delta = StringVar(self.tab_1, value='1e-8')
        self.pogreshnost = Entry(self.tab_1, fg='blue', width=25,
                                 textvariable=var_delta)

        # ___Вторая вкладка___
        # Таблица данных
        # __Стиль таблицы__
        style = Style()
        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image",
                     {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.configure("Custom.Treeview.Heading",
                        background="#F6B892", foreground="black",
                        relief="groove")
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'groove'), ('pressed', 'sunken')])

        # __ Настройка самой таблицы __
        self.columns = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        self.result_table = Treeview(self.tab_2, columns=self.columns,
                                     show='headings', height=18,
                                     style="Custom.Treeview")

        self.yscroll = Scrollbar(self.tab_2, orient="vertical",
                                 command=self.result_table.yview)
        self.result_table.column("0", anchor=CENTER, width=50)
        self.result_table.column("1", anchor=CENTER, width=50)
        self.result_table.column("2", anchor=CENTER, width=50)
        self.result_table.column("3", anchor=CENTER, width=50)
        self.result_table.column("4", anchor=CENTER, width=50)
        self.result_table.column("5", anchor=CENTER, width=50)
        self.result_table.column("6", anchor=CENTER, width=50)
        self.result_table.column("7", anchor=CENTER, width=50)
        self.result_table.column("8", anchor=CENTER, width=50)
        self.result_table.column("9", anchor=CENTER, width=50)
        self.result_table.column("10", anchor=CENTER, width=50)
        self.result_table.heading("0", text="t", anchor=CENTER)
        self.result_table.heading("1", text="r", anchor=CENTER)
        self.result_table.heading("2", text="φ", anchor=CENTER)
        self.result_table.heading("3", text="V_r", anchor=CENTER)
        self.result_table.heading("4", text="V_φ", anchor=CENTER)
        self.result_table.heading("5", text="m", anchor=CENTER)
        self.result_table.heading("6", text="P_r", anchor=CENTER)
        self.result_table.heading("7", text="P_Vr", anchor=CENTER)
        self.result_table.heading("8", text="P_Vφ", anchor=CENTER)
        self.result_table.heading("9", text="e", anchor=CENTER)
        self.result_table.heading("10", text="a", anchor=CENTER)

        self.dannye_test = []

        # Настройка меню графика
        self.plot_choice = IntVar(value=1)

        # ___Третья вкладка___
        # Параметры расчета
        var_pryrasch_1 = StringVar(self.tab_3, value="0.001")
        var_pryrasch_2 = StringVar(self.tab_3, value="0.001")
        var_pryrasch_3 = StringVar(self.tab_3, value="0.001")
        self.ent_pryrash_1 = Entry(self.tab_3, fg='blue', width=18,
                                   textvariable=var_pryrasch_1)
        self.ent_pryrash_2 = Entry(self.tab_3, fg='blue', width=18,
                                   textvariable=var_pryrasch_2)
        self.ent_pryrash_3 = Entry(self.tab_3, fg='blue', width=18,
                                   textvariable=var_pryrasch_3)
        var_koef_1 = StringVar(self.tab_3, value="1")
        var_koef_2 = StringVar(self.tab_3, value="1")
        var_koef_3 = StringVar(self.tab_3, value="1")
        self.ent_koef_nev_1 = Entry(self.tab_3, fg='blue', width=18,
                                    textvariable=var_koef_1)
        self.ent_koef_nev_2 = Entry(self.tab_3, fg='blue', width=18,
                                    textvariable=var_koef_2)
        self.ent_koef_nev_3 = Entry(self.tab_3, fg='blue', width=18,
                                    textvariable=var_koef_3)
        var_tochnost_1 = StringVar(self.tab_3, value="0.01")
        var_tochnost_2 = StringVar(self.tab_3, value="0.01")
        var_tochnost_3 = StringVar(self.tab_3, value="0.01")
        self.ent_tochnost_1 = Entry(self.tab_3, fg='blue', width=18,
                                    textvariable=var_tochnost_1)
        self.ent_tochnost_2 = Entry(self.tab_3, fg='blue', width=18,
                                    textvariable=var_tochnost_2)
        self.ent_tochnost_3 = Entry(self.tab_3, fg='blue', width=18,
                                    textvariable=var_tochnost_3)
        var_ogran_1 = StringVar(self.tab_3, value="0.1")
        var_ogran_2 = StringVar(self.tab_3, value="0.1")
        var_ogran_3 = StringVar(self.tab_3, value="0.1")
        self.ent_ogran_1 = Entry(self.tab_3, fg='blue', width=18,
                                 textvariable=var_ogran_1)
        self.ent_ogran_2 = Entry(self.tab_3, fg='blue', width=18,
                                 textvariable=var_ogran_2)
        self.ent_ogran_3 = Entry(self.tab_3, fg='blue', width=18,
                                 textvariable=var_ogran_3)
        self.ent_nevyaz_p_r = Text(self.tab_3, fg='dark blue', width=16,
                                   height=1,
                                   font="Aril 10")
        self.ent_nevyaz_b = Text(self.tab_3, fg='dark blue', width=16,
                                 height=1,
                                 font="Aril 10")
        self.ent_nevyaz_lam = Text(self.tab_3, fg='dark blue', width=16,
                                   height=1,
                                   font="Aril 10")
        # Параметры для входа в Ньютон
        self.y_0_new = []
        self.ac_new = []
        self.t_new = 0
        self.h_new = []
        self.n_new = 0
        self.i_new = 0
        self.new_del = []
        self.a_k = 0
        self.e_k = 0
        self.key = 0
        self.plot_r_0 = 0

        # Вывод данных
        self.ent_vivod = Text(self.tab_3, width=95, height=13, bg='white',
                              fg='blue', relief="ridge", font='Arial 12',
                              bd=4)
        # Прогресс расчетов
        self.var_progress = IntVar(self.tab_3, value=0)
        self.progress = Progressbar(self.tab_3, orient='horizontal',
                                    length=270,
                                    mode='determinate')

        self.lbl_bar = Text(self.tab_3, width=5, height=1, fg='dark red',
                            bg='#f0f0ed', relief='flat', bd=0)

    def draw_widgets(self):  # Метод прорисовки виджетов
        # Параметры начальной орбиты
        Label(self.tab_1, text='Введите параметры начальной орбиты:',
              height=1, font='Arial 10 bold').place(x=80, y=10)
        Label(self.tab_1, text='Начальный аргумент перицентра, град.:',
              height=1).place(x=20, y=50)
        self.ent_begin_pericenter.place(x=270, y=50)
        Label(self.tab_1, text='Начальный эксцентриситет:',
              height=1).place(x=20, y=80)
        self.ent_begin_exc.place(x=270, y=80)
        Label(self.tab_1, text='Начальная большая полуось орбиты, км:',
              height=1).place(x=20, y=110)
        self.ent_begin_poluos.place(x=270, y=110)
        Label(self.tab_1, text='Начальный аргумент широты, град.:',
              height=1).place(x=20, y=140)
        self.ent_begin_shyrota.place(x=270, y=140)

        # Параметры целевой орбиты
        Label(self.tab_1, text='Введите параметры целевой орбиты:',
              height=1, font='Arial 10 bold').place(x=550, y=10)
        Label(self.tab_1, text='Аргумент перицентра, град.:',
              height=1).place(x=500, y=50)
        self.ent_end_pericenter.place(x=690, y=50)
        Label(self.tab_1, text='Эксцентриситет:',
              height=1).place(x=500, y=80)
        self.ent_end_exc.place(x=690, y=80)
        Label(self.tab_1, text='Большая полуось орбиты, км:',
              height=1).place(x=500, y=110)
        self.ent_end_poluos.place(x=690, y=110)
        Label(self.tab_1, text='Аргумент широты, град.:',
              height=1).place(x=500, y=140)
        self.ent_end_shyrota.place(x=690, y=140)

        # Сопряженные вектор-функции
        Label(self.tab_1, text='Введите сопряженные вектор функции:',
              height=1, font='Arial 10 bold').place(x=550, y=180)
        Label(self.tab_1, text='Сопряженная переменная P_r:',
              height=1).place(x=500, y=220)
        self.ent_sopryazh_P_r.place(x=690, y=220)
        Label(self.tab_1, text='Сопряженная переменная B:',
              height=1).place(x=500, y=250)
        self.ent_sopryazh_B.place(x=690, y=250)
        Label(self.tab_1, text='Начальный угол λ, град.:',
              height=1).place(x=500, y=280)
        self.ent_sopryazh_lam.place(x=690, y=280)

        # Время полета
        Label(self.tab_1, text='Введите время полета:',
              height=1, font='Arial 10 bold').place(x=550, y=320)
        Label(self.tab_1, text='Время полета, сут.:',
              height=1).place(x=500, y=350)
        self.ent_time.place(x=690, y=350)

        # Параметры КА
        Label(self.tab_1, text='Введите параметры КА:',
              height=1, font='Arial 10 bold').place(x=80, y=180)
        Label(self.tab_1, text='Начальный масса КА, кг.:',
              height=1).place(x=20, y=210)
        self.ent_KA_mass.place(x=270, y=210)
        Label(self.tab_1, text='Тяга двигателей КА, Н.:',
              height=1).place(x=20, y=240)
        self.ent_KA_P.place(x=270, y=240)
        Label(self.tab_1, text='Скорость истечения двигателей, м/с.:',
              height=1).place(x=20, y=270)
        self.ent_KA_c.place(x=270, y=270)

        # Параметры расчета
        Label(self.tab_1, text='Параметры расчета:',
              height=1, font='Arial 10 bold').place(x=80, y=320)
        Label(self.tab_1, text='Шаг интегрирования:',
              height=1).place(x=20, y=350)
        self.shag.place(x=270, y=350)
        Label(self.tab_1, text='Погрешность интегрирования:',
              height=1).place(x=20, y=380)
        self.pogreshnost.place(x=270, y=380)

        # Переключатели графика
        Label(self.tab_2, text='Выберите зависимость:',
              font='Arial 11').place(x=620, y=20)
        Radiobutton(self.tab_2, text='Траектория перелета', font='Arial 10',
                    variable=self.plot_choice, value=1).place(x=580, y=50)
        Radiobutton(self.tab_2, text='Радиус от времени', font='Arial 10',
                    variable=self.plot_choice, value=2).place(x=580, y=80)
        Radiobutton(self.tab_2, text='Угловая дальность от времени',
                    font='Arial 10',
                    variable=self.plot_choice, value=3).place(x=580, y=110)
        Radiobutton(self.tab_2, text='Радиальная скорость от времени',
                    font='Arial 10',
                    variable=self.plot_choice, value=4).place(x=580, y=140)
        Radiobutton(self.tab_2, text='Трансверсальная скорость от времени',
                    font='Arial 10',
                    variable=self.plot_choice, value=5).place(x=580, y=170)
        Radiobutton(self.tab_2, text="Масса от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=6).place(x=580, y=200)
        Radiobutton(self.tab_2, text="Сопряженная P_r от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=7).place(x=580, y=230)
        Radiobutton(self.tab_2, text="Сопряженная P_fi от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=8).place(x=580, y=260)
        Radiobutton(self.tab_2, text="Сопряженная P_Vr от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=9).place(x=580, y=290)
        Radiobutton(self.tab_2, text="Сопряженная P_Vfi от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=10).place(x=580, y=320)
        Radiobutton(self.tab_2, text="Сопряженная P_m от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=11).place(x=580, y=350)
        Radiobutton(self.tab_2, text="Угол λ от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=12).place(x=580, y=380)
        Radiobutton(self.tab_2, text="Функция включения двигателя от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=13).place(x=580, y=410)
        Radiobutton(self.tab_2, text="Большая полуось от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=14).place(x=580, y=440)
        Radiobutton(self.tab_2, text="Эксцентриситет от времени",
                    font='Arial 10',
                    variable=self.plot_choice, value=15).place(x=580, y=470)
        # 3 вкладка
        # Размещение матрицы дельта
        Label(self.tab_3, text='1:', height=1, font='Arial 10').place(x=20,
                                                                      y=68)
        Label(self.tab_3, text='2:', height=1, font='Arial 10').place(x=20,
                                                                      y=98)
        Label(self.tab_3, text='3:', height=1, font='Arial 10').place(x=20,
                                                                      y=128)
        Label(self.tab_3, text=' Весовые \n коэффициенты \n невязок: ',
              font="Arial 8").place(x=50, y=10)
        Label(self.tab_3,
              text=' Приращения для \n '
                   'численного определения \n производных: ',
              font='Arial 8').place(x=155, y=10)
        Label(self.tab_3, text=' Точность \n решения: ', font='Arial 8').place(
            x=325, y=22)
        Label(self.tab_3, text=' Ограничения \n на приращения: ',
              font='Arial 8').place(x=440, y=22)
        self.ent_koef_nev_1.place(x=40, y=70)
        self.ent_koef_nev_2.place(x=40, y=100)
        self.ent_koef_nev_3.place(x=40, y=130)
        self.ent_pryrash_1.place(x=170, y=70)
        self.ent_pryrash_2.place(x=170, y=100)
        self.ent_pryrash_3.place(x=170, y=130)
        self.ent_tochnost_1.place(x=300, y=70)
        self.ent_tochnost_2.place(x=300, y=100)
        self.ent_tochnost_3.place(x=300, y=130)
        self.ent_ogran_1.place(x=430, y=70)
        self.ent_ogran_2.place(x=430, y=100)
        self.ent_ogran_3.place(x=430, y=130)
        # Поля ввода невязок
        Label(self.tab_3, text='Оптимизированные сопряженные:',
              font='Arial 10 bold').place(x=590, y=30)
        Label(self.tab_3, text='P_r:').place(x=620, y=68)
        Label(self.tab_3, text='B:').place(x=620, y=98)
        Label(self.tab_3, text='λ:').place(x=620, y=128)

        self.ent_nevyaz_p_r.place(x=680, y=70)
        self.ent_nevyaz_b.place(x=680, y=100)
        self.ent_nevyaz_lam.place(x=680, y=130)
        # Вывод результатов
        Label(self.tab_3,
              text='Результаты на выходе из Ньютона (Промежуточные '
                   'результаты печатаются в консоль):',
              font='Arial 10',
              fg='dark red').place(x=120, y=155)
        self.ent_vivod.place(x=15, y=180)
        self.lbl_bar.place(x=382, y=440)
        Label(self.tab_3,
              text='Прогресс расчета. Завершено: ',
              fg='dark green').place(x=200, y=440)
        self.progress.place(x=200, y=465)
        Label(self.tab_3,
              text='%',
              fg='dark green').place(x=425, y=440)

        # Упаковка всех виджетов
        self.btn_get_rk.place(x=700, y=440)
        self.btn_destroy.place(x=20, y=440)
        self.btn_back.place(x=20, y=440)
        self.btn_plot.place(x=420, y=440)
        self.tabs_control.pack(fill=BOTH, expand=TRUE)
        self.yscroll.place(x=562, y=20, height=380)
        self.result_table.place(x=10, y=20)
        self.result_table.configure(yscrollcommand=self.yscroll.set)
        self.btn_back2.place(x=20, y=440)
        self.btn_newton.place(x=700, y=440)
        self.btn_stop_newton.place(x=520, y=440)

    def get_dannye(self):  # Считывание данных для таблицы (2 вкладка)
        file_dannye = open('results/for_table.txt', 'r', encoding='utf-8')
        temp_dannye = file_dannye.readlines()
        for x in temp_dannye:
            self.dannye_test.append(x.split(','))
        file_dannye.close()

    def get_down(self):  # Завершение работы программы
        open('results/for_table.txt', 'w', encoding='utf-8').close()
        self.root.destroy()

    def get_back(self):  # Возвращение на 1 вкладку
        self.tabs_control.select(self.tab_1)

    def get_back2(self):  # Возвращение на 2 вкладку
        self.tabs_control.select(self.tab_2)

    def get_plot(self):  # Построение графиков
        flag_equal = False
        num = self.plot_choice.get()
        x_plot = []
        y_plot = []
        choice = {1: "r=f(fi)", 2: "r=f(t)", 3: "fi=f(t)", 4: "V_r=f(t)",
                  5: "V_fi=f(t)", 6: "m=f(t)", 7: "P_r=f(t)", 8: "P_fi=f(t)",
                  9: "P_Vr=f(t)", 10: "P_Vfi=f(t)", 11: "P_m=f(t)",
                  12: 'lam=f(t)', 13: 'delta=f(t)', 14: "a=f(t)", 15: "e=f(t)"}
        if num == 1:
            file_r_plot = open(f"results/r=f(t).txt", "r")
            file_fi_plot = open(f"results/fi=f(t).txt", "r")
            x_temp_plot = file_r_plot.readlines()
            y_temp_plot = file_fi_plot.readlines()
            for i in range(len(x_temp_plot)):
                x_plot.append(
                    float(x_temp_plot[i]) * cos(float(y_temp_plot[i])))
                y_plot.append(
                    float(x_temp_plot[i]) * sin(float(y_temp_plot[i])))
            file_r_plot.close()
            file_fi_plot.close()
            flag_equal = True
        elif num != 1:
            file_x_plot = open(f"results/{choice[num]}.txt", "r")
            file_y_plot = open(f"results/t.txt", "r")
            x_temp_plot = file_x_plot.readlines()
            x_plot = []
            for x in x_temp_plot:
                x_plot.append(float(x))
            y_temp_plot = file_y_plot.readlines()
            y_plot = []
            for y in y_temp_plot:
                y_plot.append(float(y) / self.koef_for_time)
            file_x_plot.close()
            file_y_plot.close()
        plt.figure(choice[num])
        plt.xlabel("")
        plt.ylabel("")
        plt.plot(y_plot, x_plot, 'k-')
        plt.grid(True)
        plt.grid(which='major', linewidth=1.0)
        plt.grid(which='minor', linewidth=0.2)
        plt.minorticks_on()

        if flag_equal is True:
            plt.gca().set_aspect("equal")
        else:
            pass
        plt.title(choice[num])
        plt.show()

    def get_integrate(self):  # Интегрирование
        # Константы
        mu_zemli = 3.98603 * (10 ** 14)
        # r_z = 6371 * (10 ** 3)
        # Снятие начальных данных и интегрирование
        # Параметры начальной орбиты
        omega_0 = float(self.ent_begin_pericenter.get())
        e_0 = float(self.ent_begin_exc.get())
        sma_0 = float(self.ent_begin_poluos.get())
        u_0 = float(self.ent_begin_shyrota.get())

        # Параметры КА и конечное время
        m_0_r = float(self.ent_KA_mass.get())
        c_0_r = float(self.ent_KA_c.get())
        p_0_r = float(self.ent_KA_P.get())
        t_razmernoe = float(self.ent_time.get())
        # Сопряженные
        sopr_p_r = float(self.ent_sopryazh_P_r.get())
        sopr_b = float(self.ent_sopryazh_B.get())
        sopr_lam = float(self.ent_sopryazh_lam.get())

        # Формирование начальных данных _ величины размерные
        par = sma_0 * (1 - (e_0 ** 2)) * 1000
        # print(f'par{par}: {sma_0} * (1 - {e_0} ^ 2)')
        r_0 = par / (1 + e_0 * cos((u_0 - omega_0) * pi / 180))  # {r}
        self.plot_r_0 = r_0
        fi_0 = u_0 * (pi / 180)  # {fi}
        v_r0 = sqrt(mu_zemli / par) * e_0 * sin((u_0 - omega_0) * pi / 180)
        # {V_r}
        v_fi_0 = (sqrt(mu_zemli / par) * (1 + e_0 * cos((u_0 - omega_0) * pi /
                  180)))  # Vfi
        # print([r_0, fi_0, v_r0, v_fi_0])
        #  СОПРЯЖЕННЫЕ
        m_0 = 0  # {m}
        # sopr_p_r = 1                                                 # {P_r}
        sopr_p_fi = 0  # {Pfi}
        sopr_p_vr = sopr_b * sin(sopr_lam * pi / 180)  # {P_Vr}
        sopr_p_vfi = sopr_b * cos(sopr_lam * pi / 180)  # {P_Vfi}
        sopr_p_m = -1  # {P_m}
        t_0 = 0  # {t}

        # Перевод переменных в безразмерные и полярные величины

        koef_bezr = sqrt(mu_zemli / r_0)
        a_r = p_0_r / m_0_r
        c = c_0_r / koef_bezr
        a = a_r * ((r_0 ** 2) / mu_zemli)

        y_0_list = [0.0] * 11

        y_0_list[0] = r_0 / r_0
        y_0_list[1] = fi_0
        y_0_list[2] = v_r0 / koef_bezr
        y_0_list[3] = v_fi_0 / koef_bezr
        y_0_list[4] = m_0
        y_0_list[5] = sopr_p_r
        y_0_list[6] = sopr_p_fi
        y_0_list[7] = sopr_p_vr
        y_0_list[8] = sopr_p_vfi
        y_0_list[9] = sopr_p_m
        y_0_list[10] = t_0

        t_k_bezr = t_razmernoe * 3600 * 24 * koef_bezr / r_0
        self.koef_for_time = 3600 * 24 * koef_bezr / r_0
        shag_rk = float(self.shag.get())
        pogr_rk = float(self.pogreshnost.get())

        # Запись данных для Ньютона
        self.y_0_new = y_0_list.copy()
        self.ac_new.append(a)
        self.ac_new.append(c)
        self.t_new = t_k_bezr
        self.h_new.append(shag_rk)
        self.h_new.append(pogr_rk)
        self.a_k = (float(self.ent_end_poluos.get()) * 1000) / r_0
        self.e_k = float(self.ent_end_exc.get())
        # Рунге-Кутта
        Mathem(a, c).rk_db(y_0_list, t_k_bezr, [shag_rk, pogr_rk])
        self.get_dannye()
        self.root.update()
        for n in self.dannye_test:
            self.result_table.insert("", END, values=n)
        showinfo(title='Информация', message='Интегрирование завершено')
        self.tabs_control.select(self.tab_2)

    def get_newton(self):  # Оптимизация перелета методом Ньютона
        self.lbl_bar.delete(1.0, END)
        self.lbl_bar.insert(END, f"0.0")
        self.progress['value'] = 0
        self.root.update()
        self.key = 0
        self.n_new = 1
        self.i_new = 0
        var_progress = 0
        var_progress_2 = 0
        message_ = 'Оптимизация завершена!'
        # Считывание данных
        # Сопряженные
        new_sopr_p_r = float(self.ent_sopryazh_P_r.get())
        new_sopr_b = float(self.ent_sopryazh_B.get())
        new_sopr_lam = float(self.ent_sopryazh_lam.get()) * (pi / 180)
        x_newton = [new_sopr_p_r, new_sopr_b, new_sopr_lam]

        # Параметры расчетов
        self.new_del = [
            [float(self.ent_koef_nev_1.get()),
             float(self.ent_pryrash_1.get()),
             float(self.ent_tochnost_1.get()),
             float(self.ent_ogran_1.get())],

            [float(self.ent_koef_nev_2.get()),
             float(self.ent_pryrash_2.get()),
             float(self.ent_tochnost_2.get()),
             float(self.ent_ogran_2.get())],

            [float(self.ent_koef_nev_3.get()),
             float(self.ent_pryrash_3.get()),
             float(self.ent_tochnost_3.get()),
             float(self.ent_ogran_3.get())]
        ]
        # Цикл обращения к Ньютону
        while self.n_new <= 200:
            if self.key == 0:
                x = Newton(self.ac_new[0], self.ac_new[1],
                           x_newton,
                           self.y_0_new, self.t_new, self.h_new,
                           self.new_del, [self.a_k, self.e_k])
                if self.n_new == 1:
                    var_progress = x.summarnaya_2
                    var_progress_2 = var_progress
                if len(x.vivod) < 5:
                    pass
                else:
                    # Вывод результатов на выходе из Ньютона (если
                    # оптимизация дала результат лучше, чем на прошлом шаге)
                    self.ent_vivod.insert(END,
                                          f'Шаг {self.n_new}: {x.vivod}\n')
                    self.ent_nevyaz_p_r.delete(1.0, END)
                    self.ent_nevyaz_b.delete(1.0, END)
                    self.ent_nevyaz_lam.delete(1.0, END)
                    self.ent_nevyaz_p_r.insert(END, f"{x.xn[0]}")
                    self.ent_nevyaz_b.insert(END, f"{x.xn[1]}")
                    self.ent_nevyaz_lam.insert(END,
                                               f"{x.xn[2] * 180 / pi}")
                    # Обновление полосы прогресса
                    param = min(
                        self.new_del[0][2],
                        self.new_del[1][2],
                        self.new_del[2][2]
                    )
                    progress_2 = (
                                  (var_progress_2 - x.summarnaya) /
                                  (var_progress_2 - param))
                    if progress_2 > var_progress:
                        self.lbl_bar.delete(1.0, END)
                        self.lbl_bar.insert(END, f"{progress_2 * 100:.1f}")
                        var_progress = progress_2
                        self.progress['value'] = int(var_progress * 100)
                    self.root.update()

                self.fun()
                self.n_new += 1
            else:
                break
            if x.ExitResult == 2:
                self.lbl_bar.delete(1.0, END)
                self.lbl_bar.insert(END, f"{100}")
                self.progress['value'] = 100
                message_ = 'Решение не найдено :('
                self.root.update()
                break
            elif x.ExitResult == 0:
                self.lbl_bar.delete(1.0, END)
                self.lbl_bar.insert(END, f"{100}")
                self.progress['value'] = 100
                message_ = 'Успешный выход! Поздравляем!'
                self.root.update()
                break
            else:
                continue
        self.ent_vivod.insert(END,
                              '_'*95)
        showinfo(title='Информация', message=f'{message_}')

    def stop_newton(self):
        if self.key == 0:
            self.key = 1
        else:
            self.key = 0

    def fun(self):
        if self.i_new < 7:
            for i in range(3):
                self.new_del[i][1] /= 10
            self.i_new += 1

        elif self.i_new >= 7:
            for i in range(3):
                self.new_del[i][1] /= 10
            self.i_new = 0

    def run_window(self):  # Прорисовка окна и всех виджетов
        self.draw_widgets()
        self.root.mainloop()


if __name__ == "__main__":  # Запуск программы
    window = Window(900, 550)
    window.run_window()
