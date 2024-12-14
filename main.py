import tkinter as tk
from tkinter import ttk, messagebox

def parse_input(input_str):
    try:
        return list(map(int, input_str.split(",")))
    except ValueError:
        messagebox.showerror("Error", "Please enter integers separated by commas.")
        return None

def first_fit(block_sizes, process_sizes):
    allocation = [-1] * len(process_sizes)
    block_summary = [block for block in block_sizes]

    for i, process in enumerate(process_sizes):
        for j, block in enumerate(block_sizes):
            if block >= process:
                allocation[i] = j
                block_sizes[j] -= process
                break

    return allocation, block_summary

def summarize_blocks(block_sizes, block_summary):
    return [original - remaining for original, remaining in zip(block_summary, block_sizes)]

def calculate_internal_fragmentation(block_sizes, allocation, process_sizes):
    """
    Calculate internal fragmentation as the unused space within allocated blocks.
    """
    internal_frag = 0
    for i, block_index in enumerate(allocation):
        if block_index != -1:  # Process is allocated to a block
            internal_frag += block_sizes[block_index]
    return internal_frag

def calculate_external_fragmentation(block_sizes, allocation):
    """
    Calculate external fragmentation as the total space of all unallocated blocks.
    """
    external_frag = sum(block_sizes)
    return external_frag

def display_results():
    block_input = parse_input(block_entry.get())
    process_input = parse_input(process_entry.get())

    if block_input is None or process_input is None:
        return

    block_sizes = block_input.copy()
    allocation, block_summary = first_fit(block_sizes, process_input)

    process_summary = summarize_blocks(block_sizes, block_summary)
    internal_frag = calculate_internal_fragmentation(block_sizes, allocation, process_input)
    external_frag = calculate_external_fragmentation(block_sizes, allocation)

    result_tree.delete(*result_tree.get_children())
    for i, process in enumerate(process_input):
        result_tree.insert("", "end", values=(i + 1, process, allocation[i] + 1 if allocation[i] != -1 else "Not Allocated"))

    block_tree.delete(*block_tree.get_children())
    for i, (original, used) in enumerate(zip(block_summary, process_summary)):
        block_tree.insert("", "end", values=(i + 1, original, used, block_sizes[i]))

    fragmentation_label.config(text=f"Internal Fragmentation: {internal_frag} | External Fragmentation: {external_frag}")

def clear_all():
    block_entry.delete(0, tk.END)
    process_entry.delete(0, tk.END)
    result_tree.delete(*result_tree.get_children())
    block_tree.delete(*block_tree.get_children())
    fragmentation_label.config(text="Internal Fragmentation: 0 | External Fragmentation: 0")

# Root configuration
root = tk.Tk()
root.title("Memory Management - First Fit Algorithm")
root.geometry("800x600")
root.configure(bg="#1E2022")

# Configure styles
style = ttk.Style()
style.theme_use("clam")

# Treeview styles
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

frame = tk.Frame(root, bg="#1E2022")
frame.pack(pady=10)

tk.Label(frame, text="Block Sizes (comma-separated):", font=("Arial", 12), bg="#1E2022", fg="#EAEAEA").grid(row=0, column=0, padx=5, pady=5)
block_entry = tk.Entry(frame, width=35, font=("Arial", 12), bg="#2E2E2E", fg="white", insertbackground="white")
block_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Process Sizes (comma-separated):", font=("Arial", 12), bg="#1E2022", fg="#EAEAEA").grid(row=1, column=0, padx=5, pady=5)
process_entry = tk.Entry(frame, width=35, font=("Arial", 12), bg="#2E2E2E", fg="white", insertbackground="white")
process_entry.grid(row=1, column=1, padx=5, pady=5)

button_frame = tk.Frame(root, bg="#1E2022")
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Allocate Memory", command=display_results).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Clear All", command=clear_all).pack(side=tk.LEFT, padx=5)

result_frame = tk.Frame(root, bg="#1E2022")
result_frame.pack(pady=10)

tk.Label(result_frame, text="Process Allocation Results", font=("Arial", 13, "bold"), bg="#1E2022", fg="#F2F2F2").pack()
result_tree = ttk.Treeview(result_frame, columns=("Process No", "Process Size", "Block No"), show="headings", height=5)
result_tree.heading("Process No", text="Process No")
result_tree.heading("Process Size", text="Process Size")
result_tree.heading("Block No", text="Block No")
result_tree.pack(side=tk.LEFT, padx=5)

scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_tree.yview)
result_tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill="y")

block_frame = tk.Frame(root, bg="#1E2022")
block_frame.pack(pady=10)

tk.Label(block_frame, text="Block Usage Summary", font=("Arial", 13, "bold"), bg="#1E2022", fg="#F2F2F2").pack()
block_tree = ttk.Treeview(block_frame, columns=("Block No", "Block Size", "Used Space", "Remaining Space"), show="headings", height=5)
block_tree.heading("Block No", text="Block No")
block_tree.heading("Block Size", text="Block Size")
block_tree.heading("Used Space", text="Used Space")
block_tree.heading("Remaining Space", text="Remaining Space")
block_tree.pack(side=tk.LEFT, padx=5)

block_scrollbar = ttk.Scrollbar(block_frame, orient="vertical", command=block_tree.yview)
block_tree.configure(yscrollcommand=block_scrollbar.set)
block_scrollbar.pack(side=tk.RIGHT, fill="y")

fragmentation_label = tk.Label(root, text="Internal Fragmentation: 0 | External Fragmentation: 0", font=("Arial", 12), bg="#1E2022", fg="#A9A9A9")
fragmentation_label.pack(pady=10)

root.mainloop()
