execute if score #k family.raid matches ..0 run return 0
execute if score #alive family.raid >= #cap family.raid run return 0
scoreboard players remove #k family.raid 1
scoreboard players add #alive family.raid 1
scoreboard players operation #m family.raid = #k family.raid
scoreboard players operation #m family.raid %= #2 family.raid
execute if score #m family.raid matches 0 run function family:undersea/raid/s/pirate/w
execute if score #m family.raid matches 1 run function family:undersea/raid/s/pirate/e
function family:undersea/raid/many/pirate/we
