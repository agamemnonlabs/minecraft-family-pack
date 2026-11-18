execute if score #on family.raid matches 1 run return fail
scoreboard players set #warn family.raid 30
function family:undersea/raid/begin
execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/surprise
execute in family:undersea run tellraw @a[distance=0..] [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": Sea raiders spotted! They attack in 30 seconds. Everyone, get ready!", "color": "white"}]
