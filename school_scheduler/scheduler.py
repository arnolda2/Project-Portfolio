import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CollegeScheduler(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Scheduler")
        self.geometry("1400x800")  # Increased window size

        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Frames for Tabs
        self.scheduler_frame = ttk.Frame(self.notebook)
        self.analytics_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.scheduler_frame, text='Scheduler')
        self.notebook.add(self.analytics_frame, text='Analytics')

        self.events = {}  # Dictionary to store events
        self.tasks = []   # List to store tasks
        self.completed_tasks = []  # List to store completed tasks

        self.create_scheduler()
        self.create_analytics()

    # ---------------------- Scheduler Tab ---------------------- #
    def create_scheduler(self):
        # Create PanedWindow
        paned_window = ttk.PanedWindow(self.scheduler_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Left Frame for Calendar
        self.calendar_frame = ttk.Frame(paned_window, relief=tk.SUNKEN)
        paned_window.add(self.calendar_frame, weight=3)

        # Right Frame for To-Do List
        self.todo_frame = ttk.Frame(paned_window, width=300, relief=tk.SUNKEN)
        paned_window.add(self.todo_frame, weight=2)

        self.create_calendar()
        self.create_todo_list()

    def create_calendar(self):
        ttk.Label(self.calendar_frame, text="Calendar", font=("Helvetica", 24)).pack(pady=10)

        self.calendar = Calendar(
            self.calendar_frame,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            firstweekday='sunday',
            showweeknumbers=False,
            font=("Helvetica", 16),  # Increased font size
            headersforeground='black',
            headersbackground='lightgrey',
            borderwidth=2,
            relief='ridge',
            disableddaybackground='white',
            weekendforeground='red',
            weekendbackground='white',
            othermonthweforeground='red',
            othermonthwebackground='white',
            othermonthforeground='grey',
            othermonthbackground='white',
            selectforeground='white',
            selectbackground='blue',
            foreground='black',
            background='white',
            cursor="hand1"
        )
        self.calendar.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Expand the calendar frame
        self.calendar_frame.pack_propagate(False)
        self.calendar_frame.config(width=800, height=600)  # Adjusted size

        # Bind the date selection event
        self.calendar.bind("<<CalendarSelected>>", self.show_events_for_selected_date)

        # Frame for adding events
        event_frame = ttk.LabelFrame(self.calendar_frame, text="Add Event")
        event_frame.pack(pady=10, fill=tk.X, padx=20)

        ttk.Label(event_frame, text="Event Title:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.event_title_entry = ttk.Entry(event_frame, width=30)
        self.event_title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(event_frame, text="Event Date:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.event_date_entry = DateEntry(event_frame, date_pattern='yyyy-mm-dd')
        self.event_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(event_frame, text="Event Type:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.event_type = tk.StringVar()
        event_types = ['Exam', 'Club Event', 'Meeting', 'Job Hunting', 'Homework', 'Other']
        self.event_type_combo = ttk.Combobox(event_frame, textvariable=self.event_type, values=event_types, state='readonly')
        self.event_type_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(event_frame, text="Recurring:", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.event_recur = tk.StringVar()
        recur_options = ['None', 'Daily', 'Weekly', 'Monthly']
        self.event_recur_combo = ttk.Combobox(event_frame, textvariable=self.event_recur, values=recur_options, state='readonly')
        self.event_recur_combo.set('None')
        self.event_recur_combo.grid(row=3, column=1, padx=5, pady=5)

        add_event_btn = ttk.Button(event_frame, text="Add Event", command=self.add_event)
        add_event_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Frame for displaying events on selected date
        self.events_display_frame = ttk.LabelFrame(self.calendar_frame, text="Events on Selected Date")
        self.events_display_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        # Search Bar
        search_frame = ttk.Frame(self.events_display_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.event_search_var = tk.StringVar()
        self.event_search_var.trace('w', self.update_event_list)
        self.event_search_entry = ttk.Entry(search_frame, textvariable=self.event_search_var)
        self.event_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Filter by Event Type
        ttk.Label(search_frame, text="Filter by Type:").pack(side=tk.LEFT, padx=5)
        self.event_filter_var = tk.StringVar()
        self.event_filter_var.set('All')
        event_filter_options = ['All'] + event_types
        self.event_filter_combo = ttk.Combobox(search_frame, textvariable=self.event_filter_var, values=event_filter_options, state='readonly')
        self.event_filter_combo.bind("<<ComboboxSelected>>", self.update_event_list)
        self.event_filter_combo.pack(side=tk.LEFT, padx=5)

        self.events_listbox = tk.Listbox(self.events_display_frame, font=("Helvetica", 12))
        self.events_listbox.pack(fill=tk.BOTH, expand=True)

    def add_event(self):
        event_title = self.event_title_entry.get()
        event_type = self.event_type.get()
        event_date = self.event_date_entry.get_date()
        recur_pattern = self.event_recur.get()

        if event_title and event_type:
            dates = [event_date]
            if recur_pattern != 'None':
                dates = self.generate_recurring_dates(event_date, recur_pattern)

            for event_date in dates:
                event_info = {'type': event_type, 'title': event_title}
                if event_date in self.events:
                    self.events[event_date].append(event_info)
                else:
                    self.events[event_date] = [event_info]

            self.event_title_entry.delete(0, tk.END)
            self.event_type_combo.set('')
            self.event_recur_combo.set('None')
            self.event_date_entry.set_date(datetime.date.today())

            messagebox.showinfo("Event Added", f"Event '{event_title}' added.")
        else:
            messagebox.showwarning("Input Error", "Please enter both event title and type.")

        self.calendar.calevent_remove('all')
        self.display_events()
        self.show_events_for_selected_date()

    def generate_recurring_dates(self, start_date, pattern):
        dates = []
        current_date = start_date
        end_date = start_date + datetime.timedelta(days=365)
        while current_date <= end_date:
            dates.append(current_date)
            if pattern == 'Daily':
                current_date += datetime.timedelta(days=1)
            elif pattern == 'Weekly':
                current_date += datetime.timedelta(weeks=1)
            elif pattern == 'Monthly':
                month = current_date.month + 1 if current_date.month < 12 else 1
                year = current_date.year + 1 if current_date.month == 12 else current_date.year
                day = min(current_date.day, 28)  # To handle February
                current_date = datetime.date(year, month, day)
            else:
                break
        return dates

    def display_events(self):
        # Highlight dates with events
        self.calendar.calevent_remove('all')
        for date, events in self.events.items():
            for event in events:
                color = self.get_event_color(event['type'])
                self.calendar.calevent_create(date, '', tags=date)
                self.calendar.tag_config(date, background=color)

    def get_event_color(self, event_type):
        color_map = {
            'Exam': 'red',
            'Club Event': 'green',
            'Meeting': 'blue',
            'Job Hunting': 'orange',
            'Homework': 'purple',
            'Other': 'grey'
        }
        return color_map.get(event_type, 'lightblue')

    def show_events_for_selected_date(self, event=None):
        self.update_event_list()

    def update_event_list(self, *args):
        # Clear the listbox
        self.events_listbox.delete(0, tk.END)

        date = self.calendar.selection_get()
        events = self.events.get(date, [])

        search_query = self.event_search_var.get().lower()
        filter_type = self.event_filter_var.get()

        filtered_events = []
        for event_info in events:
            if search_query in event_info['title'].lower():
                if filter_type == 'All' or filter_type == event_info['type']:
                    filtered_events.append(event_info)

        if filtered_events:
            for event_info in filtered_events:
                display_text = f"{event_info['type']}: {event_info['title']}"
                self.events_listbox.insert(tk.END, display_text)
        else:
            self.events_listbox.insert(tk.END, "No events on this date.")

    def create_todo_list(self):
        ttk.Label(self.todo_frame, text="To-Do List", font=("Helvetica", 18)).pack(pady=10)

        # Frame for adding tasks
        add_task_frame = ttk.LabelFrame(self.todo_frame, text="Add Task")
        add_task_frame.pack(pady=10, fill=tk.X, padx=20)

        ttk.Label(add_task_frame, text="Task:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.task_entry = ttk.Entry(add_task_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_task_frame, text="Due Date:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.task_due_date = DateEntry(add_task_frame, date_pattern='yyyy-mm-dd')
        self.task_due_date.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_task_frame, text="Priority:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.task_priority = tk.StringVar()
        priority_options = ['High', 'Medium', 'Low']
        self.task_priority_combo = ttk.Combobox(add_task_frame, textvariable=self.task_priority, values=priority_options, state='readonly')
        self.task_priority_combo.set('Medium')
        self.task_priority_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_task_frame, text="Recurring:", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.task_recur = tk.StringVar()
        recur_options = ['None', 'Daily', 'Weekly', 'Monthly']
        self.task_recur_combo = ttk.Combobox(add_task_frame, textvariable=self.task_recur, values=recur_options, state='readonly')
        self.task_recur_combo.set('None')
        self.task_recur_combo.grid(row=3, column=1, padx=5, pady=5)

        add_task_btn = ttk.Button(add_task_frame, text="Add Task", command=self.add_task)
        add_task_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Frame for displaying tasks
        self.tasks_display_frame = ttk.LabelFrame(self.todo_frame, text="Tasks")
        self.tasks_display_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        # Search Bar
        search_frame = ttk.Frame(self.tasks_display_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.task_search_var = tk.StringVar()
        self.task_search_var.trace('w', self.display_tasks)
        self.task_search_entry = ttk.Entry(search_frame, textvariable=self.task_search_var)
        self.task_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Filter by Priority
        ttk.Label(search_frame, text="Filter by Priority:").pack(side=tk.LEFT, padx=5)
        self.task_filter_var = tk.StringVar()
        self.task_filter_var.set('All')
        task_filter_options = ['All', 'High', 'Medium', 'Low']
        self.task_filter_combo = ttk.Combobox(search_frame, textvariable=self.task_filter_var, values=task_filter_options, state='readonly')
        self.task_filter_combo.bind("<<ComboboxSelected>>", self.display_tasks)
        self.task_filter_combo.pack(side=tk.LEFT, padx=5)

        self.tasks_listbox = tk.Listbox(self.tasks_display_frame, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        self.tasks_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Enable Drag-and-Drop
        self.tasks_listbox.bind('<ButtonPress-1>', self.start_drag)
        self.tasks_listbox.bind('<B1-Motion>', self.do_drag)

        complete_task_btn = ttk.Button(self.todo_frame, text="Mark as Completed", command=self.complete_task)
        complete_task_btn.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.task_due_date.get_date()
        priority = self.task_priority.get()
        recur_pattern = self.task_recur.get()

        if task:
            tasks_to_add = self.generate_recurring_tasks(task, due_date, priority, recur_pattern)
            self.tasks.extend(tasks_to_add)
            self.task_entry.delete(0, tk.END)
            self.task_due_date.set_date(datetime.date.today())
            self.task_priority_combo.set('Medium')
            self.task_recur_combo.set('None')
            self.display_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def generate_recurring_tasks(self, task, start_date, priority, pattern):
        tasks = []
        current_date = start_date
        end_date = start_date + datetime.timedelta(days=365)
        while current_date <= end_date:
            tasks.append({'task': task, 'due_date': current_date, 'priority': priority})
            if pattern == 'None':
                break
            if pattern == 'Daily':
                current_date += datetime.timedelta(days=1)
            elif pattern == 'Weekly':
                current_date += datetime.timedelta(weeks=1)
            elif pattern == 'Monthly':
                month = current_date.month + 1 if current_date.month < 12 else 1
                year = current_date.year + 1 if current_date.month == 12 else current_date.year
                day = min(current_date.day, 28)  # To handle February
                current_date = datetime.date(year, month, day)
        return tasks

    def complete_task(self):
        selected_indices = self.tasks_listbox.curselection()
        for index in reversed(selected_indices):
            self.completed_tasks.append(self.tasks[index])
            del self.tasks[index]
        self.display_tasks()
        self.update_analytics()

    def display_tasks(self, *args):
        # Sort tasks by priority and due date
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        self.tasks.sort(key=lambda x: (priority_order[x['priority']], x['due_date']))

        # Clear the listbox
        self.tasks_listbox.delete(0, tk.END)

        search_query = self.task_search_var.get().lower()
        filter_priority = self.task_filter_var.get()

        for task_info in self.tasks:
            if search_query in task_info['task'].lower():
                if filter_priority == 'All' or filter_priority == task_info['priority']:
                    task_str = f"{task_info['due_date'].strftime('%Y-%m-%d')} - [{task_info['priority']}] {task_info['task']}"
                    self.tasks_listbox.insert(tk.END, task_str)
                    # Color code based on priority
                    color = self.get_priority_color(task_info['priority'])
                    self.tasks_listbox.itemconfig(tk.END, {'fg': color})

    def get_priority_color(self, priority):
        color_map = {
            'High': 'red',
            'Medium': 'orange',
            'Low': 'green'
        }
        return color_map.get(priority, 'black')

    # Drag-and-Drop Functions
    def start_drag(self, event):
        self.dragged_item_index = self.tasks_listbox.nearest(event.y)

    def do_drag(self, event):
        new_index = self.tasks_listbox.nearest(event.y)
        if new_index != self.dragged_item_index:
            # Swap the tasks
            self.tasks[self.dragged_item_index], self.tasks[new_index] = self.tasks[new_index], self.tasks[self.dragged_item_index]
            self.display_tasks()
            self.tasks_listbox.selection_set(new_index)
            self.dragged_item_index = new_index

    # ---------------------- Analytics Tab ---------------------- #
    def create_analytics(self):
        ttk.Label(self.analytics_frame, text="Analytics and Progress Tracking", font=("Helvetica", 18)).pack(pady=10)

        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, self.analytics_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_analytics()

    def update_analytics(self):
        total_tasks = len(self.tasks) + len(self.completed_tasks)
        completed_tasks = len(self.completed_tasks)
        pending_tasks = len(self.tasks)

        if total_tasks == 0:
            # Clear the figure
            self.figure.clear()
            self.chart_canvas.draw()
            return

        # Clear the previous figure
        self.figure.clear()

        # Pie Chart
        labels = 'Completed', 'Pending'
        sizes = [completed_tasks, pending_tasks]
        colors = ['green', 'orange']

        ax = self.figure.add_subplot(111)
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        self.figure.suptitle('Task Completion Overview')

        self.chart_canvas.draw()

if __name__ == "__main__":
    app = CollegeScheduler()
    app.mainloop()

