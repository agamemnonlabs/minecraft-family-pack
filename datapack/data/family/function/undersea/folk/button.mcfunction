execute if score @s family.talk matches 1 run function family:undersea/folk/mayor_go
execute if score @s family.talk matches 2 run function family:undersea/folk/mayor_hints
execute if score @s family.talk matches 3 run function family:undersea/folk/pearl_reward
execute if score @s family.talk matches 4 run function family:undersea/folk/lunch_take
execute if score @s family.talk matches 5 run function family:undersea/race/go
execute if score @s family.talk matches 6 run function family:undersea/race/rules
execute if score @s family.talk matches 7 run function family:undersea/race/stop
scoreboard players set @s family.talk 0
