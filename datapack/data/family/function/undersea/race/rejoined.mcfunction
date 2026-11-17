scoreboard players reset @s family.race_left
execute unless entity @s[tag=family.racing] run return 0
function family:undersea/race/end
tellraw @s [{"text": "Driver Finnley", "color": "aqua"}, {"text": ": ", "color": "white"}, {"text": "Your race stopped when you left the game. Tap me to race again!", "color": "white"}]
