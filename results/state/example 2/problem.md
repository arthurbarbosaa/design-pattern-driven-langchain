Add a `STOPPED` state:

```java
class Order {

    private String status; // "NEW", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"

    public Order() {
        this.status = "NEW";
    }

    public void pay() {
        if (status.equals("NEW")) {
            status = "PAID";
            System.out.println("Order paid");
        } else {
            System.out.println("Cannot pay in state: " + status);
        }
    }

    public void ship() {
        if (status.equals("PAID")) {
            status = "SHIPPED";
            System.out.println("Order shipped");
        } else {
            System.out.println("Cannot ship in state: " + status);
        }
    }

    public void deliver() {
        if (status.equals("SHIPPED")) {
            status = "DELIVERED";
            System.out.println("Order delivered");
        } else {
            System.out.println("Cannot deliver in state: " + status);
        }
    }

    public void cancel() {
        if (status.equals("NEW") || status.equals("PAID")) {
            status = "CANCELLED";
            System.out.println("Order cancelled");
        } else {
            System.out.println("Cannot cancel in state: " + status);
        }
    }
}
```
