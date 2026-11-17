tag @s add family.met.driver
tellraw @s [{"text": "Driver Finnley", "color": "aqua"}, {"text": ": Beep beep, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! The bus is late again. Tap me!", "color": "white"}]
playsound minecraft:entity.villager.ambient neutral @s ~ ~ ~
