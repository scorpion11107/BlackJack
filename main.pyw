from core import Pile, Player

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image

def draw_card(instance):
    global player, pile
    player.draw_card(pile)
    show_cards(instance.parent)

def show_cards(window):
    global player, dealer

    for i in range(len(player.get_cards())):
        img = CardImage(num = i, source = player.get_cards()[i].get_path())
        window.add_widget(img)

class MainScreen (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        draw_button = DrawButton(text = "Carte !")

        self.add_widget(draw_button)

class DrawButton (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = draw_card)

class CardImage (Image):
    def __init__(self, num, **kwargs):
        self.num = num
        super().__init__(**kwargs)

class BlackJackApp (App):
    def build (self):
        global screen
        screen = MainScreen()
        show_cards(screen)
        return screen

pile = Pile()
player = Player("Player")
dealer = Player("Dealer")

# distribution des cartes
player.draw_card(pile)
dealer.draw_card(pile)
player.draw_card(pile)
dealer.draw_card(pile)

BlackJackApp().run()

