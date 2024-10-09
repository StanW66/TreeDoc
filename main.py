import os
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import re

### GLOBAL VARIABLES ###
width, height = 1000, 1000
start_x, start_y = 10, 10
line_number = 1
element_list = []
icon_size = 50
font_size = 30
parent_offset_y = font_size + 5
parent_offset_x = icon_size/2
child_offset_y = font_size / 2
child_offset_x = -5
line_increment = font_size + 10
depth_increment = 50

@dataclass
class Element:
    relPath: str
    name: str
    xy: tuple
    def __eq__(self, other) -> bool:
        return self.xy[1] == other.xy[1]
    def __lt__(self, other) -> bool:
        return self.xy[1] < other.xy[1]
    def __gt__(self, other) -> bool:
        return self.xy[1] > other.xy[1]

@dataclass
class File(Element):
    def get_file_suffix(self):
        match = re.search(r'\.([^.]+)$', self.name)
        return match.group(1) if match else None

@dataclass
class Directory(Element):
    children: list

### FUNCTIONS ###
def tree_walker(path, depth):
    global depth_increment, line_increment, line_number, element_list
    objects = []
    elements = os.listdir(path)
    for element in elements:
        line_number += 1
        x, y = depth * depth_increment, line_number * line_increment
        element_path = path + "/" + element
        if os.path.isdir(element_path):
            children = tree_walker(element_path, depth+1)
            obj = Directory(element_path, element, (x,y), children)
            objects.append(obj)
            element_list.append(obj)
        else:
            obj = File(element_path, element, (x,y))
            objects.append(obj)
            element_list.append(obj)
    return objects

def build_tree(path):
    elements = tree_walker(path, 1)
    return elements

def print_text(element_list):
    for element in sorted(element_list):
        draw.text( # put this in seperate funciton at some point
            xy=(element.xy), 
            text=element.name, 
            fill="black",
            font=font
            )
    return 

def print_branches(element_list):
    for element in element_list:
        if type(element) == Directory:
            parent_xy = (element.xy[0] + parent_offset_x, element.xy[1] + parent_offset_y)
            for child in element.children:
                child_xy = (child.xy[0] + child_offset_x, child.xy[1] + child_offset_y)
                elbow = (parent_xy[0], child_xy[1])
                draw.line([parent_xy, elbow], fill="black", width=1)
                draw.line([child_xy, elbow], fill="black", width=1)
    return

def print_icons(element_list):
    # Open a file here
    # the use image.paste() to put it on our main image
    return

def printer(element_tree): # add printing of the project name 
    print_icons(element_list)
    print_text(element_list)
    print_branches(element_list)

### TEST ### 
# build the tree
build_tree("./testfolder")

# initialize iamgedrawer object
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)
font = ImageFont.load_default(size=font_size)

# draw the tree into the image
printer(element_list)
image.save("example.png")