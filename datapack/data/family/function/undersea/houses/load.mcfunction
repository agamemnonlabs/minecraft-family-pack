scoreboard objectives add family.house dummy
scoreboard objectives add family.bops dummy
scoreboard objectives add family.bop_best dummy
scoreboard objectives add family.bop_day dummy
scoreboard objectives add family.riddle_day dummy
scoreboard objectives add family.joke dummy
scoreboard objectives add family.fact dummy
scoreboard players set #day_ticks family.house 24000
scoreboard players set #20 family.house 20
scoreboard players set #riddles family.house 15
scoreboard players set #jokes family.house 24
scoreboard players set #facts family.house 24
schedule function family:undersea/houses/loop 1s replace
