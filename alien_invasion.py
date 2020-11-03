#alien_invasion.py
import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame.sprite import Group
import game_functions as gf

def run_game():
    #Initialize game and create a screen object.
    pygame.init()

    game_settings = Settings()
    stats = GameStats(game_settings)
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    sb = Scoreboard(game_settings, screen, stats)


    pygame.display.set_caption("Alien Invasion!")

    play_button = Button(game_settings, screen, "Play Game!")

    ship = Ship(game_settings, screen)


    #Make a group to store the launchers in and a separate group for the alien fleet
    launchers = Group()
    aliens = Group()

    #Create a fleet of aliens
    gf.create_fleet(game_settings, screen, ship, aliens)


    #Starting the game's main loop
    while True:
        gf.check_events(game_settings, screen, stats, sb,  play_button, ship, aliens, launchers)
        if stats.game_active:
            ship.update()
            gf.update_launchers(game_settings, screen, stats, sb, ship, aliens, launchers)
            gf.update_aliens(game_settings, screen, stats, sb, ship, aliens, launchers)
            #Draw new screen at end of loop every time
        gf.update_screen(game_settings, stats, sb, screen, ship, aliens, launchers, play_button)



run_game()
