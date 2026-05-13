**Problem**  
`RubberDuck` (and the new `RobberDuck`) can’t really fly, but they inherit the concrete `fly()` method from `Duck`.  
That violates the **Liskov Substitution Principle** – a subclass should be usable anywhere its base class is expected.

**Solution – Strategy pattern**  
Extract the “fly” ability into its own _behaviour_ interface.  
`Duck` becomes a _context_ that delegates the flying operation to a `FlyBehavior` object.  
Each concrete duck composes the appropriate behaviour (`FlyWithWings` or `NoFly`).  
Now any duck – Mallard, Rubber, Robber, or a future one – can be given the right flying capability without breaking inheritance rules, and the behaviour can even be changed at runtime.

---

### Refactored code (Java)

```java
// ---------- Fly behaviour (Strategy) ----------
interface FlyBehavior {
    void fly();
}

class FlyWithWings implements FlyBehavior {
    @Override
    public void fly() {
        System.out.println("Fly");
    }
}

class NoFly implements FlyBehavior {
    @Override
    public void fly() {
        // intentionally does nothing – a duck that cannot fly
        System.out.println("I can't fly");
    }
}

// ---------- Duck (Context) ----------
abstract class Duck {
    // other behaviours can also be extracted (quack, swim) – omitted for brevity
    private FlyBehavior flyBehavior;

    protected Duck(FlyBehavior flyBehavior) {
        this.flyBehavior = flyBehavior;
    }

    public void performFly() {
        flyBehavior.fly();
    }

    // optional – allow changing the behaviour at runtime
    public void setFlyBehavior(FlyBehavior fb) {
        this.flyBehavior = fb;
    }

    public void quack() {
        System.out.println("Quack");
    }

    public void swim() {
        System.out.println("Swim");
    }
}

// ---------- Concrete Ducks ----------
class MallardDuck extends Duck {
    public MallardDuck() {
        super(new FlyWithWings());   // Mallard can fly
    }
}

class RubberDuck extends Duck {
    public RubberDuck() {
        super(new NoFly());          // Rubber ducks don’t fly
    }
}

// **New** duck that also cannot fly
class RobberDuck extends Duck {
    public RobberDuck() {
        super(new NoFly());          // Robber Duck cannot fly either
    }
}
```

### How it works

```java
public class Demo {
    public static void main(String[] args) {
        Duck mallard = new MallardDuck();
        Duck rubber = new RubberDuck();
        Duck robber = new RobberDuck();

        mallard.quack();   // Quack
        mallard.performFly(); // Fly

        rubber.quack();   // Quack
        rubber.performFly(); // I can't fly

        robber.quack();   // Quack
        robber.performFly(); // I can't fly
    }
}
```

### Benefits

| Issue                     | Before                                               | After (Strategy)                                           |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| **Liskov Substitution**   | `RubberDuck` inherits an invalid `fly()`             | Each duck gets a _compatible_ fly behaviour                |
| **Extensibility**         | Adding a new flying rule requires subclass overrides | Add a new `FlyBehavior` implementation (e.g., `RocketFly`) |
| **Runtime flexibility**   | Behaviour fixed at compile‑time                      | `setFlyBehavior()` lets you change it on the fly           |
| **Single Responsibility** | `Duck` does everything                               | `FlyBehavior` encapsulates the flying algorithm            |

If you also want to vary _quack_ or _swim_ independently, extract `QuackBehavior` and `SwimBehavior` the same way, turning `Duck` into a fully composable “behaviour‑based” class. This keeps the design clean, testable, and open for future duck types.
