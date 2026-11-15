execute unless score @s family.ret matches 1 run return run function family:undersea/to_home
execute store result storage family:undersea ret.x double 0.01 run scoreboard players get @s family.rx
execute store result storage family:undersea ret.y double 0.01 run scoreboard players get @s family.ry
execute store result storage family:undersea ret.z double 0.01 run scoreboard players get @s family.rz
function family:undersea/to_overworld with storage family:undersea ret
execute at @s run playsound minecraft:block.bubble_column.upwards_inside player @s ~ ~ ~
