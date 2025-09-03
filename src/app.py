# src/app.py
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any
from storage import Storage
from search import matches, all_field_labels, sort_entries

class PixieVaultApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pixie Vault")
        self.root.geometry("1024x640")
        self.store = Storage()

        self._build_ui()
        self._refresh_field_labels()
        self._load_entries()

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
        center.pack(side="top", fill="both", expand=True, padx=10, pady=6)

        self.tree = ttk.Treeview(center, columns=("name","protocol","website","username","id","created","last_access"), show="headings", height=18)
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
        self.detail_text = tk.Text(detail, height=20, width=40)
        self.detail_text.pack(fill="y")

        # Bottom: actions
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
        self.detail_text.delete("1.0", "end")
        
        # Format timestamps
        created_date = datetime.datetime.fromtimestamp(e.get('created_at', 0)).strftime('%Y-%m-%d %H:%M:%S') if e.get('created_at') else 'N/A'
        last_access = datetime.datetime.fromtimestamp(e.get('last_access_at', 0)).strftime('%Y-%m-%d %H:%M:%S') if e.get('last_access_at') else 'Never'
        
        base = (
            f"Name: {e.get('name','')}\n"
            f"Protocol: {e.get('protocol','')}\n"
            f"Website: {e.get('website','')}\n"
            f"Username: {e.get('username','')}\n"
            f"Password: {e.get('password','')}\n"
            f"Notes: {e.get('notes','')}\n"
            f"ID: {e.get('id','')}\n"
            f"Created: {created_date}\n"
            f"Last Accessed: {last_access}\n"
        )
        self.detail_text.insert("end", base)
        if e.get("custom"):
            self.detail_text.insert("end", "\nCustom Fields:\n")
            for k, v in e["custom"].items():
                self.detail_text.insert("end", f"  - {k}: {v}\n")

    # --- Dialogs ---
    def _add_entry_dialog(self):
        base, custom = self._entry_form_dialog("Add Entry")
        if base is None: return
        self.store.add_entry(base, custom)
        self._refresh_field_labels()
        self._load_entries()

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
        self.store.update_entry(entry_id, base, custom)
        self._refresh_field_labels()
        self._load_entries()

    def _entry_form_dialog(self, title: str, entry: Dict[str,Any] | None = None):
        # Simple synchronous dialog with dynamic custom fields
        dlg = tk.Toplevel(self.root)
        dlg.title(title)
        dlg.transient(self.root)
        dlg.grab_set()

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
        for label_key, label_txt in [("name","Name"),("protocol","Protocol"),("website","Website"),("username","UN"),("password","Password"),("notes","Notes")]:
            ttk.Label(dlg, text=label_txt).grid(row=row, column=0, sticky="e", padx=6, pady=4)
            ent = ttk.Entry(dlg, width=40, show="*" if label_key=="password" else "")
            ent.grid(row=row, column=1, padx=6, pady=4)
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
        out = {"ok": False}
        def on_ok():
            out["ok"] = True
            dlg.destroy()
        ttk.Button(btns, text="Save", command=on_ok).pack(side="left", padx=6)
        ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=6)

        dlg.wait_window(dlg)
        if not out["ok"]:
            return (None, None)

        base = {k: w.get().strip() for k, w in widgets.items()}
        custom: Dict[str,Any] = {}
        for k_ent, v_ent, _ in custom_rows:
            k = k_ent.get().strip()
            v = v_ent.get().strip()
            if k:
                custom[k] = v
        return base, custom

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Delete", "Delete selected entry?"):
            self.store.delete_entry(sel[0])
            self._refresh_field_labels()
            self._load_entries()

if __name__ == "__main__":
    root = tk.Tk()
    app = PixieVaultApp(root)
    root.mainloop()
