Got it! You want to add a `WinnerState` to your gumball machine. This is usually part of the “State Pattern” enhancement for the gumball machine: sometimes, a customer wins and gets **two gumballs** for a single quarter.

Since your current implementation uses integers for states rather than the State Pattern classes, we can implement `WinnerState` as another integer state. Here’s an updated version:

```java
class GumballMachine {

    final static int SOLD_OUT = 0;
    final static int NO_QUARTER = 1;
    final static int HAS_QUARTER = 2;
    final static int SOLD = 3;
    final static int WINNER = 4; // New winner state

    int state = SOLD_OUT;
    int count = 0;

    public GumballMachine(int count) {
        this.count = count;
        if (count > 0) {
            state = NO_QUARTER;
        }
    }

    public void insertQuarter() {
        if (state == HAS_QUARTER) {
            System.out.println("You can't insert another quarter");
        } else if (state == NO_QUARTER) {
            state = HAS_QUARTER;
            System.out.println("Quarter inserted");
        } else if (state == SOLD_OUT) {
            System.out.println("Sold out");
        } else if (state == SOLD || state == WINNER) {
            System.out.println("Wait, we're already giving you a gumball");
        }
    }

    public void turnCrank() {
        if (state == SOLD) {
            System.out.println("Turning twice doesn't get another gumball!");
        } else if (state == NO_QUARTER) {
            System.out.println("You turned but there's no quarter");
        } else if (state == SOLD_OUT) {
            System.out.println("No gumballs");
        } else if (state == HAS_QUARTER) {
            System.out.println("You turned...");
            // 10% chance to win
            if (Math.random() < 0.1 && count > 1) {
                state = WINNER;
            } else {
                state = SOLD;
            }
            dispense();
        }
    }

    public void dispense() {
        if (state == SOLD) {
            System.out.println("A gumball comes rolling out");
            count--;
            if (count == 0) {
                state = SOLD_OUT;
            } else {
                state = NO_QUARTER;
            }
        } else if (state == WINNER) {
            System.out.println("YOU'RE A WINNER! Two gumballs come rolling out");
            count -= 2;
            if (count <= 0) {
                count = 0;
                state = SOLD_OUT;
            } else {
                state = NO_QUARTER;
            }
        } else {
            System.out.println("No gumball dispensed");
        }
    }
}
```

✅ **What changed:**

1. Added `WINNER = 4` state.
2. Modified `turnCrank()` to randomly select a winner (10% chance).
3. Updated `dispense()` to handle `WINNER` state and dispense **two gumballs**.

---

If you want, I can also **refactor this into the full State Pattern version**, where each state is a separate class—making it cleaner and easier to extend with new features like `WinnerState`. That’s the classic way the “Gumball Machine” example is handled in the Head First Design Patterns book.

Do you want me to do that?
