advancement revoke @s only family:bubble_shell
tag @s add family.shell_back
schedule function family:undersea/shell_back 1t append
execute if dimension minecraft:overworld run return run function family:undersea/go_down
execute if dimension family:undersea run return run function family:undersea/go_up
tellraw @s {"text": "The Bubble Shell only works in the Overworld and the Undersea.", "color": "yellow"}
