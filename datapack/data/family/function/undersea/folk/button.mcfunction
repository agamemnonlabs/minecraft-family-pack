execute if score @s family.talk matches 1 run function family:undersea/folk/mayor_go
execute if score @s family.talk matches 2 run function family:undersea/folk/mayor_hints
execute if score @s family.talk matches 3 run function family:undersea/folk/pearl_reward
execute if score @s family.talk matches 4 run function family:undersea/folk/lunch_take
scoreboard players set @s family.talk 0
