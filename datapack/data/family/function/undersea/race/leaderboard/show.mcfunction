data modify storage family:race view set value {l0:"-",l1:"-",l2:"-",l3:"-",l4:"-"}
data modify storage family:race row set from storage family:race board[0]
data modify storage family:race row.k set value 0
execute if data storage family:race board[0] run function family:undersea/race/leaderboard/line with storage family:race row
data modify storage family:race row set from storage family:race board[1]
data modify storage family:race row.k set value 1
execute if data storage family:race board[1] run function family:undersea/race/leaderboard/line with storage family:race row
data modify storage family:race row set from storage family:race board[2]
data modify storage family:race row.k set value 2
execute if data storage family:race board[2] run function family:undersea/race/leaderboard/line with storage family:race row
data modify storage family:race row set from storage family:race board[3]
data modify storage family:race row.k set value 3
execute if data storage family:race board[3] run function family:undersea/race/leaderboard/line with storage family:race row
data modify storage family:race row set from storage family:race board[4]
data modify storage family:race row.k set value 4
execute if data storage family:race board[4] run function family:undersea/race/leaderboard/line with storage family:race row
function family:undersea/race/leaderboard/render with storage family:race view
