import os
import re
import tkinter as tk
from tkinter import messagebox, filedialog

# === DEFAULT FOLDER STRUCTURE ===
default_structure = [
    "{first}/{second}",
    "{first}/{second}/backup",
    "{first}/{second}/cache/bake_masks/bake_masks",
    "{first}/{second}/cache/bake_spectra/bake_spectra",
    "{first}/{second}/cache/compressed_cache/compressed_cache",
    "{first}/{second}/cache/filecache1/filecache1",
    "{first}/{second}/cache/HQ_SPECTRUM/HQ_SPECTRUM",
    "{first}/{second}/cache/oceanFoam/oceanFoam",
    "{first}/{second}/cache/SS_anim/waveTankPrecache",
    "{first}/{second}/cache/surface_cache/surface_cache",
    "{first}/{second}/cache/surface_extended/surface_extended",
    "{first}/{second}/cache/waveTankPrecache/waveTankPrecache",
    "{first}/{second}/playblasts",
    "{first}/{second}/USD",
]

# === HELPER FUNCTIONS ===
def expand_range(spec: str):
    """Expand strings like '001,003-005' into ['001', '003', '004', '005']."""
    parts = []
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if "-" in item:
            start, end = item.split("-")
            for i in range(int(start), int(end) + 1):
                parts.append(f"{i:03d}")
        else:
            parts.append(f"{int(item):03d}")
    return parts


def create_project_structure(base_dir, spec, structure):
    """
    Create folders based on project spec and a custom structure list.
    spec format: XX/001,002/001-005
    """
    match = re.match(r"([A-Z]{2})/([^/]+)/([^/]+)", spec, re.IGNORECASE)
    if not match:
        raise ValueError("Invalid format. Use XX/x,y-z/a,b-c")

    project_code = match.group(1).upper()
    first_set = expand_range(match.group(2))
    second_set = expand_range(match.group(3))

    created = []
    for first in first_set:
        for second in second_set:
            for f in structure:
                path = os.path.join(base_dir, project_code, f.format(first=first, second=second))
                os.makedirs(path, exist_ok=True)
            created.append(f"{project_code}/{first}/{second}")
    return created


# === GUI ===
def run_gui():
    root = tk.Tk()
    root.title("Project Folder Generator")
    root.geometry("600x500")
    root.resizable(False, False)

    # --- Variables ---
    base_dir_var = tk.StringVar()
    spec_var = tk.StringVar(value="CE/001,002/001-005")

    # --- Browse Base Directory ---
    def browse_dir():
        folder = filedialog.askdirectory(title="Select Base Directory")
        if folder:
            base_dir_var.set(folder)

    # --- Create Folders ---
    def create_folders():
        base_dir = base_dir_var.get().strip()
        spec = spec_var.get().strip()
        structure_text = structure_box.get("1.0", tk.END).strip().splitlines()

        if not base_dir or not spec:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            created = create_project_structure(base_dir, spec, structure_text)
            log_box.delete("1.0", tk.END)
            log_box.insert(tk.END, f"Created {len(created)} folder sets:\n\n")
            for c in created:
                log_box.insert(tk.END, f"✅ {c}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- Widgets ---
    tk.Label(root, text="Base Directory:", font=("Segoe UI", 10)).pack(pady=(10, 0))
    base_dir_frame = tk.Frame(root)
    base_dir_frame.pack(pady=5)
    tk.Entry(base_dir_frame, textvariable=base_dir_var, width=50).pack(side=tk.LEFT, padx=5)
    tk.Button(base_dir_frame, text="Browse", command=browse_dir).pack(side=tk.LEFT)

    tk.Label(root, text="Folder Spec (e.g., CE/001,002/001-005):", font=("Segoe UI", 10)).pack(pady=(10, 0))
    tk.Entry(root, textvariable=spec_var, width=55).pack(pady=5)

    tk.Label(root, text="Folder Structure (editable):", font=("Segoe UI", 10)).pack(pady=(10, 0))
    structure_box = tk.Text(root, height=10, width=70, bg="#f4f4f4")
    structure_box.pack(padx=10, pady=(0,10))
    # Populate with default structure
    structure_box.insert(tk.END, "\n".join(default_structure))

    tk.Button(root, text="Create Folders", command=create_folders, bg="#4CAF50", fg="white").pack(pady=10)

    tk.Label(root, text="Log:", font=("Segoe UI", 10)).pack(anchor="w", padx=10)
    log_box = tk.Text(root, height=8, width=70, bg="#f4f4f4")
    log_box.pack(padx=10, pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    run_gui()
