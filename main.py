from src.orchestrator import Orchestrator
import sys
import os
import argparse

# Ensure 'src' is in PYTHONPATH for cross-module imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def main():

    parser = argparse.ArgumentParser(
        description="Design Patterns Multi-Agent ReAct System.")
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a source code file to analyze."
    )
    args = parser.parse_args()

    # Small messy code sample for out-of-the-box testing if no file is provided
    sample_code = '''
class Order:
    def __init__(self, items, customer, payment_method):
        self.items = items
        self.customer = customer
        self.payment_method = payment_method
        self.total = sum(i['price'] for i in items)

    def process_payment(self):
        if self.payment_method == "credit_card":
            print(f"Processing credit card for {self.total}")
        elif self.payment_method == "paypal":
            print(f"Processing paypal for {self.total}")
        elif self.payment_method == "bitcoin":
            print(f"Processing bitcoin for {self.total}")
        else:
            raise Exception("Payment method not supported")
'''

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                code_to_process = f.read()
        except Exception as e:
            print(f"Error reading file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("No input file provided. Running on internal sample code...")
        code_to_process = sample_code

    print("\n--- Starting Orchestrator Pipeline ---\n")
    orchestrator = Orchestrator()

    user_prompt = f"Refactor and return the following code to use an appropriate design pattern:\n\n```python\n{code_to_process}\n```"
    final_output, used_model = orchestrator.invoke(user_prompt)

    print("\n--- Runtime Model Used ---")
    print(f"Model used: {used_model}")

    print("\n--- Final Agent Output ---\n")
    print(final_output)


if __name__ == "__main__":
    main()
