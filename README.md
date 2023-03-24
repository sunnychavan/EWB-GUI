# EWB-GUI
I am part of the Digital Agriculture subteam on campus -- a team within Cornell University's "Engineers Without Borders" Project Team. Our current project is centered around leveraging Computer Vision to identify and combat Northern Leaf Blight (NLB) disease in maize crop. This GUI helps my team plan, map and visualize the paths our ground unit (rover) will follow in farm fields while assessing various maize crop. 

# What I learned 
• UI Kivy library for Python  
• MVC framework   
• Page design and cross-functionality  

# Setup and In-depth Description    

## ewb-gui  

Engineer's Without Borders Digital Agriculture Subteam GUI design experimentation for rover and drone control application

## Overview
We plan to build our app with Python using Kivy to develop our GUI and interface with the Google Maps API (Acutally might not use Google Maps API, we'll see?)

## Getting Started with Kivy

Install kivy virtual environment and other dependecies into `ewb-gui/application` directory.

After [installing Kivy](https://kivy.org/doc/stable/installation/installation-windows.html#install-win-dist), checkout this tutorial series to get down the basics: https://www.youtube.com/watch?v=bMHK6NDVlCM&list=PLzMcBGfZo4-kSJVMyYeOQ8CXJ3z1k7gHn&ab_channel=TechWithTim

## Package Management

### To activate virtual environment:

```shell
kivy_venv\Scripts\activate
```

### Other packages to install in virtual env:

```shell
pip install -r requirements.txt
```

### Working with Google Maps API
https://github.com/googlemaps/google-maps-services-python

### Kivy Map Widget:
https://github.com/kivy-garden/garden.mapview


