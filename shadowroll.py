import re
import random
import readline
from collections import OrderedDict

def roll(count):
    return [random.choice(range(1,6)) for _ in range(count)]

def default_roll(count):
    count = int(count)

    ret = OrderedDict()

    result = roll(count)

    if sum(1 for r in result if r == 1) > count/2: # TODO round up or down
        ret["Ergebnis"] = "Kritischer Fehlschlag"

    ret["Erfolge"] = str(sum(1 for r in result if r >= 5)) + "/" + str(count)
    ret["Summe"] = sum(result)
    ret["Wurf"] = " ".join(map(str, sorted(result)))
    
    return ret

# TODO Charakterlimits

def comparing_roll(count, limit):
    count = int(count)
    limit = int(limit)

    ret = OrderedDict()

    result = roll(count)

    success_count = sum(1 for r in result if r >= 5)

    if success_count >= limit: # TODO comparison correct?
        msg = "Erfolg"
    else:
        msg = "Fehlschlag"

    if sum(1 for r in result if r == 1) > count/2: # TODO round up or down
        msg += ", Kritischer Fehlschlag"

    ret["Ergebnis"] = msg
    ret["Nettoerfolge"] = success_count - limit
    ret["Erfolge"] = str(success_count) + "/" + str(count)
    #ret["Summe"] = sum(result)
    ret["Wurf"] = " ".join(map(str, sorted(result)))

    return ret

    

def display(result : OrderedDict):
    max_key_len = max(len(k) for k in result.keys())

    for k, v in result.items():
        print(k, " " * (max_key_len - len(k)), str(v))

REGEX_TO_FUNC = {
    r"(\d+)w-(\d+)$": comparing_roll,
    r"(\d+)w$" : default_roll,
    r"exit$": lambda : exit(0),
    r"quit$": lambda : exit(0)
}

def main():

    while True:
        cmdstr = input("> ")

        # Allow for comments
        cmdstr = cmdstr.split("#")[0].strip()

        for regex, func in REGEX_TO_FUNC.items():
            m = re.match(regex, cmdstr)
            if m:
                res = func(*m.groups())
                display(res)
                break
        else:
            print("Ungültiger Befehl.")
            

if __name__ == "__main__":
    main()