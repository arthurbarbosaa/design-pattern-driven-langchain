improve this code:

```java
class Product {

    private String name;
    private int stock;

    public Product(String name, int stock) {
        this.name = name;
        this.stock = stock;
    }

    public void setStock(int stock) {
        this.stock = stock;

        // Notificações diretas (acoplamento forte)
        if (stock < 5) {
            EmailService.send("Stock low for " + name);
            SMSService.send("Stock low for " + name);
            AnalyticsService.track("low_stock", name);
        }
    }
}
```
