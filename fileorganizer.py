import os
import shutil
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

# Automatically get system folders
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
documents_folder = os.path.join(os.path.expanduser("~"), "Documents")



def get_file_hash(file_path):
    try:
        return hashlib.file_digest(open(file_path, 'rb'), 'sha256').hexdigest()
    except (PermissionError, OSError) as e:
        return None

def organize_files():
    source_dir = filedialog.askdirectory(title="Select Source Folder") or downloads_folder
    dest_dir = filedialog.askdirectory(title="Select Destination Folder") or documents_folder

    if not os.path.exists(source_dir):
        messagebox.showerror("Error", "Source folder does not exist!")
        return

    file_types = {
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
        "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executables": [".exe", ".msi", ".bat", ".sh", ".apk"],
        "Code Files": [".py", ".java", ".c", ".cpp", ".html", ".css", ".js", ".php", ".json", ".xml"],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
        "CAD Files": [".dwg", ".dxf", ".stl"],
        "Others": []
    }

    moved_count = 0
    error_count = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[-1].lower()
                moved = False

                for category, extensions in file_types.items():
                    if file_ext in extensions:
                        category_dir = os.path.join(dest_dir, category)
                        os.makedirs(category_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(category_dir, file))
                        log_message(f"Moved: {file} -> {category}")
                        moved = True
                        moved_count += 1
                        break

                if not moved:
                    other_dir = os.path.join(dest_dir, "Others")
                    os.makedirs(other_dir, exist_ok=True)
                    shutil.move(file_path, os.path.join(other_dir, file))
                    log_message(f"Moved: {file} -> Others")
                    moved_count += 1
                    
            except (PermissionError, OSError, shutil.Error) as e:
                log_message(f"Error processing {file}: {str(e)}")
                error_count += 1
                continue

    messagebox.showinfo("Complete", 
                       f"Operation completed!\nFiles moved: {moved_count}\nErrors encountered: {error_count}")

def remove_duplicates():
    source_dir = filedialog.askdirectory(title="Select Folder to Scan for Duplicates") or downloads_folder
    if not source_dir:
        messagebox.showwarning("Warning", "Please select a folder!")
        return

    seen_hashes = {}
    deleted_count = 0
    error_count = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                
                if file_hash is None:
                    error_count += 1
                    continue
                    
                if file_hash in seen_hashes:
                    os.remove(file_path)
                    log_message(f"Deleted Duplicate: {file}")
                    deleted_count += 1
                else:
                    seen_hashes[file_hash] = file_path
                    
            except (PermissionError, OSError) as e:
                log_message(f"Error processing {file}: {str(e)}")
                error_count += 1
                continue

    messagebox.showinfo("Complete", 
                       f"Removed {deleted_count} duplicate files!\nErrors encountered: {error_count}")

def rename_files():
    source_dir = filedialog.askdirectory(title="Select Folder to Rename Files") or downloads_folder
    if not source_dir:
        messagebox.showwarning("Warning", "Please select a folder!")
        return

    renamed_count = 0
    error_count = 0

    for index, file in enumerate(os.listdir(source_dir), start=1):
        try:
            file_path = os.path.join(source_dir, file)
            if os.path.isfile(file_path):
                name, ext = os.path.splitext(file)
                new_name = f"file_{index:03d}{ext}"
                new_path = os.path.join(source_dir, new_name)
                os.rename(file_path, new_path)
                log_message(f"Renamed: {file} -> {new_name}")
                renamed_count += 1
                
        except (PermissionError, OSError) as e:
            log_message(f"Error renaming {file}: {str(e)}")
            error_count += 1
            continue

    messagebox.showinfo("Complete", 
                       f"Renamed {renamed_count} files!\nErrors encountered: {error_count}")

def log_message(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)
    log_box.update()

# GUI Setup
root = tk.Tk()
root.title("Advanced File Organizer")
root.geometry("600x550")
root.configure(bg="#34495E")

frame = tk.Frame(root, bg="#34495E")
frame.pack(pady=20)

title_label = tk.Label(frame, text="Advanced File Organizer", font=("Arial", 16, "bold"), fg="#ECF0F1", bg="#34495E")
title_label.pack()

buttons = [
    ("Organize Files", organize_files, "#3498DB"),
    ("Remove Duplicates", remove_duplicates, "#E74C3C"),
    ("Rename Files in Bulk", rename_files, "#2ECC71")
]

for text, command, color in buttons:
    tk.Button(frame, text=text, command=command, font=("Arial", 12), bg=color, fg="white", activebackground=color, relief=tk.RAISED, bd=3).pack(pady=5)

log_box = tk.Text(root, height=15, width=70, bg="#ECF0F1", fg="#2C3E50", font=("Arial", 10))
log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
