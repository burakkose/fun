from cocos import layer, sprite, director, scene
from cocos.actions import Place, MoveBy, Delay

import settings
import solver


class BackgroundLayer(layer.Layer):

    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.image = sprite.Sprite(settings.BACKGROUND)
        self.image.position = (512, 384)
        self.add(self.image, z=0)


class Animation(layer.Layer):

    def __init__(self):
        super(Animation, self).__init__()

        self.cabbage = sprite.Sprite(image=settings.CABBAGE)
        self.cabbage.scale = 0.7
        self.add(self.cabbage, z=1)

        self.sheep = sprite.Sprite(image=settings.SHEEP)
        self.sheep.scale = 1.5
        self.add(self.sheep, z=1)

        self.wolf = sprite.Sprite(image=settings.WOLF)
        self.wolf.scale = 1.5
        self.add(self.wolf, z=1)

        self.farmer = sprite.Sprite(image=settings.FARMER)
        self.farmer.scale_y = 1.3
        self.add(self.farmer, z=1)

        self.boat = sprite.Sprite(image=settings.BOAT)
        self.add(self.boat, z=1)

        self.do_animate()

    def do_animate(self):
        boat_location = 'L'
        current_state = '0000'
        states = solver.path[1:]

        farmer_action = Place(settings.pos_of_farmer['L']) + Delay(2)
        cabbage_action = Place(settings.pos_of_cabbage['L']) + Delay(2)
        sheep_action = Place(settings.pos_of_sheep['L']) + Delay(2)
        wolf_action = Place(settings.pos_of_wolf['L']) + Delay(2)
        boat_action = Place(settings.pos_of_boat['L']) + Delay(2)

        for state in states:
            move = self.who_move(''.join([str(int(x) ^ int(y))
                                          for (x, y) in zip(current_state, state)]))
            current_state = state

            (x, y) = settings.pos_of_boat[boat_location]

            if boat_location == 'R':
                boat_location = 'L'
                t = 350
            else:
                boat_location = 'R'
                t = -350

            if 'w' in move:  # wolf
                wolf_action += Place((x, y + 10)) + MoveBy((t, 0), 2) \
                    + Place(settings.pos_of_wolf[boat_location])
                sheep_action += Delay(2)
                cabbage_action += Delay(2)
            elif 's' in move:  # sheep
                sheep_action += Place((x, y + 10)) + MoveBy((t, 0), 2) \
                    + Place(settings.pos_of_sheep[boat_location])
                cabbage_action += Delay(2)
                wolf_action += Delay(2)
            elif 'c' in move:  # cabbage
                cabbage_action += Place((x, y + 10)) + MoveBy((t, 0), 2) \
                    + Place(settings.pos_of_cabbage[boat_location])
                sheep_action += Delay(2)
                wolf_action += Delay(2)
            else:
                sheep_action += Delay(2)
                wolf_action += Delay(2)
                cabbage_action += Delay(2)

            farmer_action += Place((x + 20, y + 50)) + MoveBy((t, 0), 2) \
                + Place(settings.pos_of_farmer[boat_location])
            boat_action += MoveBy((t, 0), 2)

        self.farmer.do(farmer_action)
        self.wolf.do(wolf_action)
        self.cabbage.do(cabbage_action)
        self.boat.do(boat_action)
        self.sheep.do(sheep_action)

    def who_move(self, xor):
        states = ('f', 'w', 's', 'c')
        moved = []
        for (x, y) in zip(states, xor):
            if y == '1':
                moved.append(x)
        return moved


if __name__ == '__main__':
    director.director.init(width=1024, height=768, caption='AI Yazlab')
    scene = scene.Scene()

    scene.add(BackgroundLayer(), z=0)
    scene.add(Animation(), z=0)
    director.director.run(scene)
