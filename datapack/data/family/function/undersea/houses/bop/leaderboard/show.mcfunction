data modify storage family:houses view set value {l0:"-",l1:"-",l2:"-",l3:"-",l4:"-"}
data modify storage family:houses row set from storage family:houses board[0]
data modify storage family:houses row.k set value 0
execute if data storage family:houses board[0] run function family:undersea/houses/bop/leaderboard/line with storage family:houses row
data modify storage family:houses row set from storage family:houses board[1]
data modify storage family:houses row.k set value 1
execute if data storage family:houses board[1] run function family:undersea/houses/bop/leaderboard/line with storage family:houses row
data modify storage family:houses row set from storage family:houses board[2]
data modify storage family:houses row.k set value 2
execute if data storage family:houses board[2] run function family:undersea/houses/bop/leaderboard/line with storage family:houses row
data modify storage family:houses row set from storage family:houses board[3]
data modify storage family:houses row.k set value 3
execute if data storage family:houses board[3] run function family:undersea/houses/bop/leaderboard/line with storage family:houses row
data modify storage family:houses row set from storage family:houses board[4]
data modify storage family:houses row.k set value 4
execute if data storage family:houses board[4] run function family:undersea/houses/bop/leaderboard/line with storage family:houses row
function family:undersea/houses/bop/leaderboard/render with storage family:houses view
