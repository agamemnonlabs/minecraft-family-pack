tag @s remove family.chute_open
tag @s remove family.chute_brake
execute if predicate family:parachute/sneak unless predicate family:parachute/landed run tag @s add family.chute_folded
execute if items entity @s armor.chest *[minecraft:custom_data~{family_parachute:1b}] run item modify entity @s armor.chest family:parachute/fold
execute if predicate family:parachute/braking run effect clear @s minecraft:levitation
execute if predicate family:parachute/our_slow_fall run effect clear @s minecraft:slow_falling
execute on passengers if entity @s[type=minecraft:item_display,tag=family.canopy] run kill @s
