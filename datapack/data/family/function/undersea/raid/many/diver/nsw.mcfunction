execute if score #k family.raid matches ..0 run return 0
execute if score #alive family.raid >= #cap family.raid run return 0
scoreboard players remove #k family.raid 1
scoreboard players add #alive family.raid 1
scoreboard players operation #m family.raid = #k family.raid
scoreboard players operation #m family.raid %= #3 family.raid
execute if score #m family.raid matches 0 run function family:undersea/raid/s/diver/n
execute if score #m family.raid matches 1 run function family:undersea/raid/s/diver/s
execute if score #m family.raid matches 2 run function family:undersea/raid/s/diver/w
function family:undersea/raid/many/diver/nsw
