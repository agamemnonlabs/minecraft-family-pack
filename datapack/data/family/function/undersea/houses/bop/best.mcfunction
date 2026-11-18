scoreboard players operation @s family.bop_best = @s family.bops
tellraw @s [{"text": "Coach Cockle", "color": "red"}, {"text": ": That's your best yet, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "!", "color": "white"}]
function family:undersea/houses/bop/leaderboard/add
