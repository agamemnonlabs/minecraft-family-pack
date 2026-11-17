scoreboard objectives add family.talk trigger
scoreboard objectives add family.pearls dummy
scoreboard objectives add family.lunchday dummy
scoreboard objectives add family.folk dummy
scoreboard players set #day_ticks family.folk 24000
schedule function family:undersea/folk/loop 5t replace
