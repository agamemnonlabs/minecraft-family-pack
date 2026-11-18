execute as @e[tag=family.raid.new] store result entity @s Rotation[0] float 1 run random value 0..359
execute as @e[tag=family.raid.new] at @s positioned ^ ^ ^2.5 positioned over ocean_floor run tp @s ~ ~ ~
execute as @e[tag=family.raid.new] at @s run rotate @s facing -167.5 39 -143.5
tag @e[tag=family.raid.new] remove family.raid.new
