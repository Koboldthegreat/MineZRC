from mcflask.models import User, Server, staffmembers, servers, addServer, addUser


def initmembers():

    darkraider462 = addUser("owner", "DarkRaider462", is_staff = True, password = "invalid", confirmed = True)
    huntingwolf_ = addUser("co-owner", "HuntingWolf_", is_staff = True)
    SmartWizard = addUser("admin", "SmartWizard", is_staff = True)
    mcrb = addUser("admin", "McRB",  is_staff = True)
    dedicatedserver = addUser("admin", "DedicatedServer",  is_staff = True)
    winjw7 = addUser("developer", "Winjw7",  is_staff = True)
    knockbackmad = addUser("moderator", "KnockBackMad",  is_staff = True)
    koboldthegreat = addUser("(web)developer", "KoboldTheGreat",  is_staff = True)

    opprison = addServer('opprison', 'OPprison')
    kitpvp= addServer('kitpvp', 'KitPVP')
    clanwars = addServer('clanwars', 'ClanWars', True)
    creative = addServer('creative', 'Creative')
    factions = addServer('factions', 'Factions')
    skyblock = addServer('skyblock', 'Skyblock')
    survivalgames = addServer('survivalgames', 'SurvivalGames')



    for x in staffmembers:
        x.updateSkin()

def geturl(url):
    return "mcflask/" + url
