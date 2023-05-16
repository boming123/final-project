class Passenger:
    def __init__(self, name, current_floor, destination_floor):
        self.name = name
        self.current_floor = current_floor
        self.destination_floor = destination_floor

class Elevator:
    def __init__(self, id, capacity=5):
        self.id = id
        self.capacity = capacity
        self.passengers = []
        self.current_floor = 1
        self.floors_to_visit = [1]
        self.operations = []

    def can_add_passenger(self):
        return len(self.passengers) < self.capacity

    def add_passenger(self, passenger):
        if not self.can_add_passenger():
            raise Exception("Elevator is at capacity")

        self.passengers.append(passenger)
        self.operations.append(f'Elevator {self.id} take {passenger.name} at floor {passenger.current_floor}')

        if passenger.current_floor not in self.floors_to_visit:
            self.floors_to_visit.append(passenger.current_floor)
        if passenger.destination_floor not in self.floors_to_visit:
            self.floors_to_visit.append(passenger.destination_floor)

    def sort_floors(self):
        self.floors_to_visit.sort(key=lambda x: abs(x-self.current_floor))
        self.current_floor = self.floors_to_visit[0]

    def run(self):
        while self.floors_to_visit:
            current_floor = self.floors_to_visit.pop(0)
            self.operations.append(f'Elevator {self.id} arrives at floor {current_floor}')
            
            # Check if any passengers need to get off at this floor
            self.passengers = [p for p in self.passengers if p.destination_floor != current_floor]
            
            if self.floors_to_visit:
                self.sort_floors()

class Building:
    def __init__(self, elevators, passengers):
        self.elevators = elevators
        self.passengers = passengers

    def assign_passengers(self):
        while self.passengers:
            for elevator in self.elevators:
                if elevator.can_add_passenger():
                    passenger = self.passengers.pop(0)
                    elevator.add_passenger(passenger)
                    elevator.sort_floors()
                    break
            else:
                for elevator in self.elevators:
                    elevator.run()
                    
    def print_elevator_schedules(self):
        with open('elevator_log.txt', 'w') as f:
            for elevator in self.elevators:
                f.write("\n".join(elevator.operations))
                f.write("\n")


def read_passenger_file(file_name):
    passengers = []
    with open(file_name, 'r') as f:
        for line in f:
            name, current_floor, destination_floor = line.strip().split()
            passengers.append(Passenger(name, int(current_floor), int(destination_floor)))
    return passengers


def main():
    elevators = [Elevator(i+1) for i in range(4)]
    passengers = read_passenger_file('passenger.txt')
    building = Building(elevators, passengers)
    building.assign_passengers()
    building.print_elevator_schedules()


if __name__ == "__main__":
    main()
