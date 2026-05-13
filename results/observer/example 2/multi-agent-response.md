# Below are the main problems with the original snippet and a concrete refactor that solves them by applying the **Observer** pattern.

---

## 1️⃣ What is wrong / what can be improved?

| Issue                                                                                        | Why it matters                                                                         |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Tight coupling to services** – `Product` directly calls `EmailService`, `SMSService`, etc. | Any new notification requires modifying the class → violates **Open/Closed Principle** |
| **Multiple responsibilities** – `Product` handles both domain logic and notification logic   | Breaks **Single Responsibility Principle**                                             |
| **Hard to extend** – adding Push, Webhook, Logging requires editing existing code            | Leads to fragile and error-prone code                                                  |
| **No reusability of notifications**                                                          | Notification logic cannot be reused elsewhere                                          |
| **Difficult to test**                                                                        | You must mock multiple services inside `Product`                                       |

---

## 2️⃣ Design pattern that fits

| Pattern                        | Role in the system                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| **Observer**                   | Allows multiple objects (observers) to react to changes in `Product` without tight coupling |
| **Subject (Observable)**       | `Product` – maintains a list of observers                                                   |
| **Observers**                  | Email, SMS, Analytics, etc.                                                                 |
| **(Optional) Event filtering** | Only notify when stock is low                                                               |

The key idea:

> The `Product` does **not know who is listening**, it only **broadcasts changes**.

---

## 3️⃣ Refactored code (Java 17)

```java
/* ---------- 1️⃣ Observer interface ---------- */
public interface StockObserver {
    void update(String productName, int stock);
}
```

---

```java
/* ---------- 2️⃣ Subject (Observable) ---------- */
import java.util.ArrayList;
import java.util.List;

public class Product {

    private final String name;
    private int stock;

    private final List<StockObserver> observers = new ArrayList<>();

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
        for (StockObserver observer : observers) {
            observer.update(name, stock);
        }
    }

    public void setStock(int stock) {
        this.stock = stock;

        if (stock < 5) { // business rule
            notifyObservers();
        }
    }
}
```

---

```java
/* ---------- 3️⃣ Concrete Observers ---------- */
public class EmailNotifier implements StockObserver {
    @Override
    public void update(String productName, int stock) {
        System.out.println("[Email] Stock low for " + productName);
    }
}

public class SMSNotifier implements StockObserver {
    @Override
    public void update(String productName, int stock) {
        System.out.println("[SMS] Stock low for " + productName);
    }
}

public class AnalyticsTracker implements StockObserver {
    @Override
    public void update(String productName, int stock) {
        System.out.println("[Analytics] low_stock event for " + productName);
    }
}
```

---

```java
/* ---------- 4️⃣ Usage example ---------- */
public class Demo {
    public static void main(String[] args) {

        Product product = new Product("iPhone", 10);

        product.addObserver(new EmailNotifier());
        product.addObserver(new SMSNotifier());
        product.addObserver(new AnalyticsTracker());

        product.setStock(3); // triggers notifications
    }
}
```

---

## 4️⃣ What changed?

| Before                            | After                        |
| --------------------------------- | ---------------------------- |
| `Product` directly calls services | `Product` notifies observers |
| High coupling                     | Loose coupling               |
| Hard to add features              | Plug-and-play observers      |
| Multiple responsibilities         | Clear separation             |
| Hard to test                      | Easy to mock observers       |

---

## 5️⃣ Why the **Observer Pattern** is the best fit

- **Decoupling** → `Product` doesn’t depend on notification implementations
- **Open/Closed** → add new observers without modifying existing code
- **Extensibility** → easily add:
  - Push notifications
  - Webhooks
  - Logging

- **Reusability** → observers can be reused across systems
- **Testability** → inject mock observers and assert behavior

---

## 6️⃣ Possible improvements (advanced)

### 🔹 Event object instead of primitives

```java
public record StockEvent(String productName, int stock) {}
```

---

### 🔹 Filtered observers

Only some observers react to certain conditions:

```java
if (stock < threshold) notifyObservers();
```

---

### 🔹 Asynchronous observers (real-world)

Instead of calling directly:

- Publish event to Kafka / RabbitMQ
- Observers consume asynchronously

---

## 7️⃣ Alternatives (and why they are worse)

| Alternative                     | Why it’s not ideal                    |
| ------------------------------- | ------------------------------------- |
| Direct service calls            | High coupling                         |
| Strategy                        | Not about interchangeable algorithms  |
| Abstract Factory                | Not about object families             |
| Event Bus (without abstraction) | Can become implicit and hard to trace |

---

## 8️⃣ Quick checklist for integration

| ✅                                            | Item |
| --------------------------------------------- | ---- |
| ✅ Extract observer interface                 |      |
| ✅ Remove direct service calls from `Product` |      |
| ✅ Add observer registration methods          |      |
| ✅ Move notification logic into observers     |      |
| ✅ Add unit tests with mock observers         |      |
| ✅ Document event trigger rules               |      |

---

## TL;DR

Replace direct calls like `EmailService.send()` inside `Product` with a list of **observers** that are notified when the stock changes. This removes coupling, improves extensibility, and aligns the design with SOLID principles—especially **Open/Closed** and **Single Responsibility**.
