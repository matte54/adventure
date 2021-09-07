import random, json, os, time

class Mainclass():
    def __init__(self):
        #constants
        self.EVENT = False
        #stuff
        self.currentBiome = 1
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
        self.healthcap = 10
        self.damage = 0
        self.defense = 1
        self.gold = 0
        #starting gear
        self.weapon = "Fists"
        self.armor = "Cloth Tunic"
        self.data = {"level": self.level, "xp": self.xp, "xpcap": self.xpcap, "health": self.health, "healthcap": self.healthcap, "damage": self.damage, "defense": self.defense, "gold": self.gold, "weapon": self.weapon, "armor": self.armor}
        self.writeJSON(self.filePath, self.data)
        print(f'Starting a new game...')

    def move(self, direction):
        filePath = f"./data/gamememorydata.json"
        if os.path.isfile(filePath) != True:
            data = {"currentbiome": 1, "previousbiome": 1, "lastheading": "", "activity": ""}
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
        if data["lastheading"] == "":
            opposite = "south"

        with open("./data/biomes.json", "r") as bf:
            biomeData = json.load(bf)
        if direction != opposite:
            #print(f'New direction...')
            biomeList = [data["previousbiome"], data["currentbiome"]]
            for i in range(2):
                x = random.choice(list(biomeData))
                biomeList.append(x)
            biome = random.choice(biomeList)
            data["previousbiome"] = data["currentbiome"]
            data["currentbiome"] = biome
            self.currentBiome = biome
            data["lastheading"] = direction
        else:
            #print(f'Heading back...')
            extra = data["currentbiome"]
            data["currentbiome"] = data["previousbiome"]
            data["previousbiome"] = extra
            data["lastheading"] = direction

        #get text printed biomename
        biomeText = "Grasslands"
        for i in biomeData:
            if i == data["currentbiome"]:
                biomeText = biomeData[i]
                break

        self.flare("move")
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
        self.writeJSON(self.filePath, data)
        self.health = self.healthcap
        self.flare("rest")
        if random.triangular(0, 100, 40) > 70:
            print("Ambush!")
            self.fight("class1")


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

    def flare(self, type):
        with open("./data/flare.json", "r") as f:
            data = json.load(f)
        x = random.choice(data[type])
        print(x)
        f.close()


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

    def explore(self):
        self.flare("explore")
        if random.triangular(0, 100, 50) > 50:
            self.EVENT = True
            #todo add class of event depending on level of player
            eName, eFlare, eDmg, eGold, eXp, eScale = self.loadEvent("class1")
            #add high chance of combat on explore
            if bool(random.getrandbits(1)):
                self.fight("class1")
            #get the random damage from event and subtract player defense
            damage = (random.choice(eDmg) - self.defense)
            if damage <= 0:
                damage = 0
            print(f'EVENT - {eName} - {eFlare}')
            if bool(random.getrandbits(1)):  #todo add some player stat to affect success?
                print("SUCCESS!")
                self.handleProfileStats(eXp, damage, eGold)
                self.EVENT = False
            else:
                print("FAILURE!")
                self.handleProfileStats(0, damage, 0)
                self.EVENT = False
        else:
            print(f'You find nothing...')

    def loadEvent(self, classStr):
        with open(f"./data/{classStr}events.json", "r") as f:
            eventData = json.load(f)
        eventKey = random.choice(list(eventData.keys()))
        eventFlare = eventData[eventKey]["flare"]
        eventDamage = eventData[eventKey]["damage"]
        eventGold = eventData[eventKey]["gold"]
        eventXp = eventData[eventKey]["xp"]
        eventScale = eventData[eventKey]["scale"]
        return eventKey, eventFlare, eventDamage, eventGold, eventXp, eventScale


    #handles basic stats, write something else to handle gear ?
    def handleProfileStats(self, xp, health, gold):
        statchange = "Stats changed: "
        if xp != 0:
            self.xp += xp
            statchange = statchange + f'xp: +{xp} '
        if health != 0:
            self.health -= health
            statchange = statchange + f'life: -{health} '
        if gold != 0:
            self.gold += gold
            statchange = statchange + f'$: +{gold} '
        with open(self.filePath, "r") as f:
            data = json.load(f)
        data["xp"] += xp
        data["health"] -= health
        data["gold"] += gold
        print(statchange)
        print(f'Current stats: life:{data["health"]}/{data["healthcap"]} lvl:{data["level"]} xp:{data["xp"]}/{data["xpcap"]} $:{data["gold"]} dmg:{data["damage"]} def:{data["defense"]}')
        self.writeJSON(self.filePath, data)

    def fight(self, classStr):
        #grab enemy
        with open(f"./data/{classStr}enemys.json", "r") as f:
            enemyData = json.load(f)
        searching = True
        while searching:
            enemyKey = random.choice(list(enemyData.keys()))
            if int(self.currentBiome) in enemyData[enemyKey]["biome"]:
                #print(f'{enemyKey} can spawn in biome {self.currentBiome}')
                searching = False
        if enemyData[enemyKey]["horde"]:
            amount = int(random.triangular(1, 5, 1))
        else:
            amount = 1
        print(f"Suddenly {amount} {enemyKey}(s) attack!")
        #enemy data
        Elife = enemyData[enemyKey]["health"]
        Edmg = enemyData[enemyKey]["damage"]
        Escale = enemyData[enemyKey]["scale"]
        Exp = enemyData[enemyKey]["xp"]
        if enemyData[enemyKey]["gold"]:
            Egold = random.randint(1, 3)
        else:
            Egold = 0
        #combat calculations
        #loop over player and enemy damage?
        acctual_player_damage = (self.damage + 1) #this needs weapon damage added 1 for now
        acctual_enemy_health = (Elife * amount)
        acctual_enemy_damage = ((Edmg * Escale) * amount)
        acctual_enemy_xp = (Exp * amount)
        acctual_enemy_gold = (Egold * amount)
        #math? :S
        rounds = 0
        while acctual_enemy_health > 0:
            acctual_enemy_health -= acctual_player_damage
            rounds += 1
        acctual_enemy_damage = (acctual_enemy_damage * rounds) / self.defense #this needs defense from armor
        #end
        self.handleProfileStats(int(acctual_enemy_xp), int(acctual_enemy_damage), int(acctual_enemy_gold)) #rounding here hopefully no problems?


    def lootGain():
        pass

    def wipe(self):
        os.system('cls' if os.name == 'nt' else 'clear')


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
        gameobject.explore()
        while gameobject.EVENT:
            time.sleep(3)

    elif y == "rest":
        gameobject.rest()




gameobject = Mainclass()

while gameobject.health > 0:
    game()
print("You died!")
print("Goodbye")
