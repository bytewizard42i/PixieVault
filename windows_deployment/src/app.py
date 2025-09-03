# src/app.py
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List, Tuple
import os
from PIL import Image, ImageTk
from storage import Storage
from search import matches, all_field_labels, sort_entries

class PixieVaultApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("✨ Pixie Vault")
        self.root.geometry("1024x640")
        self.store = Storage()
        
        # Touch-first sizing
        self.root.tk.call('tk', 'scaling', 1.3)
        self.root.option_add('*Font', '{DejaVu Sans} 14')
        
        # Light theme styling
        self._setup_theme()
        
        # Build UI first
        self._build_ui()

        self._load_entries()
        self._refresh_field_labels()
        
        # Cleanup video on window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_theme(self):
        style = ttk.Style(self.root)
        
        # Keep default light theme but with touch-friendly row height
        style.configure("Treeview", rowheight=34)

    # --- UI ---
    def _build_ui(self):
        # Top: Search bar + field filter + sort
        top = ttk.Frame(self.root)
        top.pack(side="top", fill="x", padx=10, pady=6)

        ttk.Label(top, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top, textvariable=self.search_var, width=40)
        self.search_entry.pack(side="left", padx=6)
        self.search_entry.bind("<Return>", lambda e: self._load_entries())

        self.field_var = tk.StringVar(value="Any")
        self.field_combo = ttk.Combobox(top, textvariable=self.field_var, state="readonly", width=24)
        self.field_combo.pack(side="left", padx=6)

        self.sort_var = tk.StringVar(value="A→Z")
        self.sort_combo = ttk.Combobox(top, textvariable=self.sort_var, state="readonly", width=20,
                                       values=["A→Z","Recently Added","Recently Updated","Most Used"])
        self.sort_combo.pack(side="left", padx=6)

        ttk.Button(top, text="Search", command=self._load_entries).pack(side="left", padx=6)

        # Center: Tree list + details
        center = ttk.Frame(self.root)
        center.pack(side="top", fill="x", padx=10, pady=6)

        self.tree = ttk.Treeview(center, columns=("name","protocol","website","username","id","created","last_access"), show="headings", height=12)
        for col, label, width in [("name","Name",140), ("protocol","Protocol",80), ("website","Website",180), ("username","UN",120), ("id","ID",80), ("created","Created",120), ("last_access","Last Access",120)]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        scrollbar = ttk.Scrollbar(center, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Right: detail panel
        detail = ttk.Frame(center, width=320)
        detail.pack(side="left", fill="y", padx=10)
        
        # Password visibility toggle
        pwd_frame = ttk.Frame(detail)
        pwd_frame.pack(fill="x", pady=(0, 5))
        self.show_passwords = tk.BooleanVar(value=False)
        ttk.Checkbutton(pwd_frame, text="Show Passwords", variable=self.show_passwords, 
                       command=self._refresh_detail_display).pack(side="left")
        ttk.Label(detail, text="Entry Details", font=("DejaVu Sans", 12, "bold")).pack(anchor="w", pady=(0,6))
        
        self.detail_text = tk.Text(detail, height=12, wrap="word", font=("DejaVu Sans", 10))
        self.detail_text.pack(fill="both", expand=True)
        
        # Bottom image area
        self._add_pixie_image(detail)

        # Status bar
        status_bar = ttk.Frame(self.root)
        status_bar.pack(side="bottom", fill="x", padx=10, pady=2)
        
        self.status_left = ttk.Label(status_bar, text="0 entries")
        self.status_left.pack(side="left")
        
        self.status_right = ttk.Label(status_bar, text="")
        self.status_right.pack(side="right")

        # Bottom: actions (pack last so they appear at very bottom)
        bottom = ttk.Frame(self.root)
        bottom.pack(side="bottom", fill="x", padx=10, pady=8)

        ttk.Button(bottom, text="Add Entry", command=self._add_entry_dialog).pack(side="left", padx=5)
        ttk.Button(bottom, text="Edit Entry", command=self._edit_entry_dialog).pack(side="left", padx=5)
        ttk.Button(bottom, text="Delete", command=self._delete_selected).pack(side="left", padx=5)
        ttk.Button(bottom, text="Refresh", command=self._load_entries).pack(side="left", padx=5)

    def _refresh_field_labels(self):
        labels = ["Any"] + all_field_labels(self.store.all_entries())
        self.field_combo["values"] = labels
        if self.field_var.get() not in labels:
            self.field_var.set("Any")

    def _load_entries(self):
        term = self.search_var.get().strip()
        field = self.field_var.get()
        sort_mode = self.sort_var.get()

        entries = self.store.all_entries()
        if term:
            entries = [e for e in entries if matches(e, term, None if field == "Any" else field)]
        entries = sort_entries(entries, sort_mode)

        self.tree.delete(*self.tree.get_children())
        
        if not entries and term:
            # Empty state message
            self.status_left.config(text="No matches found ✨ — try 'Any' field or clear filters")
        else:
            # Update status bar
            count = len(entries)
            filter_text = f" (filtered)" if term else ""
            self.status_left.config(text=f"{count} entries{filter_text}")
        
        # Update time
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.status_right.config(text=current_time)
        
        for e in entries:
            created_short = datetime.datetime.fromtimestamp(e.get('created_at', 0)).strftime('%m/%d/%y') if e.get('created_at') else 'N/A'
            last_access_short = datetime.datetime.fromtimestamp(e.get('last_access_at', 0)).strftime('%m/%d/%y') if e.get('last_access_at') else 'Never'
            
            self.tree.insert("", "end", iid=e["id"], values=(
                e.get("name",""),
                e.get("protocol",""),
                e.get("website",""),
                e.get("username",""),
                e.get("id","")[:8] + "...",  # Truncated ID
                created_short,
                last_access_short
            ))
        self.detail_text.delete("1.0", "end")

    def _on_select(self, _evt=None):
        sel = self.tree.selection()
        if not sel: return
        entry_id = sel[0]
        entry = next((x for x in self.store.all_entries() if x["id"] == entry_id), None)
        if not entry: return
        self.store.record_access(entry_id)
        self._show_details(entry)

    def _show_details(self, e: Dict[str,Any]):
        self.current_entry = e  # Store for refresh
        self._refresh_detail_display()
    
    def _refresh_detail_display(self):
        if not hasattr(self, 'current_entry') or not self.current_entry:
            return
            
        e = self.current_entry
        self.detail_text.config(state="normal")
        self.detail_text.delete("1.0", "end")
        
        # Format timestamps
        created_date = datetime.datetime.fromtimestamp(e.get('created_at', 0)).strftime('%Y-%m-%d %H:%M:%S') if e.get('created_at') else 'N/A'
        last_access = datetime.datetime.fromtimestamp(e.get('last_access_at', 0)).strftime('%Y-%m-%d %H:%M:%S') if e.get('last_access_at') else 'Never'
        
        # Show or hide password based on toggle
        password_display = e.get('password','') if self.show_passwords.get() else '•' * len(e.get('password',''))
        
        base = (
            f"Name: {e.get('name','')}\n"
            f"Protocol: {e.get('protocol','')}\n"
            f"Website: {e.get('website','')}\n"
            f"Username: {e.get('username','')}\n"
            f"Password: {password_display}\n"
            f"Notes: {e.get('notes','')}\n"
            f"ID: {e.get('id','')}\n"
            f"Created: {created_date}\n"
            f"Last Accessed: {last_access}\n"
        )
        self.detail_text.config(state="normal")
        self.detail_text.insert("end", base)
        if e.get("custom"):
            self.detail_text.insert("end", "\nCustom Fields:\n")
            for k, v in e["custom"].items():
                self.detail_text.insert("end", f"  - {k}: {v}\n")
        self.detail_text.config(state="disabled")

    # --- Dialogs ---
    def _add_entry_dialog(self):
        base, custom = self._entry_form_dialog("Add Entry")
        print(f"DEBUG: Dialog returned base={base}, custom={custom}")
        if base is None: 
            print("DEBUG: Dialog was cancelled")
            return
        
        # Validation
        if not base.get("name", "").strip():
            print("DEBUG: Name validation failed")
            messagebox.showerror("Validation Error", "Name is required.")
            return
        
        # Password confirmation validation
        password = base.get("password", "")
        password_confirm = base.get("password_confirm", "")
        print(f"DEBUG: password='{password}', confirm='{password_confirm}'")
        if password and password != password_confirm:
            print("DEBUG: Password confirmation failed")
            messagebox.showerror("Validation Error", "Passwords do not match.")
            return
        
        print("DEBUG: About to save entry")
        self.store.add_entry(base, custom)
        print("DEBUG: Entry saved, refreshing UI")
        self._refresh_field_labels()
        self._load_entries()
        print("DEBUG: Showing success message")
        messagebox.showinfo("Success", "Entry saved ✨")

    def _edit_entry_dialog(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Edit", "Select an entry to edit.")
            return
        entry_id = sel[0]
        entry = next((x for x in self.store.all_entries() if x["id"] == entry_id), None)
        if not entry: return
        base, custom = self._entry_form_dialog("Edit Entry", entry)
        if base is None: return
        
        # Validation
        if not base.get("name", "").strip():
            messagebox.showerror("Validation Error", "Name is required.")
            return
        if not base.get("password", "").strip():
            messagebox.showerror("Validation Error", "Password is required.")
            return
        if len(base.get("password", "")) < 3:
            messagebox.showwarning("Validation Warning", "Password should be at least 3 characters long.")
        
        self.store.update_entry(entry_id, base, custom)
        self._refresh_field_labels()
        self._load_entries()
        messagebox.showinfo("Success", "Entry updated ✨")

    def _entry_form_dialog(self, title: str, entry: Dict[str,Any] | None = None):
        # Simple synchronous dialog with dynamic custom fields
        dlg = tk.Toplevel(self.root)
        dlg.title(title)
        # Don't use transient or grab_set - they prevent maximize/minimize
        
        # Center the dialog and enable maximize
        dlg.geometry("400x450")
        dlg.resizable(True, True)
        dlg.focus_set()
        
        # Result storage
        result = {"base": None, "custom": None}

        vals = {
            "name": (entry or {}).get("name",""),
            "protocol": (entry or {}).get("protocol",""),
            "website": (entry or {}).get("website",""),
            "username": (entry or {}).get("username",""),
            "password": (entry or {}).get("password",""),
            "notes": (entry or {}).get("notes","")
        }
        row = 0
        widgets: Dict[str, tk.Entry] = {}
        # Password visibility toggle for dialog
        dialog_show_password = tk.BooleanVar(value=False)
        
        for label_key, label_txt in [("name","Name"),("protocol","Protocol"),("website","Website"),("username","UN"),("password","Password"),("notes","Notes")]:
            ttk.Label(dlg, text=label_txt).grid(row=row, column=0, sticky="e", padx=6, pady=4)
            
            if label_key == "password":
                # Password field - no obfuscation
                ent = ttk.Entry(dlg, width=20)
                ent.grid(row=row, column=1, padx=6, pady=4, sticky="w")
                ent.insert(0, vals[label_key])
                widgets[label_key] = ent
                row += 1
                
                # Password confirmation field - no obfuscation
                ttk.Label(dlg, text="Confirm").grid(row=row, column=0, sticky="e", padx=6, pady=4)
                confirm_ent = ttk.Entry(dlg, width=20)
                confirm_ent.grid(row=row, column=1, padx=6, pady=4, sticky="w")
                widgets["password_confirm"] = confirm_ent
            else:
                ent = ttk.Entry(dlg, width=20)
                ent.grid(row=row, column=1, padx=6, pady=4, sticky="w")
                ent.insert(0, vals[label_key])
                widgets[label_key] = ent
            
            row += 1

        # Custom fields block
        ttk.Separator(dlg).grid(row=row, column=0, columnspan=2, sticky="ew", pady=6); row += 1
        ttk.Label(dlg, text="Custom fields").grid(row=row, column=0, columnspan=2, pady=4); row += 1

        custom_rows: list[tuple[tk.Entry, tk.Entry, ttk.Button]] = []

        def add_custom_row(k_init="", v_init=""):
            nonlocal row
            key_ent = ttk.Entry(dlg, width=20)
            val_ent = ttk.Entry(dlg, width=30)
            
            def remove_this_row():
                nonlocal custom_rows
                # Find and remove this row from custom_rows
                for i, (k_e, v_e, btn) in enumerate(custom_rows):
                    if k_e == key_ent:
                        # Destroy widgets
                        k_e.destroy()
                        v_e.destroy()
                        btn.destroy()
                        # Remove from list
                        custom_rows.pop(i)
                        break
            
            remove_btn = ttk.Button(dlg, text="×", width=3, command=remove_this_row)
            
            key_ent.grid(row=row, column=0, padx=6, pady=2, sticky="e")
            val_ent.grid(row=row, column=1, padx=6, pady=2, sticky="w")
            remove_btn.grid(row=row, column=2, padx=2, pady=2)
            
            key_ent.insert(0, k_init)
            val_ent.insert(0, v_init)
            custom_rows.append((key_ent, val_ent, remove_btn))
            row += 1

        # preload existing custom
        for k, v in ((entry or {}).get("custom") or {}).items():
            add_custom_row(k, v)

        # add-row button
        ttk.Button(dlg, text="Add field", command=lambda: add_custom_row()).grid(row=row, column=0, columnspan=3, pady=6); row += 1

        # Save/Cancel
        btns = ttk.Frame(dlg); btns.grid(row=row, column=0, columnspan=2, pady=8)
        
        def on_save():
            # Collect data before destroying dialog
            base = {}
            for k, w in widgets.items():
                if k != "password_confirm":
                    base[k] = w.get().strip()
                    
            # Add password_confirm for validation but don't save it
            base["password_confirm"] = widgets.get("password_confirm", tk.Entry()).get()
            
            custom: Dict[str,Any] = {}
            for k_ent, v_ent, _ in custom_rows:
                k = k_ent.get().strip()
                v = v_ent.get().strip()
                if k:
                    custom[k] = v
            result["base"] = base
            result["custom"] = custom
            dlg.destroy()
            
        def on_cancel():
            result["base"] = None
            result["custom"] = None
            dlg.destroy()
            
        ttk.Button(btns, text="Save", command=on_save).pack(side="left", padx=6)
        ttk.Button(btns, text="Cancel", command=on_cancel).pack(side="left", padx=6)

        dlg.wait_window(dlg)
        return result["base"], result["custom"]


    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Delete", "Delete selected entry?"):
            self.store.delete_entry(sel[0])
            self._refresh_field_labels()
            self._load_entries()
    

    def _add_pixie_image(self, parent):
        """Add pixie image to bottom of detail panel"""
        try:
            # Image frame at bottom
            img_frame = ttk.Frame(parent, height=180)
            img_frame.pack(side="bottom", fill="x", pady=(10, 0))
            img_frame.pack_propagate(False)
            
            # Load and resize image
            img_path = os.path.join(os.path.dirname(__file__), "..", "media", "pixie-alices_pet.png")
            if os.path.exists(img_path):
                image = Image.open(img_path)
                # Resize to fit in bottom area (max height 160px)
                image.thumbnail((500, 160), Image.Resampling.LANCZOS)
                self.pixie_photo = ImageTk.PhotoImage(image)
                
                # Display image
                img_label = ttk.Label(img_frame, image=self.pixie_photo)
                img_label.pack(expand=True)
            else:
                # Fallback if image not found
                ttk.Label(img_frame, text="🧚‍♀️ Pixie image not found", 
                         font=("DejaVu Sans", 10)).pack(expand=True)
                
        except Exception as e:
            # Fallback for any image loading errors
            ttk.Label(parent, text=f"🧚‍♀️ Image error: {e}", 
                     font=("DejaVu Sans", 8)).pack(side="bottom", pady=5)

    def _on_closing(self):
        """Clean up before closing"""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PixieVaultApp(root)
    root.mainloop()
