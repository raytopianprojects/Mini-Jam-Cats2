import pygame
import asyncio
import random


class Player:
    def __init__(self):
        self.sprite = random.randint(0, 3)
        self.pos_x = None
        self.pos_y = None


player = Player()


def generate_grid():
    # Generate blank tile map
    tile_map = []
    for y in range(10):
        tile_map.append([])
        for x in range(10):
            tile_map[y].append(0)

    current_tile_y = random.randint(0, 9)
    current_tile_x = random.randint(0, 9)

    tile_map[current_tile_y][current_tile_x] = 1

    floor_tiles = 40
    floor_tiles_count = 0
    _exit = 0
    item_count = 0
    players = 0

    # Generate floor tiles
    while floor_tiles_count <= floor_tiles:
        movement = random.randint(0, 1)

        # Choose if were moving on the x or y axis
        if movement == 0:
            current_tile_y += random.randint(-1, 1)

            # Make sure we don't go out of bounds
            if 0 > current_tile_y:
                current_tile_y = 0
            elif current_tile_y > 9:
                current_tile_y = 9

            # If the tile is currently a wall make it a floor
            if tile_map[current_tile_y][current_tile_x] == 0:
                tile_map[current_tile_y][current_tile_x] = 1
                floor_tiles_count += 1

        else:
            current_tile_x += random.randint(-1, 1)

            # Make sure we don't go out of bounds
            if 0 > current_tile_x:
                current_tile_x = 0
            elif current_tile_x > 9:
                current_tile_x = 9

            # If the tile is currently a wall make it a floor
            if tile_map[current_tile_y][current_tile_x] == 0:
                tile_map[current_tile_y][current_tile_x] = 1
                floor_tiles_count += 1

    while _exit == 0 or players == 0 or item_count < 5:
        # Attempt to place the exit
        exit_tile_y = random.randint(0, 9)
        exit_tile_x = random.randint(0, 9)

        try:
            if tile_map[exit_tile_y][exit_tile_x] == 1 and _exit == 0:
                if tile_map[exit_tile_y + 1][exit_tile_x] == 0 and tile_map[exit_tile_y - 1][exit_tile_x] == 0:
                    pass
                elif tile_map[exit_tile_y][exit_tile_x + 1] == 0 and tile_map[exit_tile_y][exit_tile_x - 1] == 0:
                    pass
                else:
                    tile_map[exit_tile_y][exit_tile_x] = 2
                    _exit += 1
        except:
            pass

        # Attempt to place other stuff
        item_tile_y = random.randint(0, 9)
        item_tile_x = random.randint(0, 9)

        if tile_map[item_tile_y][item_tile_x] == 1 and item_count < 5:
            tile_map[item_tile_y][item_tile_x] = random.randint(3, 10)
            item_count += 1

        player_tile_y = random.randint(0, 9)
        player_tile_x = random.randint(0, 9)
        if tile_map[player_tile_y][player_tile_x] == 1 and players == 0:
            player.pos_y = player_tile_y
            player.pos_x = player_tile_x
            print(player.pos_y, player.pos_x)
            tile_map[player_tile_y][player_tile_x] = 12
            players += 1

    return tile_map


async def main():
    pygame.init()
    font = pygame.font.Font("PublicPixel-z84yD.ttf", 14)
    surface = pygame.display.set_mode((320, 340))
    pygame.mixer.music.load("Coy Koi.mp3")
    pygame.mixer.music.play(loops=-1)
    tile_map = pygame.image.load("Sprite-0001.png").convert_alpha()

    tiles = []
    for y in range(4):
        for x in range(4):
            tiles.append(tile_map.subsurface(x * 32, y * 32, 32, 32))

    tile_grid = generate_grid()
    level = 0
    steps = 0
    collectables = 5

    while True:
        surface.fill((228, 219, 214))

        if level < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    try:
                        if event.key == pygame.K_w and event.key == pygame.K_UP:
                            if 0 <= player.pos_y <= 9 and tile_grid[player.pos_y - 1][player.pos_x] != 0:
                                if tile_grid[player.pos_y - 1][player.pos_x] == 2 and collectables == 0:
                                    level += 1
                                    tile_grid = generate_grid()
                                    collectables = 5
                                else:
                                    if tile_grid[player.pos_y - 1][player.pos_x] == 2:
                                        pass
                                    else:
                                        if tile_grid[player.pos_y - 1][player.pos_x] > 1:
                                            collectables -= 1
                                        tile_grid[player.pos_y][player.pos_x] = 1
                                        tile_grid[player.pos_y - 1][player.pos_x] = 12
                                        player.pos_y -= 1

                                steps += 1

                        if event.key == pygame.K_s and event.key == pygame.K_DOWN:
                            if 0 <= player.pos_y <= 9 and tile_grid[player.pos_y + 1][player.pos_x] != 0:
                                if tile_grid[player.pos_y + 1][player.pos_x] == 2 and collectables == 0:
                                    level += 1
                                    tile_grid = generate_grid()
                                    collectables = 5

                                else:
                                    if tile_grid[player.pos_y + 1][player.pos_x] == 2:
                                        pass
                                    else:
                                        if tile_grid[player.pos_y + 1][player.pos_x] > 1:
                                            collectables -= 1
                                        tile_grid[player.pos_y][player.pos_x] = 1
                                        tile_grid[player.pos_y + 1][player.pos_x] = 12
                                        player.pos_y += 1
                                steps += 1

                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            if 0 <= player.pos_y <= 9 and tile_grid[player.pos_y][player.pos_x + 1] != 0:
                                if tile_grid[player.pos_y][player.pos_x + 1] == 2 and collectables == 0:
                                    level += 1
                                    tile_grid = generate_grid()
                                    collectables = 5

                                else:
                                    if tile_grid[player.pos_y][player.pos_x + 1] == 2:
                                        pass
                                    else:
                                        if tile_grid[player.pos_y][player.pos_x + 1] > 1:
                                            collectables -= 1
                                        tile_grid[player.pos_y][player.pos_x] = 1
                                        tile_grid[player.pos_y][player.pos_x + 1] = 12
                                        player.pos_x += 1
                                steps += 1

                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            if 0 <= player.pos_x <= 9 and tile_grid[player.pos_y][player.pos_x - 1] != 0:
                                if tile_grid[player.pos_y][player.pos_x - 1] == 2 and collectables == 0:
                                    level += 1
                                    tile_grid = generate_grid()
                                    collectables = 5

                                else:
                                    if tile_grid[player.pos_y][player.pos_x - 1]  == 2:
                                        pass
                                    else:
                                        if tile_grid[player.pos_y][player.pos_x - 1] > 1:
                                            collectables -= 1
                                        tile_grid[player.pos_y][player.pos_x] = 1
                                        tile_grid[player.pos_y][player.pos_x - 1] = 12
                                        player.pos_x -= 1
                                steps += 1

                    except:
                        pass

            for y, row in enumerate(tile_grid):
                for x, tile in enumerate(row):
                    if tile == 0:
                        surface.blit(tiles[1], (x * 32, y * 32))
                    elif tile == 1:
                        continue
                    elif tile == 2:
                        surface.blit(tiles[14], (x * 32, y * 32))
                    elif tile == 12:
                        surface.blit(tiles[player.sprite * 4], (player.pos_x * 32, player.pos_y * 32))
                    elif tile == 3:
                        surface.blit(tiles[2], (x * 32, y * 32))
                    elif tile == 4:
                        surface.blit(tiles[3], (x * 32, y * 32))
                    elif tile == 5:
                        surface.blit(tiles[6], (x * 32, y * 32))
                    elif tile == 6:
                        surface.blit(tiles[7], (x * 32, y * 32))
                    elif tile == 7:
                        surface.blit(tiles[10], (x * 32, y * 32))
                    elif tile == 8:
                        surface.blit(tiles[11], (x * 32, y * 32))
                    elif tile == 9:
                        surface.blit(tiles[11], (x * 32, y * 32))
                    elif tile == 10:
                        surface.blit(tiles[15], (x * 32, y * 32))

            text_surface = font.render(f"Steps {steps}", (130, 130), (0, 0, 0))
            surface.blit(text_surface, (0, 320))

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            text_surface = font.render(f"You won! It took you", (130, 130),
                                       (0, 0, 0))

            text_surface2 = font.render(f"{steps} steps to collect it", (130, 130), (0, 0, 0))

            text_surface3 = font.render("all. Good Job!!! :)", (130, 130), (0, 0, 0))
            text_surface4 = font.render("Thanks so much for", (130, 130), (0, 0, 0))
            text_surface5 = font.render("playing!", (130, 130), (0, 0, 0))
            text_surface6 = font.render("You're awesome!!!", (130, 130), (0, 0, 0))

            surface.blit(text_surface, (1, 32))
            surface.blit(text_surface2, (1, 48))
            surface.blit(text_surface3, (1, 64))
            surface.blit(text_surface4, (52, 96))
            surface.blit(text_surface5, (52, 112))
            surface.blit(text_surface6, (52, 144 * 2))
            surface.blit(tiles[player.sprite * 4], (52, 144))

        pygame.display.flip()
        await asyncio.sleep(0)


asyncio.run(main())
