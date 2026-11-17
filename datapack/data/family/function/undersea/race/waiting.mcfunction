execute if score @s family.race_t matches 1200.. run return run function family:undersea/race/no_start
title @s actionbar {"text":"GO! Swim through the START gate!","color":"yellow"}
execute if score #spark family.race_tmp matches 0 run function family:undersea/race/spark
