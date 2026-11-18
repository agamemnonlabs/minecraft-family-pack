execute if score #c2 family.house matches 1.. run return fail
execute in family:undersea run setblock -135 40 -163 minecraft:pearlescent_froglight[axis=y]
execute if score #game family.house matches 401..600 run scoreboard players set #c2 family.house 28
execute if score #game family.house matches 201..400 run scoreboard players set #c2 family.house 22
execute if score #game family.house matches 1..200 run scoreboard players set #c2 family.house 16
execute in family:undersea run particle minecraft:bubble -134.5 40.5 -162.5 0.3 0.4 0.3 0.05 12
execute in family:undersea run playsound minecraft:block.bubble_column.bubble_pop block @a -134.5 40.5 -162.5 1 1.4
