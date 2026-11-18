execute as @a[scores={family.raid_bell=1..}] run function family:undersea/raid/bell_go
execute if score #on family.raid matches 1 in family:undersea as @a[distance=0..,scores={family.raid_hp=1..6},gamemode=!creative,gamemode=!spectator] at @s run function family:undersea/raid/rescue
