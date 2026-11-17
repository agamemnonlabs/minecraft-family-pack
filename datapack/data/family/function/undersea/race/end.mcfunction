tag @s remove family.racing
scoreboard players reset @s family.race_cp
scoreboard players reset @s family.race_t
scoreboard players reset @s family.race_cd
execute if entity @s[tag=family.race.creative] run gamemode creative @s
execute if entity @s[tag=family.race.survival] run gamemode survival @s
tag @s remove family.race.creative
tag @s remove family.race.survival
title @s actionbar ""
