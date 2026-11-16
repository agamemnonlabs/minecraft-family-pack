advancement revoke @s only family:katana_use_thunder
execute if score @s family.kcd matches 1.. run return 0
scoreboard players set @s family.kcd 60
scoreboard players set @s family.kel 3
scoreboard players set @s family.kfr 3
swing @s mainhand whack 7t
playsound minecraft:family.katana_thunder_special player @a ~ ~ ~ 1 1
title @s actionbar {"text": "Storm Strike!", "color": "#FFD23A"}
