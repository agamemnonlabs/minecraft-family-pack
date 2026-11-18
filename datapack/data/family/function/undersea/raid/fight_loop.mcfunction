execute as @a[tag=family.raid.in] at @s unless dimension family:undersea run function family:undersea/raid/leave
execute in family:undersea as @a[tag=family.raid.in] unless entity @s[x=-250,y=18,z=-232,dx=158,dy=90,dz=164] run function family:undersea/raid/leave
execute in family:undersea as @a[x=-230,y=18,z=-212,dx=118,dy=90,dz=124,tag=!family.raid.in,tag=!family.raid.exempt,tag=!family.racing,gamemode=!spectator] run function family:undersea/raid/join
execute in family:undersea run bossbar set family:raid_wave players @a[distance=0..]
execute in family:undersea run bossbar set family:raid_spirit players @a[distance=0..]
execute in family:undersea run bossbar set family:raid_captain players @a[distance=0..]
execute in family:undersea if entity @a[x=-230,y=18,z=-212,dx=118,dy=90,dz=124] run scoreboard players set #quiet family.raid 0
execute in family:undersea unless entity @a[x=-230,y=18,z=-212,dx=118,dy=90,dz=124] run scoreboard players add #quiet family.raid 1
execute if score #quiet family.raid matches 30.. run return run function family:undersea/raid/finish
scoreboard players add #regen family.raid 1
execute if score #regen family.raid matches 10.. run function family:undersea/raid/regen
execute if score #wave family.raid matches 0 run return run function family:undersea/raid/warning
function family:undersea/raid/fighting
