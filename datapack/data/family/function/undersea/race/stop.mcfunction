execute unless entity @s[tag=family.racing] run return fail
function family:undersea/race/end
tellraw @s [{"text": "Driver Finnley", "color": "aqua"}, {"text": ": OK, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! Tap me any time to race again.", "color": "white"}]
