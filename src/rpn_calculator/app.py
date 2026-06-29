import flet as ft
import operator

def main(page: ft.Page):
    # --- 1. Window Setup ---
    page.title = "RPN Visualizer"
    page.window_width = 480
    page.window_height = 850
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 15

    # --- 2. Global State ---
    stack_data = []      
    execution_queue = [] 
    
    ops = {
        '+': operator.add, '-': operator.sub,
        '*': operator.mul, '/': operator.truediv
    }

    # --- 3. UI Components ---

    # Input Field
    input_display = ft.TextField(
        value="",
        text_align=ft.TextAlign.RIGHT,
        text_size=30,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.WHITE,
        read_only=True, 
        hint_text="Type (e.g. 3 4 +)",
        border_color=ft.Colors.TRANSPARENT,
    )

    # NEW: Reference Display (Shows the full expression after you hit Enter)
    ref_display = ft.Text(
        value="", 
        size=16, 
        color=ft.Colors.BLUE_GREY_900, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        italic=True
    )

    # Status Box
    status_text = ft.Text(value="Ready to Type", size=18, weight="bold", color="white")
    status_box = ft.Container(
        content=status_text,
        bgcolor=ft.Colors.BLUE_GREY_700,
        padding=10,
        border_radius=8,
        alignment=ft.alignment.center,
        margin=ft.margin.only(bottom=5)
    )

    # Queue Display
    queue_text = ft.Text(value="", size=16, color=ft.Colors.BLUE_GREY_700)

    # Stack Visualizer
    stack_view = ft.Column(
        spacing=5,
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    stack_container = ft.Container(
        content=stack_view,
        bgcolor=ft.Colors.GREY_300,
        border=ft.border.all(2, ft.Colors.GREY_500),
        border_radius=10,
        padding=10,
        height=280,
        alignment=ft.alignment.bottom_center
    )

    # NEXT STEP Button
    next_btn = ft.ElevatedButton(
        text="EXECUTE NEXT STEP ▶",
        bgcolor=ft.Colors.GREEN_600,
        color="white",
        height=50,
        visible=False, 
    )

    # --- 4. Logic Engine ---

    def update_ui():
        stack_view.controls.clear()
        for item in reversed(stack_data):
            stack_view.controls.append(
                ft.Container(
                    content=ft.Text(str(item), size=20, weight="bold", color="white"),
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.ORANGE_400,
                    height=45,
                    border_radius=5,
                )
            )
        
        if execution_queue:
            queue_text.value = f"Next Item: {execution_queue[0]}"
            next_btn.text = f"EXECUTE: {execution_queue[0]} ▶"
            next_btn.visible = True
            next_btn.disabled = False
        elif next_btn.visible:
            queue_text.value = "Execution Complete."
            next_btn.text = "DONE (RESET)"
            next_btn.disabled = True
        
        page.update()

    def run_next_step(e):
        if not execution_queue: return

        token = execution_queue.pop(0)
        token_upper = token.upper()

        if token_upper in ops:
            if len(stack_data) < 2:
                status_text.value = "Error: Need 2 nums"
                status_box.bgcolor = ft.Colors.RED_400
            else:
                val2 = stack_data.pop()
                val1 = stack_data.pop()
                try:
                    res = ops[token_upper](val1, val2)
                    if isinstance(res, float) and res.is_integer(): res = int(res)
                    stack_data.append(res)
                    status_text.value = f"{val1} {token} {val2} = {res}"
                    status_box.bgcolor = ft.Colors.GREEN_600
                except ZeroDivisionError:
                    stack_data.append(val1); stack_data.append(val2)
                    status_text.value = "Error: Div by 0"
                    status_box.bgcolor = ft.Colors.RED_400
        
        elif token_upper == "SWAP":
             if len(stack_data) >= 2:
                v2 = stack_data.pop(); v1 = stack_data.pop()
                stack_data.append(v2); stack_data.append(v1)
                status_text.value = "Swapped Top 2"
                status_box.bgcolor = ft.Colors.PURPLE_400
        
        else:
            try:
                val = float(token)
                if val.is_integer(): val = int(val)
                stack_data.append(val)
                status_text.value = f"PUSHED: {val}"
                status_box.bgcolor = ft.Colors.BLUE_GREY_500
            except ValueError:
                status_text.value = f"Unknown: {token}"
                status_box.bgcolor = ft.Colors.RED_500

        update_ui()

    next_btn.on_click = run_next_step

    def lock_and_load():
        """Triggered by ENTER: Parses text and fills the queue"""
        raw = input_display.value.strip()
        if not raw: return

        # 1. Update the Reference Display
        ref_display.value = f"Current Expression:  {raw}"

        execution_queue.clear()
        execution_queue.extend(raw.split()) 
        
        input_display.value = "" 
        status_text.value = "Loaded! Press NEXT STEP."
        status_box.bgcolor = ft.Colors.BLUE_600
        
        update_ui()

    # --- 5. INPUT HANDLING ---

    def handle_input_action(action, char=None):
        if action == "ADD":
            input_display.value += str(char)
        elif action == "SPACE":
            input_display.value += " "
        elif action == "BACK":
            input_display.value = input_display.value[:-1]
        elif action == "ENTER":
            lock_and_load()
        elif action == "CLEAR":
            stack_data.clear()
            execution_queue.clear()
            input_display.value = ""
            ref_display.value = "" # Clear reference too
            status_text.value = "Cleared"
            next_btn.visible = False
            update_ui()
        
        page.update()

    def on_keyboard(e: ft.KeyboardEvent):
        k = e.key
        if k in "0123456789.": handle_input_action("ADD", k)
        elif k in ["+", "-", "*", "/"]: handle_input_action("ADD", k)
        elif k == " ": handle_input_action("SPACE")
        elif k == "Backspace": handle_input_action("BACK")
        elif k == "Enter": handle_input_action("ENTER")
        elif k in ["c", "C", "Escape"]: handle_input_action("CLEAR")

    page.on_keyboard_event = on_keyboard

    def on_btn_click(e):
        d = e.control.data
        if d == "ENTER": handle_input_action("ENTER")
        elif d == "CLEAR": handle_input_action("CLEAR")
        elif d == "BACK": handle_input_action("BACK")
        elif d == "SPACE": handle_input_action("SPACE")
        else: handle_input_action("ADD", d)

    # --- 6. Layout ---

    def btn(txt, data=None, color=ft.Colors.WHITE, bg=ft.Colors.BLUE_GREY_500, expand=1):
        if data is None: data = txt
        return ft.ElevatedButton(
            text=txt, data=data, on_click=on_btn_click,
            bgcolor=bg, color=color,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            expand=expand
        )

    keypad = ft.Column([
        ft.Row([btn("SWAP", bg=ft.Colors.PURPLE_400), btn("SPACE", "SPACE", bg=ft.Colors.BLUE_600, expand=2), btn("⌫", "BACK", bg=ft.Colors.RED_300)]),
        ft.Row([btn("7"), btn("8"), btn("9"), btn("/", bg=ft.Colors.ORANGE_700)]),
        ft.Row([btn("4"), btn("5"), btn("6"), btn("*", bg=ft.Colors.ORANGE_700)]),
        ft.Row([btn("1"), btn("2"), btn("3"), btn("-", bg=ft.Colors.ORANGE_700)]),
        ft.Row([btn("0", expand=2), btn("."), btn("Enter / Load", "ENTER", bg=ft.Colors.GREEN_700, expand=2)]),
        ft.Row([btn("CLEAR ALL", "CLEAR", bg=ft.Colors.RED_900, expand=True)]),
    ], spacing=5)

    page.add(
        input_display,
        ref_display,  # <--- Added Here (Visible after Enter)
        status_box,
        next_btn,
        queue_text,
        stack_container,
        ft.Divider(),
        keypad
    )

ft.app(target=main)