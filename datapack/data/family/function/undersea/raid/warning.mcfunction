scoreboard players remove #t family.raid 1
execute store result bossbar family:raid_wave value run scoreboard players get #t family.raid
bossbar set family:raid_wave name [{"text": "ENEMY ATTACK in ", "color": "red"}, {"score": {"name": "#t", "objective": "family.raid"}}, {"text": " s"}]
function family:undersea/raid/whirl/n
function family:undersea/raid/whirl/e
function family:undersea/raid/whirl/s
function family:undersea/raid/whirl/w
execute if score #t family.raid matches 20 run execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/horn
execute if score #t family.raid matches 5 run execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/horn
execute if score #t family.raid matches 1..3 run execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/count
execute if score #t family.raid matches ..0 run function family:undersea/raid/wave/1
