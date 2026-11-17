advancement revoke @s only family:folk/tap_driver
execute if items entity @s container.* minecraft:bowl[minecraft:custom_data~{family_to:"driver"}] run return run function family:undersea/folk/deliver/driver
execute if items entity @s weapon.offhand minecraft:bowl[minecraft:custom_data~{family_to:"driver"}] run return run function family:undersea/folk/deliver/driver
function family:undersea/race/menu
