```java
interface OrderState {
    void pay(Order order);
    void ship(Order order);
    void deliver(Order order);
    void cancel(Order order);
}

class NewState implements OrderState {

    public void pay(Order order) {
        System.out.println("Order paid");
        order.setState(new PaidState());
    }

    public void ship(Order order) {
        System.out.println("Cannot ship before payment");
    }

    public void deliver(Order order) {
        System.out.println("Cannot deliver before shipping");
    }

    public void cancel(Order order) {
        System.out.println("Order cancelled");
        order.setState(new CancelledState());
    }
}

class PaidState implements OrderState {

    public void pay(Order order) {
        System.out.println("Already paid");
    }

    public void ship(Order order) {
        System.out.println("Order shipped");
        order.setState(new ShippedState());
    }

    public void deliver(Order order) {
        System.out.println("Cannot deliver before shipping");
    }

    public void cancel(Order order) {
        System.out.println("Order cancelled");
        order.setState(new CancelledState());
    }
}

class ShippedState implements OrderState {

    public void pay(Order order) {
        System.out.println("Already paid");
    }

    public void ship(Order order) {
        System.out.println("Already shipped");
    }

    public void deliver(Order order) {
        System.out.println("Order delivered");
        order.setState(new DeliveredState());
    }

    public void cancel(Order order) {
        System.out.println("Cannot cancel after shipping");
    }
}

class DeliveredState implements OrderState {

    public void pay(Order order) {}
    public void ship(Order order) {}
    public void deliver(Order order) {
        System.out.println("Already delivered");
    }
    public void cancel(Order order) {
        System.out.println("Cannot cancel delivered order");
    }
}

class CancelledState implements OrderState {

    public void pay(Order order) {}
    public void ship(Order order) {}
    public void deliver(Order order) {}
    public void cancel(Order order) {
        System.out.println("Already cancelled");
    }
}

class Order {

    private OrderState state;

    public Order() {
        this.state = new NewState();
    }

    public void setState(OrderState state) {
        this.state = state;
    }

    public void pay() {
        state.pay(this);
    }

    public void ship() {
        state.ship(this);
    }

    public void deliver() {
        state.deliver(this);
    }

    public void cancel() {
        state.cancel(this);
    }
}

public class Main {
    public static void main(String[] args) {

        Order order = new Order();

        order.pay();
        order.ship();
        order.deliver();
    }
}
```
