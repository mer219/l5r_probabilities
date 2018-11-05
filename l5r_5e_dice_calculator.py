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
            combination.append([die, "Don't Care", 0])
        combinations.append(combination)
        return combinations

    if len(dicepool) == 1:
        combination = list()
        if target_number == 1:
            combination.append([die, "Success", 0])
        else:
            combination.append([die, "Explode", target_number - 1])
        combinations.append(combination)
        return combinations

    if target_number > 1:
        if kept_dice > 1:
            for i in range(target_number, 1, -1):
                this_combination = [die, "Explode", i - 1]
                other_combinations = build_combinations(dicepool[1:], target_number - i, kept_dice - 1)
                for other_combination in other_combinations:
                    combination = list()
                    combination.append(this_combination) 
                    for other_die in other_combination:
                        combination.append(other_die)
                    combinations.append(combination)
        else:
            this_combination = [die, "Explode", target_number - 1]
            other_combinations = build_combinations(dicepool[1:], 0, 0)
            for other_combination in other_combinations:
                combination = list()
                combination.append(this_combination) 
                for other_die in other_combination:
                    combination.append(other_die)
                combinations.append(combination)
            

    if kept_dice > 1 or target_number == 1:
        this_combination = [die, "Success", 0]
        other_combinations = build_combinations(dicepool[1:], target_number - 1, kept_dice - 1)
        for other_combination in other_combinations:
            combination = list()
            combination.append(this_combination) 
            for other_die in other_combination:
                combination.append(other_die)
            combinations.append(combination)

    this_combination = [die, "Failure", 0]
    other_combinations = build_combinations(dicepool[1:], target_number, kept_dice)
    for other_combination in other_combinations:
        combination = list()
        combination.append(this_combination) 
        for other_die in other_combination:
            combination.append(other_die)
        combinations.append(combination)

    return combinations


def build_success_list(rings, skills, target_number):
    dicepool = build_dicepool(rings, skills)
    kept_dice = rings
    if( rings > target_number):
        kept_dice = target_number
     
    combinations = build_combinations(dicepool, target_number, kept_dice)

    success_list = list()

    for combination in combinations:
        #print combination
        success_chance = 1
        for die in combination:
            die_type, result, number_of_explosions = die
            if (die_type == "ring"):
                if result == "Explode":
                    if ( number_of_explosions == (target_number - 1) ):
                        success_chance *= ring_success_at_least * (explosion ** number_of_explosions) 
                    else:
                        success_chance *= ring_success_exact * (explosion ** number_of_explosions)

                if result == "Success":
                    if target_number == 1:
                        success_chance *= ring_success_at_least 
                    else:
                        success_chance *= ring_success_exact
        

                if result == "Failure":
                    success_chance *= ring_failure
      
            if (die_type == "skill"):
                if result == "Explode":
                    if ( number_of_explosions == (target_number - 1) ):
                        success_chance *= skill_success_at_least * (explosion ** number_of_explosions) 
                    else:
                        success_chance *= skill_success_exact * (explosion ** number_of_explosions)

                if result == "Success":
                    if target_number == 1:
                        success_chance *= skill_success_at_least 
                    else:
                        success_chance *= skill_success_exact 

                if result == "Failure":
                    success_chance *= skill_failure

            if result == "Don't Care":
                success_chance *= dont_care

        success_list.append(success_chance)

    return success_list

def build_dicepool(rings, skills):
    dice = list()

    for _ in range(rings):
        dice.append("ring")
    
    for _ in range(skills):
        dice.append("skill")

    return dice

global ring_success_exact
ring_success_exact = 1.0/3.0 + 1.0/6.0 * 1.0/2.0 # success or explode with failure

global ring_success_at_least
ring_success_at_least = 1.0/2.0 #success or exploding success

global ring_failure
ring_failure = 0.5

global skill_success_exact
skill_success_exact = 5.0/12.0 + 1.0/6.0 * 5.0/12.0 #success or explode with failure

global skill_success_at_least
skill_success_at_least = 7.0/12.0 #success or explode with failure

global skill_failure
skill_failure = 5.0/12.0

global explosion
explosion = 1.0/6.0

global dont_care
dont_care = 1.0


target_number = int(sys.argv[1])
output = list()

for rings in range(1, 6):
    for skills in range(0, 6):
     success_list = build_success_list(rings, skills, target_number)
     output.append(calculate(success_list))

#success_list = build_success_list(2, 4, 2)
#output.append(calculate(success_list))

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
   
 
