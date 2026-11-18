scoreboard players set #wave family.raid 1
scoreboard players set #t family.raid 0
scoreboard players set #elapsed family.raid 0
function family:undersea/raid/lamps_red
data modify entity @e[type=minecraft:text_display,tag=family.raid.banner,limit=1] text set value {"text": "DEFEND THE TOWN!", "color": "gold", "bold": true}
execute store result score #n family.raid if entity @a[tag=family.raid.in]
execute if score #n family.raid matches ..0 run scoreboard players set #n family.raid 1
execute store result score #alive family.raid if entity @e[tag=family.raider,tag=!family.raid.mount]
scoreboard players operation #k family.raid = #n family.raid
scoreboard players operation #k family.raid += #n family.raid
scoreboard players add #k family.raid 4
function family:undersea/raid/many/pirate/we
function family:undersea/raid/whirl/e
function family:undersea/raid/whirl/w
execute store result score #left family.raid if entity @e[tag=family.raider,tag=!family.raid.mount]
execute store result bossbar family:raid_wave max run scoreboard players get #left family.raid
execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/wave1
