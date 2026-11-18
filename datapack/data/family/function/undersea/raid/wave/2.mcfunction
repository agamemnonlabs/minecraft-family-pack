scoreboard players set #wave family.raid 2
scoreboard players set #t family.raid 0
execute store result score #n family.raid if entity @a[tag=family.raid.in]
execute if score #n family.raid matches ..0 run scoreboard players set #n family.raid 1
execute store result score #alive family.raid if entity @e[tag=family.raider,tag=!family.raid.mount]
scoreboard players operation #k family.raid = #n family.raid
scoreboard players add #k family.raid 2
function family:undersea/raid/many/pirate/nsw
scoreboard players operation #k family.raid = #n family.raid
scoreboard players add #k family.raid 2
function family:undersea/raid/many/shambler/nsw
scoreboard players set #k family.raid 2
function family:undersea/raid/many/diver/nsw
scoreboard players set #k family.raid 1
execute if score #n family.raid matches 2.. run scoreboard players add #k family.raid 1
function family:undersea/raid/many/eye/e
function family:undersea/raid/whirl/e
function family:undersea/raid/whirl/n
function family:undersea/raid/whirl/s
function family:undersea/raid/whirl/w
execute store result score #left family.raid if entity @e[tag=family.raider,tag=!family.raid.mount]
execute store result bossbar family:raid_wave max run scoreboard players get #left family.raid
execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/wave2
execute in family:undersea run tellraw @a[distance=0..] [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": Here comes their crew! Watch out for the Spike Eyes' lasers!", "color": "white"}]
