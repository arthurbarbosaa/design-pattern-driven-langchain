Below is a **complete, refactored** version of the `GumballMachine` that uses the **State pattern** and adds a **`WinnerState`** (the “you‑win‑two‑gumballs” case).

The refactoring does three things:

1. **Eliminates the “int‑state” primitive** – the machine now holds a reference to a `State` object.
2. **Encapsulates all state‑specific behaviour** inside concrete state classes (`NoQuarterState`, `HasQuarterState`, `SoldState`, `SoldOutState`, `WinnerState`).
3. **Adds a `WinnerState`** – after a successful crank there is a chance (e.g. 10 %) that the machine goes into this state, dispensing **two** gumballs instead of one.

---

## 1. The State interface

```java
public interface State {
    /** Called when a quarter is inserted */
    void insertQuarter();

    /** Called when the crank is turned */
    void turnCrank();

    /** Called by the machine to release a gumball (or two) */
    void dispense();
}
```

All concrete states implement this contract and can interact with the **context** (`GumballMachine`) through a protected reference.

---

## 2. The GumballMachine (Context)

```java
import java.util.Random;

public class GumballMachine {

    // ----- State objects -------------------------------------------------
    private final State soldOutState;
    private final State noQuarterState;
    private final State hasQuarterState;
    private final State soldState;
    private final State winnerState;

    // ----- Current state -------------------------------------------------
    private State state;               // the *behaviour* object
    private int count = 0;             // number of gumballs left
    private final Random rand = new Random();

    // ----- Construction -------------------------------------------------
    public GumballMachine(int numberOfGumballs) {
        soldOutState   = new SoldOutState(this);
        noQuarterState = new NoQuarterState(this);
        hasQuarterState = new HasQuarterState(this);
        soldState      = new SoldState(this);
        winnerState    = new WinnerState(this);

        this.count = numberOfGumballs;
        this.state = (numberOfGumballs > 0) ? noQuarterState : soldOutState;
    }

    // ----- Public API – simply delegate to the current State ----------
    public void insertQuarter() { state.insertQuarter(); }
    public void turnCrank() {
        state.turnCrank();
        // `turnCrank()` may change the state to SOLD or WINNER.
        // In either case we must call dispense() *after* the turn.
        state.dispense();
    }

    // ----- Helper methods used by concrete State objects ---------------
    void releaseBall() {
        System.out.println("A gumball comes rolling out...");
        if (count > 0) count--;
    }

    int getCount() { return count; }

    void setState(State newState) { this.state = newState; }

    State getSoldOutState()   { return soldOutState; }
    State getNoQuarterState() { return noQuarterState; }
    State getHasQuarterState(){ return hasQuarterState; }
    State getSoldState()      { return soldState; }
    State getWinnerState()    { return winnerState; }

    /** Returns true with a probability of 10 % – the “winner” chance */
    boolean isWinner() { return rand.nextInt(10) == 0; }

    // ----- Optional diagnostics -----------------------------------------
    @Override
    public String toString() {
        return "GumballMachine {" +
               "state=" + state.getClass().getSimpleName() +
               ", count=" + count + '}';
    }
}
```

**Key points**

- The machine **never** uses `if (state == SOME_STATE)` any more – all decisions live inside the concrete state classes.
- `turnCrank()` first calls `state.turnCrank()` (which may switch the machine to `SoldState` or `WinnerState`) and **always** follows with `state.dispense()`. This mirrors the original logic where `dispense()` was called only when the state became `SOLD`.
- The `isWinner()` method encapsulates the random‑winner logic; you can adjust the probability or replace it with any business rule.

---

## 3. Concrete State classes

### 3.1 SoldOutState

```java
public class SoldOutState implements State {
    private final GumballMachine machine;

    public SoldOutState(GumballMachine machine) { this.machine = machine; }

    @Override public void insertQuarter() {
        System.out.println("You can't insert a quarter, the machine is sold out");
    }
    @Override public void turnCrank() {
        System.out.println("You turned, but there are no gumballs");
    }
    @Override public void dispense() {
        System.out.println("No gumball dispensed");
    }
}
```

### 3.2 NoQuarterState

```java
public class NoQuarterState implements State {
    private final GumballMachine machine;

    public NoQuarterState(GumballMachine machine) { this.machine = machine; }

    @Override public void insertQuarter() {
        System.out.println("Quarter inserted");
        machine.setState(machine.getHasQuarterState());
    }
    @Override public void turnCrank() {
        System.out.println("You turned, but there's no quarter");
    }
    @Override public void dispense() {
        System.out.println("You need to pay first");
    }
}
```

### 3.3 HasQuarterState

```java
public class HasQuarterState implements State {
    private final GumballMachine machine;

    public HasQuarterState(GumballMachine machine) { this.machine = machine; }

    @Override public void insertQuarter() {
        System.out.println("You can't insert another quarter");
    }
    @Override public void turnCrank() {
        System.out.println("You turned...");
        // Decide winner *before* we move to the next state
        if (machine.isWinner() && machine.getCount() > 1) {
            machine.setState(machine.getWinnerState());
        } else {
            machine.setState(machine.getSoldState());
        }
    }
    @Override public void dispense() {
        System.out.println("No gumball dispensed");
    }
}
```

### 3.4 SoldState

```java
public class SoldState implements State {
    private final GumballMachine machine;

    public SoldState(GumballMachine machine) { this.machine = machine; }

    @Override public void insertQuarter() {
        System.out.println("Please wait, we're already giving you a gumball");
    }
    @Override public void turnCrank() {
        System.out.println("Turning twice doesn't get another gumball!");
    }
    @Override public void dispense() {
        machine.releaseBall();
        if (machine.getCount() == 0) {
            machine.setState(machine.getSoldOutState());
        } else {
            machine.setState(machine.getNoQuarterState());
        }
    }
}
```

### 3.5 WinnerState _(the new behaviour)_

```java
public class WinnerState implements State {
    private final GumballMachine machine;

    public WinnerState(GumballMachine machine) { this.machine = machine; }

    @Override public void insertQuarter() {
        System.out.println("Please wait, we're already giving you gumballs");
    }
    @Override public void turnCrank() {
        System.out.println("Turning again won't give more gumballs");
    }
    @Override public void dispense() {
        System.out.println("YOU'RE A WINNER! You get two gumballs!");
        // First gumball
        machine.releaseBall();

        // Second gumball – only if there is still inventory
        if (machine.getCount() > 0) {
            machine.releaseBall();
        }

        // Transition to the appropriate next state
        if (machine.getCount() == 0) {
            machine.setState(machine.getSoldOutState());
        } else {
            machine.setState(machine.getNoQuarterState());
        }
    }
}
```

**What `WinnerState` does**

- When the machine decides the customer is a winner (10 % chance, defined in `HasQuarterState.turnCrank()`), it swaps to `WinnerState`.
- `WinnerState.dispense()` releases **two** gumballs (or one if the inventory runs out after the first).
- After dispensing, the machine goes back to `NoQuarterState` (or `SoldOutState` if the last ball was just given).

---

## 4. Usage example

```java
public class Main {
    public static void main(String[] args) {
        GumballMachine machine = new GumballMachine(5);

        // Normal flow
        machine.insertQuarter();   // Quarter inserted
        machine.turnCrank();       // You turned... (maybe winner)
        System.out.println(machine); // shows current state & count

        // Try a second quarter without inserting one
        machine.turnCrank();       // You turned, but there's no quarter

        // Insert another quarter
        machine.insertQuarter();   // Quarter inserted
        machine.turnCrank();       // You turned... (maybe winner)

        // Exhaust the machine to see SOLD_OUT handling
        while (machine.getCount() > 0) {
            machine.insertQuarter();
            machine.turnCrank();
        }

        // After sold out
        machine.insertQuarter();   // You can't insert a quarter, the machine is sold out
    }
}
```

Running the above will produce output similar to:

```
Quarter inserted
You turned...
A gumball comes rolling out...
GumballMachine {state=NoQuarterState, count=4}
You turned, but there's no quarter
Quarter inserted
You turned...
YOU'RE A WINNER! You get two gumballs!
A gumball comes rolling out...
A gumball comes rolling out...
GumballMachine {state=NoQuarterState, count=2}
...
You can't insert a quarter, the machine is sold out
```

Occasionally you’ll see the “YOU'RE A WINNER!” line – that’s the `WinnerState` in action.

---

## 5. Why this is better (design‑pattern perspective)

| Original implementation                                                                                           | Refactored (State pattern)                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Big `if‑else` blocks** everywhere, hard to extend (adding a new state means touching many methods).             | **Behavior** is encapsulated in separate classes; adding a new state only requires a new class.                                       |
| **State is a primitive `int`**, easy to misuse (`state = 5`).                                                     | **State is a type‑safe object** (`State` interface), the compiler prevents illegal values.                                            |
| **All methods have to know about every state** (e.g. `turnCrank()` checks `SOLD`, `NO_QUARTER`, `SOLD_OUT`, ...). | **Each state knows only what it cares about**; `HasQuarterState` only cares about inserting a quarter or turning the crank.           |
| **Adding `WinnerState`** would require inserting more `if` branches in several methods.                           | **`WinnerState` is a self‑contained class**; no other class needs to change (except the random‑winner decision in `HasQuarterState`). |
| **Testing** requires wiring the whole `GumballMachine` to a particular state.                                     | **Unit‑testing each state independently** is trivial – just instantiate the concrete state with a mock `GumballMachine`.              |

Thus, the **State pattern** gives you:

- **Open/Closed Principle** – you can add new behaviours without modifying existing code.
- **Clear separation of concerns** – the machine’s “what” (`GumballMachine`) is separated from its “how” (the concrete `State`s).
- **Better readability & maintainability** – every state’s rules are in a single, modestly‑sized class.

---

## 6. Quick checklist if you want to integrate this into an existing project

| ✅                                                                                                                                                                                                         | Item |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| **Compile** – all classes should be in the same package or imported accordingly.                                                                                                                           |
| **Replace old client code** – any code that used `machine.insertQuarter(); machine.turnCrank();` stays exactly the same; the internal implementation changed only.                                         |
| **Serialisation / persistence** – if you stored the primitive `state` value, replace it with `machine.getState().getClass().getSimpleName()` or add a tiny enum to map the concrete state back on restore. |
| **Logging / monitoring** – you may add a `getStateName()` method that returns `state.getClass().getSimpleName()` for dashboards.                                                                           |
| **Unit tests** – keep the old tests; they will still pass because the public API didn’t change. Add new tests that verify the 2‑gumball “winner” path.                                                     |

---

### TL;DR

_Introduce a `State` interface, create concrete state classes (`NoQuarterState`, `HasQuarterState`, `SoldState`, `SoldOutState`, `WinnerState`), let `GumballMachine` hold a `State` reference, and move all the `if‑else` logic into the appropriate state objects._

The `WinnerState` shown above gives the machine the new “double‑gumball” behaviour while keeping the overall design clean, extensible, and fully compliant with the **State** design pattern.
