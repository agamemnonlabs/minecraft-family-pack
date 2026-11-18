advancement revoke @s only family:raid/tap_alarm
execute in family:undersea run playsound minecraft:block.bell.use block @a -167.5 41.5 -147.5 2 1
execute if score #on family.raid matches 1 run return run tellraw @s [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": The raid is on, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! Chase those raiders out of town!", "color": "white"}]
execute if score #cool family.raid matches 1.. run return run function family:undersea/raid/rest
scoreboard players enable @s family.raid_bell
dialog show @s {"type":"minecraft:multi_action","title":{"text":"Alarm Bell","color":"red"},"body":[{"type":"minecraft:plain_message","contents":{"text":"Ring the alarm? Sea raiders will attack the whole town! Everyone in town switches to Adventure (no flying) until the raid is over."}}],"columns":1,"actions":[{"label":"Ring it!","action":{"type":"minecraft:run_command","command":"/trigger family.raid_bell set 1"}}],"exit_action":{"label":"Not now"}}
