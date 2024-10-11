import os
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import re

### GLOBAL VARIABLES ###
START_X, START_Y = 10, 10
LINE_NUMBER = 1
ELEMENT_LIST = [] 
ICON_SIZE = 30
FONT_SIZE = 30
PARENT_OFFSET_Y = FONT_SIZE + 5
PARENT_OFFSET_X = ICON_SIZE/2
CHILD_OFFSET_Y = FONT_SIZE / 2
CHILD_OFFSET_X = -5
LINE_INCREMENT = FONT_SIZE + 10
DEPTH_INCREMENT = 50
# Windows Size: 
WIDTH, HEIGHT = 1000, 1000

### CLASSES ###
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
    def get_file_suffix(self): # thanks gpt
        match = re.search(r'\.([^.]+)$', self.name)
        return match.group(1) if match else "generic"

@dataclass
class Directory(Element):
    children: list

### FUNCTIONS ###
def tree_walker(path, depth):
    global DEPTH_INCREMENT, LINE_INCREMENT, LINE_NUMBER, ELEMENT_LIST
    objects = []
    elements = os.listdir(path)
    for element in elements:
        LINE_NUMBER += 1
        x, y = depth * DEPTH_INCREMENT, LINE_NUMBER * LINE_INCREMENT
        element_path = path + "/" + element
        if os.path.isdir(element_path):
            children = tree_walker(element_path, depth+1)
            obj = Directory(element_path, element, (x,y), children)
            objects.append(obj)
            ELEMENT_LIST.append(obj)
        else:
            obj = File(element_path, element, (x,y))
            objects.append(obj)
            ELEMENT_LIST.append(obj)
    return objects

def get_text_dimensions(text_string, font):
    # source: https://levelup.gitconnected.com/how-to-properly-calculate-text-size-in-pil-images-17a2cc6f51fd
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent + ascent
    return (text_width, text_height)

def define_window_size():
    global WIDTH, HEIGHT
    max = 0
    longest_name = ""
    for element in ELEMENT_LIST:
        text_width, text_height = get_text_dimensions(element.name, font=font)
        length = text_width + element.xy[0]
        if length > max:
            max = length
            longest_name = element.name
    text_width, text_height = get_text_dimensions(longest_name,font=font)
    WIDTH = max + START_X*4 + ICON_SIZE
    HEIGHT = len(ELEMENT_LIST) * LINE_INCREMENT + LINE_INCREMENT*3
    return

def build_tree(path): # do i need this function? 
    elements = tree_walker(path, 1)
    define_window_size()
    return elements

def print_text(element_list):
    for element in sorted(element_list):
        xy = (element.xy[0] + ICON_SIZE + 5, element.xy[1])
        draw.text(xy=(xy), text=element.name, fill="black", font=font)
    return 

def print_branches(element_list): # fix ofset to make space for the icons
    for element in element_list:
        if type(element) == Directory:
            parent_xy = (element.xy[0] + PARENT_OFFSET_X, element.xy[1] + PARENT_OFFSET_Y)
            for child in element.children:
                child_xy = (child.xy[0] + CHILD_OFFSET_X, child.xy[1] + CHILD_OFFSET_Y)
                elbow = (parent_xy[0], child_xy[1])
                draw.line([parent_xy, elbow], fill="black", width=1)
                draw.line([child_xy, elbow], fill="black", width=1)
    return

def print_icons(element_list):
    icon_dir = "./icons/"
    for element in element_list:
        # get file extension and define icon accordingly
        if type(element) == File:
            icon = element.get_file_suffix() + ".png"
        elif len(element.children) > 0:
            icon = "full_dir.png"
        else: 
            icon = "empty_dir.png"

        # check if we have that icon, else change to generic
        if icon in os.listdir(icon_dir):
            full_path = icon_dir + icon
        else: 
            full_path = icon_dir + "generic.png"

        # print the appropriate icon to the image. 
        with Image.open(full_path) as i:
            smol_icon = i.resize((ICON_SIZE,ICON_SIZE))
            image.paste(smol_icon, element.xy, smol_icon)
    return

def printer(): # add printing of the project name 
    print_icons(ELEMENT_LIST)
    print_text(ELEMENT_LIST)
    print_branches(ELEMENT_LIST)
    return

### TEST ### 
font = ImageFont.load_default(size=FONT_SIZE)
# build the tree
build_tree("./testfolder")

# initialize iamgedrawer object
image = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(image)
# draw the tree into the image
printer()

# measuring the fontsize
for i in range(1,1000,FONT_SIZE):
    draw.point((i,i), fill="black")

image.save("example.png")