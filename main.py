import time
import os
from sys import exit as sysexit
from datetime import timedelta
import pickle
# from pprint import pprint


from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window

WORK_TIME_FILE = "worktime_data.dat"
ROUTE_FILE = "routes_data.dat"



"""Директория main.py"""
dir_name = os.getcwd()

def load_HDDfile(open_file):
    try:
        with open(os.path.join(dir_name,open_file), 'rb') as file:
            file_dict = pickle.load(file)
            print("Успешно открыт: ",open_file)
            return file_dict
    except (FileNotFoundError, IOError, EOFError):
        # Код одноразовый для первого запуска программы
        print("Не открылся: ",open_file," Создался пустой")
        with open(os.path.join(dir_name, open_file), 'wb') as obj:
            file_dict = {}
            pickle.dump(file_dict, obj)
            return file_dict

def save_HDD_DICT(dictionary:dict, name_file:str):
    with open(os.path.join(dir_name,name_file), 'wb') as file:
        pickle.dump(dictionary, file)



DICT_TIME = load_HDDfile(WORK_TIME_FILE)
DICT_ROUTE = load_HDDfile(ROUTE_FILE)



# print("DICT_TIME_STATISTIC############")
# pprint(DICT_TIME)
# print("+++++++++++++++++++++++++++++++++")
# print("DICT_ROUTE ####################")
# pprint(DICT_ROUTE)
# print("+++++++++++++++++++++++++++++++++")

month_lst = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
             'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

time_now = time.time()  # Секунды с начала эпохи
time_day = time.localtime(time_now)  # Текущее число

if time.strftime("%d", time_day)[0] == "0":
    CURRENT_DAY = time.strftime("%d", time_day)[1]
else:
    CURRENT_DAY = time.strftime("%d", time_day)

number_month = int(time.strftime("%m", time_day))
CURRENT_MONTH = month_lst[number_month - 1]



def exchange_worktime(sec):
    td = timedelta(seconds=sec)    
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if td.days > 0:
        hours = hours + td.days * 24
    return hours,minutes
    
    
def get_all_worktime(all_date):
    all_seconds = timedelta()#timedelta(hours=0, minutes=0)
    for data in all_date:
        hour = int(DICT_TIME[data][1][0])
        minutes = int(DICT_TIME[data][1][1])
        obj_time = timedelta(hours=hour, minutes=minutes)
        all_seconds+=obj_time
    total_sec = all_seconds.total_seconds()
    tot_work_time = exchange_worktime(total_sec)
    return tot_work_time

def get_all_dates_from_choice_month(choice_month) -> list:
    list_month = []  # Только даты выбранного месяца
    for i in DICT_TIME:  # Получаем в i ключи словаря
        if i.split()[1] == choice_month:  # Определяем нужный месяц из списка. Вычленяем название месяца
            list_month.append(i)  # Записываем в список только даты с нужным месяцем
    return list_month


def checking_the_time(hours,minutes):
    if hours.isdigit() and minutes.isdigit():
        return hours.zfill(2) + ":" + minutes.zfill(2)
    else:
        return "00 : 00"

def calculate_work_time(time_args:(tuple,list))->str :
    Hour_start_work = int(time_args[0])
    Hour_end_work = int(time_args[2])
    Min_start_work = int(time_args[1])
    Min_end_work = int(time_args[3])
    Hour_start_lunch = int(time_args[4])
    Min_start_lunch = int(time_args[5])
    Hour_end_lunch = int(time_args[6])
    Min_end_lunch = int(time_args[7])

    time_start_lunch = timedelta(hours=Hour_start_lunch, minutes=Min_start_lunch)
    time_end_lunch = timedelta(hours=Hour_end_lunch, minutes=Min_end_lunch)
    difference_time_lunch = time_end_lunch - time_start_lunch
    time_start_work = timedelta(hours=Hour_start_work, minutes=Min_start_work)
    time_end_work = timedelta(hours=Hour_end_work, minutes=Min_end_work)

    time_work_str = str((time_end_work - time_start_work) - difference_time_lunch)
    total_time_work = time_work_str.split()[-1] # time_work_str [-1 day, 23:00:00]
    return total_time_work

def check_value_is_numeric(value:(tuple,list))->bool:
    try:
        list(map(int,value))
        return True
    except (ValueError,TypeError):
        return False

def get_route(route_str:str):
    try:
        route,karta = route_str.split("/")
        return route,karta
    except ValueError:
        route, karta = "Не введён", ""
        return route, karta

def check_route_in_dict(route) -> list:
    try:
        time_in_route = DICT_ROUTE[route]
        return time_in_route
    except KeyError:
        return ["", "", "", ""]

def get_karta(day):
    try:
        route_and_karta = DICT_TIME[day][0].split("/")
        return route_and_karta[0],route_and_karta[1],
    except (KeyError,IndexError):
        return "Не введён", ""

def get_karta_worktime(day):
    try:
        hours_and_min = DICT_TIME[day][1]
        return hours_and_min[0],hours_and_min[1]
    except KeyError:
        return "",""

def key_input(window, key, scancode, codepoint, modifier):
    if key == 27:
        sysexit()

################################################################################
################################################################################
################################################################################

class PagesManager(MDScreenManager):
    Window.bind(on_keyboard=key_input)



class Page_main(MDScreen):
    """Читай переменные. Их имена обо всём говорят."""
    day_spinner = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)
    month_spinner_lst = ListProperty(month_lst)

    total_hours_work = StringProperty("0")
    total_minutes_work = StringProperty("0")

    date_total_time = StringProperty(CURRENT_DAY + " " + CURRENT_MONTH)

    lab_save_txt = StringProperty("Отработано:")
    key_dict_total_data = CURRENT_DAY + " " + CURRENT_MONTH

    def __init__(self, **kwargs):
        MDScreen.__init__(self, **kwargs)
    # @staticmethod
    # def show_DICT():
    #     print("DICT_TIME #########################################")
    #     pprint(DICT_TIME)
    #     print("DICT_ROUTE_WKDAY #########################################")
    #     pprint(DICT_ROUTE)
    #     print("+++++++++++++++++++++++++++++++++")

    def show_statistic(self):
        current_date = self.get_user_choice_date()
        MyPopup_page_stat(current_date).open()

    def change_data(self):
        day = self.ids.spinner_day.text
        month = self.ids.spinner_month.text
        self.date_total_time = day + " " + month


    def get_button_smena(self):
        if self.ids.sm_1.state == "down":
            return 0
        elif self.ids.sm_2.state == "down":
            return 1
        else:
            self.ids.sm_2.state = "normal"
            self.ids.sm_2.font_size = "15sp"
            self.ids.sm_1.font_size = "35sp"
            self.ids.sm_1.state = "down"
            return 0


    def get_user_choice_date(self):
        day = self.ids["spinner_day"].text
        month = self.ids["spinner_month"].text
        return day + " " + month

    def search_rout_in_dict(self):
        route_and_karta = self.get_route_user_choice()
        smena = self.get_button_smena()
        if route_and_karta in DICT_ROUTE:
            MyPopup_install_time(route_and_karta,
                                 smena,
                                 self.install_time_in_textinput)
        all_time_user_input: list = self.get_all_time_user_input()  # возвр все часы\минуты
        if check_value_is_numeric(all_time_user_input):
            self.turn_on_button_create_route()

    def install_time_in_textinput(self, HW_start, MW_start, HW_end, MW_end, HL_start, ML_start, HL_end, ML_end):
        tuple_input_time = ("startworkhours","startworkminutes",
                            "hoursendwork","minutesendwork",
                            "hoursstartlunch","minutesstartlunch",
                            "hoursendlunch","minutesendlunch")
        for textinput_name in tuple_input_time:
            self.ids[textinput_name].font_size = "30sp"
            self.ids[textinput_name].bold = True
            self.ids[textinput_name].text_color_normal = (1,0,0)


        self.ids["startworkhours"].text = HW_start
        self.ids["startworkminutes"].text = MW_start

        self.ids["hoursendwork"].text = HW_end
        self.ids["minutesendwork"].text = MW_end
        # Обед начало
        self.ids["hoursstartlunch"].text = HL_start
        self.ids["minutesstartlunch"].text = ML_start
        # Обед конец
        self.ids["hoursendlunch"].text = HL_end
        self.ids["minutesendlunch"].text = ML_end

    def get_all_time_user_input(self) -> list:
        all_time_textinput_list = [""] * 8
        # Начало раб.дня
        all_time_textinput_list[0] = self.ids["startworkhours"].text
        all_time_textinput_list[1] = self.ids["startworkminutes"].text
        # Конец раб.дня
        all_time_textinput_list[2] = self.ids["hoursendwork"].text
        all_time_textinput_list[3] = self.ids["minutesendwork"].text
        # Обед начало
        all_time_textinput_list[4] = self.ids["hoursstartlunch"].text
        all_time_textinput_list[5] = self.ids["minutesstartlunch"].text
        # Обед конец
        all_time_textinput_list[6] = self.ids["hoursendlunch"].text
        all_time_textinput_list[7] = self.ids["minutesendlunch"].text
        return all_time_textinput_list # [x.zfill(2) for x in all_time_textinput_list]

    def get_route_user_choice(self):
        route = self.ids["route_number_textinput"].text
        karta = self.ids["karta_route_number_textinput"].text
        if route.isnumeric() and karta.isnumeric():
            return route + "/" + karta
        else:
            return "Не введён"

    def install_total_working_time(self,work_time):
        tot_time = work_time.split(":")
        self.total_hours_work = tot_time[0]
        self.total_minutes_work = tot_time[1]

    def turn_on_button_create_route(self):
        if self.get_route_user_choice() != "Не введён":
            self.ids.create_route.disabled = False
        else:
            self.ids.create_route.disabled = True

    def calculation_of_working(self):
        all_time_user_input:list = self.get_all_time_user_input() # возвр все часы\минуты
        if check_value_is_numeric(all_time_user_input):
            total_time = calculate_work_time(all_time_user_input)
            self.install_total_working_time(total_time)
            self.ids.save_button.disabled = False
            self.turn_on_button_create_route()
        else:
            self.ids.save_button.disabled = True
            self.ids.create_route.disabled = True
            self.total_hours_work = "0"
            self.total_minutes_work = "00"

    def intercept_and_save_alldata(self):
        KEY: str = self.get_user_choice_date() # возвр дату => "23 Май"
        route_and_karta_in_day: str = self.get_route_user_choice() # возвр маршрут => 102/4 или "Не введён"
        all_time_user_input:list = self.get_all_time_user_input() # возвр все часы\минуты
        label_save_text = self.ids.savingtext
        if KEY not in DICT_TIME:
            DICT_TIME[KEY] = (route_and_karta_in_day,
                              (self.total_hours_work, self.total_minutes_work),
                              all_time_user_input)
            save_HDD_DICT(DICT_TIME, WORK_TIME_FILE)
            self.change_save_text_label()
        else:
            MyPopup_save_new_workday(KEY, route_and_karta_in_day, (self.total_hours_work, self.total_minutes_work),
                                     all_time_user_input, label_save_text)


    def create_route_kart(self):
        num_route:str = self.get_route_user_choice() # Получ.маршрут 102/4
        all_time_route:list = self.get_all_time_user_input() # Получ.время маршрута
        if int(all_time_route[0]) < 12:
            smena = 0
        else:
            smena = 1
        list_time_in_route:list = check_route_in_dict(num_route)
        label_savetext = self.ids.savingtext
        """Popup Вопрос: карта выходного или буднего дня"""
        MyPopup_new_route(num_route,all_time_route,smena,list_time_in_route,label_savetext)


    def my_callback(self, instance):
        self.ids.savingtext.text_color = "black"
        self.ids.savingtext.text = "Отработано:"
        return False

    def change_save_text_label(self):
        Clock.schedule_once(self.my_callback, 2)
        # self.label.theme_text_color = "Custom"
        self.ids.savingtext.text_color = "red"
        self.ids.savingtext.text = "Сохранено"


class MyPopup_install_time(Popup):
    Builder.load_file(os.path.join(dir_name, "popup_install_time.kv"))
    def __init__(self,route:str,smena:int,install_func,**kwargs):
        Popup.__init__(self, **kwargs)
        self.KEY = route
        self.smena = smena
        self.INSTALL_FUNC = install_func
        self.open()

    def weekday(self):
        try:
            list_time = DICT_ROUTE[self.KEY][self.smena]
            HW_start = list_time[0]
            MW_start = list_time[1]
            HW_end = list_time[2]
            MW_end = list_time[3]
            HL_start = list_time[4]
            ML_start = list_time[5]
            HL_end = list_time[6]
            ML_end = list_time[7]
            self.INSTALL_FUNC(HW_start,MW_start,
                              HW_end,MW_end,
                              HL_start,ML_start,
                              HL_end,ML_end)
        except IndexError:
            self.INSTALL_FUNC(HW_start="-", MW_start="-",
                              HW_end="-", MW_end="-",
                              HL_start="-", ML_start="-",
                              HL_end="-", ML_end="-")
        self.dismiss()

    def weekend(self):
        self.smena += 2
        try:
            list_time = DICT_ROUTE[self.KEY][self.smena]
            HW_start = list_time[0]
            MW_start = list_time[1]
            HW_end = list_time[2]
            MW_end = list_time[3]
            HL_start = list_time[4]
            ML_start = list_time[5]
            HL_end = list_time[6]
            ML_end = list_time[7]
            self.INSTALL_FUNC(HW_start, MW_start,
                              HW_end, MW_end,
                              HL_start, ML_start,
                              HL_end, ML_end)
        except IndexError:
            self.INSTALL_FUNC(HW_start= "-", MW_start= "-",
                              HW_end= "-", MW_end= "-",
                              HL_start= "-", ML_start= "-",
                              HL_end= "-", ML_end= "-")
        self.dismiss()





class MyPopup_save_new_workday(Popup):

    curr_data = StringProperty()
    route_str = StringProperty()
    karta_str = StringProperty()
    start_work = StringProperty()
    end_work = StringProperty()
    start_lunch = StringProperty()
    end_lunch = StringProperty()

    Builder.load_file(os.path.join(dir_name, "popup_new_day.kv"))
    def __init__(self,date,route,tot_work_time,lst_time, lab,**kwargs):
        Popup.__init__(self, **kwargs)
        self.KEY = date
        self.total_work_time = tot_work_time
        self.route = route
        self.list_time = lst_time
        self.install_time_work_in_labels()
        self.label = lab
        self.curr_data = date
        self.open()

    def install_time_work_in_labels(self):
        route_and_karta = DICT_TIME[self.KEY][0]
        self.route_str, self.karta_str = get_route(route_and_karta)
        list_time = DICT_TIME[self.KEY][2]
        self.start_work = checking_the_time(list_time[0],list_time[1])
        self.end_work = checking_the_time(list_time[2],list_time[3])
        self.start_lunch = checking_the_time(list_time[4],list_time[5])
        self.end_lunch = checking_the_time(list_time[6],list_time[7])

    def answer_ok(self):
        DICT_TIME[self.KEY] = (self.route, self.total_work_time, self.list_time)
        save_HDD_DICT(DICT_TIME, WORK_TIME_FILE)
        self.change_save_text_label()
        self.dismiss()


    def my_callback(self, ins):
        self.label.text_color = "black"
        self.label.text = "Отработано:"
        return False

    def change_save_text_label(self):
        Clock.schedule_once(self.my_callback, 2)
        self.label.text_color = "red"
        self.label.text = "Сохранено"

class MyPopup_new_route(Popup):
    Builder.load_file(os.path.join(dir_name, "popup_new_route.kv"))
    def __init__(self, num_route, all_time_new, smena, all_time_route:list["","","",""],lab, **kwargs):
        Popup.__init__(self, **kwargs)
        self.num_route = num_route
        self.all_time_new = all_time_new
        self.smena = smena
        self.all_time_route:list = all_time_route
        self.label_savetext = lab
        self.open()

    def weekday(self):
        if not self.all_time_route[self.smena]:
            self.all_time_route[self.smena] = self.all_time_new
            DICT_ROUTE[self.num_route] = self.all_time_route
            save_HDD_DICT(DICT_ROUTE, ROUTE_FILE)
            self.change_save_text_label()
        else:
            MyPopup_change_route(self.num_route, self.all_time_new, self.smena,self.label_savetext)


    def weekend(self):
        """Выходной день- индекс для списка маршрута self.smena + 2"""
        self.smena += 2
        if not self.all_time_route[self.smena]:
            self.all_time_route[self.smena] = self.all_time_new
            DICT_ROUTE[self.num_route] = self.all_time_route
            save_HDD_DICT(DICT_ROUTE, ROUTE_FILE)
            self.change_save_text_label()
        else:
            MyPopup_change_route(self.num_route, self.all_time_new, self.smena, self.label_savetext)


    def my_callback(self, ins):
        self.label_savetext.text_color = "black"
        self.label_savetext.text = "Отработано:"
        return False

    def change_save_text_label(self):
        Clock.schedule_once(self.my_callback, 3)
        self.label_savetext.text_color = "red"
        self.label_savetext.text = "Сохранено"

class MyPopup_change_route(Popup):
    route_str = StringProperty()
    karta_str = StringProperty()

    start_work = StringProperty()
    end_work = StringProperty()
    start_lunch = StringProperty()
    end_lunch = StringProperty()

    Builder.load_file(os.path.join(dir_name, "popup_change_route.kv"))
    def __init__(self, route_key, new_array_time, smena:int,lab, **kwargs):
        Popup.__init__(self, **kwargs)
        self.key = route_key
        self.route_str, self.karta_str = route_key.split("/")
        self.new_array_time = new_array_time
        self.smena:int = smena
        self.pars_dict_old_route()
        self.label_savetext = lab
        self.open()

    def pars_dict_old_route(self):
        """Ф-ция устанавливает время старого маршрута в Popup для
        ознакомления пользователя, что он меняет."""
        self.start_work = checking_the_time(DICT_ROUTE[self.key][self.smena][0],DICT_ROUTE[self.key][self.smena][1])
        self.end_work = checking_the_time(DICT_ROUTE[self.key][self.smena][2],DICT_ROUTE[self.key][self.smena][3])
        self.start_lunch = checking_the_time(DICT_ROUTE[self.key][self.smena][4],DICT_ROUTE[self.key][self.smena][5])
        self.end_lunch = checking_the_time(DICT_ROUTE[self.key][self.smena][6],DICT_ROUTE[self.key][self.smena][7])

    def answer_ok(self):
        DICT_ROUTE[self.key][self.smena] = self.new_array_time
        save_HDD_DICT(DICT_ROUTE, ROUTE_FILE)
        self.change_save_text_label()
        self.dismiss()

    def my_callback(self, instance):
        self.label_savetext.text_color = "black"
        self.label_savetext.text = "Отработано:"
        return False

    def change_save_text_label(self):
        Clock.schedule_once(self.my_callback, 3)
        self.label_savetext.text_color = "red"
        self.label_savetext.text = "Сохранено"

class MyPopup_page_stat(Popup):
    curr_date = StringProperty()
    title = StringProperty()
    quant_day = StringProperty()
    route = StringProperty()
    karta = StringProperty()
    tot_hours = StringProperty()
    tot_min = StringProperty()
    karta_hours = StringProperty()
    karta_min = StringProperty()
    Builder.load_file(os.path.join(dir_name,"popup_statistic.kv"))
    def __init__(self,title_date, **kwargs):
        Popup.__init__(self, **kwargs)
        self.title = title_date.split()[1]
        self.curr_date = title_date
        self.install_statistic()

    def install_statistic(self):
        all_dates = get_all_dates_from_choice_month(self.title)
        self.quant_day = str(len(all_dates))
        total_worktime = get_all_worktime(all_dates)
        self.tot_hours = str(total_worktime[0])
        self.tot_min = str(total_worktime[1])
        self.route, self.karta = get_karta(self.curr_date)
        self.karta_hours, self.karta_min = get_karta_worktime(self.curr_date)

class RouteTextInput(MDTextField):
    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)
    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if len(self.text) < 3:
                return super().insert_text(value, from_undo=from_undo)
    def on_focus(self, inst, args):
        if args:
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "35sp"
        else:
            if not self.text:
                self.parent.md_bg_color = self.parent_color
                self.font_size = "15sp"
                self.text = "Маршрут"

class KartaTextInput(MDTextField):
    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)
    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if len(self.text) < 2:
                return super().insert_text(value, from_undo=from_undo)
    def on_focus(self, inst, args):
        if args:
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "35sp"
        else:
            if not self.text:
                self.parent.md_bg_color = self.parent_color
                self.font_size = "18sp"
                self.text = "Карта"

class HoursTextInput(MDTextField):
    def __init__(self, **kwargs):
        super(HoursTextInput, self).__init__(**kwargs)
        self.mode = "outlined"
        self.multiline = False
        self.halign = "center"
        self.bold = True
        self.theme_text_color = "Custom"


    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.text = ""
    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if len(self.text) < 2:
                if len(self.text) == 0:
                    if int(value) >= 3:
                       return super().insert_text("0"+value, from_undo=from_undo)
                    elif int(value) < 3:
                       return super().insert_text(value, from_undo=from_undo)
                elif len(self.text) > 0:
                    if self.text == "1":
                        return super().insert_text(value, from_undo=from_undo)
                    elif self.text == "2" and int(value) < 5:
                        return super().insert_text(value, from_undo=from_undo)

    def on_focus(self, inst, args):
        if args:
            self.text_color_normal = "black"
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "30sp"
        else:
            if not self.text:
                self.text_color_normal = "black"
                self.parent.md_bg_color = self.parent_color
                self.font_size = "20sp"
                self.text = "Час"

class MinutesTextInput(MDTextField):
    def __init__(self, **kwargs):
        super(MinutesTextInput, self).__init__(**kwargs)
        self.mode = "outlined"
        self.multiline = False
        self.halign = "center"
        self.bold = True
        self.theme_text_color = "Custom"

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.text = ""

    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if len(self.text) < 2:
                if len(self.text) == 0:
                    if int(value) < 6:
                       return super().insert_text(value, from_undo=from_undo)
                elif len(self.text) == 1:
                    return super().insert_text(value, from_undo=from_undo)



    def on_focus(self, inst, args):
        if args:
            self.text_color_normal = "black"
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "30sp"
        else:
            if not self.text:
                self.text_color_normal = "black"
                self.parent.md_bg_color = self.parent_color
                self.font_size = "18sp"
                self.text = "Мин"

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Light Dark
        self.theme_cls.primary_palette = "Olive"  # "Teal" #"Purple" # , "Red" "Olive"
        # Window.clearcolor = (.8, .8, .8)
        Builder.load_file(os.path.join(dir_name, "main_kv.kv"))
        scm = PagesManager()
        scm.add_widget(Page_main())
        return scm



if __name__ == '__main__':
    MyApp().run()
