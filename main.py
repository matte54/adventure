import random, json, os

def newGame():
    filePath = f"./data/gameprofiledata.json"
    #delete old profile
    if os.path.isfile(filePath) == True:
        os.remove(filePath)
        print(f'removing old profile data...')
    #starting stats
    level = 1
    xp = 0
    xpcap = 20
    health = 10
    damage = 0
    defense = 0
    gold = 0
    #starting gear
    weapon = "Fists"
    armor = "Cloth Tunic"
    data = {"level": level, "xp": xp, "xpcap": xpcap, "health": health, "healthcap": health, "damage": damage, "defense": defense, "gold": gold, "weapon": weapon, "armor": armor}
    writeJSON(filePath, data)

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

def move(direction): #todo add opposite of last heading to lead to previous biome? but..how?
    filePath = f"./data/gamememorydata.json"
    if os.path.isfile(filePath) != True:
        data = {"currentbiome": 1, "previousbiome": 1, "lastheading": "", "activity": ""}
        writeJSON(filePath, data)
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
        #print(f'New direction...')
        biomeList = [data["previousbiome"], data["currentbiome"]]
        for i in range(2):
            x = random.choice(list(biomeData))
            biomeList.append(x)
        biome = random.choice(biomeList)
        data["previousbiome"] = data["currentbiome"]
        data["currentbiome"] = biome
        data["lastheading"] = direction
    else:
        #print(f'Heading back...')
        extra = data["currentbiome"]
        data["currentbiome"] = data["previousbiome"]
        data["previousbiome"] = extra
        data["lastheading"] = direction

    #get text printed biomename
    for i in biomeData:
        if i == data["currentbiome"]:
            biomeText = biomeData[i]

    msg = f'You are in a {biomeText} biome , what will you do?'
    f.close()
    bf.close()
    writeJSON(filePath, data)
    return msg

def rest():
    with open("./data/gameprofiledata.json", "r") as f:
        data = json.load(f)
    #refill hp to max.
    data["health"] = data["healthcap"]

def explore():
    pass

def spawnMob():
    pass

def choice():
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

def writeJSON(filePath, data):
    with open(filePath, "w") as f:
        json.dump(data, f, indent=4)
        f.close()

def readProfile():
    with open("./data/gameprofiledata.json", "r") as f:
        data = json.load(f)
    f.close()
    return data

def inputMove():
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


def game():#gameloop
    #wait for input from user
    i = None
    while i == None:
        i = inputMove()
    mMsg = move(i)
    print(mMsg)
    y = None
    while y == None:
        y = choice()
    if y == "move":
        return # go back to start of gameloop
    elif y == "explore":
        print("exploring...")
    elif y == "rest":
        rest()
        print("resting...")






while True:
    game()
