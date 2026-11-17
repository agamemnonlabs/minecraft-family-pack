execute unless score @s family.race matches 0.. run return fail
data remove storage family:race new
item replace entity @e[type=minecraft:item_display,tag=family.race.namer,limit=1] contents with minecraft:player_head
item modify entity @e[type=minecraft:item_display,tag=family.race.namer,limit=1] contents {type:"minecraft:fill_player_head",entity:"this"}
data modify storage family:race new.n set from entity @e[type=minecraft:item_display,tag=family.race.namer,limit=1] item.components."minecraft:profile".name
execute unless data storage family:race new.n run data modify storage family:race new.n set value "?"
data modify storage family:race new.u set from entity @s UUID
execute store result storage family:race new.p int 1 run scoreboard players get @s family.race
scoreboard players operation #b family.race_tmp = #base family.race_tmp
scoreboard players operation #b family.race_tmp -= @s family.race
scoreboard players operation #bs family.race_tmp = #b family.race_tmp
scoreboard players operation #bs family.race_tmp /= #10 family.race_tmp
scoreboard players operation #bd family.race_tmp = #b family.race_tmp
scoreboard players operation #bd family.race_tmp %= #10 family.race_tmp
execute store result storage family:race new.s int 1 run scoreboard players get #bs family.race_tmp
execute store result storage family:race new.d int 1 run scoreboard players get #bd family.race_tmp
function family:undersea/race/leaderboard/drop with storage family:race new
scoreboard players operation #np family.race_tmp = @s family.race
data modify storage family:race at.i set value 0
function family:undersea/race/leaderboard/insert with storage family:race at
data remove storage family:race board[10]
function family:undersea/race/leaderboard/show
