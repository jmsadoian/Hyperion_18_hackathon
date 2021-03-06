# Import statements
import pygame
from pygame.locals import *
import sys
import copy
# File imports
import constants
import HistoryGen
import tile
import WorldGen
import drawing


def main():
    # Start pygame and create the display at a start of 700x700
    pygame.init()
    pygame.display.set_caption("RPG Storyteller")
    display = pygame.display.set_mode((1200, 700), 0, 32)
    # Create map
    tile_map = tile.generate_tilemap(constants.WORLDSIZE)
    # Generate the first tilemap
    WorldGen.generate_terrain(tile_map)
    # Variables
    label_list = drawing.yes_labels()
    # --------------------------------------------
    # -------------- MAP -------------------------
    # --------------------------------------------
    loop_var = True
    while loop_var:
        # Draw map, and option squares
        drawing.draw_geography(tile_map, display)
        pygame.draw.rect(display, constants.GRAY, constants.SQUAREOFTRUTH)
        display.blit(label_list[0], (820, 140))
        display.blit(label_list[1], (810, 475))
        pygame.draw.line(display, constants.BLACK, (700, 350), (1200, 350))
        # Look through all events
        for event in pygame.event.get():
            # Quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # User clicks either yes or no to finish making maps or move on
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 700:
                    if mouse_y > 350:
                        WorldGen.generate_terrain(tile_map)
                    else:
                        loop_var = False
        pygame.display.update()
    # Generate history and then loop until user is also satisfied with that
    backup_map = copy.deepcopy(tile_map)
    HistoryGen.start_making_history(constants.TURNS, constants.CIVS, tile_map)
    owner_list = drawing.set_influence_colors(tile_map)
    # ----------------------------------------
    # -----------------HISTORY ---------------
    # ----------------------------------------
    # Loop through until the user is happy with the map
    loop_var = True
    while loop_var:
        # Draw map, and option squares
        drawing.draw_geography(tile_map, display)
        drawing.draw_civilization(tile_map, display)
        drawing.draw_influence(tile_map, display, owner_list)
        pygame.draw.rect(display, constants.GRAY, constants.SQUAREOFTRUTH)
        display.blit(label_list[0], (820, 140))
        display.blit(label_list[1], (810, 475))
        pygame.draw.line(display, constants.BLACK, (700, 350), (1200, 350))
        # Look through all events
        for event in pygame.event.get():
            # Quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # User clicks either yes or no to finish making maps or move on
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 700:
                    if mouse_y > 350:
                        tile_map = copy.deepcopy(backup_map)
                        HistoryGen.start_making_history(constants.TURNS, constants.CIVS, tile_map)
                        owner_list = drawing.set_influence_colors(tile_map)
                    else:
                        loop_var = False
        pygame.display.update()
    # Clear the yes/no labels, generate a history given the tile_map and develop the owners of the colors
    label_list.clear()
    town_list = drawing.get_town_list(tile_map)
    # ----------------------------------
    # -------------MAIN LOOP -----------
    # ----------------------------------
    # Main "game" loop, where the user can inspect specific squares
    while True:
        # Draw geography, civilizations, influence, then the info box
        drawing.draw_geography(tile_map, display)
        drawing.draw_civilization(tile_map, display)
        drawing.draw_influence(tile_map, display, owner_list)
        pygame.draw.rect(display, constants.GRAY, constants.SQUAREOFTRUTH)
        # Look through all events
        for event in pygame.event.get():
            # Quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # User clicks a square it gives information
            if event.type == MOUSEBUTTONDOWN:
                tile_x, tile_y = drawing.get_indices(constants.WIDTH, constants.HEIGHT, len(tile_map))
                if tile_y >= len(tile_map) or tile_x >= len(tile_map):
                    # Generate hook
                    label_list = drawing.draw_hooks(display, town_list)
                else:
                    label_list = drawing.tile_info(tile_map[tile_y][tile_x])
        # Draw the text when tile clicked
        drawing.draw_text(display, label_list)
        pygame.display.update()


if __name__ == "__main__":
    main()
