```java
interface PizzaIngredientFactory {
    Dough createDough();
    Sauce createSauce();
    Cheese createCheese();
}

class NYPizzaIngredientFactory implements PizzaIngredientFactory {

    public Dough createDough() {
        return new ThinCrustDough();
    }

    public Sauce createSauce() {
        return new MarinaraSauce();
    }

    public Cheese createCheese() {
        return new ReggianoCheese();
    }
}

class CheesePizza extends Pizza {

    PizzaIngredientFactory ingredientFactory;

    public CheesePizza(PizzaIngredientFactory factory) {
        this.ingredientFactory = factory;
    }

    void prepare() {
        dough = ingredientFactory.createDough();
        sauce = ingredientFactory.createSauce();
        cheese = ingredientFactory.createCheese();
    }
}

class NYPizzaStore extends PizzaStore {

    protected Pizza createPizza(String item) {

        Pizza pizza = null;
        PizzaIngredientFactory factory =
            new NYPizzaIngredientFactory();

        if (item.equals("cheese")) {
            pizza = new CheesePizza(factory);
        }

        return pizza;
    }
}
```
