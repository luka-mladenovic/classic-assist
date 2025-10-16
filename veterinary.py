FindType(3617)
ClearJournal()
PromptAlias("animal")
PromptAlias("bandage")

while True:
    while Hits("animal") < (MaxHits("animal") - 10):
        UseObject("bandage")
        WaitForTargetOrFizzle(500)
        Target("animal")
        Pause(2000)
    
    while Hits("animal") == MaxHits("animal"):
        WarMode("on")
        Attack("animal")
        Pause(100)
    
    WarMode("off")
    
    if InJournal("Looks Hungry"):
        Feed("animal", 0x171F)
        print("Animal fed!!!")
        ClearJournal()
