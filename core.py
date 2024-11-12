from random import sample

class Player:

    def __init__ (self):
        self.hand = []
    
    def __repr__ (self):
        return self.n + " - " + str(self.hand)
    
    def draw_card(self, pile):
        """
            Fait piocher une carte au joueur
        """

        self.hand.append(pile.draw_card())
    
    def get_cards(self):
        return self.hand
    
    def get_score(self):
        """
            Calcule le score du joueur
        """

        score = 0
        n_as = 0
        for card in self.get_cards():
            if card.val in ["10", "valet", "dame", "roi"]:
                score += 10
            elif card.val == "as":
                n_as += 1
            else:
                score += int(card.val)
        for i in range(n_as):
            if score + 11 > 21:
                score += 1
            else:
                score += 11
        return score

class Card:

    def __init__ (self, info):
        self.val = info[0]
        self.col = info[1]
    
    def __repr__(self):
        return str(self.val) + "_" + self.col
    
    def get_path(self):
        """
            Renvoie le chemin d'accés de l'image liée à la carte
        """

        name = str(self.val) + "_" + self.col
        path = "img/" + name + ".gif"
        return path

class Pile:

    def __init__ (self):
        """
            Initialise le paquet de jeu
        """

        col = ["carreau", "coeur", "pique", "trefle"]
        num = ["as", "2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi"]
        l = []
        for i in num:
            for j in col:
                l.append((i, j))
        self.con = [Card(elt) for elt in sample(6*l, 6*len(l))]
    
    def __repr__ (self):
        return str(self.con)
    
    def draw_card(self):
        """
            Renvoie une carte du paquet, en la suprimant de ce dernier
        """

        return self.con.pop() if len(self.con) > 0 else None

