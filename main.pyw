####   Imports   ####

from core import Pile, Player

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

# Définition de la taille de la fenêtre
from kivy.config import Config
Config.set('graphics', 'width', '610')
Config.set('graphics', 'height', '400')

####   Fonctions de logique   ####

# Fonctions des boutons #

def player_draw_card(instance):
    """
        Quand l'utilisateur clique sur le boutton 'Tirer'
    """

    if is_playing:
        global player, pile
        player.draw_card(pile)

        draw_screen()

def player_stop(instance):
    """
        Quand l'utilisateur clique sur le boutton 'Rester'
    """

    global is_playing, dealer, player
    if is_playing:
        is_playing = False
        
        # Tour du croupier
        while dealer.get_score() < 17:
            dealer_draw_card()
        
        draw_screen()

def next_round(instance):
    global player, dealer, is_playing, player_win, dealer_win
    player = Player()
    dealer = Player()

    is_playing = True
    player_win = False
    dealer_win = False

    player.draw_card(pile)
    dealer.draw_card(pile)
    player.draw_card(pile)
    dealer.draw_card(pile)

    draw_screen()

# Fonctions de logique générale #

def check_score():
    global player, dealer, player_win, dealer_win, is_playing

    p_score =  player.get_score()
    d_score = dealer.get_score()

    if p_score > 21:
        dealer_win = True
        is_playing = False
    elif d_score > 21:
        player_win = True
    elif is_playing == False:
        if d_score > p_score:
            dealer_win = True
        elif p_score > d_score:
            player_win = True
        elif p_score == d_score:
            player_win = True
            dealer_win = True

def dealer_draw_card():
    global dealer, pile
    dealer.draw_card(pile)

def add_layout():
    """
        Ajoute tout les éléments autres que les cartes à la fenêtre
    """

    check_score()

    player_score = player.get_score()
    player_score_text = "Score joueur: " + str(player_score)
    dealer_score = dealer.get_score()
    dealer_score_text = "Score croupier: " + str(dealer_score)

    if player_win and dealer_win:
        window.add_widget(ResultLabel(text = "Egalité !"))
    elif player_win:
        window.add_widget(ResultLabel(text = "Vous avez gagné, bravo !"))
    elif dealer_win:
        window.add_widget(ResultLabel(text = "Vous avez perdu, dommage !"))

    window.add_widget(BoutonPiocher(text = "Tirer"))
    window.add_widget(BoutonRester(text = "Rester"))
    window.add_widget(BoutonProchaineManche(text = "Prochaine manche"))
    window.add_widget(BoutonQuitter(text = "Quitter"))
    window.add_widget(PlayerHandLabel(text = "Main du joueur : "))
    window.add_widget(PlayerScoreLabel(text = player_score_text))
    window.add_widget(DealerHandLabel(text = "Main du croupier : "))
    if not is_playing:
        window.add_widget(DealerScoreLabel(text = dealer_score_text))
    window.add_widget(CardsLeftLabel(text = "Cartes restantes: " + str(pile.get_cards_left())))
    window.add_widget(CardsLeftBeforeMixLabel(text = "Avant mélange: " + str(pile.get_cards_left() - 77)))

def add_player_card(path, n):
    """
        Ajoute une carte de la main du joueur à la fenêtre
        Prend en paramètre le chemin de l'image et le numéro de la carte (pour le décalage)
    """

    img = PlayerCardImage(num = n, source = path)
    window.add_widget(img)

def add_dealer_card(path, n):
    """
        Ajoute une carte de la main du croupier à la fenêtre
        Prend en paramètre le chemin de l'image et le numéro de la carte (pour le décalage)
    """

    img = DealerCardImage(num = n, source = path)
    window.add_widget(img)

def draw_screen():
    """
        Ajoute à la fenêtre tout ce qui doit être affiché
    """

    global player, dealer

    window.clear_widgets()

    add_layout()

    # Affichage dess cartes du joueur
    for i in range(len(player.get_cards())):
        add_player_card(player.get_cards()[i].get_path(), i)
    
    # Affichage des cartes du croupier
    if is_playing: # N'affiche que la première carte si le joueur pioche toujours
        add_dealer_card(dealer.get_cards()[0].get_path(), 0)
        add_dealer_card("img/dos.gif", 1)
    else:
        for i in range(len(dealer.get_cards())):
            add_dealer_card(dealer.get_cards()[i].get_path(), i)

####   Classes graphiques ####

class MainScreen (FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BoutonPiocher (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = player_draw_card)

class BoutonRester(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = player_stop)

class BoutonProchaineManche(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = next_round)

class BoutonQuitter (Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press = exit)

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

class DealerScoreLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ResultLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CardsLeftLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CardsLeftBeforeMixLabel (Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BlackJackApp (App): # Class de l'app principale
    def build (self):
        global window
        window = MainScreen()
        draw_screen()
        return window


####   Set-up original   ####
pile = Pile()
player = Player()
dealer = Player()

is_playing = True
player_win = False
dealer_win = False

player.draw_card(pile)
dealer.draw_card(pile)
player.draw_card(pile)
dealer.draw_card(pile)

BlackJackApp().run()

