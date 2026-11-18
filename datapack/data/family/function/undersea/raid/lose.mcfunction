execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/lose
execute in family:undersea run tellraw @a[distance=0..] [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": Oh no! The raiders swam off with the cafe's cookies! Don't worry, the chef will bake more. The alarm bell can ring again in 15 minutes.", "color": "white"}]
function family:undersea/raid/finish
