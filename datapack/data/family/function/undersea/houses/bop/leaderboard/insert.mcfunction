$execute unless data storage family:houses board[$(i)] run return run data modify storage family:houses board append from storage family:houses new
$execute store result score #bp family.house run data get storage family:houses board[$(i)].p
$execute if score #np family.house > #bp family.house run return run data modify storage family:houses board insert $(i) from storage family:houses new
$scoreboard players set #i family.house $(i)
scoreboard players add #i family.house 1
execute store result storage family:houses at.i int 1 run scoreboard players get #i family.house
function family:undersea/houses/bop/leaderboard/insert with storage family:houses at
