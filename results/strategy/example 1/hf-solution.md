```java
interface FlyBehavior {
    void fly();
}
class FlyWithWings implements FlyBehavior {
    public void fly() {
        System.out.println("Flying with wings");
    }
}
class FlyNoWay implements FlyBehavior {
    public void fly() {
        System.out.println("I can't fly");
    }
}
class Duck {
    FlyBehavior flyBehavior;

    void performFly() {
        flyBehavior.fly();
    }
}
class MallardDuck extends Duck {
    MallardDuck() {
        flyBehavior = new FlyWithWings();
    }
}

class RubberDuck extends Duck {
    RubberDuck() {
        flyBehavior = new FlyNoWay();
    }
}
duck.flyBehavior = new FlyNoWay();
```
