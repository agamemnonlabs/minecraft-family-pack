scoreboard players add #t family.raid 1
scoreboard players add #elapsed family.raid 1
execute store result score #left family.raid if entity @e[tag=family.raider,tag=!family.raid.mount]
execute in family:undersea positioned -167.5 39 -143.5 store result score #hub family.raid if entity @e[tag=family.raider,tag=!family.raid.mount,distance=..8]
scoreboard players operation #spirit family.raid -= #hub family.raid
execute if score #hub family.raid matches 1.. as @a[tag=family.raid.in] run title @s actionbar {"text": "Raiders in the square! Town Spirit is dropping!", "color": "red"}
execute store result bossbar family:raid_spirit value run scoreboard players get #spirit family.raid
execute store result bossbar family:raid_wave value run scoreboard players get #left family.raid
bossbar set family:raid_wave name [{"text": "Wave ", "color": "red"}, {"score": {"name": "#wave", "objective": "family.raid"}}, {"text": " of 3 - "}, {"score": {"name": "#left", "objective": "family.raid"}}, {"text": " raiders left"}]
execute if score #wave family.raid matches 3 store result bossbar family:raid_captain value run data get entity @e[tag=family.raid.captain,limit=1] Health
tag @e[tag=family.raid.mount] add family.raid.lonely
execute as @e[tag=family.raid.rider] on vehicle run tag @s remove family.raid.lonely
execute as @e[tag=family.raid.lonely] at @s run function family:undersea/raid/flee
execute in family:undersea as @e[tag=family.raider,tag=!family.raid.rider,x=-250,y=63,z=-232,dx=158,dy=175,dz=164] at @s run function family:undersea/raid/pull
execute in family:undersea as @e[tag=family.raider,tag=!family.raid.rider] unless entity @s[x=-250,y=18,z=-232,dx=158,dy=90,dz=164] at @s run function family:undersea/raid/pull
tag @e[tag=family.raid.moved] remove family.raid.moved
execute in family:undersea as @e[tag=family.raider,tag=!family.raid.rider,tag=!family.raid.moved] at @s unless entity @a[distance=..16,gamemode=!creative,gamemode=!spectator] facing -167.5 ~ -143.5 positioned ^ ^0 ^1 if block ~ ~ ~ #family:raid_open if block ~ ~1 ~ #family:raid_open run function family:undersea/raid/step
execute in family:undersea as @e[tag=family.raider,tag=!family.raid.rider,tag=!family.raid.moved] at @s unless entity @a[distance=..16,gamemode=!creative,gamemode=!spectator] facing -167.5 ~ -143.5 positioned ^ ^1 ^1 if block ~ ~ ~ #family:raid_open if block ~ ~1 ~ #family:raid_open run function family:undersea/raid/step
execute if score #spirit family.raid matches ..0 run return run function family:undersea/raid/lose
execute if score #elapsed family.raid matches 480.. run return run function family:undersea/raid/lose
execute if score #wave family.raid matches 3 unless entity @e[tag=family.raid.captain] run return run function family:undersea/raid/win
execute if score #wave family.raid matches 1..2 if score #left family.raid matches ..2 if score #t family.raid matches 5.. run return run function family:undersea/raid/next
execute if score #wave family.raid matches 1..2 if score #t family.raid matches 90.. run function family:undersea/raid/next
