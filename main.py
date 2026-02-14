#!/usr/bin/env python3
import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

class OneDriveSanitizer:
    INVALID_CHARS = r'[<>:"/\\|?*]'
    RESERVED_NAMES = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 
                      'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 
                      'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    
    def __init__(self, root):
        self.root = root
        self.root.title("OneDrive File Sanitizer")
        self.root.geometry("900x600")
        self.issues = []
        self.setup_ui()
    
    def setup_ui(self):
        # Directory selection
        frame_top = ttk.Frame(self.root, padding="10")
        frame_top.pack(fill=tk.X)
        
        ttk.Label(frame_top, text="OneDrive Path:").pack(side=tk.LEFT)
        self.path_var = tk.StringVar()
        ttk.Entry(frame_top, textvariable=self.path_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="Browse", command=self.browse_dir).pack(side=tk.LEFT)
        ttk.Button(frame_top, text="Scan", command=self.scan_files).pack(side=tk.LEFT, padx=5)
        
        # Results tree
        frame_mid = ttk.Frame(self.root, padding="10")
        frame_mid.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_mid, text="Issues Found:").pack(anchor=tk.W)
        
        self.tree = ttk.Treeview(frame_mid, columns=("Original", "Fixed", "Issue"), show="headings")
        self.tree.heading("Original", text="Original Path")
        self.tree.heading("Fixed", text="Fixed Path")
        self.tree.heading("Issue", text="Issue Type")
        self.tree.column("Original", width=350)
        self.tree.column("Fixed", width=350)
        self.tree.column("Issue", width=150)
        
        scrollbar = ttk.Scrollbar(frame_mid, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        frame_bottom = ttk.Frame(self.root, padding="10")
        frame_bottom.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(frame_bottom, textvariable=self.status_var).pack(side=tk.LEFT)
        ttk.Button(frame_bottom, text="Fix All", command=self.fix_all).pack(side=tk.RIGHT)
    
    def browse_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
    
    def scan_files(self):
        path = self.path_var.get()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        self.issues = []
        self.tree.delete(*self.tree.get_children())
        self.status_var.set("Scanning...")
        self.root.update()
        
        for root, dirs, files in os.walk(path):
            for name in dirs + files:
                full_path = os.path.join(root, name)
                fixed_name = self.sanitize_name(name)
                
                if fixed_name != name:
                    issue_type = self.get_issue_type(name)
                    fixed_path = os.path.join(root, fixed_name)
                    self.issues.append((full_path, fixed_path))
                    self.tree.insert("", tk.END, values=(full_path, fixed_path, issue_type))
        
        self.status_var.set(f"Found {len(self.issues)} issues")
    
    def sanitize_name(self, name):
        # Remove invalid characters
        fixed = re.sub(self.INVALID_CHARS, '_', name)
        
        # Remove trailing spaces and periods
        fixed = fixed.rstrip('. ')
        
        # Handle reserved names
        name_part = os.path.splitext(fixed)[0].upper()
        if name_part in self.RESERVED_NAMES:
            fixed = '_' + fixed
        
        # Ensure not empty
        if not fixed:
            fixed = 'unnamed'
        
        return fixed
    
    def get_issue_type(self, name):
        issues = []
        if ':' in name:
            issues.append("NTFS stream")
        if re.search(self.INVALID_CHARS, name):
            issues.append("Invalid chars")
        if name.endswith((' ', '.')):
            issues.append("Trailing space/period")
        if os.path.splitext(name)[0].upper() in self.RESERVED_NAMES:
            issues.append("Reserved name")
        return ", ".join(issues)
    
    def fix_all(self):
        if not self.issues:
            messagebox.showinfo("Info", "No issues to fix")
            return
        
        if not messagebox.askyesno("Confirm", f"Fix {len(self.issues)} files/folders?"):
            return
        
        fixed_count = 0
        errors = []
        
        # Sort by depth (deepest first) to avoid parent/child conflicts
        sorted_issues = sorted(self.issues, key=lambda x: x[0].count(os.sep), reverse=True)
        
        for old_path, new_path in sorted_issues:
            try:
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    fixed_count += 1
            except Exception as e:
                errors.append(f"{old_path}: {str(e)}")
        
        if errors:
            messagebox.showwarning("Completed with errors", 
                                   f"Fixed {fixed_count} items\nErrors: {len(errors)}\n\n" + "\n".join(errors[:5]))
        else:
            messagebox.showinfo("Success", f"Fixed {fixed_count} items")
        
        self.scan_files()

if __name__ == "__main__":
    root = tk.Tk()
    app = OneDriveSanitizer(root)
    root.mainloop()
