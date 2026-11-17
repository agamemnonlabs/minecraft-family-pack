advancement revoke @s only family:folk/tap_driver
execute if items entity @s container.* minecraft:bowl[minecraft:custom_data~{family_to:"driver"}] run return run function family:undersea/folk/deliver/driver
execute if items entity @s weapon.offhand minecraft:bowl[minecraft:custom_data~{family_to:"driver"}] run return run function family:undersea/folk/deliver/driver
dialog show @s {"type":"minecraft:notice","title":{"text":"Driver Finnley","color":"aqua"},"body":[{"type":"minecraft:plain_message","contents":{"text":"Beep beep! I'm building a race track around town: the Current Race. Come back soon and race your friends!"}}],"action":{"label":"OK!"}}
