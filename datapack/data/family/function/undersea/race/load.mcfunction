scoreboard objectives add family.race dummy {"text":"Current Race","color":"aqua","bold":true}
scoreboard objectives add family.race_cp dummy
scoreboard objectives add family.race_t dummy
scoreboard objectives add family.race_cd dummy
scoreboard objectives add family.race_tmp dummy
scoreboard objectives add family.race_left minecraft.custom:minecraft.leave_game
scoreboard players set #2 family.race_tmp 2
scoreboard players set #10 family.race_tmp 10
scoreboard players set #base family.race_tmp 3000
team add family.undersea {"text":"Undersea"}
team modify family.undersea color aqua
scoreboard objectives setdisplay sidebar.team.aqua family.race
