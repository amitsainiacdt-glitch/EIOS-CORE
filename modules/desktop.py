import tkinter as tk

window = tk.Tk()

window.title("EIOS - Everest Investment Operating System")
window.geometry("800x500")

title = tk.Label(
    window,
    text="EIOS\nEverest Investment Operating System",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)

def company_registry():
    new_window = tk.Toplevel(window)
    new_window.title("Company Registry")
    new_window.geometry("500x400")

    tk.Label(
        new_window,
        text="EIOS Company Registry",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Button(new_window, text="ANUP Engineering", width=30).pack(pady=5)
    tk.Button(new_window, text="KPIT Technologies", width=30).pack(pady=5)
    tk.Button(new_window, text="Coromandel International", width=30).pack(pady=5
                                                                          tk.Button(
    window,
    text="Company Registry",
    width=30,
    command=company_registry
).pack(pady=10)

tk.Button(window, text="Research Engine", width=30).pack(pady=10)
tk.Button(window, text="Portfolio", width=30).pack(pady=10)
tk.Button(window, text="Exit", width=30, command=window.destroy).pack(pady=20)

window.mainloop()