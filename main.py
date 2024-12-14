import tkinter as tk
from tkinter import ttk, messagebox

# Function to parse input string into a list of integers, returns None if invalid input
def parse_input(input_str):
    try:
        return list(map(int, input_str.split(",")))  # Split the input string by commas and convert to integers
    except ValueError:
        messagebox.showerror("Error", "Please enter integers separated by commas.")  # Show error if input is invalid
        return None

# First Fit Memory Allocation Algorithm
def first_fit(block_sizes, process_sizes):
    allocation = [-1] * len(process_sizes)  # Initialize allocation list, -1 indicates no allocation
    block_summary = [block for block in block_sizes]  # Store the original block sizes for later summary

    # Loop over each process to find the first suitable block for allocation
    for i, process in enumerate(process_sizes):
        for j, block in enumerate(block_sizes):
            if block >= process:  # Check if the block can fit the process
                allocation[i] = j  # Allocate the block to the process
                block_sizes[j] -= process  # Decrease the block size by the process size
                break

    return allocation, block_summary  # Return the allocation list and the original block sizes

# Function to summarize block usage (used space) by calculating the difference between original and remaining block sizes
def summarize_blocks(block_sizes, block_summary):
    return [original - remaining for original, remaining in zip(block_summary, block_sizes)]

# Function to calculate internal fragmentation (unused space within allocated blocks)
def calculate_internal_fragmentation(block_sizes, allocation, process_sizes):
    internal_frag = 0
    for i, block_index in enumerate(allocation):
        if block_index != -1:  # If the process is allocated to a block
            internal_frag += block_sizes[block_index]  # Add the remaining block space to internal fragmentation
    return internal_frag

# Function to calculate external fragmentation (unused space in unallocated blocks)
def calculate_external_fragmentation(block_sizes, allocation):
    external_frag = sum(block_sizes)  # Total space in all blocks
    return external_frag  # Return the total unused space

# Function to display results in the GUI
def display_results():
    # Parse block and process sizes from user input
    block_input = parse_input(block_entry.get())
    process_input = parse_input(process_entry.get())

    if block_input is None or process_input is None:
        return  # Return if there is an error in input

    # Create a copy of block sizes for further modification
    block_sizes = block_input.copy()
    allocation, block_summary = first_fit(block_sizes, process_input)  # Perform First Fit allocation

    # Summarize the block usage (used space) and calculate fragmentation
    process_summary = summarize_blocks(block_sizes, block_summary)
    internal_frag = calculate_internal_fragmentation(block_sizes, allocation, process_input)
    external_frag = calculate_external_fragmentation(block_sizes, allocation)

    # Update the Treeview for process allocation results
    result_tree.delete(*result_tree.get_children())  # Clear previous results
    for i, process in enumerate(process_input):
        result_tree.insert("", "end", values=(i + 1, process, allocation[i] + 1 if allocation[i] != -1 else "Not Allocated"))

    # Update the Treeview for block usage summary
    block_tree.delete(*block_tree.get_children())  # Clear previous block data
    for i, (original, used) in enumerate(zip(block_summary, process_summary)):
        block_tree.insert("", "end", values=(i + 1, original, used, block_sizes[i]))

    # Display the calculated fragmentation values
    fragmentation_label.config(text=f"Internal Fragmentation: {internal_frag} | External Fragmentation: {external_frag}")

# Function to clear all input fields and results
def clear_all():
    block_entry.delete(0, tk.END)
    process_entry.delete(0, tk.END)
    result_tree.delete(*result_tree.get_children())
    block_tree.delete(*block_tree.get_children())
    fragmentation_label.config(text="Internal Fragmentation: 0 | External Fragmentation: 0")

# Root window configuration
root = tk.Tk()
root.title("Memory Management - First Fit Algorithm")
root.geometry("800x600")
root.configure(bg="#1E2022")

# Configure styles for GUI elements
style = ttk.Style()
style.theme_use("clam")

# Treeview styles for result and block tables
style.configure(
    "Treeview",
    background="#4E9F3D",
    foreground="white",
    rowheight=25,
    fieldbackground="#1E5128",
    font=("Arial", 10),
)
style.map(
    "Treeview",
    background=[("selected", "#64C4ED")],
    foreground=[("selected", "black")],
)
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#FF6363", foreground="white")

# Button styles
style.configure("TButton", font=("Arial", 10), padding=5, background="#6A0572", foreground="white")

# Frame to hold block and process input fields
frame = tk.Frame(root, bg="#1E2022")
frame.pack(pady=10)

# Block size input field with label
tk.Label(frame, text="Block Sizes (comma-separated):", font=("Arial", 12), bg="#1E2022", fg="#EAEAEA").grid(row=0, column=0, padx=5, pady=5)
block_entry = tk.Entry(frame, width=35, font=("Arial", 12), bg="#2E2E2E", fg="white", insertbackground="white")
block_entry.grid(row=0, column=1, padx=5, pady=5)

# Process size input field with label
tk.Label(frame, text="Process Sizes (comma-separated):", font=("Arial", 12), bg="#1E2022", fg="#EAEAEA").grid(row=1, column=0, padx=5, pady=5)
process_entry = tk.Entry(frame, width=35, font=("Arial", 12), bg="#2E2E2E", fg="white", insertbackground="white")
process_entry.grid(row=1, column=1, padx=5, pady=5)

# Frame for buttons (Allocate Memory and Clear All)
button_frame = tk.Frame(root, bg="#1E2022")
button_frame.pack(pady=10)

# Allocate Memory button
ttk.Button(button_frame, text="Allocate Memory", command=display_results).pack(side=tk.LEFT, padx=5)

# Clear All button
ttk.Button(button_frame, text="Clear All", command=clear_all).pack(side=tk.LEFT, padx=5)

# Frame for process allocation result table
result_frame = tk.Frame(root, bg="#1E2022")
result_frame.pack(pady=10)

# Label for process allocation result
tk.Label(result_frame, text="Process Allocation Results", font=("Arial", 13, "bold"), bg="#1E2022", fg="#F2F2F2").pack()

# Treeview for displaying allocation results
result_tree = ttk.Treeview(result_frame, columns=("Process No", "Process Size", "Block No"), show="headings", height=5)
result_tree.heading("Process No", text="Process No")
result_tree.heading("Process Size", text="Process Size")
result_tree.heading("Block No", text="Block No")
result_tree.pack(side=tk.LEFT, padx=5)

# Scrollbar for process allocation result Treeview
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_tree.yview)
result_tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill="y")

# Frame for block usage summary table
block_frame = tk.Frame(root, bg="#1E2022")
block_frame.pack(pady=10)

# Label for block usage summary
tk.Label(block_frame, text="Block Usage Summary", font=("Arial", 13, "bold"), bg="#1E2022", fg="#F2F2F2").pack()

# Treeview for displaying block usage summary
block_tree = ttk.Treeview(block_frame, columns=("Block No", "Block Size", "Used Space", "Remaining Space"), show="headings", height=5)
block_tree.heading("Block No", text="Block No")
block_tree.heading("Block Size", text="Block Size")
block_tree.heading("Used Space", text="Used Space")
block_tree.heading("Remaining Space", text="Remaining Space")
block_tree.pack(side=tk.LEFT, padx=5)

# Scrollbar for block usage summary Treeview
block_scrollbar = ttk.Scrollbar(block_frame, orient="vertical", command=block_tree.yview)
block_tree.configure(yscrollcommand=block_scrollbar.set)
block_scrollbar.pack(side=tk.RIGHT, fill="y")

# Label for showing internal and external fragmentation
fragmentation_label = tk.Label(root, text="Internal Fragmentation: 0 | External Fragmentation: 0", font=("Arial", 12), bg="#1E2022", fg="#A9A9A9")
fragmentation_label.pack(pady=10)

# Start the GUI loop
root.mainloop()
