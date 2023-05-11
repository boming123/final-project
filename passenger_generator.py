import random

with open('passenger.txt', 'w') as f:
    for i in range(1, 101):
        current_floor = random.randint(1, 6)
        destination_floor = random.randint(1, 6)
        # Ensure the destination floor is different from the current floor
        while destination_floor == current_floor:
            destination_floor = random.randint(1, 6)
        f.write(f"Passenger{i} {current_floor} {destination_floor}\n")
