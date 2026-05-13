### What’s wrong with the original code?

| Problem                                                                                                                        | Why it matters                                                              | Example from the code                                                  |
| ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Tight coupling** – `WeatherData` knows three concrete display objects (`currentDisplay`, `statsDisplay`, `forecastDisplay`). | Adding, removing or changing a display forces you to edit `WeatherData`.    | `currentDisplay.update(...)`                                           |
| **Open‑Closed Principle violation** – every new display means a new line (or a new field) in `WeatherData`.                    | The class cannot be extended without modification.                          | Adding a `historicalDisplay` → edit `measurementsChanged()`.           |
| **Single‑Responsibility Principle violation** – `WeatherData` stores data **and** pushes updates.                              | The class does two unrelated things, making it harder to test and maintain. | The `measurementsChanged()` method mixes notification logic with data. |

The classic solution for this kind of “many‑to‑many” notification problem is the **Observer pattern** (also called Publish‑Subscribe). The subject (here, `WeatherData`) maintains a list of observers and notifies them when its state changes. Observers implement a common interface, so the subject never needs to know the concrete classes.

---

## Refactored design – Observer pattern

```java
/* ==================== 1. Observer interface ==================== */
public interface WeatherObserver {
    /**
     * Called by WeatherData whenever new measurements are available.
     */
    void update(float temperature, float humidity, float pressure);
}

/* ==================== 2. Subject (Observable) ==================== */
public interface WeatherSubject {
    void registerObserver(WeatherObserver o);
    void removeObserver(WeatherObserver o);
    void notifyObservers();
}

/* ==================== 3. Concrete subject ==================== */
import java.util.ArrayList;
import java.util.List;

public class WeatherData implements WeatherSubject {

    private final List<WeatherObserver> observers = new ArrayList<>();

    private float temperature;
    private float humidity;
    private float pressure;

    /* ---- Subject API ------------------------------------------------- */
    @Override
    public void registerObserver(WeatherObserver o) {
        observers.add(o);
    }

    @Override
    public void removeObserver(WeatherObserver o) {
        observers.remove(o);
    }

    @Override
    public void notifyObservers() {
        for (WeatherObserver o : observers) {
            o.update(temperature, humidity, pressure);
        }
    }

    /* ---- Business logic ------------------------------------------------- */
    public void setMeasurements(float temperature,
                                float humidity,
                                float pressure) {
        this.temperature = temperature;
        this.humidity    = humidity;
        this.pressure   = pressure;
        measurementsChanged();               // internal hook
    }

    /** Called after the measurements have been updated. */
    private void measurementsChanged() {
        notifyObservers();                  // ← now decoupled
    }
}
```

### Concrete observers (displays)

Each display implements `WeatherObserver`.  
They can be added/removed at runtime without touching `WeatherData`.

```java
/* -------------------- Current conditions display -------------------- */
public class CurrentConditionsDisplay implements WeatherObserver {

    @Override
    public void update(float temperature,
                       float humidity,
                       float pressure) {
        System.out.printf("Current conditions: %.1f°F, %.1f%% humidity, %.1f mb%n",
                          temperature, humidity, pressure);
    }
}

/* -------------------- Statistics display -------------------- */
public class StatisticsDisplay implements WeatherObserver {

    private float maxTemp = Float.MIN_VALUE;
    private float minTemp = Float.MAX_VALUE;
    private float sumTemp = 0f;
    private int   count   = 0;

    @Override
    public void update(float temperature,
                       float humidity,
                       float pressure) {
        count++;
        sumTemp += temperature;
        maxTemp = Math.max(maxTemp, temperature);
        minTemp = Math.min(minTemp, temperature);
        System.out.printf("Avg/Max/Min temperature = %.1f/%.1f/%.1f%n",
                          sumTemp / count, maxTemp, minTemp);
    }
}

/* -------------------- Forecast display -------------------- */
public class ForecastDisplay implements WeatherObserver {

    private float lastPressure = 0f;

    @Override
    public void update(float temperature,
                       float humidity,
                       float pressure) {
        String forecast = (pressure > lastPressure) ? "Improving weather"
                       : (pressure == lastPressure) ? "More of the same"
                       : "Watch out for cooler, rainy weather";
        System.out.println("Forecast: " + forecast);
        lastPressure = pressure;
    }
}
```

### Wiring everything together

```java
public class WeatherStationDemo {
    public static void main(String[] args) {
        WeatherData weatherData = new WeatherData();

        // Create displays (observers)
        WeatherObserver current  = new CurrentConditionsDisplay();
        WeatherObserver stats    = new StatisticsDisplay();
        WeatherObserver forecast = new ForecastDisplay();

        // Register them with the subject
        weatherData.registerObserver(current);
        weatherData.registerObserver(stats);
        weatherData.registerObserver(forecast);

        // Simulate new measurements
        weatherData.setMeasurements(80f, 65f, 30.4f);
        weatherData.setMeasurements(82f, 70f, 29.2f);
        weatherData.setMeasurements(78f, 90f, 29.2f);
    }
}
```

Running the demo produces something like:

```
Current conditions: 80.0°F, 65.0% humidity, 30.4 mb
Avg/Max/Min temperature = 80.0/80.0/80.0
Forecast: Improving weather
Current conditions: 82.0°F, 70.0% humidity, 29.2 mb
Avg/Max/Min temperature = 81.0/82.0/80.0
Forecast: Watch out for cooler, rainy weather
Current conditions: 78.0°F, 90.0% humidity, 29.2 mb
Avg/Max/Min temperature = 80.0/82.0/78.0
Forecast: More of the same
```

---

## Why the Observer pattern is the right fit

| Aspect                    | Before (hard‑coded)                             | After (Observer)                                                    |
| ------------------------- | ----------------------------------------------- | ------------------------------------------------------------------- |
| **Coupling**              | `WeatherData` → concrete display classes        | `WeatherData` → `WeatherObserver` interface only                    |
| **Extensibility**         | Adding a new display = edit `WeatherData`       | New display just implements `WeatherObserver` & registers itself    |
| **Single Responsibility** | Stores data **and** notifies concrete UI        | `WeatherData` only stores & publishes; displays handle presentation |
| **Testability**           | Hard to mock displays; unit tests touch UI code | Easy to mock `WeatherObserver` and verify `notifyObservers()` calls |

---

## Quick checklist for further improvement (optional)

1. **Thread‑safety** – If measurements can be set from multiple threads, protect the observer list (`CopyOnWriteArrayList` or synchronize).
2. **Immutable data transfer** – Instead of three floats, you could pass a `WeatherMeasurements` value object to `update`.
3. **Unregister on dispose** – UI components should call `removeObserver` when they are no longer needed to avoid memory leaks.
4. **Use Java 8+ lambdas** – For very simple observers you can register a lambda instead of creating a full class.

---

### TL;DR

_Replace the direct calls to concrete display objects with a proper Observer implementation._  
`WeatherData` becomes the **Subject**, each display becomes an **Observer**, and the subject notifies all registered observers whenever its state changes. This eliminates tight coupling, respects the Open‑Closed and Single‑Responsibility principles, and makes the system easy to extend and maintain.
