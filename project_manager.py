import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window

class MyLayout(TabbedPanel):
    pass
        


class ProjectManagerApp(App):
    def build(self):
        self.title = "Artix Project Manager"
        Window.clearcolor = (95/255, 118/255, 133/255, 1)
        return MyLayout()

if __name__ == "__main__":
    ProjectManagerApp().run()