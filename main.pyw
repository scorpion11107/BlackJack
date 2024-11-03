from core import Pile, Player

from kivy.app import App
from kivy.uix.widget import Widget


class MainScreen (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BlackJackApp (App):
    def build (self):
        return MainScreen()

pile = Pile()
player = Player("Player")
dealer = Player("Dealer")

# distribution des cartes
player.draw_card(pile)
dealer.draw_card(pile)
player.draw_card(pile)
dealer.draw_card(pile)

player.show_cards()
dealer.show_cards()

BlackJackApp().run()

