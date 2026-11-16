advancement revoke @s only family:katana_use_flame
execute if score @s family.kcd matches 1.. run return 0
scoreboard players set @s family.kcd 60
scoreboard players set @s family.kel 1
scoreboard players set @s family.kfr 3
swing @s mainhand whack 10t
playsound minecraft:family.katana_flame_special player @a ~ ~ ~ 1 1
title @s actionbar {"text": "Ember Crescent!", "color": "#FF7A1A"}
