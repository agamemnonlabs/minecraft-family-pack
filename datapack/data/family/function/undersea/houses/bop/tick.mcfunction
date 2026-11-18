scoreboard players remove #game family.house 1
execute if score #game family.house matches 601.. run return run function family:undersea/houses/bop/countdown
execute if score #game family.house matches 600 run function family:undersea/houses/bop/go
execute as @e[type=minecraft:interaction,tag=family.tap.clam0] if data entity @s attack run function family:undersea/houses/bop/hit/0
execute as @e[type=minecraft:interaction,tag=family.tap.clam1] if data entity @s attack run function family:undersea/houses/bop/hit/1
execute as @e[type=minecraft:interaction,tag=family.tap.clam2] if data entity @s attack run function family:undersea/houses/bop/hit/2
execute as @e[type=minecraft:interaction,tag=family.tap.clam3] if data entity @s attack run function family:undersea/houses/bop/hit/3
execute as @e[type=minecraft:interaction,tag=family.tap.clam4] if data entity @s attack run function family:undersea/houses/bop/hit/4
execute as @e[type=minecraft:interaction,tag=family.tap.clam5] if data entity @s attack run function family:undersea/houses/bop/hit/5
execute as @e[type=minecraft:interaction,tag=family.tap.clam6] if data entity @s attack run function family:undersea/houses/bop/hit/6
execute as @e[type=minecraft:interaction,tag=family.tap.clam7] if data entity @s attack run function family:undersea/houses/bop/hit/7
execute if score #c0 family.house matches 1 run function family:undersea/houses/bop/shut/0
execute if score #c1 family.house matches 1 run function family:undersea/houses/bop/shut/1
execute if score #c2 family.house matches 1 run function family:undersea/houses/bop/shut/2
execute if score #c3 family.house matches 1 run function family:undersea/houses/bop/shut/3
execute if score #c4 family.house matches 1 run function family:undersea/houses/bop/shut/4
execute if score #c5 family.house matches 1 run function family:undersea/houses/bop/shut/5
execute if score #c6 family.house matches 1 run function family:undersea/houses/bop/shut/6
execute if score #c7 family.house matches 1 run function family:undersea/houses/bop/shut/7
execute if score #c0 family.house matches 1.. run scoreboard players remove #c0 family.house 1
execute if score #c1 family.house matches 1.. run scoreboard players remove #c1 family.house 1
execute if score #c2 family.house matches 1.. run scoreboard players remove #c2 family.house 1
execute if score #c3 family.house matches 1.. run scoreboard players remove #c3 family.house 1
execute if score #c4 family.house matches 1.. run scoreboard players remove #c4 family.house 1
execute if score #c5 family.house matches 1.. run scoreboard players remove #c5 family.house 1
execute if score #c6 family.house matches 1.. run scoreboard players remove #c6 family.house 1
execute if score #c7 family.house matches 1.. run scoreboard players remove #c7 family.house 1
scoreboard players remove #next family.house 1
execute if score #next family.house matches ..0 run function family:undersea/houses/bop/pop
scoreboard players operation #s family.house = #game family.house
scoreboard players operation #s family.house /= #20 family.house
execute in family:undersea as @a[x=-143,y=39,z=-167,dx=12,dy=11,dz=13] run function family:undersea/houses/bop/show
execute if score #game family.house matches 0 run function family:undersea/houses/bop/end
