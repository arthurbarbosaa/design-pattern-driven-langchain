```java
interface Subject {
    void registerObserver(Observer o);
    void removeObserver(Observer o);
    void notifyObservers();
}

interface Observer {
    void update(float temp, float humidity, float pressure);
}

class WeatherData implements Subject {
    private List<Observer> observers = new ArrayList<>();

    public void registerObserver(Observer o) {
        observers.add(o);
    }

    public void removeObserver(Observer o) {
        observers.remove(o);
    }

    public void notifyObservers() {
        for (Observer o : observers) {
            o.update(temperature, humidity, pressure);
        }
    }

    void measurementsChanged() {
        notifyObservers();
    }
}

class CurrentConditionsDisplay implements Observer {
    public void update(float temp, float humidity, float pressure) {
        System.out.println("Temp: " + temp + " Humidity: " + humidity);
    }
}

WeatherData weatherData = new WeatherData();

CurrentConditionsDisplay display = new CurrentConditionsDisplay();

weatherData.registerObserver(display);

weatherData.measurementsChanged();
```
