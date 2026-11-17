execute unless dimension family:undersea run return run function family:undersea/race/away
execute if score @s family.race_cd matches 1.. run return run function family:undersea/race/countdown
scoreboard players add @s family.race_t 1
execute if score @s family.race_cp matches 0 run return run function family:undersea/race/waiting
execute if score @s family.race_t matches 6000.. run return run function family:undersea/race/timeout
scoreboard players operation #t family.race_tmp = @s family.race_t
scoreboard players operation #t family.race_tmp /= #2 family.race_tmp
scoreboard players operation #s family.race_tmp = #t family.race_tmp
scoreboard players operation #s family.race_tmp /= #10 family.race_tmp
scoreboard players operation #d family.race_tmp = #t family.race_tmp
scoreboard players operation #d family.race_tmp %= #10 family.race_tmp
execute if score @s family.race_cp matches ..11 run title @s actionbar [{"text": "Hoop ", "color": "aqua"}, {"score": {"name": "@s", "objective": "family.race_cp"}}, {"text": " of 11   |   "}, {"score": {"name": "#s", "objective": "family.race_tmp"}}, {"text": "."}, {"score": {"name": "#d", "objective": "family.race_tmp"}}, {"text": "s"}]
execute if score @s family.race_cp matches 12 run title @s actionbar [{"text": "Back through the gate!   |   ", "color": "gold"}, {"score": {"name": "#s", "objective": "family.race_tmp"}}, {"text": "."}, {"score": {"name": "#d", "objective": "family.race_tmp"}}, {"text": "s"}]
execute if score #spark family.race_tmp matches 0 run function family:undersea/race/spark
