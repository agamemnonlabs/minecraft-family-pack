tag @s remove family.bopper
scoreboard players add @s family.bops 0
title @s times 5 60 20
title @s subtitle [{"text":"You bopped ","color":"white"},{"score":{"name":"@s","objective":"family.bops"},"color":"gold"},{"text":" clams!","color":"white"}]
title @s title {"text":"Time's up!","color":"light_purple","bold":true}
playsound minecraft:entity.player.levelup master @s ~ ~ ~
execute store result score #day family.house run time query gametime
scoreboard players operation #day family.house /= #day_ticks family.house
execute if score @s family.bops matches 10.. unless score @s family.bop_day = #day family.house run function family:undersea/houses/bop/prize
execute if score @s family.bops matches 1.. unless score @s family.bop_best >= @s family.bops run function family:undersea/houses/bop/best
