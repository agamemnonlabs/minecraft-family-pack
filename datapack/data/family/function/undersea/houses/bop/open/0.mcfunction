execute if score #c0 family.house matches 1.. run return fail
execute in family:undersea run setblock -140 40 -162 minecraft:pearlescent_froglight[axis=y]
execute if score #game family.house matches 401..600 run scoreboard players set #c0 family.house 28
execute if score #game family.house matches 201..400 run scoreboard players set #c0 family.house 22
execute if score #game family.house matches 1..200 run scoreboard players set #c0 family.house 16
execute in family:undersea run particle minecraft:bubble -139.5 40.5 -161.5 0.3 0.4 0.3 0.05 12
execute in family:undersea run playsound minecraft:block.bubble_column.bubble_pop block @a -139.5 40.5 -161.5 1 1.4
