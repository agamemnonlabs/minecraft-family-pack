execute if score #k family.raid matches ..0 run return 0
execute if score #alive family.raid >= #cap family.raid run return 0
scoreboard players remove #k family.raid 1
scoreboard players add #alive family.raid 1
function family:undersea/raid/s/rider/n
function family:undersea/raid/many/rider/n
