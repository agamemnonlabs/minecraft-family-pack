execute unless score @s family.bop_best matches 0.. run return fail
data remove storage family:houses new
item replace entity @e[type=minecraft:item_display,tag=family.house.namer,limit=1] contents with minecraft:player_head
item modify entity @e[type=minecraft:item_display,tag=family.house.namer,limit=1] contents {type:"minecraft:fill_player_head",entity:"this"}
data modify storage family:houses new.n set from entity @e[type=minecraft:item_display,tag=family.house.namer,limit=1] item.components."minecraft:profile".name
execute unless data storage family:houses new.n run data modify storage family:houses new.n set value "?"
data modify storage family:houses new.u set from entity @s UUID
execute store result storage family:houses new.p int 1 run scoreboard players get @s family.bop_best
function family:undersea/houses/bop/leaderboard/drop with storage family:houses new
scoreboard players operation #np family.house = @s family.bop_best
data modify storage family:houses at.i set value 0
function family:undersea/houses/bop/leaderboard/insert with storage family:houses at
data remove storage family:houses board[10]
function family:undersea/houses/bop/leaderboard/show
