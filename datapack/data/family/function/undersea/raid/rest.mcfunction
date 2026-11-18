scoreboard players operation #min family.raid = #cool family.raid
scoreboard players add #min family.raid 59
scoreboard players operation #min family.raid /= #60 family.raid
tellraw @s [{"text": "The alarm bell needs a rest. Ring it again in ", "color": "yellow"}, {"score": {"name": "#min", "objective": "family.raid"}}, {"text": " min."}]
