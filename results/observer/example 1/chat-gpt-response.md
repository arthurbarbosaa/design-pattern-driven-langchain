A good improvement is to remove the tight coupling between `WeatherData` and the display classes by applying the **Observer pattern**. Right now, `WeatherData` directly knows about every display and must be modified whenever a new display is added.

Here’s a cleaner and more extensible version:

```java
import java.util.ArrayList;
import java.util.List;

interface Observer {
    void update(float temperature, float humidity, float pressure);
}

interface Subject {
    void registerObserver(Observer observer);
    void removeObserver(Observer observer);
    void notifyObservers();
}

class WeatherData implements Subject {

    private final List<Observer> observers = new ArrayList<>();

    private float temperature;
    private float humidity;
    private float pressure;

    @Override
    public void registerObserver(Observer observer) {
        observers.add(observer);
    }

    @Override
    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }

    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(temperature, humidity, pressure);
        }
    }

    public void setMeasurements(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;

        measurementsChanged();
    }

    private void measurementsChanged() {
        notifyObservers();
    }
}
```

Example observer implementation:

```java
class CurrentDisplay implements Observer {

    @Override
    public void update(float temperature, float humidity, float pressure) {
        System.out.println("Current conditions: " + temperature + "°C");
    }
}
```

Usage:

```java
WeatherData weatherData = new WeatherData();

CurrentDisplay currentDisplay = new CurrentDisplay();

weatherData.registerObserver(currentDisplay);

weatherData.setMeasurements(25.5f, 65f, 1013f);
```

Key improvements:

- Loose coupling between data source and displays
- Easy to add/remove displays without changing `WeatherData`
- Better encapsulation (`private` fields)
- Single responsibility and open/closed principle compliance
- More testable and maintainable code
