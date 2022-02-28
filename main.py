from kivy.config import Config

Config.set('graphics', 'resizable', False)
from kivy.core.window import Window

Window.size = (600, 600)
Window.left = 350
Window.top = 100

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import IRightBodyTouch, ThreeLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineIconListItem
from kivy.properties import StringProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.resources import resource_add_path
from kivymd.uix.dialog import MDDialog
from datetime import date
import random
import sys
import os
from db import LogData


class WindowSignin(Screen):
    pass


class WindowSignup(Screen):
    pass


class WindowMain(Screen):
    pass


class ListItemWithCheckbox(ThreeLineAvatarIconListItem):
    """Custom list item."""

    icon = StringProperty("tools")


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    """Custom right container."""


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.email_admin = None
        self.btn_del = None
        self.chech_checkbox = None
        self.btn_issues = None
        self.label_issues = None
        self.label_admin = None
        self.department = None
        self.greet_message = None
        self.menu = None
        self.dialog = None
        self.screen = Builder.load_file("main.kv")

    def build(self):
        self.title = 'I.T Maintance'
        self.icon = "./assets/lamp.ico"

        return self.screen

    def message_login(self):

        self.root.get_screen('signin').add_widget((MDLabel(
            text='Email/Password is not valid!.',
            pos_hint={'center_x': 0.5, 'center_y': 0.34},
            size_hint=(.5, .5),
            halign='center',
            font_style="Caption"
        )))

    def signup_register(self):

        # Sign Up user
        name_reg = self.root.get_screen("signup").ids.name_register.text
        sector_reg = self.root.get_screen("signup").ids.sector_register.text
        email_reg = self.root.get_screen("signup").ids.email_register.text
        password_reg = self.root.get_screen("signup").ids.password_register.text

        if name_reg and sector_reg and email_reg and password_reg:

            LogData().create_user(user_email=email_reg, user_password=password_reg)

            LogData().set_profile(name=name_reg, sector=sector_reg, user_email=email_reg, user_password=password_reg)

        else:
            self.show_alert_dialog()

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                width_offset=dp(200),
                text="Complete all the fieds",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        theme_text_color="Custom",
                        md_bg_color=(.9, 0, .8, 1),
                        on_release=lambda _: self.dialog.dismiss()

                    )
                ]
            )
        self.dialog.open()

    def toggle(self):

        if self.root.get_screen('signin').ids.user_password.password:
            self.root.get_screen('signin').ids.user_password.password = False
            self.root.get_screen('signin').ids.btn_show.icon = 'eye-off'
            self.root.get_screen('signin').ids.btn_show.opacity = .3

        elif not self.root.get_screen('signin').ids.user_password.password:
            self.root.get_screen('signin').ids.btn_show.icon = 'eye'
            self.root.get_screen('signin').ids.user_password.password = True
            self.root.get_screen('signin').ids.btn_show.opacity = .3

    def database_login(self):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        try:
            greet_message = LogData().logsession(user_email=email, user_password=password)
            self.root.current = "main"
            self.root.transition.direction = 'left'
            self.root.get_screen('main').ids.label_welcome.text = f"Hi {greet_message}, Welcome!"
            self.root.get_screen('main').ids.label_welcome.font_size = "23dp"
            self.issues()
            self.greet_message = greet_message
            self.department = LogData().load_profile(user_email=email, user_password=password)
            self.email_admin = LogData().admin_profile(email=email, password=password)

        except Exception:
            self.message_login()

    def admin(self):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        if email == self.email_admin and password == password:
            self.root.get_screen('main').ids.label_welcome.text = "Config Area"
            self.root.get_screen('main').ids.label_welcome.pos_hint = {'center_x': 0.5, 'center_y': 0.95}
            self.root.get_screen('main').ids.tela1.text = 'Test'
            self.root.get_screen('main').ids.tela2.icon = 'key'
            self.root.get_screen('main').ids.tela3.icon = 'view-list'
            self.root.get_screen('main').ids.tela3.text = 'Historic Issues'

            self.root.get_screen('main').ids.icon_quit.opacity = 0
            self.root.get_screen('main').ids.icon_quit.disabled = True
            self.root.get_screen('main').ids.tela2.remove_widget(self.root.get_screen('main').ids.container)

            # Add Text field and button issues
            self.label_issues = MDTextField(
                pos_hint={'center_x': 0.35, 'center_y': 0.78},
                size_hint=(.5, .5),
                halign='center',
            )
            self.root.get_screen('main').ids.tela1.add_widget(self.label_issues)

            self.btn_issues = MDFlatButton(
                text='Add',
                pos_hint={'center_x': 0.8, 'center_y': 0.78},
                size_hint=(.3, .05),
                theme_text_color="Custom",
                md_bg_color=(1, 0, 1, 1),
                halign='center',
                on_release=self.issue_save
            )
            self.root.get_screen('main').ids.tela1.add_widget(self.btn_issues)

            # Select issue
            self.root.get_screen('main').ids.label_issues.text = ''
            self.root.get_screen('main').ids.field_issue.pos_hint = {'center_x': 0.5, 'center_y': 0.60}
            self.root.get_screen('main').ids.field_issue.hint_text = 'Issues List'
            # Describe issue
            self.root.get_screen('main').ids.field_describe.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
            # Button Test
            self.root.get_screen('main').ids.send_request.text = 'Test Request'
            self.root.get_screen('main').ids.send_request.pos_hint = {'center_x': 0.5, 'center_y': 0.07}

            self.label_admin = MDLabel(
                text='Add Issue',
                pos_hint={'center_x': 0.2, 'center_y': 0.85},
                halign='center'
            )
            self.root.get_screen('main').ids.tela1.add_widget(self.label_admin)

            self.btn_del = MDFlatButton(
                text='Delete',
                pos_hint={'center_x': 0.8, 'center_y': 0.05},
                size_hint=(.10, None),
                theme_text_color="Custom",
                md_bg_color=(1, 0, 1, 1),
                halign='center',
                on_release=self.status_checked
            )
            self.root.get_screen('main').ids.tela2.add_widget(self.btn_del)

    def issue_save(self, *args):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        part = self.label_issues.text
        LogData().save_issues(user_email=email, user_password=password, part=part)
        self.issues()

    def issues(self):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        issues_list = LogData().load_issues(user_email=email, user_password=password)
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "text": f'{i}',
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in issues_list]

        self.menu = MDDropdownMenu(
            caller=self.root.get_screen('main').ids.field_issue,
            items=menu_items,
            position="auto",
            width_mult=3,
        )

    def set_item(self, text__item):
        self.root.get_screen('main').ids.field_issue.text = text__item
        self.menu.dismiss()

    def requests(self):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        name = self.greet_message
        issue = self.root.get_screen("main").ids.field_issue.text
        describe = self.root.get_screen("main").ids.field_describe.text
        time = date.today().strftime("%m/%d/%Y")
        id_req = random.randint(1, 20000000)

        LogData().requests(name=name, issue_select=issue, description=describe, dep=self.department,
                           time=time, user_email=email, user_password=password, id_req=id_req)

    def queue(self):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        request_dict = LogData().queue(user_email=email, user_password=password)
        if email == self.email_admin and password == password:
            # clean the widgets to update de view
            if self.root.get_screen('main').ids.container.children:
                self.root.get_screen('main').ids.container.clear_widgets()

            for i in range(len(request_dict)):
                self.chech_checkbox = self.root.get_screen('main').ids.container.add_widget(
                    ListItemWithCheckbox(
                        text=f"{request_dict[i]['name']} -{request_dict[i]['time']} {request_dict[i]['id_req']} ",
                        secondary_text=f"Issue: {request_dict[i]['issue']} ({request_dict[i]['department']})",
                        tertiary_text=f"Describe Issue: {request_dict[i]['description']}"
                    )
                )

        else:
            # clean the widgets to update de view
            if self.root.get_screen('main').ids.container.children:
                self.root.get_screen('main').ids.container.clear_widgets()

            for i in range(len(request_dict)):
                self.root.get_screen("main").ids.container.add_widget(
                    ThreeLineIconListItem(
                        text=f"{request_dict[i]['name']}- {request_dict[i]['time']} ",
                        secondary_text=f"Issue: {request_dict[i]['issue']} ({request_dict[i]['department']})",
                        tertiary_text=f"Describe Issue: {request_dict[i]['description']}",

                    ))

    def status_checked(self, *args):
        mdlist = self.root.get_screen('main').ids.container  # get reference to the MDList
        for wid in mdlist.children:
            if isinstance(wid, ListItemWithCheckbox):  # only interested in the ListItemWithCheckboxes
                rcb = wid.ids.rcb  # use the id defined in kv
                if rcb.active:  # only print selected items
                    mdlist.remove_widget(wid)  # remove selected
                    item_infos = wid.text.split(" ")
                    self.remove_request_db(id_req=int(item_infos[2]))

    def remove_request_db(self, id_req):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        LogData().remove_request(user_email=email, user_password=password, id_req=id_req)

    def back_home(self):
        self.root.current = 'signin'
        self.root.transition.direction = 'right'

    def graph(self):
        email = self.root.get_screen("signin").ids.user_email.text
        password = self.root.get_screen("signin").ids.user_password.text

        if email == self.email_admin:
            graph = LogData().stat_requests(user_email=email, user_password=password)
            self.root.get_screen('main').ids.tela3.add_widget(FigureCanvasKivyAgg(graph))
        else:
            pass


if __name__ == '__main__':
    # This part of the Try/Except is important when the app is packaged with pyinstaller
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = MyApp()
        app.run()
    except Exception as e:
        print(e)
        input("Press any key")
