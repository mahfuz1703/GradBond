# utils.py
def get_room_name(user1, user2):
    ids = sorted([user1.id, user2.id])
    return f"room_{ids[0]}_{ids[1]}"
