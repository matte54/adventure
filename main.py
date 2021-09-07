import random, json, os

class Mainclass():
    def __init__(self):
        self.filePath = f"./data/gameprofiledata.json"
        #delete old profile
        if os.path.isfile(self.filePath) == True:
            os.remove(self.filePath)
            print(f'removing old profile data...')
        #starting stats
        self.level = 1
        self.xp = 0
        self.xpcap = 20
        self.health = 10
        self.damage = 0
        self.defense = 0
        self.gold = 0
        #starting gear
        self.weapon = "Fists"
        self.armor = "Cloth Tunic"
        self.data = {"level": self.level, "xp": self.xp, "xpcap": self.xpcap, "health": self.health, "healthcap": self.health, "damage": self.damage, "defense": self.defense, "gold": self.gold, "weapon": self.weapon, "armor": self.armor}
        self.writeJSON(self.filePath, self.data)
        print(f'Starting a new game...')

    def move(self, direction):
        print(direction)
        filePath = f"./data/gamememorydata.json"
        if os.path.isfile(filePath) != True:
            data = {"currentbiome": 1, "previousbiome": 1, "lastheading": "south", "activity": ""}
            self.writeJSON(filePath, data)
        with open(filePath, "r") as f:
            data = json.load(f)
        #ugly calculate opposite
        if data["lastheading"] == "north":
            opposite = "south"
        if data["lastheading"] == "south":
            opposite = "north"
        if data["lastheading"] == "west":
            opposite = "east"
        if data["lastheading"] == "east":
            opposite = "west"

        with open("./data/biomes.json", "r") as bf:
            biomeData = json.load(bf)
        if direction != opposite:
            print(f'New direction...')
            biomeList = [data["previousbiome"], data["currentbiome"]]
            for i in range(2):
                x = random.choice(list(biomeData))
                biomeList.append(x)
            biome = random.choice(biomeList)
            data["previousbiome"] = data["currentbiome"]
            data["currentbiome"] = biome
            data["lastheading"] = direction
        else:
            print(f'Heading back...')
            extra = data["currentbiome"]
            data["currentbiome"] = data["previousbiome"]
            data["previousbiome"] = extra
            data["lastheading"] = direction

        #get text printed biomename
        for i in biomeData:
            if i == data["currentbiome"]:
                print(f'yay {biomeData[i]}')
                biomeText = biomeData[i]

        msg = f'You are in a {biomeText} biome , what will you do?'
        f.close()
        bf.close()
        self.writeJSON(filePath, data)
        return msg

    def rest(self):
        with open("./data/gameprofiledata.json", "r") as f:
            data = json.load(f)
        #refill hp to max.
        data["health"] = data["healthcap"]

    def choice(self):
        i = input('Make your choice (EXPLORE/REST/MOVE?):')
        if i == "explore" or i == "e":
            return "explore"
        elif i == "rest" or i == "r":
            return "rest"
        elif i == "move" or i == "m":
            return "move"
        else:
            print(f'invalid input')
            return None

    def writeJSON(self, filePath, data):
        with open(filePath, "w") as f:
            json.dump(data, f, indent=4)
            f.close()

    def readProfile(self):
        with open("./data/gameprofiledata.json", "r") as f:
            data = json.load(f)
        f.close()
        return data

    def inputMove(self):
        i = input('Where to? (NORTH/EAST/SOUTH/WEST?):')
        if i == "north" or i == "n":
            return "north"
        elif i == "south" or i == "s":
            return "south"
        elif i == "east" or i == "e":
            return "east"
        elif i == "west" or i == "w":
            return "west"
        else:
            print(f'invalid input')
            return None

    def explore():
        pass

    def spawnMob():
        pass

    def xpGain():
        pass

    def goldGain():
        pass

    def lootGain():
        pass

    def attack(monster):
        pass

    def hurt():
        pass


def game():#gameloop
    #wait for input from user
    i = None
    while i == None:
        i = gameobject.inputMove()
    mMsg = gameobject.move(i)
    print(mMsg)
    y = None
    while y == None:
        y = gameobject.choice()
    if y == "move":
        return # go back to start of gameloop
    elif y == "explore":
        print("exploring...")
    elif y == "rest":
        gameobject.rest()
        print("resting...")




gameobject = Mainclass()

while True:
    game()
