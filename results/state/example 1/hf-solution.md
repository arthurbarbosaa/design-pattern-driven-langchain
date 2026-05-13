```java
interface State {
    void insertQuarter();
    void ejectQuarter();
    void turnCrank();
    void dispense();
}

class SoldOutState implements State {

    GumballMachine machine;

    public SoldOutState(GumballMachine machine) {
        this.machine = machine;
    }

    public void insertQuarter() {
        System.out.println("Machine is sold out");
    }

    public void ejectQuarter() {
        System.out.println("You didn't insert a quarter");
    }

    public void turnCrank() {
        System.out.println("You turned, but there are no gumballs");
    }

    public void dispense() {
        System.out.println("No gumball dispensed");
    }
}

class SoldOutState implements State {

    GumballMachine machine;

    public SoldOutState(GumballMachine machine) {
        this.machine = machine;
    }

    public void insertQuarter() {
        System.out.println("Machine is sold out");
    }

    public void ejectQuarter() {
        System.out.println("You didn't insert a quarter");
    }

    public void turnCrank() {
        System.out.println("You turned, but there are no gumballs");
    }

    public void dispense() {
        System.out.println("No gumball dispensed");
    }
}

import java.util.Random;

class NoQuarterState implements State {

    GumballMachine machine;

    public NoQuarterState(GumballMachine machine) {
        this.machine = machine;
    }

    public void insertQuarter() {
        System.out.println("You inserted a quarter");
        machine.setState(machine.getHasQuarterState());
    }

    public void ejectQuarter() {
        System.out.println("You haven't inserted a quarter");
    }

    public void turnCrank() {
        System.out.println("You turned but there's no quarter");
    }

    public void dispense() {
        System.out.println("You need to pay first");
    }
}

class HasQuarterState implements State {

    GumballMachine machine;
    Random randomWinner = new Random();

    public HasQuarterState(GumballMachine machine) {
        this.machine = machine;
    }

    public void insertQuarter() {
        System.out.println("You can't insert another quarter");
    }

    public void ejectQuarter() {
        System.out.println("Quarter returned");
        machine.setState(machine.getNoQuarterState());
    }

    public void turnCrank() {
        System.out.println("You turned...");

        int winner = randomWinner.nextInt(10);
        if (winner == 0 && machine.getCount() > 1) {
            machine.setState(machine.getWinnerState());
        } else {
            machine.setState(machine.getSoldState());
        }
    }

    public void dispense() {
        System.out.println("No gumball dispensed");
    }
}

class SoldState implements State {

    GumballMachine machine;

    public SoldState(GumballMachine machine) {
        this.machine = machine;
    }

    public void insertQuarter() {
        System.out.println("Please wait, we're already giving you a gumball");
    }

    public void ejectQuarter() {
        System.out.println("Sorry, you already turned the crank");
    }

    public void turnCrank() {
        System.out.println("Turning twice doesn't get another gumball!");
    }

    public void dispense() {
        machine.releaseBall();

        if (machine.getCount() > 0) {
            machine.setState(machine.getNoQuarterState());
        } else {
            System.out.println("Oops, out of gumballs!");
            machine.setState(machine.getSoldOutState());
        }
    }
}

class WinnerState implements State {

    GumballMachine machine;

    public WinnerState(GumballMachine machine) {
        this.machine = machine;
    }

    public void insertQuarter() {
        System.out.println("Please wait, we're already giving you gumballs");
    }

    public void ejectQuarter() {
        System.out.println("Sorry, you already turned the crank");
    }

    public void turnCrank() {
        System.out.println("Turning again doesn't get you more gumballs!");
    }

    public void dispense() {
        System.out.println("YOU'RE A WINNER! You get two gumballs!");

        machine.releaseBall();

        if (machine.getCount() == 0) {
            machine.setState(machine.getSoldOutState());
        } else {
            machine.releaseBall();

            if (machine.getCount() > 0) {
                machine.setState(machine.getNoQuarterState());
            } else {
                System.out.println("Oops, out of gumballs!");
                machine.setState(machine.getSoldOutState());
            }
        }
    }
}

class GumballMachine {

    State soldOutState;
    State noQuarterState;
    State hasQuarterState;
    State soldState;
    State winnerState;

    State state;
    int count = 0;

    public GumballMachine(int numberGumballs) {

        soldOutState = new SoldOutState(this);
        noQuarterState = new NoQuarterState(this);
        hasQuarterState = new HasQuarterState(this);
        soldState = new SoldState(this);
        winnerState = new WinnerState(this);

        this.count = numberGumballs;

        if (numberGumballs > 0) {
            state = noQuarterState;
        } else {
            state = soldOutState;
        }
    }

    public void insertQuarter() {
        state.insertQuarter();
    }

    public void ejectQuarter() {
        state.ejectQuarter();
    }

    public void turnCrank() {
        state.turnCrank();
        state.dispense();
    }

    void setState(State state) {
        this.state = state;
    }

    void releaseBall() {
        if (count != 0) {
            System.out.println("A gumball comes rolling out...");
            count--;
        }
    }

    int getCount() {
        return count;
    }

    State getSoldOutState() { return soldOutState; }
    State getNoQuarterState() { return noQuarterState; }
    State getHasQuarterState() { return hasQuarterState; }
    State getSoldState() { return soldState; }
    State getWinnerState() { return winnerState; }
}

public class TestDrive {
    public static void main(String[] args) {

        GumballMachine machine = new GumballMachine(5);

        machine.insertQuarter();
        machine.turnCrank();

        System.out.println("----");

        machine.insertQuarter();
        machine.ejectQuarter();

        System.out.println("----");

        machine.insertQuarter();
        machine.turnCrank();
    }
}
```
