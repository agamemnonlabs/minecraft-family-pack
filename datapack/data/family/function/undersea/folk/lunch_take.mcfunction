execute if items entity @s container.* minecraft:bowl[minecraft:custom_data~{family_lunch:1}] run return fail
execute store result score #day family.folk run time query gametime
scoreboard players operation #day family.folk /= #day_ticks family.folk
execute if score @s family.lunchday = #day family.folk run return fail
scoreboard players operation @s family.lunchday = #day family.folk
execute store result score #pick family.folk run random value 1..5
execute if score #pick family.folk matches 1 run return run function family:undersea/folk/lunch/mayor
execute if score #pick family.folk matches 2 run return run function family:undersea/folk/lunch/farmer
execute if score #pick family.folk matches 3 run return run function family:undersea/folk/lunch/driver
execute if score #pick family.folk matches 4 run return run function family:undersea/folk/lunch/professor
execute if score #pick family.folk matches 5 run return run function family:undersea/folk/lunch/coach
