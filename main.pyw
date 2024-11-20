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
        global pl, pile
        pl.draw_card(pile)

        draw_screen()

def player_stop(instance):
    """
        Quand l'utilisateur clique sur le boutton 'Rester'
    """

    global is_playing, dl, pl
    if is_playing:
        is_playing = False
        
        # Tour du croupier
        while dl.get_score() < 17:
            dealer_draw_card()
        
        draw_screen()

def next_round(instance):
    global pl, dl, is_playing, pl_win, dl_win
    pl = Player()
    dl = Player()

    is_playing = True
    pl_win = False
    dl_win = False

    pl.draw_card(pile)
    dl.draw_card(pile)
    pl.draw_card(pile)
    dl.draw_card(pile)

    draw_screen()

# Fonctions de logique générale #

def check_score():
    global pl, dl, pl_win, dl_win, is_playing

    p_score =  pl.get_score()
    d_score = dl.get_score()

    if p_score > 21:
        dl_win = True
        is_playing = False
    elif d_score > 21:
        pl_win = True
    elif is_playing == False:
        if d_score > p_score:
            dl_win = True
        elif p_score > d_score:
            pl_win = True
        elif p_score == d_score:
            pl_win = True
            dl_win = True

def dealer_draw_card():
    global dl, pile
    dl.draw_card(pile)

def add_layout():
    """
        Ajoute tout les éléments autres que les cartes à la fenêtre
    """

    check_score()

    p_score = pl.get_score()
    p_score_txt = "Score joueur: " + str(p_score)
    d_score = dl.get_score()
    d_score_txt = "Score croupier: " + str(d_score)

    if pl_win and dl_win:
        window.add_widget(ResultLabel(text = "Egalité !"))
    elif pl_win:
        window.add_widget(ResultLabel(text = "Vous avez gagné, bravo !"))
    elif dl_win:
        window.add_widget(ResultLabel(text = "Vous avez perdu, dommage !"))

    window.add_widget(BoutonPiocher(text = "Tirer"))
    window.add_widget(BoutonRester(text = "Rester"))
    window.add_widget(BoutonProchaineManche(text = "Prochaine manche"))
    window.add_widget(BoutonQuitter(text = "Quitter"))
    window.add_widget(PlayerHandLabel(text = "Main du joueur : "))
    window.add_widget(PlayerScoreLabel(text = p_score_txt))
    window.add_widget(DealerHandLabel(text = "Main du croupier : "))
    if not is_playing:
        window.add_widget(DealerScoreLabel(text = d_score_txt))
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

    global pl, dl

    window.clear_widgets()

    add_layout()

    # Affichage dess cartes du joueur
    for i in range(len(pl.get_cards())):
        add_player_card(pl.get_cards()[i].get_path(), i)
    
    # Affichage des cartes du croupier
    if is_playing: # N'affiche que la première carte si le joueur pioche toujours
        add_dealer_card(dl.get_cards()[0].get_path(), 0)
        add_dealer_card("img/dos.gif", 1)
    else:
        for i in range(len(dl.get_cards())):
            add_dealer_card(dl.get_cards()[i].get_path(), i)

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
pl = Player()
dl = Player()

is_playing = True
pl_win = False
dl_win = False

pl.draw_card(pile)
dl.draw_card(pile)
pl.draw_card(pile)
dl.draw_card(pile)

BlackJackApp().run()

