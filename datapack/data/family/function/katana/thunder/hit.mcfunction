advancement revoke @s only family:katana_hit_thunder
execute if entity @s[tag=family.caster] run return 0
function family:katana/thunder/swing
execute rotated ~ 0 anchored eyes positioned ^ ^-0.4 ^2 run function family:katana/thunder/burst
