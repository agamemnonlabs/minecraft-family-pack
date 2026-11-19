execute if entity @s[tag=family.chute_open] run function family:parachute/drift
execute if entity @s[tag=!family.chute_open] run function family:parachute/closed
execute if predicate family:parachute/jump run return run tag @s add family.chute_jump
tag @s remove family.chute_jump
