# class MyList(list):
#     def __getitem__ (self, offset):
#         return list.__getitem__ (self, offset - 1)

# class MyTuggButton(ToggleButton):
#     btn1 = ToggleButton(text='Male', group='sex', pos=(100, 100))
#     btn2 = ToggleButton(text='Female', group='sex', state='down', pos=(100, 200))


import time
import os
from datetime import timedelta
import pickle
from pprint import pprint
import re

from sys import platform
if platform == "win32":
    os.environ["KCFG_GRAPHICS_BORDERLESS"] = "0"


from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window

# os.path.join(dir_name,FILE_STATISTIC_NAME


WORK_TIME_FILE = "worktime_data.dat"
ROUTE_FILE_SM_1 = "route_sm_1.dat"
ROUTE_FILE_SM_2 = "route_sm_2.dat"

"""Директория main.py"""
dir_name = os.getcwd()

def load_HDDfile_time():
    try:
        with open(os.path.join(dir_name,WORK_TIME_FILE), 'rb') as file:
            file_dict = pickle.load(file)
            print("Успешно открыт worktime_data.dat")
            return file_dict
    except (FileNotFoundError, IOError, EOFError):
        # Код одноразовый для первого запуска программы
        print("Не открылся worktime_data.dat. Создался пустой")
        with open(os.path.join(dir_name, "worktime_data.dat"), 'wb') as obj:
            file_dict = {}
            pickle.dump(file_dict, obj)
    return file_dict


def load_HDDfile_route(sm):
    if sm == 1:
        open_file = ROUTE_FILE_SM_1
    elif sm == 2:
        open_file = ROUTE_FILE_SM_2
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


DICT_TIME_STATISTIC = load_HDDfile_time()
# DICT_TIME_STATISTIC = {}
DICT_ROUT_1 = load_HDDfile_route(1)
# DICT_ROUT = {}
DICT_ROUT_2 = load_HDDfile_route(2)
pprint(DICT_ROUT_1)
print("#########################################")
pprint(DICT_ROUT_2)
print("+++++++++++++++++++++++++++++++++")
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


class PagesManager(MDScreenManager):
    def __init__(self, **kwargs):
        MDScreenManager.__init__(self, **kwargs)

    def on_touch_down(self, touch):
        self.tap_X_Down = touch.x
        self.tap_Y_Down = touch.y
        return super(PagesManager, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.tap_X_Up = touch.x
        self.tap_Y_Up = touch.y
        if (self.tap_X_Down - self.tap_X_Up) > 100:
            if self.current == "main_screen":
                self.transition = SlideTransition()
                self.transition.direction = "left"
                self.current = "main_page"

        if self.tap_X_Down < self.tap_X_Up:
            if self.current == "main_page":
                self.transition = SlideTransition()
                self.transition.direction = "right"
                self.current = "main_screen"

        if (self.tap_Y_Down - self.tap_Y_Up) > 100:
            if self.current == "main_page":
                self.transition.direction = "down"
                self.current = "setting_page"
        return super(PagesManager, self).on_touch_up(touch)

def checking_the_time(hours,minutes):
    if hours.isdigit() and minutes.isdigit():
        return hours + ":" + minutes
    else:
        return "00 : 00"

def calculate_work_time(time_args:tuple[str,str,str,str,str,str,str,str])->str :
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
    total_time_work = time_work_str.split()[-1]
    return total_time_work

def get_route_and_karta(route,karta):
    return route + "/" + karta

def check_value_numeric(value:tuple)->bool:
    try:
        list(map(int,value))
        return True
    except (ValueError,TypeError):
        return False
def check_smena(start_time):
    if int(start_time) < 12:
        return DICT_ROUT_1,ROUTE_FILE_SM_1
    else:
        return DICT_ROUT_2,ROUTE_FILE_SM_2







##################################################################
##########################################################################
#################################################################
class WordSave_or_Time(MDLabel):
    def __init__(self, **kwargs):
        super(WordSave_or_Time, self).__init__(**kwargs)
        # self.role = "small"
        #  self.size_hint = (1, 1)
        self.font_style = "Title"
        self.bold = True
        self.text_size = self.size
        self.halign = "center"
        self.valign = "center"



class Create_route_kart(MDScreen):
    Builder.load_file(os.path.join(dir_name, "create_kart.kv"))
    ROUTE_STR = StringProperty("")
    KARTA_STR = StringProperty("")
    def __init__(self, **kwargs):
        super(Create_route_kart, self).__init__(**kwargs)
        self.total_time = ""
        self.box_word_save = MDBoxLayout(WordSave_or_Time(text="Сохранено",
                                                          text_color = "red",
                                                          role = "large"))

    def create_box_total_time(self):
        tot_time = self.total_time.split(":")
        self.time_and_save_box.clear_widgets()
        box_total_time = MDBoxLayout(WordSave_or_Time(text="Отработка:", size_hint_x=.3, role="small"),
                                          WordSave_or_Time(text=tot_time[0], size_hint_x=.1, role="large",
                                                           text_color="red"),
                                          WordSave_or_Time(text="часов", size_hint_x=.2, role="small"),
                                          WordSave_or_Time(text=tot_time[1], size_hint_x=.1, role="large",
                                                           text_color="red"),
                                          WordSave_or_Time(text="минут", size_hint_x=.2, role="small"))
        self.time_and_save_box.add_widget(box_total_time)




    def get_all_time_textinput(self)->list:
        all_time_textinput_list = [""] * 8

        all_time_textinput_list[0] = self.ids.start_hour_smena_input.text
        all_time_textinput_list[1] = self.ids.start_minutes_smena_input.text

        all_time_textinput_list[2] = self.ids.end_hours_smena_input.text
        all_time_textinput_list[3] = self.ids.end_minutes_smena_input.text

        all_time_textinput_list[4] = self.ids.start_lunch_hours_input.text
        all_time_textinput_list[5] = self.ids.start_lunch_minutes_input.text

        all_time_textinput_list[6] = self.ids.end_lunch_hours_input.text
        all_time_textinput_list[7] = self.ids.end_lunch_minutes_input.text
        return all_time_textinput_list


    def collecting_route_data(self):
        route = self.ids.route_input.text
        karta = self.ids.karta_input.text

        if check_value_numeric((route,karta)):
            self.ROUTE_STR = route
            self.KARTA_STR = karta



        all_time:list = self.get_all_time_textinput() # Получение всех TextInput

        self.ids.start_smena_time_label.text = checking_the_time(all_time[0],all_time[1])
        self.ids.end_smena_time_label.text = checking_the_time(all_time[2],all_time[3])
        self.ids.start_lunch_label.text = checking_the_time(all_time[4],all_time[5])
        self.ids.end_lunch_label.text = checking_the_time(all_time[6],all_time[7])
        tuple_correct_time = (route,
                              karta,
                              all_time[0],all_time[1],all_time[2],all_time[3],
                              all_time[4],all_time[5],all_time[6],all_time[7])

        if check_value_numeric(tuple_correct_time):
            self.total_time: str = calculate_work_time(tuple_correct_time[2:])
            self.create_box_total_time()
            self.ids.save_button.disabled = False
        else:
            self.ids.save_button.disabled = True

    def intercept_and_save_data(self):
        all_time: list = self.get_all_time_textinput()
        dict_and_file_for_record:tuple[dict,str] = check_smena(all_time[0])
        DICT = dict_and_file_for_record[0]
        FILE = dict_and_file_for_record[1]
        route = self.ids.route_input.text
        karta = self.ids.karta_input.text
        KEY = get_route_and_karta(route,karta)
        print(KEY)
        if KEY not in DICT:
            DICT[KEY] = all_time
            save_HDD_DICT(DICT, FILE)
            self.change_word_save()
        else:
            print("Popup")
            MyPopup_save_route(DICT,KEY,all_time).open()




    def my_callback(self,qt):
        self.time_and_save_box.clear_widgets()
        self.create_box_total_time()

    def change_word_save(self):
        Clock.schedule_once(self.my_callback, 2)
        self.time_and_save_box.clear_widgets()
        self.time_and_save_box.add_widget(self.box_word_save)

class MyPopup_save_route(Popup):
    route_str = StringProperty()
    karta_str = StringProperty()



    Builder.load_file(os.path.join(dir_name, "Popup_new_route.kv"))
    def __init__(self,dct,key,arr_time, **kwargs):
        Popup.__init__(self, **kwargs)
        self.dct = dct
        self.key = key
        self.arr_time = arr_time
        self.route_str,self.karta_str = key.split("/")














class Page_main(MDScreen):
    """Читай переменные. Их имена обо всём говорят."""
    day_spinner = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)
    month_spinner_lst = ListProperty(month_lst)

    hours_start_lunch = StringProperty("0")
    minutes_start_lunch = StringProperty("00")

    hours_end_lunch = StringProperty("0")
    minutes_end_lunch = StringProperty("00")

    hours_start_work = StringProperty("0")
    minutes_start_work = StringProperty("00")

    hours_end_work = StringProperty("0")
    minutes_end_work = StringProperty("00")

    total_hours_work = StringProperty("0")
    total_minutes_work = StringProperty("0")

    date_total_time = StringProperty(CURRENT_DAY + " " + CURRENT_MONTH)

    lab_save_txt = StringProperty("Отработано:")
    key_dict_total_data = CURRENT_DAY + " " + CURRENT_MONTH

    def __init__(self, **kwargs):
        MDScreen.__init__(self, **kwargs)

    @staticmethod
    def check_spinner_list(spinner_lst: list) -> list:
        total = sum(map(int, spinner_lst))
        if total == 0:
            return False
        else:
            return spinner_lst

    @staticmethod
    def show_DICT():
        pprint(DICT_TIME_STATISTIC)
        pprint(DICT_ROUT_1)
        pprint(DICT_ROUT_2)


    def search_rout_in_dict(self):
        route_and_karta = self.get_route_user_choice()
        if route_and_karta in DICT_ROUT_1:
            list_time = DICT_ROUT_1[route_and_karta]
            HW_start = list_time[0]
            MW_start = list_time[1]
            HW_end = list_time[2]
            MW_end = list_time[3]
            HL_start = list_time[4]
            ML_start = list_time[5]
            HL_end = list_time[6]
            ML_end = list_time[7]
            self.install_time_in_spinner(HW_start, MW_start, HW_end, MW_end, HL_start, ML_start, HL_end, ML_end)
        else:
            self.install_time_in_spinner("0", "00", "0", "00", "0", "00", "0", "00")






    def install_time_in_spinner(self, HW_start, MW_start, HW_end, MW_end, HL_start, ML_start, HL_end, ML_end):
        self.ids["startworkhours"].text = HW_start
        self.ids["startworkminutes"].text = MW_start
        # Конец раб.дня
        self.ids["hoursendwork"].text = HW_end
        self.ids["minutesendwork"].text = MW_end
        # Обед начало
        self.ids["hoursstartlunch"].text = HL_start
        self.ids["minutesstartlunch"].text = ML_start
        # Обед конец
        self.ids["hoursendlunch"].text = HL_end
        self.ids["minutesendlunch"].text = ML_end


    def incorrect_rout_or_kart(self):
        print("MyPoput()")


    def create_route_kart(self):
        spinners_list = self.get_all_time_spinners()
        spinner_correct_list = self.check_spinner_list(spinners_list)
        if not spinner_correct_list:
            return

        route_and_karta_in_day: str or False = self.get_route_user_choice()
        if not route_and_karta_in_day:
            self.incorrect_rout_or_kart()
        else:
            if int(self.ids.startworkhours.text) >= 14:
                DICT_ROUT_2[route_and_karta_in_day] = spinners_list
                print("more 14 Записываем во вторую смену")
            else:
                print("less 14 Записываем в первую смену")
                DICT_ROUT_1[route_and_karta_in_day] = spinners_list



        # else:
        #     list_all_time_spinners: list = self.get_all_time_spiners()
        #     self.save_data_in_dict_route(route_and_karta_in_day, list_all_time_spinners)



    def intercept_data_main_screen(self):
        date_choice_user: str = self.get_user_choice_date()
        total_time: tuple[str, str] = self.get_total_time_in_a_day()
        route_and_karta_in_day: str = self.get_route_user_choice()
        self.save_date_in_dict_time(date_choice_user, route_and_karta_in_day, total_time)

    def save_date_in_dict_time(self, key: str, route: str, tot_time: tuple[str, str]):
        label_text_save = self.ids["savingtext"]
        route_and_time: list = [route,tot_time]
        check_key = self.check_day_in_dict(key,flag="date")
        if check_key:
            print("Popup")
            MyPopup_save_worktime(check_key,route_and_time,label_text_save)
        else:
            print("else")
            DICT_TIME_STATISTIC[key] = route_and_time
            save_HDD_DICT_TIME(DICT_TIME_STATISTIC, "worktime_data.dat")
            self.change_save_text_label()






    def save_data_in_dict_route(self, route: str, spinners: list):
        label_text_save = self.ids["savingtext"]
        check_key = self.check_day_in_dict(route, flag=False)
        if check_key:
            MyPoput_save_route(route, spinners, label_text_save)
        else:
            DICT_ROUT_1[route] = spinners
            save_HDD_DICT_TIME(DICT_ROUT_1, "route_data.dat")
            self.change_save_text_label()

    def get_all_time_spinners(self) -> list:
        all_time_spinners_list = [""] * 8
        # Начало раб.дня
        all_time_spinners_list[0] = self.ids["startworkhours"].text
        all_time_spinners_list[1] = self.ids["startworkminutes"].text
        # Конец раб.дня
        all_time_spinners_list[2] = self.ids["hoursendwork"].text
        all_time_spinners_list[3] = self.ids["minutesendwork"].text
        # Обед начало
        all_time_spinners_list[4] = self.ids["hoursstartlunch"].text
        all_time_spinners_list[5] = self.ids["minutesstartlunch"].text
        # Обед конец
        all_time_spinners_list[6] = self.ids["hoursendlunch"].text
        all_time_spinners_list[7] = self.ids["minutesendlunch"].text
        return all_time_spinners_list

    @staticmethod
    def check_day_in_dict(key, flag):
        if flag == "date":
            if key in DICT_TIME_STATISTIC:
                return key
        if flag == "smena_1":
            if key in DICT_ROUT_1:
                return key
        if flag == "smena_2":
            if key in DICT_ROUT_2:
                return key
        else:
            return False


    def get_route_user_choice(self):
        route = self.ids["route_number_textinput"].text
        karta = self.ids["karta_route_number_textinput"].text
        if route and karta:
            return route + "/" + karta
        else:
            return False

    def get_total_time_in_a_day(self):
        hours = self.total_hours_work
        mitutes = self.total_minutes_work
        return hours, mitutes

    def get_user_choice_date(self):
        day = self.ids["spinner_day"].text
        month = self.ids["spinner_month"].text
        return day + " " + month

    def start_calculate_work_time(self):
        # Начало раб.дня
        start_work_H = self.ids["startworkhours"].text
        start_work_M = self.ids["startworkminutes"].text
        # Конец раб.дня
        end_work_H = self.ids["hoursendwork"].text
        end_work_M = self.ids["minutesendwork"].text
        # Обед начало
        start_lunch_H = self.ids["hoursstartlunch"].text
        start_lunch_M = self.ids["minutesstartlunch"].text
        # Обед конец
        end_lunch_H = self.ids["hoursendlunch"].text
        end_lunch_M = self.ids["minutesendlunch"].text

        time_tuple = (
        start_work_H, start_work_M, end_work_H, end_work_M, start_lunch_H, start_lunch_M, end_lunch_H, end_lunch_M)
        if int(start_work_H) > int(end_work_H):
            total_time_work = self.calculate_time_more_day(time_tuple)
        else:
            total_time_work = self.calculate_time_less_day(time_tuple)
        self.install_total_time_work_in_label(total_time_work)

    def install_total_time_work_in_label(self, total_time_work):
        try:
            time_struct = time.gmtime(total_time_work.total_seconds())
            self.total_hours_work = str(time_struct.tm_hour)
            self.total_minutes_work = str(time_struct.tm_min)
        except OSError:
            self.install_time_in_spinner("0", "00", "0", "00", "0", "00", "0", "00")


        day = self.ids["spinner_day"].text
        month = self.ids["spinner_month"].text
        self.date_total_time = day + " " + month






    def my_callback(self, instance):
        self.ids["savingtext"].text_color = "black"
        self.lab_save_txt = "Отработано:"
        return False

    def change_save_text_label(self):
        Clock.schedule_once(self.my_callback, 2)
        self.ids["savingtext"].theme_text_color = "Custom"
        self.ids["savingtext"].text_color = "red"
        self.lab_save_txt = "Сохранено"



class Page_stat(MDScreen):
    def __init__(self, **kwargs):
        MDScreen.__init__(self, **kwargs)

class Page_setting(MDScreen):
    pass

# def install_total_time_after_save(self):
#     tuple_time = (self.hours_start_work, self.minutes_start_work, self.hours_end_work,
#                   self.minutes_end_work, self.hours_start_lunch, self.minutes_start_lunch,
#                   self.hours_end_lunch, self.minutes_end_lunch)
#     self.work_time_calc(tuple_time)
#
# def update_statistic(self,choice_month:str=CURRENT_MONTH):
#     lst_dates_current_month = self.get_dates_from_current_month(choice_month) # Список дат с нужным месяцем
#     lst_sorted_num_current_month = self.get_num_days(lst_dates_current_month) # Список чисел нужного месяца
#     lst_keys_dates = self.create_keys_date_choice_month(lst_sorted_num_current_month) # Список ["10 Октябрь"]
#     time_statistic = self.update_total_time_statistic(lst_keys_dates) # Кортеж (170,45) часы минуты
#     lst_all_month = self.get_set_all_month()
#
#     self.install_statistic(lst_sorted_num_current_month,lst_all_month,time_statistic,choice_month)
#
# def install_statistic(self,*args):
#     self.spinner_month_statistic_lst = args[1] # Устан.всех месяцев в Spinner
#     self.total_month_spinner = args[3]  # Устан.выбранного месяца в Spinner
#     try:
#         self.from_total_days_spinner = str(args[0][0])  # Первое число месяца
#         self.to_total_days_spinner = str(args[0][-1])  # Последнее число месяца
#     except IndexError:
#         self.from_total_days_spinner = "0" # Первое число месяца, если словарь пустой!
#         self.to_total_days_spinner = "0"   # Последнее число месяца, если словарь пустой!
#
#     self.list_from_total_days = map(str, args[0])  # Установка списка чисел
#     self.list_to_total_days = map(str, args[0])  # Установка списка чисел
#     self.total_hours_work_statistic = args[2][0] # Установка времени часы
#     self.total_minutes_work_statistic = args[2][1] # Установка времени минуты
#
# def get_set_all_month(self):
#     all_month = []
#     for i in self.file_dict: # Получаем в i ключи словаря
#         all_month.append(i.split()[1])
#     return set(all_month)
#
# def get_dates_from_current_month(self, choice_month):
#     list_month = []  # Только даты выбранного месяца
#     for i in self.file_dict:  # Получаем в i ключи словаря
#         if i.split()[1] == choice_month:  # Определяем нужный месяц из списка. Вычленяем название месяца
#             list_month.append(i)  # Записываем в список только даты с нужным месяцем
#     return list_month
#
# def get_num_days(self,lst_current_month:list):
#     lst_num_days = []
#     for i in lst_current_month: # Идём по списку месяца
#         num_day = int(i.split()[0]) # Вычленяя только число месяца оборачивая в int()
#         lst_num_days.append(num_day) # Только числа: int выбранного месяца
#     lst_num_days.sort()
#     return lst_num_days
#
# def create_keys_date_choice_month(self, sorted_num_current_days:list, month_choice:str=CURRENT_MONTH):
#     keys_all_work = []
#     for i in range(len(sorted_num_current_days)): # Проход по длинне списка дат
#         keys_all_work.append(str(sorted_num_current_days[i]) + " " + month_choice) # создание строки ключа словаря и запись в список
#     return keys_all_work
#
# def update_total_time_statistic(self,keys_all_work_data_sorted:list):
#     hours = 0
#     minutes = 0
#     for i in keys_all_work_data_sorted: # ==========>>>>>>> ключи
#         hours += int(self.file_dict[i].split(":")[0])
#         minutes += int(self.file_dict[i].split(":")[1])
#
#     hours_delta = timedelta(hours=hours).total_seconds()
#     minutes_delta = timedelta(minutes=minutes).total_seconds()
#     total_time_in_sec = minutes_delta + hours_delta
#     hours_total = int(total_time_in_sec // 3600)
#     minut = int((total_time_in_sec - hours_total * 3600) / 60)
#     return str(hours_total), str(minut)
#
# def list_sort_choices_num_days(self,list_num_choice_month,firstday,lastday):
#     list_num_choice = []
#     for i in list_num_choice_month:
#         if int(firstday) <= i <= int(lastday):
#             list_num_choice.append(i)
#     return list_num_choice
#
# def create_choice_spinner(self, spinner):
#     match spinner.uid:
#         case 3581:
#             self.from_total_days_spinner = spinner.text
#             if self.total_month_spinner != '' and  self.to_total_days_spinner != '':
#                 self.statistic_from_spinner(self.total_month_spinner)
#         case 3617:
#             self.total_month_spinner = spinner.text
#             if self.from_total_days_spinner != '' and  self.to_total_days_spinner != '':
#                 self.install_firsday_lastday(self.total_month_spinner)
#                 self.statistic_from_spinner(self.total_month_spinner)
#         case 3653:
#             self.to_total_days_spinner = spinner.text
#             if self.from_total_days_spinner != '' and self.total_month_spinner != '':
#                 self.statistic_from_spinner(self.total_month_spinner)
#
# def install_firsday_lastday(self,c_month):
#     """Устанавливает первый и последний день выбранного месяца после выбора spinner месяца"""
#     lst_dates_choice_month = self.get_dates_from_current_month(c_month)  # Получаем даты с нужным месяцем list
#     sort_num_choice = self.get_num_days(lst_dates_choice_month)  # Список int выбранных чисел для Spinner
#
#     self.from_total_days_spinner = str(sort_num_choice[0])
#     self.to_total_days_spinner = str(sort_num_choice[-1])
#
# def statistic_from_spinner(self,choice_month):
#     lst_dates_choice_month = self.get_dates_from_current_month(choice_month) # Получаем даты с нужным месяцем list
#     sort_num_choice = self.get_num_days(lst_dates_choice_month) # Список int выбранных чисел для Spinner
#
#     list_sort_num_choice = self.list_sort_choices_num_days(sort_num_choice,self.from_total_days_spinner,
#                                                            self.to_total_days_spinner)
#     lst_keys_choice_date = self.create_keys_date_choice_month(list_sort_num_choice,choice_month)
#     time_statistic = self.update_total_time_statistic(lst_keys_choice_date)  # Получаем кортеж (170,45) часы минуты
#     self.install_totaltime_statistic(sort_num_choice,time_statistic)
#
# def install_totaltime_statistic(self,sort_num_choice, totaltime):
#     self.list_from_total_days = map(str, sort_num_choice) # Установка списка чисел
#     self.list_to_total_days = map(str, sort_num_choice)  # Установка списка чисел
#
#     self.total_hours_work_statistic = str(totaltime[0])  # Установка времени часы
#     self.total_minutes_work_statistic = str(totaltime[1])  # Установка времени минуты
#
# def get_from_current_month(self, choice_month,firstday,lastday):
#     list_dates = self.get_dates_from_current_month(choice_month) # даты выбранного месяца List
#     list_num_choice_month = self.get_num_days(list_dates) # Список чисел выбранного месяца List
#     list_keys = self.create_keys_date_choice_month(list_num_choice_month,choice_month) # Список ключей
#     return list_keys
#
#
# def my_callback(self,instance):
#     self.lab_save_txt = "Отработано:"
#     return False
#
# def write_file_time_work(self):
#     with open("data_base.dat", 'wb') as files:
#         pickle.dump(self.file_dict, files)
#     Clock.schedule_once(self.my_callback, 2)
#     self.lab_save_txt = "Сохранено"
#     self.update_statistic()
#
#
#
#
#
#
#
#
#
#
# def create_a_date_for_label(self):
#     """Формируется ключ для словаря
#     key_dict_total_data = "10 Января" """
#     self.label_month_lst.clear()
#     day = self.ids['day'].text
#     month = self.ids['month'].text
#     self.label_month_lst.append(day)
#     self.label_month_lst.append(month)
#     self.key_dict_total_data = day + " " + month
#
# def validate_file_time_work(self):
#     data = self.key_dict_total_data
#     time_work = self.value_dict_total_time_work
#
#     if data in self.file_dict:
#         self.write_or_cancel_poput()
#     else:
#         self.file_dict[data] = time_work
#         self.write_file_time_work()
#
# def overwriting(self):
#     data = self.key_dict_total_data
#     time_work = self.value_dict_total_time_work
#     self.file_dict[data] = time_work
#     self.write_file_time_work()

class RouteTextInputMain(MDTextField):
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
            self.font_size = "25dp"
        else:
            if not self.text:
                self.parent.md_bg_color = "aquamarine"
                self.font_size = "20dp"
                self.text = "Маршрут"
class KartaTextInputMain(MDTextField):
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
            self.font_size = "25dp"
        else:
            if not self.text:
                self.parent.md_bg_color = "aquamarine"
                self.font_size = "20dp"
                self.text = "Карта"

class RouteTextInputCreate(MDTextField):
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
            self.font_size = "25dp"
        else:
            if not self.text:
                self.parent.md_bg_color = self.parent_color
                self.font_size = "20dp"
                self.text = "Маршрут"



class KartaTextInputCreate(MDTextField):
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
            self.font_size = "25dp"
        else:
            if not self.text:
                self.parent.md_bg_color = self.parent_color
                self.font_size = "20dp"
                self.text = "Карта"



class HoursTextInput(MDTextField):
    def __init__(self, **kwargs):
        super(HoursTextInput, self).__init__(**kwargs)
        self.temp_lst = ["", ""]

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.text = ""
        self.temp_lst = ["", ""]

    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if not self.temp_lst[0]:
                self.temp_lst[0]= value
                if int(value) < 3:
                    if len(self.text) < 2:
                        return super().insert_text(value, from_undo=from_undo)
                else:
                    self.temp_lst = ["", ""]
            else:
                self.temp_lst[1] = value
                if self.temp_lst[0] == "2":
                    if int(value) < 4:
                        if len(self.text) < 2:
                            self.temp_lst = ["", ""]
                            return super().insert_text(value, from_undo=from_undo)
                else:
                    if len(self.text) < 2:
                        return super().insert_text(value, from_undo=from_undo)
    def on_focus(self, inst, args):
        if args:
            self.temp_lst = ["", ""]
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "30dp"
        else:
            if not self.text:
                # self.temp_lst = ["", ""]
                self.parent.md_bg_color = self.parent_color
                self.font_size = "20dp"
                self.text = "Час"



class MinutesTextInput(MDTextField):
    def __init__(self, **kwargs):
        super(MinutesTextInput, self).__init__(**kwargs)
        self.temp_lst = ["", ""]

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.text = ""
        self.temp_lst = ["", ""]

    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if not self.temp_lst[0]:
                self.temp_lst[0] = value
                if int(value) < 6:
                    if len(self.text) < 2:
                        return super().insert_text(value, from_undo=from_undo)
                else:
                    self.temp_lst = ["", ""]
            else:
                self.temp_lst[1] = value
                if len(self.text) < 2:
                    self.temp_lst = ["", ""]
                    return super().insert_text(value, from_undo=from_undo)

    def on_focus(self, inst, args):
        if args:
            self.temp_lst = ["", ""]
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "30dp"
        else:
            if not self.text:
                self.parent.md_bg_color = self.parent_color
                self.font_size = "18dp"
                self.text = "Мин"














class MyPopup_save_worktime(Popup):
    message_info = StringProperty("Рабочий день на эту дату существует.\n Переписать?")
    Builder.load_file(os.path.join(dir_name, "Popup_new_time.kv"))
    def __init__(self,date,work_time,lab,**kwargs):
        Popup.__init__(self, **kwargs)
        self.key = date
        self.work_time = work_time
        self.label = lab
        self.open()

    def answer_ok(self):
        print("worktime_data.dat")
        DICT_TIME_STATISTIC[self.key] = self.work_time
        save_HDD_DICT_TIME(DICT_TIME_STATISTIC, "worktime_data.dat")
        self.change_save_text_label()
        # else:
        #     DICT_ROUT[self.key] = self.work_time
        #     save_HDD_DICT_TIME(DICT_ROUT, "route_data.dat")
        #     self.change_save_text_label()
        self.dismiss()
        return

    def my_callback(self, instance):
        self.label.text_color = "black"
        self.label.text = "Отработано:"
        return False

    def change_save_text_label(self):
        Clock.schedule_once(self.my_callback, 2)
        self.label.theme_text_color = "Custom"
        self.label.text_color = "red"
        self.label.text = "Сохранено"


class Screen_main(MDScreen):
    Builder.load_file(os.path.join(dir_name, "mainScreen.kv"))

    def show_karta_btn_turn_on(self):
        self.ids.show_karta_btn_color.md_bg_color = 1,.1,.1,.7
        self.ids.show_karta_btn_text.text = "Такой карты нет"

    def find_a_karta(self):
        pprint(DICT_ROUT_1)
        print("##################################")
        pprint(DICT_ROUT_2)
        print("+++++++++++++++++++++++++++++++++")



class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Light Dark
        self.theme_cls.primary_palette = "Olive"  # "Teal" #"Purple" # , "Red" "Olive"
        # Window.clearcolor = (.8, .8, .8)
        Builder.load_file(os.path.join(dir_name, "main_kv.kv"))
        scm = PagesManager()
        scm.add_widget(Screen_main())
        scm.add_widget(Create_route_kart())
        scm.add_widget(Page_main())
        scm.add_widget(Page_stat())
        scm.add_widget(Page_setting())
        return scm



if __name__ == '__main__':
    MyApp().run()
