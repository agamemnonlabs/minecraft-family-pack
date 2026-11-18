tag @s remove family.raid.in
effect clear @s minecraft:regeneration
execute if entity @s[tag=family.racing,tag=family.raid.creative] run tag @s add family.race.creative
execute if entity @s[tag=family.racing,tag=family.raid.survival] run tag @s add family.race.survival
execute if entity @s[tag=!family.racing,tag=family.raid.creative] run gamemode creative @s
execute if entity @s[tag=!family.racing,tag=family.raid.survival] run gamemode survival @s
tag @s remove family.raid.creative
tag @s remove family.raid.survival
