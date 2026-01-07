new_direction = "North"
directions = ["North", "East", "South", "West"]
def left_turn():
    global new_direction
    new_direction = directions[(directions.index(new_direction)+3)%4]
    print(new_direction)
left_turn()
left_turn()
left_turn()
left_turn()
left_turn()
left_turn()
left_turn()
left_turn()