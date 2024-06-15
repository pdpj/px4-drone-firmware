class GPSCoordinateLibrary:
    def __init__(self):
        self.coordinates = {
            "a1": (39.819052, -7.515000),
            "a2": (39.819052, -7.514500),
            "a3": (39.819052, -7.514000),
            "a4": (39.819052, -7.513500),
            "a5": (39.819052, -7.513000),
            "a6": (39.819052, -7.512500),
            "a7": (39.819052, -7.512000),
            "a8": (39.819052, -7.511500),
            "a9": (39.819052, -7.511000),
            "a10": (39.819052, -7.510500),
            "b1": (39.818552, -7.515000),
            "b2": (39.818552, -7.514500),
            "b3": (39.818552, -7.514000),
            "b4": (39.818552, -7.513500),
            "b5": (39.818552, -7.513000),
            "b6": (39.818552, -7.512500),
            "b7": (39.818552, -7.512000),
            "b8": (39.818552, -7.511500),
            "b9": (39.818552, -7.511000),
            "b10": (39.818552, -7.510500),
        }

    def get_coordinate(self, point):
        return self.coordinates.get(point, "Invalid point")

# Example usage
if __name__ == "__main__":
    gps_library = GPSCoordinateLibrary()
    point = "a1"
    coordinate = gps_library.get_coordinate(point)
    print(f"The coordinates for {point} are: {coordinate}")
    
    point = "b5"
    coordinate = gps_library.get_coordinate(point)
    print(f"The coordinates for {point} are: {coordinate}")
    
    point = "c1"
    coordinate = gps_library.get_coordinate(point)
    print(f"The coordinates for {point} are: {coordinate}")

