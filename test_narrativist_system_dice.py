import heapq, random
import statistics
from sys import argv

def get_karma_type(die, karma_d):
    if die in [1, karma_d]:
        return die
    else:
        return 0


def get_def_dies(def_dies):
    dies = []
    if type(def_dies) == list:
        for d in def_dies:
            dies.append(random.randint(1,d))
    else:
        dies.append(random.randint(1,def_dies))
    return dies


def test_dies(def_d, karma_d):
    res = []
    dice_n = [1,2,3]
    df = karma_d/2 + (def_d[0]/2)*int(len(def_d)) + 2
    skill = 0
    result = []
    for neg in [True, False]:
        for df in [df-2, df, df+2]:
            for n in dice_n:
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
                    def_dies = get_def_dies(def_d)
                    success = 0
                    if karma_die + sum(def_dies) + skill >= df:
                        success = 1
                    karma = get_karma_type(karma_die, karma_d)
                    res.append(str(success)+str(karma))
                 
                print ('rolling ' + ("-" if neg else "+") + str(n) + 'd' + str(karma_d) + ' karma dice and dice' + str(def_d) +  ' and skill +' + str(skill) + ' against ' + str(df))
                successes = res.count("10")+res.count("11")+res.count("1"+str(karma_d))
                fails = (100000 - successes) /1000
                succ_with_cost = res.count("11")
                fail_with_boon = res.count("0"+str(karma_d))
                result.append([succ_with_cost/1000, fail_with_boon/1000])
                res = []
                if succ_with_cost/1000 + fail_with_boon/1000 > 10 and fail_with_boon/1000 > 3 and succ_with_cost/1000 > 3:
                    print ('success with cost: ' + str(succ_with_cost /1000))
                    print ('fail with bonus: ' + str(fail_with_boon /1000))
                    print ("successes: " + str(successes/1000))

            avg_success_with_cost = statistics.mean([r[0] for r in result]) 
            median_success_with_cost = statistics.median([r[0] for r in result]) 
            avg_fail_with_boon = statistics.mean([r[1] for r in result]) 
            median_fail_with_boon = statistics.median([r[1] for r in result]) 

            result_dict["defaultdie: " + str(def_d) + " Karma die " + str(karma_d) + " diff: " + str(df)] = str(
                    "avg, mean success with cost: " + str(avg_success_with_cost) + ", " + str(median_success_with_cost) +
                     ", avg, mean fail with boon: " + str(avg_fail_with_boon)  + ", " + str(median_fail_with_boon)
                )

result_dict = {}

default_die_list = [
    [8,8,8],
    [10,10],
    [10,10,10],
    [12,12],
    [20],
]

karma_die_list = [
        6,
        8,
        10,
    ]

for def_d in default_die_list:
    for karma_d in karma_die_list:
        test_dies(def_d, karma_d)

print(result_dict)


