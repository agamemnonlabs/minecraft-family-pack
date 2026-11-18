execute if score #on family.raid matches 1 run return fail
scoreboard players set #warn family.raid 10
function family:undersea/raid/begin
execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/alarm
execute in family:undersea run tellraw @a[distance=0..] [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": " rang the alarm bell! Sea raiders are coming! Everyone, defend the town!", "color": "white"}]
