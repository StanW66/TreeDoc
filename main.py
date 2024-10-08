import os
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

### CLASS DEFINITIONS ###
@dataclass
class Element:
    relPath: str
    name: str
    xy: tuple
    # def __eq__(self, other) -> bool:
        # return self.xy[1] == other.xy[1]
    # def __lt__(self, other) -> bool:
    #     return self.xy[1] < other.xy[1]
    # def __gt__(self, other) -> bool:
        # return self.xy[1] > other.xy[1]

@dataclass
class File(Element):
    pass

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

def drawLine(element):
    return

def print_tree(element_list):
    for element in sorted(element_list):
        print(element.name)
        draw.text( # put this in seperate funciton at some point
            xy=(element.xy), 
            text=element.name, 
            fill="black",
            font=font
            )
    return 

def printer(element_tree): # add printing of the project name 
    print_tree(element_tree)

### TEST ### 

# initialize global variables
width, height = 1000, 1000
start_x, start_y = 10, 10
line_increment, depth_increment = 30, 30
line_number = 1
element_list = []

# build the tree
build_tree("./testfolder")

# initialize iamgedrawer object
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)
font = ImageFont.load_default(size=30)

# draw the tree into the image
printer(element_list)
image.save("example.png")