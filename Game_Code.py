import sys,random,time
from collections import deque
import pandas as pd

# names_file=pd.read_csv('''C:\Users\Hriday Desai\OneDrive\Desktop\Python\Card_Game\baby_names.csv''')
# names=names_file["Name"]
unique_names=['Dom','Charlotte','Tanmay','Vignesh','Soham','Mandy','Kohli','Dhoni','Sushil','Candice','Albert','Xander','Rohan','Zeno','Steven','Sorloth','Xavier','Akash']



card_elem = ["S","H","C","D"]             #S means Spade, H means Heart, C means Club, D means Diamond .
card_num=[2,3,4,5,6,7,8,9,10,11,12,13,14] #numbers from 2 to 10 denote numbers of normal cards, numbers from 11-14 denote Jack,Queen,King and Ace respectively.

#Class to create a 52 cards deck object.
class Deck:
    def __init__(self):
        card_elem = ["S","H","C","D"]
        self.deck = [elem + "_" + str(num) for num in range(2,15) for elem in card_elem]
    
    #Shuffling the deck    
    def shuffle(self):
        import random
        random.shuffle(self.deck)
    
    #Dealing cards to the players
    def dealing(self,hand1,hand2,hand3,play_hand):
        import random
        hands=[hand1,hand2,hand3,play_hand]
        removed=[]
        for h in hands:
            random.shuffle(self.deck)
            while(len(h)<13):
                nom=random.choice(self.deck)
                if(nom not in removed):
                    removed.append(nom)
                    h.append(nom)            
        return hands

#To check validity of the card input of the player.
def validity(choc,hand,rulesuit=["S","D","H","C"]):
    rule_cou=0
    for card in hand:
        if(card[0]==rulesuit[0]):
            rule_cou=rule_cou+1
    if(len(choc)>4 or len(choc)<3):
        return 0
    else:
        if(choc[0] not in card_elem):
            return 0
        else:
            if(choc not in hand):
                return 0
            else:
                if(rule_cou>0 and choc[0] not in rulesuit):
                    return 0
                else:
                    return 1
        
#To create a Bot object to optimally place cards and compete with the player.
class Bot:
    def __init__(self,hand,name):
        self.hand = hand
        self.name = name
    
    #Placing cards when turn is not first.    
    def play(self,platform,rulesuit):
        
        p=rulesuit[0]
        ma=0
        maxi=0
        mi=20
        mini=0
        index=-1
        found=0
        arr=[]
        for card in self.hand:
            go=card.split(sep="_")
            naam=go[0]
            if(naam==p):
                arr.append(card)
                
        if(len(arr)==0):
            for card in self.hand:
                go=card.split(sep="_")
                naam=go[0]
                if(naam=="S"):
                    arr.append(card)
            if(len(arr)==0):
                arr=self.hand
        
        for card in arr:
            index=index+1
            go=card.split(sep="_")
            power=int(go[1])
            naam=go[0]
            namess=["S"]
            if(p not in namess):
                namess.append(p)
            if(power>=ma and naam in namess):
                ma=power
                maxi=index
                found=1
            if(power<=mi):
                mi=power
                mini=index
        les=arr[mini]
        if(found==1):
            choc=arr[maxi]
        
            platform.append(choc)
            suit=choc[0]
            if(suit!="S"):
                po=[]
                for r in platform:
                    someo=r.split(sep="_")
                    power=int(someo[1])
                    po.append(power)
                tre=po[-1]
                po.sort()
                if(tre==po[-1]):
                    self.hand.remove(choc)
                    platform.remove(choc)
                    return choc
                else:
                    self.hand.remove(les)
                    platform.remove(choc)
                    return les
            else:
                po=[]
                for r in platform:
                    someo=r.split(sep="_")
                    power=int(someo[1])
                    sonki=someo[0]
                    if(sonki=="S"):
                        po.append(power)
                tre=po[-1]
                po.sort()
                if(tre==po[-1]):
                    self.hand.remove(choc)
                    platform.remove(choc)
                    return choc
                else:
                    self.hand.remove(les)
                    platform.remove(choc)
                    return les
        else:
            self.hand.remove(les)   
            return les
    
    #Placing cards when starting a new round.
    def start(self):
        ma=0
        maxi=0
        index=-1
        for card in self.hand:
            index=index+1
            go=card.split(sep="_")
            power=int(go[1])
            if(power>=ma):
                ma=power
                maxi=index
                
        choc=self.hand[maxi]
        self.hand.remove(choc)
             
        return choc

#To create a Player object to allow player to interact and play the game optimally.  
class Playk:
    def __init__(self,hand,name):
        self.play_hand = hand
        self.name = name
    
    #To place a card when turn isn't first.
    def play(self,platform,rulesuit):   
        valid=0
        while(valid==0):
            print("Your hand: ",end="")
            print(*self.play_hand)
            print()
            print_slow("The cards currently on the deck are: ")
            print(*platform)
            print()
            print_slow("Which card would you like to play? ")
            choc=input()
            valid=validity(choc,self.play_hand,rulesuit)
            if(valid==0):
                print_slow("Placed card is invalid. Please place correct card as per the rules.")
                print()
        self.play_hand.remove(choc)
        
        return choc
    
    #To place a card when turn is first.
    def start(self):
        valid=0
        while(valid==0):
            print("Your hand: ",end="")
            print(*self.play_hand)
            print()
            print_slow("Which card would you like to play? ")
            choc=input()
            valid=validity(choc,self.play_hand)
            if(valid==0):
                print_slow("Placed card is invalid. Please place correct card which is in your hand.")
                print()
        self.play_hand.remove(choc)
        
        return choc

#To determine the winner of a particular round.   
def WinnerCheck(platform):
    sui=[]
    numsp=[]
    for card in platform:
        info=card.split(sep="_")
        sui.append(info[0])
        numsp.append(int(info[1]))
    rulingsuit=sui[0]
    if("S" in sui):
        rulingsuit="S"
    cppp=[]
    
    for jok in range(4):
        if(sui[jok]==rulingsuit):
            cppp.append(numsp[jok])
        else:
            cppp.append(0)    
    maxpo=max(cppp)
    winindex=cppp.index(maxpo)
    return winindex

#Function which mimics typing behaviour.
def print_slow(str):
    i=0
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        if(i%25==0):
            sleep_time=0.08
        else:
            sleep_time=0.03
        i=i+1
        time.sleep(sleep_time)
    print()
    
#Function which mimics typing behaviour.
def print_med(str):
    i=0
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        if(i%15==0):
            sleep_time=0.05
        else:
            sleep_time=0.01
        i=i+1
        time.sleep(sleep_time)
    print()

#Introduction to the game
print_slow("Hi, we are really excited to host you in this amazing card game.")
print_slow("""The card game which we are going to play is an easier version of the card game popularly called 'Twenty-Nine'.""")
print()
#Choice to view the Rules or skipping them.
print_slow("Click Y to view the game rules or Click any key to skip.")

s=input()
s=s.lower()
if(s=="y"):
    print()
    print_slow("The rules of this game are as follows:")
    print()
    repository = user.get_repo('Card-Game-Hriday')

    file_content = repository.get_contents('Rules_of_the_Card_Game.txt')
    f=open("Card_Game\Rules_of_the_Card_Game.txt")
    rules=f.read()
    print_med(rules)
    f.close()

print()
print()
print_slow("Hi! my name is Bond. I might not be James Bond (lol) but I am rather your guide in this game.\n I will explain the results of each turn to you and keep track of the score.")

print_slow("Let's start the Game!!!")
print_slow("Enter your name to start the game: ")
garb=input()

continu="y"
while(continu=="y"):
    hand1=[]
    hand2=[]
    hand3=[]
    play_hand=[]

    name1=random.choice(unique_names)
    while(name1==garb):
        name1=random.choice(unique_names)
    unique_names.remove(name1)
    name2=random.choice(unique_names)
    while(name2==garb):
        name2=random.choice(unique_names)
    unique_names.remove(name2)
    name3=random.choice(unique_names)
    while(name3==garb):
        name3=random.choice(unique_names)
    
    
    Bot1=Bot(hand1,name1)
    Bot2=Bot(hand2,name2)
    Bot3=Bot(hand3,name3)
    Player=Playk(play_hand,garb)

    deck=Deck()
    deck.shuffle()
    deck.shuffle()
    deck.shuffle()
    hands=deck.dealing(hand1,hand2,hand3,play_hand)

    hand1=hands[0]
    hand2=hands[1]
    hand3=hands[2]
    play_hand=hands[3]

    # print(hand1)
    # print(hand2)
    # print(hand3)
    # print(play_hand)

    print_slow("The names of your fellow players are:")
    print(name1+", "+name2+", "+name3+".")
    print()



    first=random.choice([Bot1.name,Bot2.name,Bot3.name,Player.name])
    print("The first move will be played by: ",end="")
    print(first)
    print()
    ning=[Bot1,Bot2,Bot3,Player]
    playing=deque(ning)
    
    win_count={}
    win_count[Bot1.name]=0
    win_count[Bot2.name]=0
    win_count[Bot3.name]=0
    win_count[Player.name]=0
    
    for games in range(13):
        
        
        if(first==Bot1.name):
            
            key=0
            while(key==0):
                if(playing[0]!=Bot1):
                    temp=playing[0]
                    playing.popleft()
                    playing.append(temp)
                else:
                    key=1
                    temp=0                 
        elif(first==Bot2.name):
            
            key=0
            while(key==0):
                if(playing[0]!=Bot2):
                    temp=playing[0]
                    playing.popleft()
                    playing.append(temp)
                else:
                    key=1
                    temp=0     
        elif(first==Bot3.name):
            
            key=0
            while(key==0):
                if(playing[0]!=Bot3):
                    temp=playing[0]
                    playing.popleft()
                    playing.append(temp)
                else:
                    key=1
                    temp=0  
        elif(first==Player.name):
            
            key=0
            while(key==0):
                if(playing[0]!=Player):
                    temp=playing[0]
                    playing.popleft()
                    playing.append(temp)
                else:
                    key=1
                    temp=0
    
        platform=[]
        rulesuit=[]
        for kokil in range(4):
            if(kokil==0):
                lom=playing[kokil].start()
                rulesuit.append(lom[0])
                print()
                print("Now it is the turn of: ",end="")
                print(playing[kokil].name)
                print()
                print("The starting card been played is: ",end="")
                print_slow(lom)
                print()
                platform.append(lom)
                time.sleep(1)
            else:
                lom=playing[kokil].play(platform,rulesuit)
                print("Now it is the turn of: ",end="")
                print(playing[kokil].name)
                print("The card been played is: ",end="")
                print_slow(lom)
                print()
                print_slow("The cards on the platform are: ")
                print()
                platform.append(lom)
                print(*platform)
                print()
                time.sleep(1)
    
        winindex=WinnerCheck(platform)
        time.sleep(0.5)
        platform=[]
        # if(winindex==0):
        first=playing[winindex].name
        print()
        print_slow("The winner of this round is")
        print(first)
        win_count[first]=win_count[first]+1
        
    print_slow("The game has ended. The final scores are:")
    print()
    print("Alfred : ", end="")
    print(win_count[Bot1.name])
    print("Bruno : ", end="")
    print(win_count[Bot2.name])
    print("Candice : ", end="")
    print(win_count[Bot3.name])
    print("You : ", end="")
    print(win_count[Player.name])
    
    a=win_count[Bot1.name]
    b=win_count[Bot2.name]
    c=win_count[Bot3.name]
    d=win_count[Player.name]
    moxo=max(a,b,c,d)
    li=[Bot1.name,Bot2.name,Bot3.name,Player.name]
    print()
    print_slow("Hence the final winner is: ")
    for na in li:
        if(win_count[na]==moxo):
            print(na)
    
    print_slow("If you wish to play one more game press Y or any other key to exit.")
    continu=input()
    continu=continu.lower()
    

print_slow("Thanks for playing this game. Hope you enjoyed the game.")
