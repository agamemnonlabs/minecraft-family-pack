advancement revoke @s only family:folk/tap_professor
execute if items entity @s container.* minecraft:bowl[minecraft:custom_data~{family_to:"professor"}] run return run function family:undersea/folk/deliver/professor
execute if items entity @s weapon.offhand minecraft:bowl[minecraft:custom_data~{family_to:"professor"}] run return run function family:undersea/folk/deliver/professor
function family:undersea/houses/prof/menu
