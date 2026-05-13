```java
interface ShippingStrategy {
    double calculate(double weight);
}

class SedexShipping implements ShippingStrategy {
    public double calculate(double weight) {
        return weight * 2.0 + 10;
    }
}

class PacShipping implements ShippingStrategy {
    public double calculate(double weight) {
        return weight * 1.2 + 5;
    }
}

class PickupShipping implements ShippingStrategy {
    public double calculate(double weight) {
        return 0;
    }
}

class ShippingService {

    private ShippingStrategy strategy;

    public void setStrategy(ShippingStrategy strategy) {
        this.strategy = strategy;
    }

    public double calculate(double weight) {
        return strategy.calculate(weight);
    }
}

public class Main {
    public static void main(String[] args) {

        ShippingService service = new ShippingService();

        service.setStrategy(new SedexShipping());
        System.out.println(service.calculate(10));

        service.setStrategy(new PacShipping());
        System.out.println(service.calculate(10));

        service.setStrategy(new PickupShipping());
        System.out.println(service.calculate(10));
    }
}
```
