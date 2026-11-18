execute unless score #on family.raid matches 1 run return fail
execute in family:undersea run tellraw @a[distance=0..] [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": The raid is called off. Thanks for helping, everyone!", "color": "white"}]
function family:undersea/raid/finish
