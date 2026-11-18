scoreboard objectives add family.raid dummy
scoreboard objectives add family.raid_bell trigger
scoreboard objectives add family.raid_hp health
team add family.raiders {"text":"Sea Raiders"}
scoreboard players set #2 family.raid 2
scoreboard players set #3 family.raid 3
scoreboard players set #60 family.raid 60
scoreboard players set #cap family.raid 24
execute unless score #on family.raid matches 0..1 run scoreboard players set #on family.raid 0
execute unless score #surprise family.raid matches 0..1 run scoreboard players set #surprise family.raid 1
execute unless score #since family.raid matches 0.. run scoreboard players set #since family.raid 3600
schedule function family:undersea/raid/loop 1s replace
execute if score #on family.raid matches 1 if score #wave family.raid matches 0 run schedule function family:undersea/raid/blink 10t replace
