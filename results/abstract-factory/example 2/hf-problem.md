Add `Linux` OS:

```java
class Application {

    Button button;
    Checkbox checkbox;

    public Application(String osType) {

        if (osType.equals("Windows")) {
            button = new WindowsButton();
            checkbox = new WindowsCheckbox();
        } else if (osType.equals("Mac")) {
            button = new MacButton();
            checkbox = new MacCheckbox();
        }
    }

    public void render() {
        button.paint();
        checkbox.paint();
    }
}
```
