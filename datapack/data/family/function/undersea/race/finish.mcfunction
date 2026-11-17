scoreboard players operation #t family.race_tmp = @s family.race_t
scoreboard players operation #t family.race_tmp /= #2 family.race_tmp
scoreboard players operation #s family.race_tmp = #t family.race_tmp
scoreboard players operation #s family.race_tmp /= #10 family.race_tmp
scoreboard players operation #d family.race_tmp = #t family.race_tmp
scoreboard players operation #d family.race_tmp %= #10 family.race_tmp
scoreboard players operation #pts family.race_tmp = #base family.race_tmp
scoreboard players operation #pts family.race_tmp -= #t family.race_tmp
function family:undersea/race/end
title @s times 5 60 20
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
particle minecraft:totem_of_undying ~ ~1 ~ 0.6 0.6 0.6 0.4 50
execute unless score @s family.race >= #pts family.race_tmp run return run function family:undersea/race/new_best
title @s subtitle [{"score": {"name": "#s", "objective": "family.race_tmp"}}, {"text": "."}, {"score": {"name": "#d", "objective": "family.race_tmp"}}, {"text": " seconds", "color": "white"}]
title @s title {"text":"FINISH!","color":"gold","bold":true}
scoreboard players operation #b family.race_tmp = #base family.race_tmp
scoreboard players operation #b family.race_tmp -= @s family.race
scoreboard players operation #bs family.race_tmp = #b family.race_tmp
scoreboard players operation #bs family.race_tmp /= #10 family.race_tmp
scoreboard players operation #bd family.race_tmp = #b family.race_tmp
scoreboard players operation #bd family.race_tmp %= #10 family.race_tmp
tellraw @s [{"text": "Driver Finnley", "color": "aqua"}, {"text": ": ", "color": "white"}, {"text": "Nice swim, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! ", "color": "white"}, {"score": {"name": "#s", "objective": "family.race_tmp"}}, {"text": "."}, {"score": {"name": "#d", "objective": "family.race_tmp"}}, {"text": " seconds. Your best is ", "color": "white"}, {"score": {"name": "#bs", "objective": "family.race_tmp"}}, {"text": "."}, {"score": {"name": "#bd", "objective": "family.race_tmp"}}, {"text": " seconds. Try again?", "color": "white"}]
function family:undersea/race/leaderboard/add
