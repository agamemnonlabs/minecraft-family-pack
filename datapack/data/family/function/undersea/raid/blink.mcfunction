execute unless score #on family.raid matches 1 run return 0
execute unless score #wave family.raid matches 0 run return 0
schedule function family:undersea/raid/blink 10t replace
scoreboard players add #blink family.raid 1
execute if score #blink family.raid matches 2.. run scoreboard players set #blink family.raid 0
execute if score #blink family.raid matches 0 run function family:undersea/raid/lamps_red
execute if score #blink family.raid matches 1 run function family:undersea/raid/lamps_white
