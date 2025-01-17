import tkinter as tk
from tkinter import filedialog, messagebox

class ProcessorSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Processor Simulator")

        # Rejestry procesora
        self.registers = {
            'AX': 0,
            'BX': 0,
            'CX': 0,
            'DX': 0
        }

        # Instrukcje programu
        self.program = []
        self.current_instruction = 0

        # Interfejs użytkownika
        self.create_widgets()

    def create_widgets(self):
        # Pole na kod programu
        self.program_label = tk.Label(self.root, text="Program")
        self.program_label.pack()
        self.program_text = tk.Text(self.root, height=10, width=50)
        self.program_text.pack()

        # Przyciski do obsługi programu
        self.run_button = tk.Button(self.root, text="Run", command=self.run_program)
        self.run_button.pack()

        self.step_button = tk.Button(self.root, text="Step", command=self.step_program)
        self.step_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_program)
        self.reset_button.pack()

        self.save_button = tk.Button(self.root, text="Save Program", command=self.save_program)
        self.save_button.pack()

        self.load_button = tk.Button(self.root, text="Load Program", command=self.load_program)
        self.load_button.pack()

        # Pole wyświetlania rejestrów
        self.registers_label = tk.Label(self.root, text="Registers")
        self.registers_label.pack()
        self.registers_text = tk.Text(self.root, height=5, width=50)
        self.registers_text.pack()
        self.update_register_display()

    def update_register_display(self):
        self.registers_text.delete(1.0, tk.END)
        for reg, value in self.registers.items():
            self.registers_text.insert(tk.END, f"{reg}: {value:04X}\n")

    def parse_instruction(self, instruction):
        parts = instruction.split()
        if len(parts) < 2:
            raise ValueError("Invalid instruction format")
        cmd = parts[0].upper()
        args = parts[1:]
        return cmd, args

    def execute_instruction(self, instruction):
        cmd, args = self.parse_instruction(instruction)

        if cmd == "MOV":
            if args[1].startswith("#"):
                value = int(args[1][1:], 16)
                self.registers[args[0]] = value
            else:
                self.registers[args[0]] = self.registers[args[1]]

        elif cmd == "ADD":
            if args[1].startswith("#"):
                value = int(args[1][1:], 16)
                self.registers[args[0]] += value
            else:
                self.registers[args[0]] += self.registers[args[1]]

        elif cmd == "SUB":
            if args[1].startswith("#"):
                value = int(args[1][1:], 16)
                self.registers[args[0]] -= value
            else:
                self.registers[args[0]] -= self.registers[args[1]]

        else:
            raise ValueError(f"Unknown command: {cmd}")

        # Ensure 16-bit values
        for reg in self.registers:
            self.registers[reg] &= 0xFFFF

    def run_program(self):
        self.program = self.program_text.get(1.0, tk.END).strip().splitlines()
        try:
            for instruction in self.program:
                self.execute_instruction(instruction)
            self.update_register_display()
            messagebox.showinfo("Success", "Program executed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def step_program(self):
        if not self.program:
            self.program = self.program_text.get(1.0, tk.END).strip().splitlines()

        if self.current_instruction < len(self.program):
            try:
                instruction = self.program[self.current_instruction]
                self.execute_instruction(instruction)
                self.current_instruction += 1
                self.update_register_display()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Info", "Program execution complete.")

    def reset_program(self):
        self.registers = {key: 0 for key in self.registers}
        self.program = []
        self.current_instruction = 0
        self.update_register_display()
        messagebox.showinfo("Reset", "Processor reset successfully.")

    def save_program(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.program_text.get(1.0, tk.END))
            messagebox.showinfo("Saved", "Program saved successfully.")

    def load_program(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.program_text.delete(1.0, tk.END)
                self.program_text.insert(tk.END, file.read())
            messagebox.showinfo("Loaded", "Program loaded successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessorSimulator(root)
    root.mainloop()
