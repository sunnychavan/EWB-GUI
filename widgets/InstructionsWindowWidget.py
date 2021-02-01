"""
Design Instructions for Instructions window in Kv language 
"""

from kivy.lang import Builder

Builder.load_string("""
<InstructionsWindow>:
    name: "instructions_window"
    GridLayout:
        id: instructions_grid
        rows: 3
        columns: 1
        spacing: 100
        Button:
            pos_hint: {"x": 0.02, "center_y": 0.5}
            size_hint: (0.1, 0.8)
            text: "Home"
            on_release: 
                app.root.current = "home_window"
                root.manager.transition.direction = "right"
        Label:
            text: root.current_instruction
        GridLayout:
            columns: 2
            rows: 1
            Button:
                text: "Previous"
                on_release: root.goBack()
            Button:
                text: "Next"
                on_release: root.updateInstructions()
""")
