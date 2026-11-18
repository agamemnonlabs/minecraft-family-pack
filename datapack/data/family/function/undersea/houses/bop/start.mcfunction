execute if score #game family.house matches 1.. run return fail
execute at @s unless entity @e[type=minecraft:villager,tag=family.folk.coach,distance=..12] run return fail
scoreboard players set #game family.house 661
execute in family:undersea as @a[x=-143,y=39,z=-167,dx=12,dy=11,dz=13] run title @s times 0 20 5
execute in family:undersea as @a[x=-143,y=39,z=-167,dx=12,dy=11,dz=13] run title @s subtitle {"text":"Get ready to bop!","color":"light_purple"}
tellraw @s [{"text": "Coach Cockle", "color": "red"}, {"text": ": Here we go, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! Bop the clams when they glow pink!", "color": "white"}]
