advancement revoke @s only family:folk/tap_farmer
execute if items entity @s container.* minecraft:bowl[minecraft:custom_data~{family_to:"farmer"}] run return run function family:undersea/folk/deliver/farmer
execute if items entity @s weapon.offhand minecraft:bowl[minecraft:custom_data~{family_to:"farmer"}] run return run function family:undersea/folk/deliver/farmer
