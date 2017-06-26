# coding: UTF-8

# imports
import json as json
from presets import Player, FallingTile, FinishTile
from text_handler import drawText as draw_text
from level_manager import Level
from edgey_camera import EdgeyCamera
from pygltoolbox.glpython import *
from pygltoolbox.opengl_lib import *

# constants
with open("config.json") as json_config:
    config_dict = json.load(json_config)

config = config_dict["settings"]

FPS = config_dict["display_constants"]["fps"]
WINDOW_SIZE = config_dict["display_constants"]["dimensions"]

# init
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], "Edgey", centered=True)
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True,
       numlights=1,
       perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
       texture=True, verbose=False)
reshape(*WINDOW_SIZE)
initLight(GL_LIGHT0)
glClearColor(210.0 / 255, 224.0 / 255, 224.0 / 255, 1.0)


clock = pygame.time.Clock()

surface = pygame.display.get_surface()

# carga inicial
font = pygame.font.Font(config["font"], 40)

level = Level("maps/flat.json")

shards = level.get_shards()
shardcount = 0
total_shards = len(shards)

falling_tiles = level.get_fallers()

pushers = level.get_pushers()

# crea y ubica al jugador en el nivel
player = Player()
player.place(level)

# crea cámara
camera = EdgeyCamera(player)

frame = 0
print "Main loop started"

while(True):
    clock.tick(FPS)
    clearBuffer()
    camera.place()

    orientation = camera.get_orientation()

    # eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key == K_q:
                camera.gradual_rotateLeft()
            elif event.key == K_e:
                camera.gradual_rotateRight()

            # relative movements
            # mata de codigo, cuidado al entrar
            if not player.is_falling():
                if orientation == 0:
                    if event.key == K_w:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                        else:
                            player.rise_neg_x()
                    elif event.key == K_s:
                        if not player.can_rise_x(level):
                            player.move_x()
                        else:
                            player.rise_x()
                    elif event.key == K_a:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                        else:
                            player.rise_neg_y()
                    elif event.key == K_d:
                        if not player.can_rise_y(level):
                            player.move_y()
                        else:
                            player.rise_y()
                elif orientation == 1:
                    if event.key == K_w:
                        if not player.can_rise_y(level):
                            player.move_y()
                        else:
                            player.rise_y()
                    elif event.key == K_s:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                        else:
                            player.rise_neg_y()
                    elif event.key == K_a:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                        else:
                            player.rise_neg_x()
                    elif event.key == K_d:
                        if not player.can_rise_x(level):
                            player.move_x()
                        else:
                            player.rise_x()
                elif orientation == 2:
                    if event.key == K_w:
                        if not player.can_rise_x(level):
                            player.move_x()
                        else:
                            player.rise_x()
                    elif event.key == K_s:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                        else:
                            player.rise_neg_x()
                    elif event.key == K_a:
                        if not player.can_rise_y(level):
                            player.move_y()
                        else:
                            player.rise_y()
                    elif event.key == K_d:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                        else:
                            player.rise_neg_y()
                elif orientation == 3:
                    if event.key == K_w:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                        else:
                            player.rise_neg_y()
                    elif event.key == K_s:
                        if not player.can_rise_y(level):
                            player.move_y()
                        else:
                            player.rise_
                            y()
                    elif event.key == K_a:
                        if not player.can_rise_x(level):
                            player.move_x()
                        else:
                            player.rise_x()
                    elif event.key == K_d:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                        else:
                            player.rise_neg_x()

    keys = pygame.key.get_pressed()

    # lógica del nivel
    player_coord = player.get_grid_coordinates()

    obj = level.get_object_below(player_coord)
    if obj is None:
        player.fall(player_coord, level)
    elif isinstance(obj, FallingTile):
        obj.fall()
    elif isinstance(obj, FinishTile) and shardcount == total_shards:
        print "player victory"
    print shardcount, total_shards

    if player_coord[2] <= 0:
        print "player dead"

    for shard in shards:
        if shard.get_grid_coordinates() == player_coord:
            shards.remove(shard)
            shardcount += 1

    for falling_tile in falling_tiles:
        if falling_tile.is_deletable():
            level.remove_object_at(falling_tile.get_original_coordinates())
        falling_tile.update(player)

    for pusher in pushers:
        if pusher.check_front(player) and not player.sliding():
            pusher.push()
            direction = pusher.get_orientation()
            player.slide(direction)

    # actualiza camara
    camera.update()

    # actualiza modelos
    player.update()

    for pusher in pushers:
        pusher.update()

    # dibuja luces
    glLightfv(GL_LIGHT0, GL_POSITION, [-1000, -250, 1000])

    # dibuja mapa
    level.draw()

    # dibuja modelos
    for shard in shards:
        shard.draw()

    player.draw()

    # dibuja texto
    progress_string = str(shardcount) + "/" + str(total_shards) + " shards collected"
    shard_progress = font.render(progress_string, True, (0.0, 0.0, 0.0))

    pygame.display.flip()
