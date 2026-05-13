Improve this code:

```java
class ShippingCalculator {

    public double calculate(String type, double weight) {

        if (type.equals("SEDEX")) {
            return weight * 2.0 + 10;
        } else if (type.equals("PAC")) {
            return weight * 1.2 + 5;
        } else if (type.equals("PICKUP")) {
            return 0;
        } else {
            throw new IllegalArgumentException("Invalid type");
        }
    }
}
```
