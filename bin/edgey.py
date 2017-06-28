# coding: UTF-8

# imports
import json as json
from OpenGL import GL
from presets import Player, FallingTile, FinishTile, OptionTile, Shard
from level_manager import Level
from edgey_camera import EdgeyCamera
from pygltoolbox.glpython import *
from pygltoolbox.opengl_lib import *


# function definitions
def load_level(level_name):
    print "loading ", level_name
    global level, shards, shardcount, total_shards, falling_tiles, pushers, options, player, camera, finishes
    level = Level(level_name)

    shards = level.get_shards()
    shardcount = 0
    total_shards = len(shards)

    falling_tiles = level.get_fallers()

    pushers = level.get_pushers()

    options = level.get_options()

    finishes = level.get_finish()

    player = Player()
    player.place(level)

    camera = EdgeyCamera(player)

# constants
with open("config.json") as json_config:
    config_dict = json.load(json_config)

config = config_dict["settings"]

FPS = config_dict["display_constants"]["fps"]
WINDOW_SIZE = config_dict["display_constants"]["dimensions"]

# init
icon = pygame.image.load("textures/icon.png")
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], "Edgey", centered=True, icon=icon)
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True,
       numlights=1,
       perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
       texture=True, verbose=False)
reshape(*WINDOW_SIZE)
initLight(GL_LIGHT0)
glClearColor(210.0 / 255, 224.0 / 255, 224.0 / 255, 1.0)

clock = pygame.time.Clock()

surface = pygame.display.get_surface()

font = pygame.font.Font(config["font"], 40)

load_level("maps/main_menu.json")


while(True):
    clock.tick(FPS)
    clearBuffer()
    camera.place()

    orientation = camera.get_orientation()
    player_coord = player.get_grid_coordinates()
    obj = level.get_object_below(player_coord)

    # eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_q:
                camera.gradual_rotateLeft()
            if event.key == K_e:
                camera.gradual_rotateRight()

            # relative movements
            # mata de codigo, cuidado al entrar
            if not player.is_falling() and not player.is_moving():
                if orientation == 0:
                    if event.key == K_UP:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                            camera.move_neg_x()
                        else:
                            player.rise_neg_x()
                            camera.rise_neg_x()
                    elif event.key == K_DOWN:
                        if not player.can_rise_x(level):
                            player.move_x()
                            camera.move_x()
                        else:
                            player.rise_x()
                            camera.rise_x()
                    elif event.key == K_LEFT:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                            camera.move_neg_y()
                        else:
                            player.rise_neg_y()
                            camera.rise_neg_y()
                    elif event.key == K_RIGHT:
                        if not player.can_rise_y(level):
                            player.move_y()
                            camera.move_y()
                        else:
                            player.rise_y()
                            camera.rise_y()
                elif orientation == 1:
                    if event.key == K_UP:
                        if not player.can_rise_y(level):
                            player.move_y()
                            camera.move_y()
                        else:
                            player.rise_y()
                            camera.rise_y()
                    elif event.key == K_DOWN:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                            camera.move_neg_y()
                        else:
                            player.rise_neg_y()
                            camera.rise_neg_y()
                    elif event.key == K_LEFT:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                            camera.move_neg_x()
                        else:
                            player.rise_neg_x()
                            camera.rise_neg_x()
                    elif event.key == K_RIGHT:
                        if not player.can_rise_x(level):
                            player.move_x()
                            camera.move_x()
                        else:
                            player.rise_x()
                            camera.rise_x()
                elif orientation == 2:
                    if event.key == K_UP:
                        if not player.can_rise_x(level):
                            player.move_x()
                            camera.move_x()
                        else:
                            player.rise_x()
                            camera.rise_x()
                    elif event.key == K_DOWN:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                            camera.move_neg_x()
                        else:
                            player.rise_neg_x()
                            camera.rise_neg_x()
                    elif event.key == K_LEFT:
                        if not player.can_rise_y(level):
                            player.move_y()
                            camera.move_y()
                        else:
                            player.rise_y()
                            camera.rise_y()
                    elif event.key == K_RIGHT:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                            camera.move_neg_y()
                        else:
                            player.rise_neg_y()
                            camera.rise_neg_y()
                elif orientation == 3:
                    if event.key == K_UP:
                        if not player.can_rise_neg_y(level):
                            player.move_neg_y()
                            camera.move_neg_y()
                        else:
                            player.rise_neg_y()
                            camera.rise_neg_y()
                    elif event.key == K_DOWN:
                        if not player.can_rise_y(level):
                            player.move_y()
                            camera.move_y()
                        else:
                            player.rise_y()
                            camera.rise_y()
                    elif event.key == K_LEFT:
                        if not player.can_rise_x(level):
                            player.move_x()
                            camera.move_x()
                        else:
                            player.rise_x()
                            camera.rise_x()
                    elif event.key == K_RIGHT:
                        if not player.can_rise_neg_x(level):
                            player.move_neg_x()
                            camera.move_neg_x()
                        else:
                            player.rise_neg_x()
                            camera.rise_neg_x()

            if event.key == K_SPACE:
                if isinstance(obj, OptionTile):
                    if obj.get_action() == "load":
                        load_level(obj.get_param())
                    elif obj.get_action() == "quit":
                        exit()

    keys = pygame.key.get_pressed()

    # lógica del nivel
    if obj is None or isinstance(obj, Shard) or (isinstance(obj, FallingTile) and not obj.stable and obj.stable is not None):
        player.fall(player_coord, level)

    if isinstance(obj, FallingTile):
        obj.fall()
    elif isinstance(obj, FinishTile) and shardcount == total_shards:
        load_level("maps/victory.json")
    elif isinstance(obj, OptionTile) and not obj.highlighted():
        obj.highlight()

    if shardcount == total_shards:
        for finish in finishes:
            finish.activate()

    if player_coord[2] <= -100:
        load_level("maps/failure.json")

    for shard in shards:
        if shard.get_grid_coordinates() == player_coord:
            level.remove_object_at(shard.get_grid_coordinates())
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

    for option in options:
        option.update(player)

    # dibuja luces
    glLightfv(GL_LIGHT0, GL_POSITION, [-1000, -250, 1000])

    # dibuja mapa
    level.draw()

    # dibuja modelos
    for shard in shards:
        shard.draw()

    # dibuja texto de progreso
    if level.get_tag() == "menu":
        position = (3000, 5000, player_coord[2] * 80)
        text_surface = font.render("Select with spacebar", True, (0.0, 0.0, 0.0, 255), (210, 224, 224, 0))
        text_date = pygame.image.tostring(text_surface, "RGBA", True)
        GL.glRasterPos3d(*position)
        GL.glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, text_date)
    elif level.get_tag() == "game":
        progress_string = str(shardcount) + "/" + str(total_shards) + " shards collected"
        position = (3000, 2000, player_coord[2] * 80)
        text_surface = font.render(progress_string, True, (0.0, 0.0, 0.0, 255), (210, 224, 224, 0))
        text_date = pygame.image.tostring(text_surface, "RGBA", True)
        GL.glRasterPos3d(*position)
        GL.glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, text_date)
    elif level.get_tag() == "victory":
        position = (3000, 5000, player_coord[2] * 80)
        text_surface = font.render("You beat the level!", True, (0.0, 0.0, 0.0, 255), (210, 224, 224, 0))
        text_date = pygame.image.tostring(text_surface, "RGBA", True)
        GL.glRasterPos3d(*position)
        GL.glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, text_date)
    elif level.get_tag() == "fail":
        position = (3000, 5000, player_coord[2] * 80)
        text_surface = font.render("You fell off :(", True, (0.0, 0.0, 0.0, 255), (210, 224, 224, 0))
        text_date = pygame.image.tostring(text_surface, "RGBA", True)
        GL.glRasterPos3d(*position)
        GL.glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, text_date)

    player.draw()

    pygame.display.flip()
