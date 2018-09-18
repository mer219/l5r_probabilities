#! /usr/bin/env python

import sys

def calculate(success_list):

    if len(success_list) > 0 :
        return success_list[0] + (1 - success_list[0]) * calculate(success_list[1:])
   
    return 0

def build_combinations(dicepool, target_number, kept_dice):
    combinations = list()

    if (target_number <= 0) or ( kept_dice <= 0):
        return list()

    for die in dicepool:
        combinations.append([(die, target_number - 1)]) # we return the type of die and number of explosions

    if (kept_dice != 1) and (target_number != 1):
        for die in range (len(dicepool)):
            for i in range (1, target_number):
                other_combinations = build_combinations(dicepool[die + 1:], i, kept_dice - 1)
                for other_combination in other_combinations:
                    combination = list()
                    combination.append((dicepool[die], target_number - i - 1)) # we return the type of die and number of explosions
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
        success_chance = 1
        for die in combination:
            die_type, number_of_explosions = die
            if (die_type == "ring"):
                if ( number_of_explosions == (target_number - 1) ):
                    success_chance *= ring_success_at_least * (explosion ** number_of_explosions) 
                else:
                    success_chance *= ring_success_exact * (explosion ** number_of_explosions)
      
            if (die_type == "skill"):
                if ( number_of_explosions == (target_number - 1) ):
                    success_chance *= skill_success_at_least * (explosion ** number_of_explosions) 
                else:
                    success_chance *= skill_success_exact * (explosion ** number_of_explosions)

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

global skill_success_exact
skill_success_exact = 5.0/12.0 + 1.0/6.0 * 5.0/12.0 #success or explode with failure

global skill_success_at_least
skill_success_at_least = 7.0/12.0 #success or explode with failure

global explosion
explosion = 1.0/6.0


#rings = int(sys.argv[1])
#skills = int(sys.argv[2])
target_number = int(sys.argv[1])
output = list()

for rings in range(1, 6):
    for skills in range(0, 6):
         success_list = build_success_list(rings, skills, target_number)
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
   
 
