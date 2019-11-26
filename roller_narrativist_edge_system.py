import heapq, random
from sys import argv

def get_karma_type(die, karma_d):
    if die in [1,karma_d]:
        return die
    else:
        return 0

def get_def_dies(def_dies):
    dies = 0
    if type(def_dies) == list:
        for d in def_dies:
            dies += random.randint(1,d)
    else:
        dies += random.randint(1,def_dies)
    return dies


res = []
n = int(argv[1])
skill = int(argv[2])
karma_d = 6
def_d = [20]
df = karma_d/2 + (def_d[0]/2)*int(len(def_d)) + 2*len(def_d)
for neg in [True, False]:
    if n == 1 and neg == True:
        continue
    for i in range(1,100000):
        rolls = []
        for r in range(0,n):
            rolls.append(random.randint(1,karma_d))
        if neg:
            karma_die = rolls[0] if len(rolls) <= 1 else min(rolls)
        else:
            karma_die = rolls[0] if len(rolls) <= 1 else max(rolls)
        def_die = get_def_dies(def_d)
        success = 0
        if karma_die + def_die + skill >= df:
            success = 1
        karma = get_karma_type(karma_die, karma_d)
        res.append(str(success)+str(karma))
     
    print ('rolling '+ ("-" if neg else "+") + str(n) + 'd' + str(karma_d) + ' karma dice and dice ' + str(def_d) +  ' and skill +' + str(skill) + ' against ' + str(df))
    successes = res.count("10")+res.count("11")+res.count("1"+str(karma_d))
    fails = (100000 - successes) /1000
    succ_with_cost = res.count("11")
    fail_with_boon = res.count("0"+str(karma_d))
    crit = res.count("1"+str(karma_d))
    fumble = res.count("01")
    res = []
    print ('success with cost: ' + str(succ_with_cost /1000))
    print ('fail with bonus: ' + str(fail_with_boon /1000))
    print ("successes: " + str(successes/1000))
    print ("crits: " + str(crit/1000))
    print ("fumbles: " + str(fumble/1000))
 
    