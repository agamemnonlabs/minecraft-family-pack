effect give @s minecraft:instant_health 1 1 true
effect give @s minecraft:resistance 5 4 true
particle minecraft:bubble ~ ~1 ~ 0.4 0.8 0.4 0.1 40
execute in family:undersea run tp @s -167.5 39 -139.5
title @s times 5 40 10
title @s subtitle {"text": "Catch your breath, then jump back in!", "color": "yellow"}
title @s title {"text": "Bubble rescue!", "color": "aqua", "bold": true}
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.5
