advancement revoke @s only family:folk/tap_coach
execute if items entity @s container.* minecraft:bowl[minecraft:custom_data~{family_to:"coach"}] run return run function family:undersea/folk/deliver/coach
execute if items entity @s weapon.offhand minecraft:bowl[minecraft:custom_data~{family_to:"coach"}] run return run function family:undersea/folk/deliver/coach
function family:undersea/houses/bop/menu
