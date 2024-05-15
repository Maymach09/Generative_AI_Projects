import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import os
from tkinter import filedialog
from completion_tc_generator import OpenAIClient as PromptsOpenAIClient, summarize_requirements, generate_code, generate_test_cases, generate_traceability_matrix

# Code for UI tab 1: tc_generator_prompts
def run_summarize_requirements():
    requirements = text_requirements.get("1.0", tk.END)
    output_summary = summarize_requirements(requirements, client)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output_summary)

def run_generate_code():
    requirements = text_requirements.get("1.0", tk.END)
    output_code = generate_code(requirements, client)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output_code)

def run_generate_test_cases():
    requirements = text_requirements.get("1.0", tk.END)
    output_test_cases = generate_test_cases(requirements, client)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output_test_cases)

def run_generate_traceability_matrix():
    requirements = text_requirements.get("1.0", tk.END)
    output_test_cases = text_output.get("1.0", tk.END)
    output_tm = generate_traceability_matrix(requirements, output_test_cases, client)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output_tm)

def import_requirements():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            output_requirements = file.read()
            text_requirements.delete("1.0", tk.END)  # Clear existing text
            text_requirements.insert(tk.END, output_requirements)

def create_ui():
    # Create the main window
    window = tk.Tk()
    window.title("Requirements Analysis Tool")

    # Create input text box for requirements
    global text_requirements
    text_requirements = scrolledtext.ScrolledText(window, width=80, height=15, wrap=tk.WORD)
    text_requirements.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Load requirements from file button
    btn_load_from_file = tk.Button(window, text="Import Requirements", command=import_requirements)
    btn_load_from_file.grid(row=0, column=3, padx=5, pady=5)

    # Create summarize requirements button
    btn_summarize = tk.Button(window, text="Summarize Requirements", command=run_summarize_requirements)
    btn_summarize.grid(row=1, column=0, padx=5, pady=5)

    # Create generate code button
    btn_generate_code = tk.Button(window, text="Generate Code", command=run_generate_code)
    btn_generate_code.grid(row=1, column=1, padx=5, pady=5)

    # Create generate test cases button
    btn_generate_test_cases = tk.Button(window, text="Generate Test Cases", command=run_generate_test_cases)
    btn_generate_test_cases.grid(row=1, column=2, padx=5, pady=5)
    
    # Create generate traceability matrix button
    btn_generate_tm = tk.Button(window, text="Generate Traceability Matrix", command=run_generate_traceability_matrix)
    btn_generate_tm.grid(row=1, column=3, padx=5, pady=5)

    # Create export button
    btn_export = tk.Button(window, text="Export", command=export_output)
    btn_export.grid(row=1, column=4, padx=5, pady=5)

    # Create output text box for results
    global text_output
    text_output = scrolledtext.ScrolledText(window, width=80, height=20, wrap=tk.WORD)
    text_output.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # Initialize OpenAI client
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    global client
    client = PromptsOpenAIClient(openai_api_key)

    # Start the GUI event loop
    window.mainloop()

def export_output():
    output = text_output.get("1.0", tk.END)
    with open("C:\Documents\AI\GenAI\chatgpt-openai\Gen_AI_Projects\Output_Files\output.txt", "w") as file:
        file.write(output)
    print("Output exported")

# Create UI
create_ui()