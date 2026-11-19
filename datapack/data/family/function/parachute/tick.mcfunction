execute as @e[type=minecraft:item_display,tag=family.canopy] unless predicate family:parachute/riding run kill @s
execute as @e[type=minecraft:item_display,tag=family.canopy_grow] run function family:parachute/grow
tag @a remove family.chute_mount
execute as @a[tag=family.chute_open] unless items entity @s armor.chest *[minecraft:custom_data~{family_parachute:1b}] at @s run function family:parachute/close
execute as @a if items entity @s armor.chest *[minecraft:custom_data~{family_parachute:1b}] at @s run function family:parachute/worn
