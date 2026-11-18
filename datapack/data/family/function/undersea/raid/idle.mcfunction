execute as @e[tag=family.raider] at @s run function family:undersea/raid/flee
kill @e[type=minecraft:text_display,tag=family.raid.banner]
execute as @a[tag=family.raid.in] run function family:undersea/raid/leave
execute if score #cool family.raid matches 1.. run scoreboard players remove #cool family.raid 1
scoreboard players add #since family.raid 1
execute in family:undersea if entity @a[x=-230,y=18,z=-212,dx=118,dy=90,dz=124,tag=!family.raid.exempt,gamemode=!spectator] run scoreboard players add #town family.raid 1
execute in family:undersea unless entity @a[x=-230,y=18,z=-212,dx=118,dy=90,dz=124,tag=!family.raid.exempt,gamemode=!spectator] run scoreboard players set #town family.raid 0
execute if score #night family.alive matches 0 run scoreboard players set #dusk family.raid 0
execute if score #night family.alive matches 1 unless score #dusk family.raid matches 1 run function family:undersea/raid/dusk
execute in family:undersea positioned -167.5 39 -143.5 if entity @a[distance=..24] run scoreboard players add #near family.raid 1
execute in family:undersea positioned -167.5 39 -143.5 unless entity @a[distance=..24] run scoreboard players set #near family.raid 0
execute if score #built family.raid matches 1 if score #near family.raid matches 5.. run function family:undersea/raid/repair
scoreboard players add #heal family.raid 1
execute if score #heal family.raid matches 30.. run function family:undersea/raid/lamps_white
