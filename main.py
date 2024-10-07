import os
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

### CLASS DEFINITIONS ###
@dataclass
class Element:
    relPath: str
    name: str

@dataclass
class File(Element):
    pass

@dataclass
class Directory(Element):
    children: list


### FUNCTIONS ###
def tree_walker(path):
    objects = []
    elements = os.listdir(path)
    for element in elements:
        element_path = path + "/" + element
        if os.path.isdir(element_path):
            children = tree_walker(element_path)
            objects.append(Directory(element_path, element, children))
        else:
            objects.append(File(element_path, element))
    return objects

def build_tree(path):
    elements = tree_walker(path)
    return Directory(path, ".", elements)

def drawLine(element):
    return

def print_tree(obj, depth):
    global draw, depth_increment, line_increment, line_number
    for element in obj.children:
        line_number += 1
        x, y = depth * depth_increment, line_number * line_increment
        print(f"x:{x}, y:{y} = {element.name}") # debug print
        draw.text(
            xy=(depth* depth_increment, line_number* line_increment), 
            text=element.name, 
            fill="black",
            font=font
            )
        if type(element) == Directory:
            print_tree(element, depth+1)
    

def printer(root):
    print_tree(root, 1)

### TEST ### 

# build tree: 
root = build_tree("./testfolder")

# initiate the image and the draw object
width, height = 1000, 1000
start_x, start_y = 10, 10
line_increment, depth_increment = 30, 30
line_number = 1
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)
font = ImageFont.load_default(size=30)

draw.text((start_x, start_y),root.name, fill='black', font=font)

# draw the tree into the image
printer(root)

image.save("example.png")