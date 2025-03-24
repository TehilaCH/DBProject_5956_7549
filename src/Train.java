public class Train implements Comparable, Movable{
    public static final int PASSENGER_LIMIT = 500;
    public static final int STATION_LIMIT = 5;
    int licenceNumber;
    Location source, destination;
    int numberOfStations;
    int currentStation;
    int maximalPassenger;
    public Train(int id, Location src, Location dst, int numOfStations, int maxPassengers) {
        licenceNumber = id;
        source = src;
        destination = dst;
        numberOfStations = numOfStations;
        currentStation = 0;
        maximalPassenger = maxPassengers;
    }

    @Override
    public String toString() {
        return String.format("licence = %d, source = %s, destination = %s, station = %d, maxPassengers = %d",
                licenceNumber, source, destination, currentStation, maximalPassenger);
    }

    @Override
    public String getType() {
        // TODO: Implement.
        return "Train";
    }

    @Override
    public int getId() {
        return licenceNumber;
    }

    @Override
    public Location getSource() {
        return source;
    }

    @Override
    public Location getDestination() {
        return destination;
    }

    @Override
    public String getCurrentLocation() {
        // TODO: Implement.
        if (currentStation == 0) {
            return source.toString();
        } else if (currentStation == numberOfStations) {
            return destination.toString();
        } else {
            return "station " + currentStation + " between " + source + " and " + destination;
        }
    }

    @Override
    public void move() {
        // TODO: implement;
        if (currentStation < numberOfStations) {
            currentStation++;
        } else {
            // Swap source and destination
            Location temp = source;
            source = destination;
            destination = temp;
            currentStation = 0;
        }

    }

    @Override
    public int compareTo(Object o) {
        // TODO: implement;
        return Integer.compare(this.maximalPassenger, ((Train)o).maximalPassenger);
    }
}

