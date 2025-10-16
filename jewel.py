ClearJournal()
PromptAlias("bag")
PromptAlias("trash")
PromptAlias("ingots")
PromptAlias("gem")

items = {
    "ring":      {"type": 0x108A, "id": 6},
    "necklace":  {"type": 0x1089, "id": 5},
    "earring":   {"type": 0x1087, "id": 3},
    "bracelet":  {"type": 0x1086, "id": 2},
    "wand":      {"type": 0xdf2, "id": 7},
}

def enchantItem(itemName):
    ClearJournal()

    if FindType(items[itemName]["type"], -1, "backpack"):
        UseObject(0x5A86FF38)
        WaitForTarget(5000)
        Target("found")
        Pause(3000)
        
        if InJournal("You enchant the item!"):
            ClearJournal()
            UseSkill("Item Identification")
            WaitForTarget(5000)
            Target("found")
            Pause(2000)

            if retryUntilSuperb and GetAlias("trash") != 0:
                if InJournal("superb"):
                    MoveItem("found", "bag")
                else:
                    MoveItem("found", "trash")
            else:              
                MoveItem("found", "bag")

            print("Enchanted and moved to bag.")
        
        elif InJournal("obsidian"):
            print("Obsidian detected, stopping.")
            Stop()
        else:
            print(itemName + " enchant attempt failed or unknown result.")
    else:
        print("No " + itemName + " found in backpack.")


def createItem(itemName):
    attempts = 0

    while True:
        ClearJournal()
        attempts += 1
        print("Attempt " + str(attempts) + ": creating " + itemName + "...")

        UseObject(0x5A86FF38)
        WaitForTarget(5000)
        Target("ingots")
        
        WaitForMenu(0x0, 5000)
        ReplyMenu(0x0, items[itemName]["id"])
        
        WaitForTarget(5000)
        Target("gem")
        Pause(7000)

        if InJournal("create the item"):
            print(itemName + " created — enchanting...")
            enchantItem(itemName)

        if attempts >= 5:
            print("Failed to create superb " + itemName + " after 5 attempts — stopping.")
            break

        if retryUntilSuperb:
            if InJournal("superb"):
                print("Superb " + itemName + " created after " + str(attempts) + " attempt(s).")
                return True
            else:
                print(itemName + " not superb — retrying...")
                Pause(500)
                continue
        else:
            break

def createSet(withWand = False):
    for name in items:
        if name == "wand" and not withWand:
            continue
        print("Creating and enchanting " + name + "...")
        success = createItem(name)
        Pause(1000)

def createSelectedItem(itemName):
    createdCount = 0
    while True:
        if maxItems > 0 and createdCount == maxItems:
            break
            
        if GetAlias("gem") == 0:
            print("No gem alias or out of gems — stopping.")
            break

        ClearJournal()
        success = createItem(itemName)

        if success == True:
            createdCount += 1

        Pause(1000)

itemName = "wand"
retryUntilSuperb = True
maxItems = 1 

if itemName == "set": # make full jewelry set once
    createSet(false)   
else: # repeatedly craft selected item
    createSelectedItem(itemName)  
