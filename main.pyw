####   Imports   ####

from core import Pile, Player

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

# Définition de la taille de la fenêtre
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')

####   Fonctions de logique   ####

def player_draw_card(instance: Widget):
    """
        Quand l'utilisateur clique sur le boutton 'Tirer'
    """
    global player, pile
    player.draw_card(pile)

    draw_screen(instance.parent)

def player_stop(instance: Widget):
    """
        Quand l'utilisateur clique sur le boutton 'Rester'
    """
    global is_playing
    is_playing = 0

    draw_screen(instance.parent)

def restart_game(instance: Widget):
    """
        Quand l'utilisateur clique sur le boutton 'Nouvelle partie'
        Réinitialise le paquet de carte, ainsi que les mains du joueur et du croupier
    """
    global pile, player, is_playing, dealer

    pile = Pile()
    player = Player()
    is_playing = 1
    dealer = Player()

    player.draw_card(pile)
    dealer.draw_card(pile)
    player.draw_card(pile)
    dealer.draw_card(pile)

    draw_screen(instance.parent)

def add_layout(window: Widget):
    """
        Ajoute tout les éléments autres que les cartes à le fenêtre
    """
    player_score = player.check_score()
    if player_score > 21:
        pass
    elif player_score == 21:
        if len(player.get_cards) == 2:
            pass
        else:
            pass
    else:
        player_score_text = "Score: " + str(player_score)

    window.add_widget(BoutonPioche(text = "Tirer"))
    window.add_widget(BoutonReste(text = "Rester"))
    window.add_widget(BoutonRecommencer(text = "Nouvelle partie"))
    window.add_widget(PlayerHandLabel(text = "Main du joueur : "))
    window.add_widget(PlayerScoreLabel(text = player_score_text))
    window.add_widget(DealerHandLabel(text = "Main du croupier : "))

def add_player_card(window: Widget, path, n):
    """
        Ajoute une carte de la main du joueur à la fenêtre
        Prend en paramètre le chemin de l'image et le numéro de la carte (pour le décalage)
    """
    img = PlayerCardImage(num = n, source = path)
    window.add_widget(img)

def add_dealer_card(window: Widget, path, n):
    """
        Ajoute une carte de la main du croupier à la fenêtre
        Prend en paramètre le chemin de l'image et le numéro de la carte (pour le décalage)
    """
    img = DealerCardImage(num = n, source = path)
    window.add_widget(img)

def draw_screen(window: Widget):
    """
        Ajoute à la fenêtre tout ce qui doit être affiché
    """
    window.clear_widgets()

    global player, dealer

    add_layout(window)

    for i in range(len(player.get_cards())):
        add_player_card(window, player.get_cards()[i].get_path(), i)
    
    if is_playing:
        add_dealer_card(window, dealer.get_cards()[0].get_path(), 0)
        add_dealer_card(window, "img/dos.gif", 1)
    else:
        for i in range(len(dealer.get_cards())):
            add_dealer_card(window, dealer.get_cards()[i].get_path(), i)

####   Classes graphiques ####

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
        self.bind(on_press = restart_game)

class PlayerCardImage (Image): # Widget pour les cartes du joueur
    def __init__(self, num, **kwargs):
        self.num = num
        super().__init__(**kwargs)

class DealerCardImage (Image): # Widget pour les cartes du croupier
    def __init__(self, num, **kwargs):
        self.num = num
        super().__init__(**kwargs)

class PlayerHandLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class PlayerScoreLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DealerHandLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BlackJackApp (App): # Class de l'app principale
    def build (self):
        screen = MainScreen()
        draw_screen(screen)
        return screen


####   Set-up original   ####
pile = Pile()
player = Player()
is_playing = 1
dealer = Player()

player.draw_card(pile)
dealer.draw_card(pile)
player.draw_card(pile)
dealer.draw_card(pile)

BlackJackApp().run()

