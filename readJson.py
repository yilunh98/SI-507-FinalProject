import json

def retrieveFunds():
    cache_file = open('fundsData.json', 'r')
    funds_data = json.loads(cache_file.read())
    cache_file.close()
    return funds_data

def retrieveManagers():
    cache_file = open('managersData.json', 'r')
    managers_data = json.loads(cache_file.read())
    cache_file.close()
    return managers_data