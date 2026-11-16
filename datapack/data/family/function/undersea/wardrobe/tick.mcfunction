scoreboard players set @a family.pad 0
execute in family:undersea run scoreboard players set @a[x=-163,y=39,z=-152,dx=0,dy=1,dz=0] family.pad 1
execute in family:undersea run scoreboard players set @a[x=-160,y=39,z=-149,dx=0,dy=1,dz=0] family.pad 2
execute in family:undersea run scoreboard players set @a[x=-160,y=39,z=-139,dx=0,dy=1,dz=0] family.pad 3
execute in family:undersea run scoreboard players set @a[x=-163,y=39,z=-136,dx=0,dy=1,dz=0] family.pad 4
execute in family:undersea run scoreboard players set @a[x=-173,y=39,z=-136,dx=0,dy=1,dz=0] family.pad 5
execute in family:undersea run scoreboard players set @a[x=-176,y=39,z=-139,dx=0,dy=1,dz=0] family.pad 6
execute in family:undersea run scoreboard players set @a[x=-176,y=39,z=-149,dx=0,dy=1,dz=0] family.pad 7
execute in family:undersea run scoreboard players set @a[x=-173,y=39,z=-152,dx=0,dy=1,dz=0] family.pad 8
execute as @a unless score @s family.pad = @s family.lastpad run function family:undersea/wardrobe/step
