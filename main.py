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

    # def on_touch_down(self, touch):
    #     self.tap_X_Down = touch.x
    #     self.tap_Y_Down = touch.y
    #     return super(PagesManager, self).on_touch_down(touch)

    # def on_touch_up(self, touch):
    #     self.tap_X_Up = touch.x
    #     self.tap_Y_Up = touch.y
    #     if (self.tap_X_Down - self.tap_X_Up) > 100:
    #         if self.current == "main_screen":
    #             self.transition = SlideTransition()
    #             self.transition.direction = "left"
    #             self.current = "main_page"
    #
    #     if self.tap_X_Down < self.tap_X_Up:
    #         if self.current == "main_page":
    #             self.transition = SlideTransition()
    #             self.transition.direction = "right"
    #             self.current = "main_screen"
    #
    #     if (self.tap_Y_Down - self.tap_Y_Up) > 100:
    #         if self.current == "main_page":
    #             self.transition.direction = "down"
    #             self.current = "setting_page"
    #     return super(PagesManager, self).on_touch_up(touch)



def checking_the_time(hours,minutes):
    if hours.isdigit() and minutes.isdigit():
        return hours + ":" + minutes
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
    total_time_work = time_work_str.split()[-1]
    return total_time_work

def check_value_is_numeric(value:(tuple,list))->bool:
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


################################################################################
################################################################################
################################################################################

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

    def get_user_choice_date(self):
        day = self.ids["spinner_day"].text
        month = self.ids["spinner_month"].text
        return day + " " + month

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
            self.install_time_in_textinput(HW_start, MW_start, HW_end, MW_end, HL_start, ML_start, HL_end, ML_end)

    def install_time_in_textinput(self, HW_start, MW_start, HW_end, MW_end, HL_start, ML_start, HL_end, ML_end):

        tuple_input_time = ("startworkhours","startworkminutes",
                            "hoursendwork","minutesendwork",
                            "hoursstartlunch","minutesstartlunch",
                            "hoursendlunch","minutesendlunch")
        for textinput_name in tuple_input_time:
            self.ids[textinput_name].font_size = "30dp"
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

    def calculation_of_working(self):
        all_time_user_input:list = self.get_all_time_user_input() # возвр все часы\минуты
        if check_value_is_numeric(all_time_user_input):
            total_time = calculate_work_time(all_time_user_input)

            self.install_total_working_time(total_time)
            self.ids.save_button.disabled = False
        else:
            self.ids.save_button.disabled = True
            self.total_hours_work = "0"
            self.total_minutes_work = "00"


############################################################################################################
    def intercept_data_main_screen(self):
        date_choice_user: str = self.get_user_choice_date() # возвр дату => "23 Май"
        route_and_karta_in_day: str = self.get_route_user_choice() # возвр маршрут => 102/4 или "Не введён"
        all_time_user_input = self.get_all_time_user_input() # возвр все часы\минуты



        # self.save_date_in_dict_time(date_choice_user, route_and_karta_in_day, total_time)






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






    def my_callback(self, instance):
        self.ids["savingtext"].text_color = "black"
        self.lab_save_txt = "Отработано:"
        return False

    def change_save_text_label(self):
        Clock.schedule_once(self.my_callback, 2)
        self.ids["savingtext"].theme_text_color = "Custom"
        self.ids["savingtext"].text_color = "red"
        self.lab_save_txt = "Сохранено"




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

class MyPopup_save_route(Popup):
    route_str = StringProperty()
    karta_str = StringProperty()

    start_work = StringProperty()
    end_work = StringProperty()
    start_lunch = StringProperty()
    end_lunch = StringProperty()

    Builder.load_file(os.path.join(dir_name, "Popup_new_route.kv"))
    def __init__(self,dct,key,file_name,new_array_time, **kwargs):
        Popup.__init__(self, **kwargs)
        self.dct = dct
        self.key = key
        self.file_name = file_name
        self.new_array_time = new_array_time
        self.route_str,self.karta_str = key.split("/")
        self.box_word_save = MDBoxLayout(WordSave_or_Time(text="Сохранено",
                                                          text_color="red",
                                                          role="large"))
        self.pars_dict_old_route()

    def pars_dict_old_route(self):
        """Ф-ция устанавливает время старого маршрута в Popup для
        ознакомления пользователя, что он меняет."""
        self.start_work = checking_the_time(self.dct[self.key][0],self.dct[self.key][1])
        self.end_work = checking_the_time(self.dct[self.key][2],self.dct[self.key][3])
        self.start_lunch = checking_the_time(self.dct[self.key][4],self.dct[self.key][5])
        self.end_lunch = checking_the_time(self.dct[self.key][6],self.dct[self.key][7])




    def answer_ok(self):
        self.dct[self.key] = self.new_array_time
        save_HDD_DICT(self.dct, self.file_name)
        self.change_word_save()

    def my_callback(self,qt):
        self.dismiss()

    def change_word_save(self):
        """После сохранения, вместо кнопок, появляется
        красная надпись 'Сохранено'. """
        Clock.schedule_once(self.my_callback, 1)
        self.box_answer_ok.clear_widgets()
        self.box_answer_ok.add_widget(self.box_word_save)

class Page_stat(MDScreen):
    Builder.load_file(os.path.join(dir_name,"statistic_page.kv"))

class Page_setting(MDScreen):
    pass

class RouteTextInput(MDTextField):
    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)
        self.halign = "center"
        self.bold = True
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
                self.font_size = "15dp"
                self.text = "Маршрут"

class KartaTextInput(MDTextField):
    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)
        self.halign = "center"
        self.bold = True
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
                self.font_size = "18dp"
                self.text = "Карта"

class HoursTextInput(MDTextField):
    def __init__(self, **kwargs):
        super(HoursTextInput, self).__init__(**kwargs)
        self.mode = "outlined"
        self.multiline = False
        self.halign = "center"
        self.bold = True
        self.theme_text_color = "Custom"
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
            self.text_color_normal = "black"
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "30dp"
        else:
            if not self.text:
                self.text_color_normal = "black"
                self.parent.md_bg_color = self.parent_color
                self.font_size = "20dp"
                self.text = "Час"

class MinutesTextInput(MDTextField):
    def __init__(self, **kwargs):
        super(MinutesTextInput, self).__init__(**kwargs)
        self.mode = "outlined"
        self.multiline = False
        self.halign = "center"
        self.bold = True
        self.theme_text_color = "Custom"
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
            self.text_color_normal = "black"
            self.parent.md_bg_color = "greenyellow"
            self.text = ""
            self.font_size = "30dp"
        else:
            if not self.text:
                self.text_color_normal = "black"
                self.parent.md_bg_color = self.parent_color
                self.font_size = "18dp"
                self.text = "Мин"

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Light Dark
        self.theme_cls.primary_palette = "Olive"  # "Teal" #"Purple" # , "Red" "Olive"
        # Window.clearcolor = (.8, .8, .8)
        Builder.load_file(os.path.join(dir_name, "main_kv.kv"))
        scm = PagesManager()
        scm.add_widget(Page_main())
        scm.add_widget(Page_stat())
        scm.add_widget(Page_setting())
        return scm



if __name__ == '__main__':
    MyApp().run()
