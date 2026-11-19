execute if items entity @s armor.chest *[minecraft:item_model="family:parachute_open"] run item modify entity @s armor.chest family:parachute/fold
execute if predicate family:parachute/landed run tag @s remove family.chute_folded
execute if predicate family:parachute/can_open if block ~ ~-1 ~ #minecraft:air if block ~ ~-2 ~ #minecraft:air if block ~ ~-3 ~ #minecraft:air run function family:parachute/try_open
