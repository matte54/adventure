import random, json, os, time

class Mainclass():
    def __init__(self):
        #constants
        self.EVENT = False
        #stuff
        self.currentBiome = 1
        self.filePath = f"./data/gameprofiledata.json"
        #delete old profile and memory
        if os.path.isfile(self.filePath) == True:
            os.remove(self.filePath)
            print(f'removing old profile data...')
        if os.path.isfile('./data/gamememorydata.json') == True:
            os.remove('./data/gamememorydata.json')
            print(f'removing old memory data...')
        #starting stats
        self.level = 1
        self.xp = 0
        self.xpcap = 20
        self.health = 10
        self.healthcap = 10
        self.damage = 0
        self.defense = 1
        self.luck = 1
        self.gold = 0
        #starting gear
        self.weapon = "Fists"
        self.armor = "Cloth Tunic"
        self.data = {"level": self.level, "xp": self.xp, "xpcap": self.xpcap, "health": self.health, "healthcap": self.healthcap, "damage": self.damage, "defense": self.defense, "luck": self.luck, "gold": self.gold, "weapon": self.weapon, "armor": self.armor}
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
        self.wipe()
        with open("./data/gameprofiledata.json", "r") as f:
            data = json.load(f)
        #refill hp to max.
        data["health"] = data["healthcap"]
        self.writeJSON(self.filePath, data)
        self.health = self.healthcap
        self.flare("rest")
        if random.triangular(0, 100, 50) > (55 + self.luck):
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
        self.wipe()
        self.flare("explore")
        if random.triangular(0, 100, 50) > 50:
            self.EVENT = True
            #todo add class of event depending on level of player
            eName, eFlare, eDmg, eGold, eXp, eScale, lClass = self.loadEvent()
            #add high chance of combat on explore
            if bool(random.getrandbits(1)):
                self.fight("class1")
            #get the random damage from event and subtract player defense
            damage = (random.choice(eDmg) - self.defense)
            if damage <= 0:
                damage = 0
            print(f'EVENT - {eName} - {eFlare}')
            if random.triangular(0, 100, 50) > (50 - self.luck):
                print("SUCCESS!")
                self.handleProfileStats(eXp, damage, eGold)
                #loot
                if random.triangular(0, 100, 35) > (50 - self.luck):
                    if bool(random.getrandbits(1)):
                        l = "armor"
                    else:
                        l = "weapon"
                    self.lootGain(lClass, l) #give loot
                self.EVENT = False
            else:
                print("FAILURE!")
                self.handleProfileStats(0, damage, 0)
                self.EVENT = False
        else:
            #add high chance of combat on explore
            if bool(random.getrandbits(1)):
                self.fight("class1")
            else:
                print(f'You find nothing...')

    def loadEvent(self):
        #must be an easier way to do this :S
        eventClassNr = "1"
        lootClass = "1"
        if self.level >= 5 and self.level <= 10:
            eventClassNr = "2"
            lootClass = "2"
        if self.level >= 11 and self.level <= 16:
            eventClassNr = "3"
            lootClass = "3"
        if self.level >= 17 and self.level <= 21:
            eventClassNr = "4"
            lootClass = "4"
        if self.level >= 22 and self.level <= 27:
            eventClassNr = "5"
            lootClass = "5"
        if self.currentBiome == 8:
            eventClassNr = "Dun"
            lootClass = "Dun"

        with open(f"./data/event/class{eventClassNr}events.json", "r") as f:
            eventData = json.load(f)
        eventKey = random.choice(list(eventData.keys()))
        eventFlare = eventData[eventKey]["flare"]
        eventDamage = eventData[eventKey]["damage"]
        eventGold = eventData[eventKey]["gold"]
        eventXp = eventData[eventKey]["xp"]
        eventScale = eventData[eventKey]["scale"]
        f.close()
        return eventKey, eventFlare, eventDamage, eventGold, eventXp, eventScale, lootClass


    #handles basic stats
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

        #levelup
        if self.xp >= self.xpcap:
            excess = (self.xp - self.xpcap) #get excess if over the cap
            #memory stat update
            self.level += 1
            self.xp = 0
            self.xp += excess
            self.xpcap += (self.xpcap + self.level) #classic level cap increase
            self.damage += 1
            self.defense += 1
            self.luck += 1
            self.healthcap += 2
            #file stat update
            data["level"] = self.level
            data["xpcap"] = self.xpcap
            data["damage"] = self.damage
            data["defense"] = self.defense
            data["luck"] = self.luck
            data["healthcap"] = self.healthcap
            print(f'DING! level {self.level}! +1 to all stats! and +2 healthcap')
        else:
            data["xp"] = self.xp
        data["health"] = self.health
        data["gold"] = self.gold
        if len(statchange) > 15:
            print(statchange)
        print(f'Current stats: life:{data["health"]}/{data["healthcap"]} lvl:{data["level"]} xp:{data["xp"]}/{data["xpcap"]} $:{data["gold"]} dmg:{data["damage"]} def:{data["defense"]} luck:{data["luck"]}')
        self.writeJSON(self.filePath, data)
        f.close()
        #print(f'DEBUG - {self.xp} / {self.xpcap} - DEBUG')

    def fight(self, classStr):
        #grab enemy
        with open(f"./data/enemy/{classStr}enemys.json", "r") as f:
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

        #get gear Stats
        gDmg, gDef = self.gearStats()
        #combat calculations
        #loop over player and enemy damage?
        acctual_player_damage = (self.damage + gDmg)
        acctual_enemy_health = (Elife * amount)
        acctual_enemy_damage = ((Edmg * Escale) * amount)
        acctual_enemy_xp = (Exp * amount)
        acctual_enemy_gold = ((Egold + self.luck) * amount)
        #math? :S
        rounds = 0
        while acctual_enemy_health > 0:
            acctual_enemy_health -= acctual_player_damage
            rounds += 1
        acctual_enemy_damage = (acctual_enemy_damage * rounds) / (self.defense + gDef)
        #end
        #add some random luck based chances for diffrent things?
        self.handleProfileStats(int(acctual_enemy_xp), int(acctual_enemy_damage), int(acctual_enemy_gold)) #rounding here hopefully no problems?

    def gearStats(self):
        armorsPath = os.listdir("./data/armor/")
        weaponsPath = os.listdir("./data/weapon/")
        currentArmor = self.armor
        currentWeapon = self.weapon
        for i in armorsPath:
            with open(f"./data/armor/{i}", "r") as a:
                #print(f'Loading {i}...')
                data = json.load(a)
                if currentArmor in data.keys():
                    #print("yup")
                    currentArmorDefense = data[currentArmor]
                    a.close()
                    break
        for i in weaponsPath:
            with open(f"./data/weapon/{i}", "r") as w:
                #print(f'Loading {i}...')
                data = json.load(w)
                if currentWeapon in data.keys():
                    #print("yup")
                    currentWeaponDamage = data[currentWeapon]
                    w.close()
                    break
        return currentWeaponDamage ,currentArmorDefense

    #this needs level based loot for class files
    def lootGain(self, classNr, typeN):
        with open(f"./data/{typeN}/class{classNr}{typeN}.json", "r") as f:
            lootData = json.load(f)
        gearKey = random.choice(list(lootData.keys()))
        currentDamage, currentArmor = self.gearStats()
        f.close()

        if typeN == "armor":
            if currentArmor >= lootData[gearKey]:
                print(f'You looted {gearKey} but what you have is better.')
            else:
                print(f'You looted {gearKey}!')
                self.armor = gearKey
                with open(self.filePath, "r") as a:
                    pData = json.load(a)
                pData["armor"] = self.armor
                self.writeJSON(self.filePath, pData)
                a.close()

        if typeN == "weapon":
            if currentDamage >= lootData[gearKey]:
                print(f'You looted {gearKey} but what you have is better.')
            else:
                print(f'You looted {gearKey}!')
                self.weapon = gearKey
                with open(self.filePath, "r") as a:
                    pData = json.load(a)
                pData["weapon"] = self.weapon
                self.writeJSON(self.filePath, pData)
                a.close()




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
