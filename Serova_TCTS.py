import pandas as pd
import datetime as datetime

from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from random import randint

Config.set('graphics', 'fullscreen', 1)


class UserId:
    def __init__(self):
        self.data = []
        self.group = 1
        self.id = 1
        self.ready = False
        self.instruction = ['Это исследование изучает вегетативные реакции'
                            ' на изображения эротического характера в условиях постороннего шума. Вам нужно будет'
                            ' просмотреть 10 изображений с перерывами между ними (вам будет виден'
                            ' только черный экран). Не требуется ничего запоминать, просто смотрите'
                            ' на изображения, а мы замерим температуру вашего тела с помощью умных часов, которые лежат'
                            ' перед вами. Звук, который вы будете слышать в наушниках'
                            '  – просто посторонний шум, вы можете его игнорировать. Если вы надели наушники и часы,'
                            ' нажмите кнопку внизу экрана, чтобы начать исследование.',
                            'Это исследование изучает вегетативные реакции'
                            ' на изображения эротического характера. Вам нужно будет'
                            ' просмотреть 10 изображений с перерывами между ними (вам будет виден'
                            ' только черный экран). Не требуется ничего запоминать, просто смотрите'
                            ' на изображения, а мы замерим ваше сердцебиение с помощью умных наушников, которые лежат'
                            ' перед вами. Звук, который вы будете слышать в наушниках'
                            '  – звук вашего сердцебиения. Если вы надели наушники,'
                            ' нажмите кнопку внизу экрана, чтобы начать исследование.']


class CarouselApp(App):
    def build(self):

        userid = UserId()
        userid.group = randint(0, 1)
        userid.id = str(datetime.datetime.now())

        # ___SCREEN_MANAGER_______________
        sm = ScreenManager()

        def change_screen2(instance, manager=sm):
            manager.current = 'Scores'
        Clock.schedule_once(change_screen2, 650)

        def change_screen(instance, manager=sm):
            manager.current = 'Girls'
            sound = SoundLoader.load('heartbeat.wav')  
            if sound:
                sound.play()
            Clock.schedule_interval(carousel.load_next, 15)

        # ______tech_funcs

        def on_enter(instance, new_user=userid):
            print(instance.text)
            new_user.data.append(instance.text)
            instance.readonly = True

        def saveme(instance, new_user=userid):
            new_user.data.append(new_user.group)
            s=pd.DataFrame(new_user.data)
            s.to_csv('data%s.csv' %userid.id)

        # _________FIRST_SCREEN___________

        bl1 = BoxLayout(orientation='vertical')
        bl1.add_widget(TextInput(text='ИНСТРУКЦИЯ', font_size='60', size_hint=(1, .3)))
        bl1.add_widget(TextInput(text=userid.instruction[userid.group], multiline=True, font_size='20'))

        bl1.add_widget(Button(text='далее', font_size='40', size_hint=(1, .2), on_press=change_screen))

        screen1 = Screen(name='Instruction')
        screen1.add_widget(bl1)
        sm.add_widget(screen1)

        # _________2_SCREEN___________

        bl2 = BoxLayout(orientation='vertical')

        carousel = Carousel(direction='right', size_hint=(1, .9))
        for i in range(1, 43):
            src = "girls/playboy%d.png" % i
            image = AsyncImage(source=src, allow_stretch=False)
            carousel.add_widget(image)

        bl2.add_widget(carousel)

        screen2 = Screen(name='Girls')
        screen2.add_widget(bl2)
        sm.add_widget(screen2)

        # _________3_SCREEN___________

        gl = GridLayout(cols=4, spacing=3, size_hint=(1, .9))
        bl3 = BoxLayout(orientation='vertical', padding=25)

        bl3.add_widget(TextInput(text='Вы только что просмотрели эти'
                                      ' изображения. Оцените, насколько привлекательной'
                                      ' вам кажется каждая из девушек по 100-бальной шкале, где'
                                      ' 1 - совершенно не привлекательна,'
                                      ' 100 - крайне привлекательна. Введите число в каждое поле'
                                      ' и нажмите enter. После ввода чисел во все поля'
                                      ' нажмите кнопку внизу экрана. На этом исследование будет'
                                      ' окончено, можете закрыть окно.', font_size='15', size_hint=(1, .20),
                                 multiline=True))

        for i in range(1, 11):
            im = Image(source='nudes/playboy%d.png' % i)
            a = TextInput(text='Введите число от 1 до 100', multiline=False, font_size='13')
            a.bind(on_text_validate=on_enter)
            gl.add_widget(im)
            gl.add_widget(a)

        bl3.add_widget(gl)

        bt = Button(text='submit', size_hint=(1, .1), on_press=saveme)

        bl3.add_widget(bt)

        screen3 = Screen(name='Scores')
        screen3.add_widget(bl3)
        sm.add_widget(screen3)

        return sm


if __name__ == '__main__':
    CarouselApp().run()