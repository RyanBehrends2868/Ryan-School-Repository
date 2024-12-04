import re
import tkinter as tk
from tkinter import ttk

class LogicalExpressionEvaluator:
    def __init__(self, expression):
        self.expression = expression
        self.variables = self.getVariables()
        self.combinations = self.makeCombinations()
        self.results = self.evaluateLogic()

    def getVariables(self):
        # Extract unique variables from the logical expression using regular expressions.
        return sorted(set(re.findall(r'\b[A-Za-z]\b', self.expression)))

    def makeCombinations(self):
        n = len(self.variables)
        combinations = []
        for i in range(2 ** n):
            binary_string = bin(i)[2:].zfill(n)  # Convert i to binary, remove prefix, pad with 0s to match number of variables
            combination = [bool(int(bit)) for bit in binary_string]
            combinations.append(combination)
        return combinations

    def evaluateLogic(self):
        results = []
        for combination in self.combinations:
            values = dict(zip(self.variables, combination))
            evaluate_expression = self.expression
            # Use Regex to replace variables with their truth values
            for var, val in values.items():
                evaluate_expression = re.sub(rf'\b{var}\b', "True" if val else "False", evaluate_expression)
            # Evaluate the expression    
            try:
                result = eval(evaluate_expression)
            except Exception as e:
                result = f"Error: {e}"
            results.append((values, result))
        return results

    def printResults(self):
        # Header
        header = ' | '.join(self.variables) + f' | {self.expression}'
        print(header)
        print('-' * len(header))
        # Results
        for values, result in self.results:
            row = ' | '.join(str(values[var]) for var in self.variables) + f' | {result}'
            print(row)

    def displayResultsInGUI(self):
        root = tk.Tk()
        root.title("Truth Table Generator")

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text=f"Logical Expression: {self.expression}").grid(row=0, column=0, columnspan=len(self.variables) + 1, pady=5)

        # Header
        for col_index, var in enumerate(self.variables):
            ttk.Label(main_frame, text=var, borderwidth=1, relief="solid", padding=5).grid(row=1, column=col_index, padx=5, pady=5)
        ttk.Label(main_frame, text="Result", borderwidth=1, relief="solid", padding=5).grid(row=1, column=len(self.variables), padx=5, pady=5)

        # Results
        for row_index, (values, result) in enumerate(self.results, start=2):
            for col_index, var in enumerate(self.variables):
                ttk.Label(main_frame, text=str(values[var]), borderwidth=1, relief="solid", padding=5).grid(row=row_index, column=col_index, padx=5, pady=5)
            ttk.Label(main_frame, text=str(result), borderwidth=1, relief="solid", padding=5).grid(row=row_index, column=len(self.variables), padx=5, pady=5)

        for col_index in range(len(self.variables) + 1):
            main_frame.columnconfigure(col_index, weight=1)

        root.mainloop()


def main():
    def on_generate(event=None):
        expression = entry_expression.get()
        evaluator = LogicalExpressionEvaluator(expression)
        evaluator.printResults()
        evaluator.displayResultsInGUI()

    root = tk.Tk()
    root.title("Truth Table Generator")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(main_frame, text="Enter Logical Expression (eg. A and B or not C):").grid(row=0, column=0, columnspan=2, pady=5)

    entry_expression = ttk.Entry(main_frame, width=50)
    entry_expression.grid(row=1, column=0, columnspan=2, pady=5)
    entry_expression.bind('<Return>', on_generate)


    generate_button = ttk.Button(main_frame, text="Generate Truth Table", command=on_generate)
    generate_button.grid(row=2, column=0, columnspan=2, pady=10)


    root.mainloop()

main()
