from core import Pile, Player

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

def player_draw_card(instance: Widget):
    global player, pile
    player.draw_card(pile)

    show_cards(instance.parent)

def player_stop(instance: Widget):
    global is_playing
    is_playing = 0

    show_cards(instance.parent)

def reset(instance: Widget):
    global pile, player, is_playing, dealer

    pile = Pile()
    player = Player()
    is_playing = 1
    dealer = Player()

    player.draw_card(pile)
    dealer.draw_card(pile)
    player.draw_card(pile)
    dealer.draw_card(pile)

    show_cards(instance.parent)

def add_default_layout(window: Widget):
    window.add_widget(BoutonPioche(text = "Tirer"))
    window.add_widget(BoutonReste(text = "Rester"))
    window.add_widget(BoutonRecommencer(text = "Nouvelle partie"))
    window.add_widget(PlayerHandLabel(text = "Main du joueur : "))
    window.add_widget(DealerHandLabel(text = "Main du croupier : "))

def add_player_card(window: Widget, path, n):
    img = PlayerCardImage(num = n, source = path)
    window.add_widget(img)

def add_dealer_card(window: Widget, path, n):
    img = DealerCardImage(num = n, source = path)
    window.add_widget(img)

def show_cards(window: Widget):
    window.clear_widgets()

    global player, dealer

    add_default_layout(window)

    for i in range(len(player.get_cards())):
        add_player_card(window, player.get_cards()[i].get_path(), i)
    
    if is_playing:
        add_dealer_card(window, dealer.get_cards()[0].get_path(), 0)
        add_dealer_card(window, "img/dos.gif", 1)
    else:
        for i in range(len(dealer.get_cards())):
            add_dealer_card(window, dealer.get_cards()[i].get_path(), i)

class MainScreen (Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BoutonPioche (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = player_draw_card)

class BoutonReste (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = player_stop)

class BoutonRecommencer (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = reset)

class PlayerCardImage (Image):
    def __init__(self, num, **kwargs):
        self.num = num
        super().__init__(**kwargs)

class DealerCardImage (Image):
    def __init__(self, num, **kwargs):
        self.num = num
        super().__init__(**kwargs)

class PlayerHandLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DealerHandLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BlackJackApp (App):
    def build (self):
        screen = MainScreen()
        show_cards(screen)
        return screen

pile = Pile()
player = Player()
is_playing = 1
dealer = Player()

player.draw_card(pile)
dealer.draw_card(pile)
player.draw_card(pile)
dealer.draw_card(pile)

BlackJackApp().run()

