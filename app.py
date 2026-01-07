import tkinter as tk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import lineStyles

# Load CSV
df = pd.read_csv("strategy_users.csv")
participants = df["participant_id"].unique()
current_idx = 0
clicks = []
lines = []
results = []

# Tkinter window
window = tk.Tk()
window.geometry("900x700")
window.title("Strategy Label Program")


plot_frame = tk.Frame(window)
plot_frame.pack(fill=tk.BOTH, expand=True)

control_frame = tk.Frame(window)
control_frame.pack(fill=tk.X)

# --- Matplotlib figure embedded properly ---
fig = Figure(figsize=(8,5))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# --- Plot participant function ---
def plot_participant():
    global clicks, lines
    clicks = []
    lines = []
    ax.clear()

    pid = participants[current_idx]
    # Filter participant AND rotated trials
    pdat = df[(df["participant_id"] == pid) & (df["trial_type.x"] == "rotated")]

    # Make sure the trial number column exists
    ax.plot(pdat["cutrial_no"], pdat["aimdeviation_deg"], c="#94d6b5",  marker='o',linestyle="none")
    ax.set_title(f"Participant {pid} (rotated trials only)")
    ax.set_xlabel("Trial")
    ax.set_ylabel("Aim Deviation (deg)")
    ax.set_ylim([-20, 65])
    next_btn.config(state=tk.DISABLED)
    canvas.draw()


# --- Click handler ---
def on_click(event):
    global lines
    if event.xdata is None:
        return
    trial = int(round(event.xdata))
    clicks.append(trial)
    line = ax.axvline(trial, color="red")
    lines.append(line)
    canvas.draw()
    if len(clicks) == 2:
        next_btn.config(state=tk.NORMAL)

canvas.mpl_connect("button_press_event", on_click)

# --- Next button ---
def next_participant():
    global current_idx
    start, end = clicks
    results.append({
        "participant_id": participants[current_idx],
        "learning_start": start,
        "learning_end": end
    })
    if current_idx < len(participants) - 1:
        current_idx += 1
        plot_participant()
    else:
        print("All participants labeled")
        pd.DataFrame(results).to_csv(
            "/Users/elysa/Desktop/learning_labels.csv", index=False
        )
        window.quit()

# --- Reset button ---
def reset_clicks():
    global clicks, lines
    clicks = []
    for line in lines:
        line.remove()     # remove from axes
    lines = []
    next_btn.config(state=tk.DISABLED)
    canvas.draw()

# --- Buttons ---
next_btn = tk.Button(
    control_frame,
    text="Next Participant",
    command=next_participant,
    state=tk.DISABLED,
    font=("Arial", 12)
)
next_btn.pack(side=tk.RIGHT, padx=10, pady=10)

reset_btn = tk.Button(
    control_frame,
    text="Reset",
    command=reset_clicks,
    font=("Arial", 12)
)
reset_btn.pack(side=tk.LEFT, padx=10, pady=10)

def open_window():
    new_window = tk.Toplevel(window)
    new_window.title("Instructions")
    new_window.geometry("900x700")
    new_window.config(background="lightblue")

    tk.Label(new_window, text="Your job is to label learning onset and the timepoint at which aims become most stable").pack(pady=2)
    tk.Label(new_window,text="Onset = when aiming first deviations past 0 (and over 5 degrees").pack(pady=2)
    tk.Label(new_window, text="End = the point at which an aim is similar to the final trials").pack(pady=2)
    button = tk.Button(new_window, text="OK", command=new_window.destroy).pack(pady=10)

button = tk.Button(window, text="To Instructions", command=open_window).pack(pady=10)



# --- Initial plot ---
plot_participant()
window.mainloop()









