Add a `RobberDuck` that cannot fly:

```java
class Duck {
    void quack() { System.out.println("Quack"); }
    void swim() { System.out.println("Swim"); }
    void fly() { System.out.println("Fly"); }
}
class MallardDuck extends Duck {}
class RubberDuck extends Duck {}
```
