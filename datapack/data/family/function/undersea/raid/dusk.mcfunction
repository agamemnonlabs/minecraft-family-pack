scoreboard players set #dusk family.raid 1
execute unless score #surprise family.raid matches 1 run return 0
execute unless score #since family.raid matches 3600.. run return 0
execute unless score #town family.raid matches 600.. run return 0
execute store result score #r family.raid run random value 0..1
execute if score #r family.raid matches 1 run function family:undersea/raid/begin_surprise
