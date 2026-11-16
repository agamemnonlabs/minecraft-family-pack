advancement revoke @s only family:katana_use_wind
execute if score @s family.kcd matches 1.. run return 0
scoreboard players set @s family.kcd 60
scoreboard players set @s family.kel 4
scoreboard players set @s family.kfr 4
swing @s mainhand stab 6t
playsound minecraft:family.katana_wind_special player @a ~ ~ ~ 1 1
title @s actionbar {"text": "Gale Spiral!", "color": "#6FF2C0"}
