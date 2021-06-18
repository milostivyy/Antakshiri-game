import random
#BackEnd
class StoreManager:
    def __init__(self, file):
        #lyrics from store
        self.lyrics = []

        #Open the file for reading. If file is not found then a runtime error (FileNotFoundError) is raised.
        fh = open(file, 'r')

        #read the file (lyrics store)
        for x in fh: #line by line reading until end of the file
            #' hello world\n'.strip() ---> 'hello world'
            x = x.strip() #removing begining and trailing spaces, tabs and newline characters
            if len(x) != 0:
                self.lyrics.append(x) #add to the lyrics (list)

        #close the file
        fh.close()

    def getAllLyrics(self):
        return self.lyrics

#Business Logic
class GameManager:
    def __init__(self, sm):
        #fetch the lyrics from the StoreManager
        allLyrics = sm.getAllLyrics()
        #Shuffle the lyrics
        random.shuffle(allLyrics)
        #Slice the lyrics
        set1 = allLyrics[0::2] #0,2,4,6,...
        set2 = allLyrics[1::2] #1,3,5,7,...
        #players
        self.pl = Player(set1)
        self.bt = Bot(set2)

    def toss(self, call):
        x = random.randint(1, 1000) #flip

        result = 'Heads' if x % 2 == 0 else 'Tails' #result of flip
        #print(x, result, call)
        return result == call #result match with call

    #game logic
    def play(self):
        state = 0 #flag
        if self.toss('Heads'):
            current = 0 #Human Player
        else :
            current = 1 #Bot
        gameOn = True #flag
        letter = ' '
        while gameOn:
            print('Score:')
            print('Player: ', self.pl.getScore())
            print('Bot: ', self.bt.getScore())

            if current == 0: #human player
                if state == 0:
                    flag, letter = self.pl.singAnySong()
                elif state == 1:
                    if letter != ' ':
                        backup = letter
                    flag, letter = self.pl.singSong(letter)

                if flag == True:
                    #switch current player to Bot
                    current = 1
                    #switch state
                    state = 1
                elif flag == False and letter == 'GIVEUP':
                    print('Player loses a point, Bot Gains!!!')
                    self.bt.increaseScore()
                    self.bt.addToOthersLimitations(backup)
                    #no switch
                    current = 0
                    #state switch
                    state =0

            elif current == 1: #bot
                if state == 0:
                    flag, letter = self.bt.singAnySong()
                elif state == 1:
                    flag, letter = self.bt.singSong(letter)

                if flag == True:
                    #switch current player to Player
                    current = 0
                    #switch state
                    state = 1
                elif flag == False and letter == 'GIVEUP':
                    print('Bot loses a point, Player Gains!!!')
                    self.pl.increaseScore()
                    #allow the bot to play any song
                    state = 0

            gameOn = self.pl.canPlay() and self.bt.canPlay()

        if self.pl.getScore() > self.bt.getScore():
            print('Player WINS!!!!')
        elif self.bt.getScore() > self.pl.getScore():
            print('Bot WINS!!!!')
        else:
            print('Game DRAW!!!!')


#FrontEnd
class Player:
    def __init__(self, songs):
        self.myLyrics = songs
        self.score = 0

    def increaseScore(self):
        self.score +=1

    def getScore(self):
        return self.score

    def canPlay(self):
        return len(self.myLyrics) >0

    def singAnySong(self):
        i =0
        tot = len(self.myLyrics)
        while i < tot:
            print(i+1, ') ', self.myLyrics[i])
            i+=1

        ch = int(input('Select any song to play '))
        ch-=1
        if ch>=0 and ch < tot:
            temp = self.myLyrics.pop(ch) #By pop we avoid play the same song next time
            print('Player sings : ', temp )
            return True, temp[-1]
        else:
            print('Invalid Choice')
            return False, ' '


    def singSong(self, letter):
        i =0
        tot = len(self.myLyrics)
        while i < tot:
            print(i+1, ') ', self.myLyrics[i])
            i+=1

        print('-1 )  to giveup')
        ch = int(input('Select a song with beginning with \''+ letter +'\' to play '))

        ch-=1
        if ch>=0 and ch < tot:
            if self.myLyrics[ch].startswith(letter):
                temp = self.myLyrics.pop(ch)
                print('Player sings : ', temp)
                return True, temp[-1]
            else:
                print('Selected song starts with ', self.myLyrics[ch][0], 'and not with', letter)
                return False, ' '
        elif ch == -2:
            #giveup
            return False , 'GIVEUP'
        else:
            print('Invalid Choice')
            return False, ' '


#A Bot is special kind of Player
class Bot(Player):
    def __init__(self, songs):
        #inheritance of data
        Player.__init__(self, songs)
        #extended data
        self.othersLimitations = []

    #extended code
    def addToOthersLimitations(self, letter):
        self.othersLimitations.append(letter)

    #override
    def singAnySong(self):
        if len(self.othersLimitations) == 0: #no limitation recorded yet
            anySong = random.choice(self.myLyrics)
            print('Bot sings', anySong)
            return True, anySong[-1]
        else:
            i =0
            tot = len(self.myLyrics)

            while i <tot:
                if self.myLyrics[i][-1] in self.othersLimitations: #trying to find a song that ends with other limitation
                    temp = self.myLyrics.pop(i)
                    print('Bot sings', temp)
                    return True, temp[-1]
                i+=1

            #no song in quota, that ends with others limitation, so random choice applied.
            anySong = random.choice(self.myLyrics)
            print('Bot sings', anySong)
            return True, anySong[-1]

    #override
    def singSong(self, letter):
        i =0
        tot = len(self.myLyrics)
        options = []
        while i <tot:
            if self.myLyrics[i].startswith(letter):
                options.append(i) #7,12,18
            i+=1

        if len(options) == 0: #no song begins with given letter
            return False, 'GIVEUP'
        else:
            tot = len(options) #3
            i =0
            while i < tot:
                if self.myLyrics[options[i]][-1] in self.othersLimitations:
                    temp = self.myLyrics.pop(options[i])
                    print('Bot sings', temp)
                    return True, temp[-1]
                i+=1

            #non of the song of quota end with otherslimitations
            temp = self.myLyrics.pop(random.choice(options))
            print('Bot sings', temp)
            return True, temp[-1]


def main():
    #initialize the StoreManager
    sm = StoreManager('/address')
    #initialize the GameManager
    gm = GameManager(sm)
    gm.play()


main()
