from mcflask.models import User, Server, staffmembers, servers, addServer, addUser


def initmembers():

    darkraider462 = addUser("owner", "DarkRaider462", is_staff = True, password = "invalid", confirmed = True, panel = True)

    opprison = addServer('opprison', 'OPprison')
    kitpvp= addServer('kitpvp', 'KitPVP')
    clanwars = addServer('clanwars', 'ClanWars', True)
    creative = addServer('creative', 'Creative')
    factions = addServer('factions', 'Factions')
    skyblock = addServer('skyblock', 'Skyblock')
    survivalgames = addServer('survivalgames', 'SurvivalGames')


def geturl(url):
    return "mcflask/" + url
