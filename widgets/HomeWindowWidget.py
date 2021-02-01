"""
Design of HomeWindow screen in Kv langauge
"""


from kivy.lang import Builder

Builder.load_string("""
<HomeWindow>:
    name: "home_window"

    # Video:
    #    source: "resources/images/test.avi"
    #    pos: self.pos
    #    size: self.size

    GridLayout:
        rows: 2
        columns: 1
        padding: 100
        spacing: 100
        orientation: "vertical"
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "resources/images/light-green.jpg"
        # Title
        Label:
            size_hint: (1, 0.2)
            text: "Digital Agriculture"
            font_size: 60
            font_name: "resources/fonts/Orbitron-Bold.ttf"
            bold: True
            color: (240, 240, 240, 1)
        
        # Navigation Buttons
        GridLayout:
            col: 1
            rows: 4
            spacing: 10
            Button:
                text: "Start"
                on_release: 
                    app.root.current = "map_window"
                    root.manager.transition.direction = "left"
            Button:
                text: "Instructions"
                on_release:
                    app.root.current = "instructions_window"
                    root.manager.transition.direction = "left"
            Button:
                text: "Documentation"
                on_release:
                    root.open_documentation()
            Button:
                text: "Project Information"
                on_release:
                    root.open_projectinfo("https://ewb.engineering.cornell.edu/subteams.html")
""")
