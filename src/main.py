from controllers.flight_controller import FlightController

def main():
    flight_controller = FlightController()
    flight_controller.initialize()
    flight_controller.start_mission()

if __name__ == "__main__":
    main()

