import random

deck = [
     'A-h'  ,'A-c'  ,'A-d'  ,'A-s'
    ,'2-h'  ,'2-c'  ,'2-d'  ,'2-s'
    ,'3-h'  ,'3-c'  ,'3-d'  ,'3-s'
    ,'4-h'  ,'4-c'  ,'4-d'  ,'4-s'
    ,'5-h'  ,'5-c'  ,'5-d'  ,'5-s'
    ,'6-h'  ,'6-c'  ,'6-d'  ,'6-s'
    ,'7-h'  ,'7-c'  ,'7-d'  ,'7-s'
    ,'8-h'  ,'8-c'  ,'8-d'  ,'8-s'
    ,'9-h'  ,'9-c'  ,'9-d'  ,'9-s'
    ,'10-h' ,'10-c' ,'10-d' ,'10-s'
    ,'J-h'  ,'J-c'  ,'J-d'  ,'J-s'
    ,'Q-h'  ,'Q-c'  ,'Q-d'  ,'Q-s'
    ,'K-h'  ,'K-c'  ,'K-d'  ,'K-s'
]

def deal(deck_count):
    #
    random_number = random.randrange(51)
    random_card = deck[random_number]
    return random_card

if __name__ == '__main__':
    my_card = deal(0)
    print(my_card)