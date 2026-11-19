execute if entity @s[tag=!family.chute_folded] if predicate family:parachute/fall_far run return run function family:parachute/open
execute if entity @s[tag=!family.chute_jump] if predicate family:parachute/jump if predicate family:parachute/falling run function family:parachute/open
