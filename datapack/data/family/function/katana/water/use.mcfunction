advancement revoke @s only family:katana_use_water
execute if score @s family.kcd matches 1.. run return 0
scoreboard players set @s family.kcd 60
scoreboard players set @s family.kel 2
scoreboard players set @s family.kfr 4
swing @s mainhand whack 12t
playsound minecraft:family.katana_water_special player @a ~ ~ ~ 1 1
title @s actionbar {"text": "Tide Ribbon!", "color": "#3FA9FF"}
