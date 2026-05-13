A `RubberDuck` inheriting `fly()` is a design problem because rubber ducks should not fly.
A cleaner approach is to separate behaviors into interfaces instead of putting everything in the base class.

```java
interface Flyable {
    void fly();
}

interface Quackable {
    void quack();
}

class Duck {
    void swim() {
        System.out.println("Swim");
    }
}

class MallardDuck extends Duck implements Flyable, Quackable {

    public void fly() {
        System.out.println("Fly");
    }

    public void quack() {
        System.out.println("Quack");
    }
}

class RubberDuck extends Duck implements Quackable {

    public void quack() {
        System.out.println("Squeak");
    }
}
```

Now:

- `MallardDuck` can fly and quack.
- `RubberDuck` can swim and squeak, but has no `fly()` method.
- The design follows the Interface Segregation Principle and avoids giving subclasses invalid behavior.
