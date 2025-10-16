from ClassicAssist.UO.Data import Statics
from ClassicAssist.UO import UOMath
from Assistant import Engine
from System import Convert
import clr
clr.AddReference('System.Core')

logs = [0x1bdd]
chopping = False

moveLogsToPackAnimal = True
treeNames = ["walnut tree"]

if moveLogsToPackAnimal == True:
    PromptAlias("pack animal")

def moveToPackAnimal():
    for log in logs:
        while FindType(log, -1, 'backpack'):
            if InJournal("out of sight"):
              break
            MoveItem("found", "pack animal")
            SysMessage("Logs moved to pack animal")
            Pause(1000)

def GetNearestTree():
    trees = []
    for x in range(Engine.Player.X - 20, Engine.Player.X + 20):
        for y in range(Engine.Player.Y - 20, Engine.Player.Y + 20):
            statics = Statics.GetStatics(Convert.ChangeType(Engine.Player.Map, int), x, y)
            if statics is None:
                continue
            for s in statics:
                if s.Name.lower() in treeNames:
                    trees.append({'X': s.X, 'Y': s.Y, 'Z': s.Z})
    trees.sort(key=lambda t: (t['X'], t['Y']))
    return trees

def moveToTree(tree):
    Msg("All follow me")
    global chopping
    chopping = False
    i = 0
    while X("self") != tree['X'] or Y("self") != tree['Y']:
        if i >= 5 or InJournal("maximum distance"): 
            print("Pathfinding failed. Skipping tree.")            
            ClearJournal()
            return False
        print("*Pathfinding*")
        Pathfind(tree['X'], tree['Y'], tree['Z'])
        Pause(2000)
        i += 1
    return True

def lumberjack():
    global chopping
    ClearJournal()
    while not InJournal("not enough") and not InJournal("can't use an axe") and not InJournal("You cannot harvest wood"):
        if (chopping == False):
            UseLayer("TwoHanded")
            chopping = True
            WaitForTarget(1000)
            TargetTileOffsetResource(-1, 0, 0)
        Pause(1500)

Trees = GetNearestTree()
if len(Trees) > 0:
    TotalTrees = len(Trees)
    SysMessage(str(TotalTrees) + " total trees in queue")
    for tree in Trees:
        tree['X'] += 1
        if moveToTree(tree):
            lumberjack()
            if GetAlias("pack animal") != 0:
               moveToPackAnimal()
            TotalTrees -= 1
            SysMessage(str(TotalTrees) + " trees left in the queue!")
            ClearJournal()