"""
Contains template rules for MapWindow in kv language
"""

from kivy.lang import Builder

Builder.load_string("""
<MapWindow>:
    name: "map_window"
    AnchorLayout:
        id: map_window_AnchorLayout
        anchor_y: "top"
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "resources/images/dark-grey.jpg"

        

        # Main Box that contains Map
        FloatLayout:
            pos: (100, 100)
            BoxLayout:
                id: map_container
                orientation: "horizontal"
                DrawableMapView:
                    pos_hint: {'top': 1, 'bottom': 1}
                    id: map
                    canvas:
                        Rectangle:
                            source: 'resources/images/tanzania_drone_pic2.jpg'
                            size: self.size
            Label:
                id: add_image_label
                text: "Please add your own image"
                font_size: 20
                bold: True
                        # Image:
                        #     id: draw_image
                        #     source: "resources/images/marker.png"
                        #     size_hint: (0.03, 0.03)
                        #     allow_stretch: True
                        #     opacity: 0

        # Back Button and Title
        FloatLayout:
            id: title_FloatLayout
            size_hint_y: 0.1
            canvas.before:
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: "resources/images/dark-grey.jpg"
            Button:
                pos_hint: {"x": 0.02, "center_y": 0.5}
                size_hint: (0.1, 0.8)
                text: "Home"
                on_release: 
                    app.root.current = "home_window"
                    root.manager.transition.direction = "right"
            Label:
                pos_hint: {"center_x": 0.5, "center_y":0.5}
                size_hint: (0.8, 0.8)
                text: "Route Planning"
                font_size: 30
                font_name: "resources/fonts/Orbitron-Bold.ttf"
                bold: True
                color: "#C0C0C0"

        # Map Drawing Tools
        AnchorLayout:
            anchor_y: "bottom"
            GridLayout:
                id: drawing_tools_GridLayout
                name: "drawing_tools"
                size_hint_y: 0.2
                cols: 2
                padding: 20
                canvas.before:
                    Rectangle:
                        pos: self.pos
                        size: self.size
                        source: "resources/images/dark-grey.jpg"
                GridLayout:
                    cols: 6
                    size_hint_y: 0.3
                    size_hint_x: 1
                    AnchorLayout:
                        Button:
                            text: "Insert Image"
                            size_hint: (1, 0.6)
                            on_release: 
                                root.show_load()
                    AnchorLayout:
                        Button:
                            text: "Undo"
                            size_hint: (1, 0.6)
                            padding_x: 10
                            on_release: 
                                root.ids["map"].undo()
                    AnchorLayout:
                        Button:
                            text: "Clear"
                            size_hint: (1, 0.6)
                            padding_x: 10
                            on_release: 
                                root.ids["map"].clear()
                    AnchorLayout:
                        Button:
                            text: "Recenter"
                            size_hint: (1, 0.6)
                            padding_x: 10
                            on_release:
                                root.ids["map"].recenter()
                    AnchorLayout:
                        Button:
                            text: "Lasso"
                            size_hint: (1, 0.6)
                            padding_x: 10
                    AnchorLayout:
                        Button:
                            id: draw_mode_button
                            text: "Draw Path"
                            size_hint: (1, 0.6)
                            padding_x: 10
                            on_release: 
                                root.ids["map"].toggle_draw_mode()
                AnchorLayout:
                    anchor_x: "right"
                    size_hint_x: 0.3
                    padding: 10
                    Button:
                        text: "Run"
                        size_hint: (1, 1)
                        on_release:
                            root.ids["map"].run()

<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            path: "../../../"
            rootpath: "../"
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)

<CoordinateDialog>:
    GridLayout:
        size: root.size
        pos: root.pos
        rows: 10
        orientation: "vertical"
        Label:
            size_hint_y: 0.3
            font_size: 14
            halign: 'center'
            text: "\\n\\nInput at least three GPS Coordinates into the fields. \\nFor example: Top Left Coordinate should take in the GPS value of the top left coordinate of the image.\\n"
        BoxLayout:
            orientation: "horizontal"

            BoxLayout:
                orientation: "vertical"
                Label:
                    id: tl_coord_lat_label
                    text: "Top Left Coordinate Latitude"
                
                TextInput:
                    id: tl_coord_lat
              
            BoxLayout:
                orientation: "vertical"
                Label:
                    id: tl_coord_lon_label
                    text: "Top Left Coordinate Longitude"
                TextInput:
                    id: tl_coord_lon


        BoxLayout:
            orientation: "horizontal"

            BoxLayout:
                orientation: "vertical"
                Label:
                    id: tr_coord_lat_label
                    text: "Top Right Coordinate Latitude"
                
                TextInput:
                    id: tr_coord_lat
              
            BoxLayout:
                orientation: "vertical"
                Label:
                    id: tr_coord_lon_label
                    text: "Top Right Coordinate Longitude"
                TextInput:
                    id: tr_coord_lon

        
        BoxLayout:
            orientation: "horizontal"

            BoxLayout:
                orientation: "vertical"
                Label:
                    id: bl_coord_lat_label
                    text: "Bottom Left Coordinate Latitude"
                
                TextInput:
                    id: bl_coord_lat
              
            BoxLayout:
                orientation: "vertical"
                Label:
                    id: bl_coord_lon_label
                    text: "Bottom Left Coordinate Longitude"
                TextInput:
                    id: bl_coord_lon


        BoxLayout:
            orientation: "horizontal"

            BoxLayout:
                orientation: "vertical"
                Label:
                    id: br_coord_lat_label
                    text: "Bottom Right Coordinate Latitude"
                
                TextInput:
                    id: br_coord_lat
              
            BoxLayout:
                orientation: "vertical"
                Label:
                    id: br_coord_lon_label
                    text: "Bottom Right Coordinate Longitude"
                TextInput:
                    id: br_coord_lon

                
        Button:
            id: submit_coord
            size_hint: (0.1, 0.7)   
            text: "Submit"
            on_release:
                root.submit_coordinates()

""")
