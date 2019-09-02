import random
possibleDictionary ='ABCDEFGHKMNPQRSTUVWXYZabcdefghkmnpqrstuvwxyz23456789'
dicts_len =len(possibleDictionary)
def dictionaryRandom(lenChars=12):
    text = ''

    for i in range(lenChars):
        idx=random.randint(0,dicts_len-1)
        text+=possibleDictionary[idx]
    return text
