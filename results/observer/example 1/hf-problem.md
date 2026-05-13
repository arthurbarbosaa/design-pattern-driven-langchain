Improve this code:

```java
class WeatherData {
    float temperature;
    float humidity;
    float pressure;

    void measurementsChanged() {
        currentDisplay.update(temperature, humidity, pressure);
        statsDisplay.update(temperature, humidity, pressure);
        forecastDisplay.update(temperature, humidity, pressure);
}
}
```
