#game_functions.py
import sys
import pygame
from launcher import Launcher
from alien import Alien
from time import sleep



def check_keydown_events(event, game_settings, screen, ship, stats, sb, launchers, aliens):
    """Respond to keydown presses."""
    if event.key == pygame.K_RIGHT:
        #Move ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #Move ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #Fire launcher
        fire_launcher(game_settings, screen, ship, launchers)
    elif event.key == pygame.K_p:
        start_game(game_settings, screen, stats, sb, ship, aliens, launchers)
    elif event.key == pygame.K_q:
        record_high_scores(stats, sb)
        sys.exit()


def check_keyup_presses(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        #Move ship to the left
        ship.moving_left = False


def record_high_scores(stats, sb):
    filename = 'high_scores.txt'
    with open(filename, 'a') as high_scores:
        high_scores.write(str(sb.stats.high_score) + "\n")

def read_in_high_scores():
    filename = 'high_scores.txt'
    with open(filename, 'r') as high_scores:
        max_score = 0
        for score in high_scores:
            num_score = int(score)
            if num_score > max_score:
                max_score = num_score
        return max_score

def start_game(game_settings, screen, stats, sb, ship, aliens, launchers):
    """Start game here."""
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    #Reset the scoreboard image
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    #Empty the list of aliens and launchers
    aliens.empty()
    launchers.empty()

    #Create a new fleet and center the ship
    create_fleet(game_settings, screen, ship, aliens)
    ship.center_ship()


def check_play_button(game_settings, screen, stats, sb, play_button, ship, aliens, launchers, mouse_x, mouse_y):
    """Start a new game when the player clicks play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        game_settings.initialize_dynamic_settings()
        start_game(game_settings, screen, stats, sb, ship, aliens, launchers)


def check_events(game_settings, screen, stats, sb, play_button, ship, aliens, launchers):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            record_high_scores(stats,sb)
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, sb,  play_button, ship, aliens, launchers, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, stats, sb, launchers, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_presses(event, ship)


def update_launchers(game_settings, screen, stats, sb, ship, aliens, launchers):
    """Update launcher positions and get rid of old launchers."""
    launchers.update()
    #Get rid of launchers above the alien fleet
    for launcher in launchers.copy():
        if launcher.rect.bottom <= 0:
            launchers.remove(launcher)
    #Check for any launchers that have blasted aliens
    check_launcher_alien_collisions(game_settings, screen,stats, sb, ship, aliens, launchers)

def check_launcher_alien_collisions(game_settings,screen,stats, sb, ship, aliens,launchers):
    collisions = pygame.sprite.groupcollide(launchers, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #Destroy the existing launchers and create a new fleet
        launchers.empty()
        game_settings.increase_speed()

        #Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(game_settings, screen, ship, aliens)


def fire_launcher(game_settings, screen, ship, launchers):
    """Fire a launcher if limit not reached yet."""
    #Create a new launcher and add it to the launchers group
    if len(launchers) < game_settings.launchers_allowed:
        new_launcher = Launcher(game_settings, screen, ship)
        launchers.add(new_launcher)


def get_num_rows(game_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_num_aliens_x(game_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    #Spacing b/w aliens == 1 alien width (alien_rect)
    available_space_x = game_settings.screen_width - 2 * alien_width
    num_aliens_x = int(available_space_x / (2 * alien_width))
    return num_aliens_x

def create_alien(game_settings, screen, aliens, alien_number, row_number):
    """"Create an alien and place it in the row."""
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 *  alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(game_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(game_settings, screen)
    num_aliens_x = get_num_aliens_x(game_settings, alien.rect.width)
    num_rows = get_num_rows(game_settings, ship.rect.height, alien.rect.height)
    #Create the fleet of aliens
    for row_number in range(num_rows):
        #Create an alien and place it in row
        for alien_number in range(num_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(game_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break

def change_fleet_direction(game_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def update_aliens(game_settings, screen, stats, sb, ship, aliens, launchers):
    """Check if fleet is at edge, and update positions of all aliens in the fleet."""
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    #Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, screen, stats, sb, ship, aliens, launchers)

    #Validate when aliens reach bottom of screen
    check_aliens_bottom(game_settings, screen,  stats, sb, ship, aliens, launchers)

def check_aliens_bottom(game_settings, screen, stats, sb, ship, aliens, launchers):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Equiv to ship hit
            ship_hit(game_settings, screen, stats, sb, ship, aliens, launchers)



def ship_hit(game_settings, screen, stats, sb, ship, aliens, launchers):
    """Respond to ship being hit by alien."""
    #Decrement ships left
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #Update scoreboard
        sb.prep_ships()

        #Empty the list of aliens and launchers
        aliens.empty()
        launchers.empty()

        #Create new fleet and center the ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()



def update_screen(game_settings, stats, sb, screen, ship, aliens, launchers, play_button):
    """Update the images on screen and flip them to new screen."""
    screen.fill(game_settings.bg_color)

    #Redraw all launchers behind the ship and the aliens
    for launcher in launchers.sprites():
        launcher.draw_launcher()

    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()
