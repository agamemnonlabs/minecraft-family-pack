$execute unless data storage family:race board[$(i)] run return run data modify storage family:race board append from storage family:race new
$execute store result score #bp family.race_tmp run data get storage family:race board[$(i)].p
$execute if score #np family.race_tmp > #bp family.race_tmp run return run data modify storage family:race board insert $(i) from storage family:race new
$scoreboard players set #i family.race_tmp $(i)
scoreboard players add #i family.race_tmp 1
execute store result storage family:race at.i int 1 run scoreboard players get #i family.race_tmp
function family:undersea/race/leaderboard/insert with storage family:race at
