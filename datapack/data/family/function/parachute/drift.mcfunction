execute if predicate family:parachute/should_close run return run function family:parachute/close
execute unless predicate family:parachute/drifting run effect give @s minecraft:slow_falling 2 0 true
execute if predicate family:parachute/too_fast run tag @s add family.chute_brake
execute if predicate family:parachute/gentle run tag @s remove family.chute_brake
execute if entity @s[tag=family.chute_brake] unless predicate family:parachute/braking run effect give @s minecraft:levitation 1 0 true
execute if entity @s[tag=!family.chute_brake] if predicate family:parachute/braking run effect clear @s minecraft:levitation
