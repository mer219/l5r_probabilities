#! /usr/bin/env python

import sys

def calculate(success_list):

    first = True
    success_chance = 1
    for success in success_list:
        if first:
            success_chance *= success
            first = False
        else:
            success_chance += success

    return success_chance

def build_combinations(dicepool, target_number, kept_dice):
    combinations = list()
    die = dicepool[0]
    if target_number == 0 or kept_dice == 0:
        combination = list()
        for die in dicepool:
            combination.append([die, "Ignored", 0])
        combinations.append(combination)
        return combinations

    if len(dicepool) == 1:
        combination = list()
        if target_number == 1:
            #have 1 remaining die, need 1 success, doesn't matter how
            combination.append([die, "Success", 0])
        else:
            #have 1 remaining die, need TN successes, doesn't matter how many bonuses
            combination.append([die, "Explode", target_number - 1])
        combinations.append(combination)
        return combinations

    if target_number > 1:
        if kept_dice > 1:
            for i in range(target_number, 1, -1):
                #Want an exact number of explosions
                this_combination = [die, "Explode", i - 1]
                other_combinations = build_combinations(dicepool[1:], target_number - i, kept_dice - 1)
                for other_combination in other_combinations:
                    combination = list()
                    combination.append(this_combination) 
                    for other_die in other_combination:
                        combination.append(other_die)
                    combinations.append(combination)
        else:
            #Want at least TN explosions
            this_combination = [die, "Explode", target_number - 1]
            other_combinations = build_combinations(dicepool[1:], 0, 0)
            for other_combination in other_combinations:
                combination = list()
                combination.append(this_combination) 
                for other_die in other_combination:
                    combination.append(other_die)
                combinations.append(combination)
            

    if kept_dice > 1 or target_number == 1:
        #want exactly a success
        this_combination = [die, "Success", 0]
        other_combinations = build_combinations(dicepool[1:], target_number - 1, kept_dice - 1)
        for other_combination in other_combinations:
            combination = list()
            combination.append(this_combination) 
            for other_die in other_combination:
                combination.append(other_die)
            combinations.append(combination)

    #all other results
    this_combination = [die, "Failure", 0]
    other_combinations = build_combinations(dicepool[1:], target_number, kept_dice)
    for other_combination in other_combinations:
        combination = list()
        combination.append(this_combination) 
        for other_die in other_combination:
            combination.append(other_die)
        combinations.append(combination)

    return combinations


def build_dicepool(rings, skills):
    dice = list()

    for i in range(rings):
        dice.append(["Ring", "Ring" + str(i)])
    
    for i in range(skills):
        dice.append(["Skill", "Skill" + str(i)])

    return dice

def determine_probabilities(combinations, dice_pool):
    odds = dict()
    odds['Ring'] = dict()
    odds['Skill'] = dict()
    odds['Ring']['Ignored'] = 1.0
    odds['Ring']['Success'] = 3.0/6.0
    odds['Ring']['Explode'] = odds['Ring']['Success']
    odds['Skill']['Ignored'] = 1.0
    odds['Skill']['Success'] = 7.0/12.0
    odds['Skill']['Explode'] = odds['Ring']['Success']
    odds['Explode'] = 1.0/6.0

    encountered_results = dict()
    failure_odds = dict()
    for die in dicepool:
        failure_odds[die[1]] = 1
        encountered_results[die[1]] = list()
        for i in range(0, 10):
            encountered_results[die[1]].append(False)

    for combination in combinations:
        for die in combination:
            die_info, die_result, number_of_explosions = die
            if die_result != "Failure" and die_result != "Ignored":
                if encountered_results[die_info[1]][number_of_explosions] == False:
                    failure_odds[die_info[1]] -= odds[die_info[0]][die_result] * (odds['Explode'] ** number_of_explosions)
                    encountered_results[die_info[1]].insert(number_of_explosions, "True")

    success_chances = list()
    for combination in combinations:
        #print combination
        success_chance = 1
        for die in combination:
            die_info, die_result, number_of_explosions = die
            die_odds = 1
            if die_result == "Failure":
                die_odds = failure_odds[die_info[1]]
            else:
                die_odds = odds[die_info[0]][die_result] * (odds['Explode'] ** number_of_explosions)
            success_chance *= die_odds
        success_chances.append(success_chance)

    return success_chances




target_number = int(sys.argv[1])
output = list()

for rings in range(1, 6):
    for skills in range(0, 6):
        dicepool = build_dicepool(rings, skills)   
        combinations = build_combinations(dicepool, target_number, rings)
        success_list = determine_probabilities(combinations, dicepool)
        output.append(calculate(success_list))



i = 0
string = ""
for result in output:
    if i == 6:
        print string

        i = 0
        string = ""
    string = string + " " +  str(result)
    i += 1
print string
