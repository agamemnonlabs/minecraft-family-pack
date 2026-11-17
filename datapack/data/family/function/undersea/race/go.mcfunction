execute if entity @s[tag=family.racing] run return fail
execute at @s unless dimension family:undersea run return fail
execute at @s unless entity @e[type=minecraft:villager,tag=family.folk.driver,distance=..10] run return fail
tag @s add family.racing
execute if entity @s[gamemode=creative] run tag @s add family.race.creative
execute if entity @s[gamemode=survival] run tag @s add family.race.survival
gamemode adventure @s
scoreboard players set @s family.race_cp 0
scoreboard players set @s family.race_t 0
scoreboard players set @s family.race_cd 61
execute in family:undersea positioned -168 38 -144 run tp @s ~0 ~3 ~14 0 0
title @s times 0 20 5
title @s subtitle {"text":"Get ready...","color":"aqua"}
tellraw @s [{"text": "Driver Finnley", "color": "aqua"}, {"text": ": Ready, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "? Wait for GO, then swim through the START gate!", "color": "white"}]
