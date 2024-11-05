from random import sample

class Player:

    def __init__ (self):
        self.hand = []
    
    def __repr__ (self):
        return self.n + " - " + str(self.hand)
    
    def draw_card(self, pile):
        self.hand.append(pile.draw_card())
    
    def get_cards(self):
        return self.hand

class Card:

    def __init__ (self, charac):
        self.val = charac[0]
        self.col = charac[1]
    
    def __repr__(self):
        return str(self.val) + "_" + self.col
    
    def get_path(self):
        name = str(self.val) + "_" + self.col
        path = "img/" + name + ".gif"
        return path

class Pile:

    def __init__ (self):
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
        return self.con.pop() if len(self.con) > 0 else None

