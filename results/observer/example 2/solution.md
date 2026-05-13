```java
interface StockObserver {
    void update(String productName, int stock);
}

import java.util.ArrayList;
import java.util.List;

class Product {

    private String name;
    private int stock;

    private List<StockObserver> observers = new ArrayList<>();

    public Product(String name, int stock) {
        this.name = name;
        this.stock = stock;
    }

    public void addObserver(StockObserver observer) {
        observers.add(observer);
    }

    public void removeObserver(StockObserver observer) {
        observers.remove(observer);
    }

    private void notifyObservers() {
        for (StockObserver o : observers) {
            o.update(name, stock);
        }
    }

    public void setStock(int stock) {
        this.stock = stock;

        if (stock < 5) {
            notifyObservers();
        }
    }
}

class EmailNotifier implements StockObserver {
    public void update(String productName, int stock) {
        System.out.println("Email: Stock low for " + productName);
    }
}

class SMSNotifier implements StockObserver {
    public void update(String productName, int stock) {
        System.out.println("SMS: Stock low for " + productName);
    }
}

class AnalyticsTracker implements StockObserver {
    public void update(String productName, int stock) {
        System.out.println("Tracking event: low_stock for " + productName);
    }
}

public class Main {
    public static void main(String[] args) {

        Product product = new Product("iPhone", 10);

        product.addObserver(new EmailNotifier());
        product.addObserver(new SMSNotifier());
        product.addObserver(new AnalyticsTracker());

        product.setStock(3); // dispara notificações
    }
}
```
