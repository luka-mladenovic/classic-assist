from System import Array, UInt32, Nullable, Type, Object
from System.Reflection import BindingFlags
from Assistant import Engine
from ClassicAssist.UO.Network.PacketFilter import PacketFilterInfo, PacketDirection
from ClassicAssist.Data.Macros.Commands.MainCommands import Pause

# === Reflection setup for ClassicUO internals ===
UIManager_type = Engine.ClassicAssembly.GetType("ClassicUO.Game.Managers.UIManager")
TextEntryDialogGump_type = Engine.ClassicAssembly.GetType("ClassicUO.Game.UI.Gumps.TextEntryDialogGump")
OnButtonClick_method = TextEntryDialogGump_type.GetMethod("OnButtonClick")

GetGump_method = UIManager_type.GetMethod(
    "GetGump",
    BindingFlags.Static | BindingFlags.Public,
    None,
    Array[Type]([Nullable[UInt32]]),
    None
).MakeGenericMethod(TextEntryDialogGump_type)

# === Core helpers ===
def GetTextEntry():
    """Return the active TextEntryDialogGump if it exists."""
    return GetGump_method.Invoke(None, Array[Object]([None]))

def WaitForTextEntry(timeout_ms=5000):
    """Wait for a text entry gump to appear (up to timeout_ms)."""
    if GetTextEntry():
        return True

    pfi = PacketFilterInfo(0xAB)  # 0xAB = server text entry prompt
    wait_entry = Engine.PacketWaitEntries.Add(pfi, PacketDirection.Incoming, True)
    
    if not wait_entry.Lock.WaitOne(timeout_ms):
        Engine.PacketWaitEntries.Remove(wait_entry)
        return False

    # Give the client up to 1s to build the gump
    for _ in range(20):
        if GetTextEntry():
            return True
        Pause(50)
    
    return False

def ReplyTextEntry(value):
    """Fill and submit a text entry dialog safely."""
    gump = GetTextEntry()
    if not gump:
        return False

    # Find the text box inside the gump
    textBoxes = [c for c in gump.Children if c.GetType().Name == "TextBox"]
    if not textBoxes:
        return False

    # Fill the text box with our value
    textBoxes[0].Text = str(value)

    # Try both common button IDs
    try:
        OnButtonClick_method.Invoke(gump, Array[Object]([1]))  # ID 1 = OK
    except:
        OnButtonClick_method.Invoke(gump, Array[Object]([0]))  # fallback

    return True
