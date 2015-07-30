import pyglet

pyglet.resource.path = ["../resources"]
pyglet.resource.reindex()

WOLF = pyglet.resource.image("Wolf.png")
BOAT = pyglet.resource.image("Boat.png")
SHEEP = pyglet.resource.image("Sheep.png")
FARMER = pyglet.resource.image("Farmer.png")
CABBAGE = pyglet.resource.image("Cabbage.png")
BACKGROUND = pyglet.resource.image("Background.jpg")

pos_of_sheep = {'L': (300, 80), 'R': (90, 350)}
pos_of_wolf = {'L': (670, 268), 'R': (380, 380)}
pos_of_boat = {'L': (500, 300), 'R': (150, 300)}
pos_of_farmer = {'L': (425, 170), 'R': (190, 400)}
pos_of_cabbage = {'L': (560, 200), 'R': (270, 370)}
