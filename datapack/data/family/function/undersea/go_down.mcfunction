execute store result score @s family.rx run data get entity @s Pos[0] 100
execute store result score @s family.ry run data get entity @s Pos[1] 100
execute store result score @s family.rz run data get entity @s Pos[2] 100
scoreboard players set @s family.ret 1
effect give @s minecraft:conduit_power 20 0 true
function family:undersea/to_hub with storage family:undersea hub
execute at @s run playsound minecraft:block.bubble_column.whirlpool_inside player @s ~ ~ ~
title @s actionbar {"text": "Welcome to the Undersea! Step on a pink pad to dress up.", "color": "aqua"}
