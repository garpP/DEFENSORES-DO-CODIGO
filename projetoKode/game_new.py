import pgzrun
from pygame import Rect
import random
import math

WIDTH = 1280
HEIGHT = 720
TITLE = "Code Defenders "


GRAVITY = 0.5
JUMP_STRENGTH = 12
PLAYER_SPEED = 4


TILE_SIZE = 33


game_state = "menu"
current_level = 1


music_enabled = True
music_playing = False
mouse_pos = (0, 0)


btn_start = Rect((WIDTH//2 - 100, 300), (200, 50))
btn_audio = Rect((WIDTH//2 - 100, 380), (200, 50))
btn_exit = Rect((WIDTH//2 - 100, 460), (200, 50))

player = None
enemies = []
tiles = []
terminals = []  
seniors = []  
barriers = []  
camera_x = 0
camera_y = 0
game_state = "menu"
background_image = None  
background_width = 0
current_level = 1  
terminal_puzzle_solved = False  
showing_terminal = False  
showing_error_message = False  
showing_senior_dialogue = False  
current_senior_type = 29  
dialogue_page = 0  
dialogue_max_pages = 11  
balloon_float_offset = 0  
balloon_animation_timer = 0  
selected_option = 0  
key_cooldown = 0  


class Tile:
    """Represents a ground/platform tile using PgZero screen.blit"""
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.width = TILE_SIZE 
        self.height = 124   
        self.rect = Rect(self.x, self.y, self.width, self.height)
        
            
        from level_data import TILE_COLLISION
        
        if not TILE_COLLISION.get(tile_type, False):
                
            self.collision_rect = Rect(-1000, -1000, 0, 0)
        else:
                
            collision_width = 240
            collision_height = 20  
            
          
            if tile_type in [1, 2, 3, 26, 27, 28]:
                collision_y = self.y + 60  
            else:
                collision_y = self.y  
            
            self.collision_rect = Rect(self.x, collision_y, collision_width, collision_height)
        
     
        self.sprite_x = 0  
        self.sprite_y = 0  
        self.sprite_w = 33  
        self.sprite_h = 21  
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        
        from level_data import TILE_SPRITES, TILE_Y_OFFSET, TILE_AUTO_DECORATION
        
      
        y_offset = TILE_Y_OFFSET.get(self.tile_type, 0)
        
      
        if self.tile_type == 4:
            y_offset += 50  
        try:
            if self.tile_type in TILE_SPRITES:
                sprite_name = TILE_SPRITES[self.tile_type]
             
                screen.blit(sprite_name, (screen_x, screen_y + y_offset))
                
           
                if self.tile_type in TILE_AUTO_DECORATION:
                    deco_type, deco_offset = TILE_AUTO_DECORATION[self.tile_type]
                    if deco_type in TILE_SPRITES:
                        deco_sprite = TILE_SPRITES[deco_type]
                        deco_y_offset = TILE_Y_OFFSET.get(deco_type, 0)
                        screen.blit(deco_sprite, (screen_x, screen_y + deco_offset + deco_y_offset))
        except:
            pass  


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 79   
        self.height = 134  
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.hp = 5
        self.max_hp = 5
        self.invincible_timer = 0
        self.state = "fall"  
        self.animation_frame = 0
        self.animation_timer = 0
        self.landing_timer = 0  
        self.is_sprinting = False  
        self.is_attacking = False  
        self.attack_timer = 0  
        self.attack_frame_current = 0  
        self.damage_timer = 0  
        self.is_dashing = False  
        self.dash_timer = 0  
        self.dash_direction = 0  
        self.dash_frame = 0 
        self.rect = Rect(self.x, self.y, self.width, self.height)
    
    def move(self, direction, is_sprinting=False):
        self.is_sprinting = is_sprinting  
        if direction != 0:
            speed = PLAYER_SPEED * 1.5 if is_sprinting else PLAYER_SPEED
            self.velocity_x = direction * speed
            self.facing_right = direction > 0
        else:
            self.velocity_x = 0
    
    def jump(self, is_sprinting=False):
        if self.on_ground:
           
            jump_power = JUMP_STRENGTH * 1.3 if is_sprinting else JUMP_STRENGTH
            self.velocity_y = -jump_power
    
    def dash(self, direction):
        """Executa dash (Q = esquerda, E = direita)"""
        if not self.is_dashing and self.on_ground:
            self.is_dashing = True
            self.dash_timer = 0.4 
            self.dash_direction = direction
            self.dash_frame = 0
            
           
            self.x += direction * 80
            self.rect.x = self.x
    
    def attack(self):
        """Inicia ataque - cada clique mostra uma sprite diferente"""
        if not self.is_attacking and self.on_ground:
            self.is_attacking = True
            self.attack_timer = 0.2  
            
            self.attack_frame_current = (self.attack_frame_current + 1) % 3
            
           
            attack_range = 150  
            for enemy in enemies:
               
                if self.facing_right:
                   
                    is_in_direction = enemy.x > self.x
                else:
                  
                    is_in_direction = enemy.x < self.x
                
                enemy_distance = abs(self.x - enemy.x)
                
                if is_in_direction and enemy_distance < attack_range and abs(self.y - enemy.y) < 150:
                   
                    enemy.take_damage(1)
    
    def update(self, dt, tiles):
      
        self.velocity_y += GRAVITY
        
      
        if self.velocity_y > 15:
            self.velocity_y = 15
        
      
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        
        
        self.x += self.velocity_x
        self.rect.x = self.x
        
       
        for tile in tiles:
            if self.rect.colliderect(tile.collision_rect):
                if self.velocity_x > 0:
                    self.x = tile.collision_rect.left - self.width
                elif self.velocity_x < 0:
                    self.x = tile.collision_rect.right
                self.rect.x = self.x
                self.velocity_x = 0
        
      
        self.y += self.velocity_y
        self.rect.y = self.y
        self.on_ground = False
        
      
        for tile in tiles:
            if self.rect.colliderect(tile.collision_rect):
                if self.velocity_y > 0:
                  
                    self.y = tile.collision_rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                  
                    if self.state == "fall":
                        self.state = "landing"
                        self.landing_timer = 0.1  
                elif self.velocity_y < 0:
                    
                    self.y = tile.collision_rect.bottom
                    self.velocity_y = 0
                self.rect.y = self.y
        
        
        if self.landing_timer > 0:
            self.landing_timer -= dt
            if self.landing_timer <= 0:
                self.landing_timer = 0
        
       
        if self.attack_timer > 0:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.is_attacking = False  
        
      
        if self.damage_timer > 0:
            self.damage_timer -= dt
        
      
        if self.dash_timer > 0:
            self.dash_timer -= dt
            
            if self.dash_timer <= 0.2:
                self.dash_frame = 1
            if self.dash_timer <= 0:
                self.is_dashing = False
               
                if self.dash_direction == -1:
                 
                    self.facing_right = True
                else:
                
                    self.facing_right = False
        

        if self.is_dashing:
            self.state = "dash"

        elif self.landing_timer > 0:
            self.state = "landing"
       
        elif self.is_attacking and self.on_ground:
            self.state = "attack"
        
        elif not self.on_ground:
           
            if self.velocity_y < 0:
                self.state = "jump"  
            else:
                self.state = "fall"  
        else:
            if self.velocity_x != 0:
                self.state = "walk"
            else:
                self.state = "idle"
        
       
        self.animation_timer += dt
        if self.state == "idle" and self.animation_timer > 0.3:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 3  
        elif self.state == "walk":
        
            walk_speed = 0.075 if self.is_sprinting else 0.15
            if self.animation_timer > walk_speed:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 4
        elif self.state == "jump":
          
            self.animation_frame = 0
        elif self.state == "fall":
           
            self.animation_frame = 0
    
    def take_damage(self, amount):
        if self.invincible_timer <= 0:
            self.hp -= amount
            self.hurt_timer = 0.1
            self.invincible_timer = 0.2
            self.damage_timer = 0.4  
            
           
            if self.facing_right:
                self.x -= 10 
            else:
                self.x += 10  
            self.rect.x = self.x
            
            if self.hp < 0:
                self.hp = 0
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
      
        try:
            direction = "right" if self.facing_right else "left"
            
         
            if self.damage_timer > 0:
                screen.blit(f"player/damage_{direction}_0", (screen_x, screen_y))
            elif self.state == "dash":
              
                if self.dash_direction == -1:
                    
                    dash_sprite = f"player/playerdash{self.dash_frame + 1}l"
                else:
                   
                    if self.dash_frame == 0:
                        dash_sprite = "player/playerdashr1"
                    else:
                        dash_sprite = "player/playerdashr"
                screen.blit(dash_sprite, (screen_x, screen_y))
            elif self.state == "attack":
              
                screen.blit(f"player/attack_{direction}_{self.attack_frame_current}", (screen_x, screen_y))
            elif self.state == "walk":
                frame = self.animation_frame % 3 
                screen.blit(f"player/walk_{direction}_{frame}", (screen_x, screen_y))
            elif self.state == "jump":
                
                screen.blit(f"player/jump_{direction}_0", (screen_x, screen_y))
            elif self.state == "fall":
               
                screen.blit(f"player/jump_{direction}_1", (screen_x, screen_y))
            elif self.state == "landing":
               
                screen.blit(f"player/jump_{direction}_2", (screen_x, screen_y))
            elif self.state == "idle":
               
                frame = self.animation_frame % 3 + 1  
                suffix = "r" if self.facing_right else "l"
                screen.blit(f"player/stop{frame}{suffix}", (screen_x, screen_y))
        except Exception as e:
           
            screen.draw.filled_rect(Rect(screen_x, screen_y, self.width, self.height), (100, 150, 255))
            
            

class Terminal:
    def __init__(self, x, y, column_x):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.column_x = column_x  
    
    def is_near_player(self, player):
        """Verifica se player está perto"""
        distance = abs(player.x - self.x)
        return distance < 150 and abs(player.y - self.y) < 150
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        try:
            screen.blit('tiles/terminal', (screen_x, screen_y))
        except:
            screen.draw.filled_rect(Rect(screen_x, screen_y, 50, 50), (100, 100, 100))

class Senior:
    """NPC Senior o Ancião que dá dicas sobre o jogo"""
    def __init__(self, x, y, senior_type=29):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.animation_frame = 0
        self.animation_timer = 0
        self.facing_right = True
        self.senior_type = senior_type  # 29, 2901, 2902, 2903
    
    def is_near_player(self, player):
        """Verifica se player está perto"""
        distance = abs(player.x - self.x)
        return distance < 150 and abs(player.y - self.y) < 150
    
    def update(self, dt):
        """Atualiza animação"""
        self.animation_timer += dt
        if self.animation_timer > 0.5:  
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 3  # 3 frames: 0, 1, 2
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        try:
            
            direction = "r" if self.facing_right else ""
            
            if self.animation_frame == 0:
                sprite_name = f'tiles/senioranciao{direction}'
            elif self.animation_frame == 1:
                sprite_name = f'tiles/senioranciao1{direction}'
            else:  
                sprite_name = f'tiles/senioranciao2{direction}'
            
            screen.blit(sprite_name, (screen_x, screen_y))
        except Exception as e:
           
            screen.draw.filled_rect(Rect(screen_x, screen_y, self.width, self.height), (50, 200, 50))




class Barrier:
    """Barreira que bloqueia passagem entre níveis até puzzle ser resolvido"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 150
        self.is_broken = False
        self.collision_rect = Rect(self.x, self.y, self.width, self.height)
    
    def break_barrier(self):
        """Quebra a barreira, removendo colisão"""
        self.is_broken = True
        self.collision_rect = Rect(-1000, -1000, 0, 0)  # Remove colisão
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        try:
            if self.is_broken:
                sprite_name = 'tiles/quebrada'
            else:
                sprite_name = 'tiles/barreira'
            
            screen.blit(sprite_name, (screen_x, screen_y))
        except:
          
            color = (100, 100, 100) if self.is_broken else (200, 50, 50)
            screen.draw.filled_rect(Rect(screen_x, screen_y, self.width, self.height), color)


class Enemy:
    def __init__(self, x, y, patrol_range, column_x):
        self.x = x
        self.y = y
        self.start_x = x
        
        self.width = 196   
        self.height = 220  
        self.patrol_range = patrol_range
        self.speed = 2.0 
        self.direction = 1
        self.column_x = column_x  
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.animation_frame = 0
        self.animation_timer = 0
        self.active = False  
        self.velocity_y = 0  
        self.on_ground = False
        
       
        self.hp = 12  
        self.max_hp = 12
        self.state = "idle"  
        self.hurt_timer = 0  
        self.attack_timer = 0  
        self.attack_cooldown = 0  
        self.attack_damage_cooldown = 0  
        self.attack_frame_fixed = 0 
        self.is_attacking = False
        
      
        self.hibernating = False
        self.hibernate_timer = 0
        self.hibernate_duration = 15  
        self.damage_multiplier = 1  
    
    def take_damage(self, amount=1):
        """Recebe dano da player"""
        if not self.hibernating:
            self.hp -= amount
            self.hurt_timer = 0.3  
            self.state = "hurt"
            
            if self.hp <= 0:
               
                self.hp = 0
                self.hibernating = True
                self.hibernate_timer = self.hibernate_duration
                self.state = "hibernate"
    
    def update(self, dt, tiles):
       
        self.velocity_y += GRAVITY
        
       
        self.y += self.velocity_y
        self.rect.y = self.y
        self.on_ground = False
        
     
        for tile in tiles:
            if self.rect.colliderect(tile.collision_rect):
                if self.velocity_y > 0:  
                    self.y = tile.collision_rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  
                    self.y = tile.collision_rect.bottom
                    self.velocity_y = 0
                self.rect.y = self.y
        
       
        if self.hurt_timer > 0:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.state = "chase" if self.active else "idle"
        
      
        if self.attack_timer > 0:
            self.attack_timer -= dt
          
            if self.attack_damage_cooldown > 0:
                self.attack_damage_cooldown -= dt
            
          
            if player and self.is_attacking:
                distance_to_player = abs(player.x - self.x)
                if distance_to_player < 150 and abs(player.y - self.y) < 150:
                
                    if self.attack_damage_cooldown <= 0:
                        player.take_damage(1 * self.damage_multiplier) 
                        self.attack_damage_cooldown = 1.0  
            
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.state = "chase" if self.active else "idle"
              
                if self.hp <= 3:
                    self.attack_cooldown = 1.5  
                else:
                    self.attack_cooldown = 3.0  
        
       
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
     
        if self.hibernating:
            self.hibernate_timer -= dt
            if self.hibernate_timer <= 0:
                # Volta à vida
                self.hibernating = False
                self.hp = self.max_hp
                self.state = "idle"
            return  
        
        
        if player:
            distance = abs(player.x - self.x)
            if distance <= 600:  
                self.active = True
        
      
        if self.active and self.state != "hurt":
            
            if player:
                if player.x > self.x:
                    self.direction = 1
                else:
                    self.direction = -1
                
                
                if not self.is_attacking and self.attack_cooldown <= 0:
                    self.is_attacking = True
                    
                    
                    if self.hp <= 3:
                        self.attack_timer = 4.0  
                    else:
                        self.attack_timer = 2.0  
                    
                    self.attack_damage_cooldown = 0  
                    self.attack_frame_fixed = random.randint(0, 2)  
                    self.state = "attack"
                elif not self.is_attacking:
                
                    self.state = "chase"
                    self.x += self.speed * self.direction
                    self.rect.x = self.x
            

            self.animation_timer += dt
            if self.animation_timer > 0.5:  
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 3
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        

        try:
            direction = "right" if self.direction > 0 else "left"
            
            if self.hibernating:
                frame = self.animation_frame % 3
                sprite_name = f"enemies/lava_hibernate_left_{frame}"
            
            elif self.state == "hurt":        
                direction_letter = "r" if self.direction > 0 else "l"
                sprite_name = f"enemies/lavadamage{direction_letter}"
            
            elif self.state == "attack":
                sprite_name = f"enemies/lava_attack_{direction}_{self.attack_frame_fixed}"
            
            elif self.state == "idle":
                frame = self.animation_frame % 3
                sprite_name = f"enemies/lava_idle_{direction}_{frame}"
            
            else:
                frame = self.animation_frame % 3
                sprite_name = f"enemies/lava_walk_{direction}_{frame}"
            
            screen.blit(sprite_name, (screen_x, screen_y))
        except:
        
            screen.draw.filled_rect(Rect(screen_x, screen_y, self.width, self.height), (200, 50, 50))

            
            

def create_level():
    """Create level from map data"""
    global player, enemies, tiles, terminals, seniors, barriers, current_level, terminal_puzzle_solved, camera_x, camera_y
    

    from level_data import LEVEL_01, LEVEL_02, MAP_WIDTH, MAP_HEIGHT, TILE_SPACING, TILE_ROW_HEIGHT, EMPTY, ENEMY_SPAWN, PLAYER_SPAWN, GROUND_Y_BASE, TERMINAL, SENIOR_ANCIAO
    

    WATER_ENEMY_ID = 71
    

    if current_level == 1:
        current_map = LEVEL_01
    elif current_level == 2:
        current_map = LEVEL_02
    else:
        current_level = 1
        current_map = LEVEL_01
    
    terminal_puzzle_solved = False
    tiles = []
    enemies = []
    terminals = []
    seniors = []
    barriers = []
    player_spawn_x = 100
    player_spawn_y = 300
    

    barriers.append(Barrier(50, 400))
    barriers.append(Barrier(MAP_WIDTH * TILE_SPACING - 100, 400))
    
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_type = current_map[y][x]
            tile_y = GROUND_Y_BASE - ((MAP_HEIGHT - 1 - y) * TILE_ROW_HEIGHT)
            

            if tile_type == PLAYER_SPAWN:
                player_spawn_x = x * TILE_SPACING
                player_spawn_y = tile_y
            

            elif tile_type == ENEMY_SPAWN:
                enemy_x = x * TILE_SPACING
                enemy_y = tile_y
                enemies.append(Enemy(enemy_x, enemy_y, 80, x))
                

                surrounding_tile = None
                ignore_list = [EMPTY, PLAYER_SPAWN, ENEMY_SPAWN, WATER_ENEMY_ID, TERMINAL, SENIOR_ANCIAO, 2901, 2902, 2903]
                
                if x > 0 and current_map[y][x-1] not in ignore_list:
                    surrounding_tile = current_map[y][x-1]
                elif x < MAP_WIDTH - 1 and current_map[y][x+1] not in ignore_list:
                    surrounding_tile = current_map[y][x+1]
                
                if surrounding_tile is not None:
                    tiles.append(Tile(x * TILE_SPACING, tile_y, surrounding_tile))


            elif tile_type == WATER_ENEMY_ID:
                enemy_x = x * TILE_SPACING
                enemy_y = tile_y
 
                enemies.append(WaterEnemy(enemy_x, enemy_y, 80, x))
                

                surrounding_tile = None
                ignore_list = [EMPTY, PLAYER_SPAWN, ENEMY_SPAWN, WATER_ENEMY_ID, TERMINAL, SENIOR_ANCIAO, 2901, 2902, 2903]
                
                if x > 0 and current_map[y][x-1] not in ignore_list:
                    surrounding_tile = current_map[y][x-1]
                elif x < MAP_WIDTH - 1 and current_map[y][x+1] not in ignore_list:
                    surrounding_tile = current_map[y][x+1]
                
                if surrounding_tile is not None:
                    tiles.append(Tile(x * TILE_SPACING, tile_y, surrounding_tile))
            

            elif tile_type == TERMINAL:
                terminal_x = x * TILE_SPACING
                terminal_y = tile_y + 80
                terminals.append(Terminal(terminal_x, terminal_y, x))
            

            elif tile_type in [SENIOR_ANCIAO, 2901, 2902, 2903]:
                senior_x = x * TILE_SPACING
                senior_y = tile_y + 20
                seniors.append(Senior(senior_x, senior_y, tile_type))
            

            elif tile_type != EMPTY:
                tiles.append(Tile(x * TILE_SPACING, tile_y, tile_type))
                
            
    

    player = Player(player_spawn_x, player_spawn_y)
    

    camera_x = player.x - WIDTH // 3
    if camera_x < 0:
        camera_x = 0
    
    camera_y = player.y - HEIGHT // 2


def initialize_game():
    global game_state
    create_level()
    game_state = "playing"


def update(dt):
    global game_state, current_level, music_enabled, mouse_pos, game_state, camera_x, camera_y, showing_terminal, selected_option, terminal_puzzle_solved, key_cooldown, showing_error_message, showing_senior_dialogue, dialogue_page, balloon_float_offset, balloon_animation_timer, current_senior_type
    
    if game_state == "playing":
        if key_cooldown > 0:
            key_cooldown -= dt
        
        
        balloon_animation_timer += dt
        balloon_float_offset = math.sin(balloon_animation_timer * 2) * 10
        
        
        near_terminal = None
        for terminal in terminals:
            if terminal.is_near_player(player):
                near_terminal = terminal
                break
        
        
        if showing_error_message:
            
            if keyboard.y and key_cooldown <= 0:
                showing_error_message = False
                selected_option = 0  
                key_cooldown = 0.5  
            return  
        
        
        if showing_terminal:
            
            if key_cooldown <= 0:
                if keyboard.down:
                    selected_option = (selected_option + 1) % 3
                    key_cooldown = 0.2  
                elif keyboard.up:
                    selected_option = (selected_option - 1) % 3
                    key_cooldown = 0.2
            
            
            if keyboard.y and key_cooldown <= 0:
                key_cooldown = 0.5  
                if selected_option == 1:
                    terminal_puzzle_solved = True
                    
                    print(f"DEBUG: Terminal na coluna {near_terminal.column_x if near_terminal else 'None'}")
                    hibernated_count = 0
                    for enemy in enemies:
                        print(f"DEBUG: Inimigo na coluna {enemy.column_x}, distância: {abs(enemy.column_x - near_terminal.column_x) if near_terminal else 'N/A'}")
                        
                        if near_terminal and abs(enemy.column_x - near_terminal.column_x) <= 10:
                            enemy.hibernating = True
                            enemy.hibernate_timer = 20  
                            hibernated_count += 1
                            print(f"DEBUG: Inimigo hibernado! Total: {hibernated_count}")
                  
                    for barrier in barriers:
                        barrier.break_barrier()
                    showing_terminal = False
                    selected_option = 0  
                else:
                   
                    showing_error_message = True
                    showing_terminal = False
                   
                    for enemy in enemies:
                        if near_terminal and abs(enemy.column_x - near_terminal.column_x) <= 10:
                            enemy.hibernating = False  
                            enemy.hibernate_timer = 0
                            enemy.hp = enemy.max_hp  
                            enemy.damage_multiplier *= 2 
                            enemy.state = "chase"  
           
            elif keyboard.x:
                showing_terminal = False
           
        
      
        if showing_senior_dialogue:
            
            if keyboard.y and key_cooldown <= 0:
                dialogue_page += 1
                key_cooldown = 0.3
                
            elif keyboard.x:
                showing_senior_dialogue = False
                dialogue_page = 0
            return  
        
       
        near_senior = None
        for senior in seniors:
            if senior.is_near_player(player):
                near_senior = senior
               
                if keyboard.f:
                    
                    if player.x > senior.x:
                        senior.facing_right = True
                    else:
                        senior.facing_right = False
                    
                    showing_senior_dialogue = True
                    current_senior_type = senior.senior_type  
                    dialogue_page = 0  
                    key_cooldown = 0.3
                break
        
        
        if near_terminal and keyboard.f:
            showing_terminal = True
            selected_option = 0
            key_cooldown = 0.3  
        
        
        is_sprinting = keyboard.lshift or keyboard.rshift
        
       
        direction = 0
        if keyboard.a:
            direction = -1
        elif keyboard.d:
            direction = 1
        
        player.move(direction, is_sprinting)
        
        
        if keyboard.space and player.on_ground:
            player.jump(is_sprinting)
        
        
        if keyboard.q:
            player.dash(-1)  
        elif keyboard.e:
            player.dash(1)           
        
        player.update(dt, tiles)
        
        
        for barrier in barriers:
            if not barrier.is_broken and player.rect.colliderect(barrier.collision_rect):
                
                if player.x < barrier.x:
                  
                    player.x = barrier.x - player.width - 5
                else:
                    
                    player.x = barrier.x + barrier.width + 5
                player.rect.x = player.x
        
        
        from level_data import GROUND_Y_BASE, TILE_ROW_HEIGHT
        max_ground_y = GROUND_Y_BASE + TILE_ROW_HEIGHT  
        
        if player.y > max_ground_y + 200:  
            global current_level
            current_level += 1
            create_level()
        
        
        for enemy in enemies[:]:
            enemy.update(dt, tiles)
        
        
        for senior in seniors:
            senior.update(dt)
        
       
        camera_x = player.x - WIDTH // 3
        if camera_x < 0:
            camera_x = 0
        
        camera_y = player.y - HEIGHT // 2  
        
      
        if player.hp <= 0:
             game_state = "game_over"
        #if player.x > 1500:
        #     game_state = "victory"


def draw():
    global showing_senior_dialogue, dialogue_page
    screen.clear()
    screen.fill((135, 206, 235))
    
    if game_state == "menu":
        screen.clear()
        screen.draw.text("CODE DEFENDERS", center=(WIDTH//2, 150), fontsize=80, color="white", owidth=2, ocolor="blue")
        
        
        s_color = "green" if btn_start.collidepoint(mouse_pos) else (0, 160, 0)
        screen.draw.filled_rect(btn_start, s_color)
        screen.draw.text("START GAME", center=btn_start.center, fontsize=30, color="white")
        
        
        m_label = "MUSIC: ON" if music_enabled else "MUSIC: OFF"
        m_color = "blue" if btn_audio.collidepoint(mouse_pos) else (0, 0, 160)
        screen.draw.filled_rect(btn_audio, m_color)
        screen.draw.text(m_label, center=btn_audio.center, fontsize=30, color="white")
        
        
        e_color = "red" if btn_exit.collidepoint(mouse_pos) else (160, 0, 0)
        screen.draw.filled_rect(btn_exit, e_color)
        screen.draw.text("EXIT", center=btn_exit.center, fontsize=30, color="white")
    
    elif game_state == "playing":
        
        
        try:
            
            bg_x_offset = int(camera_x) % 1280  
            screen.blit("lvl1", (-bg_x_offset, 0))
            screen.blit("lvl1", (1280 - bg_x_offset, 0))
            screen.blit("lvl1", (2560 - bg_x_offset, 0))
        except:
            
            screen.fill((135, 206, 235))
        
        
        for tile in tiles:
            tile.draw(screen, camera_x, camera_y)
        
        
        for enemy in enemies:
            enemy.draw(screen, camera_x, camera_y)
        
        
        for senior in seniors:
            senior.draw(screen, camera_x, camera_y)
          
            if senior.is_near_player(player):
                senior_screen_x = int(senior.x - camera_x)
                senior_screen_y = int(senior.y - camera_y)
                screen.draw.text(
                    "Aperte F para conversar",
                    center=(senior_screen_x + 50, senior_screen_y - 40),
                    fontsize=20,
                    color="white",
                    owidth=1,
                    ocolor="black"
                )
        
        
        for barrier in barriers:
            barrier.draw(screen, camera_x, camera_y)
        
       
        for terminal in terminals:
            terminal.draw(screen, camera_x, camera_y)
           
            if terminal_puzzle_solved:
                terminal_screen_x = int(terminal.x - camera_x)
                terminal_screen_y = int(terminal.y - camera_y)
                try:
                    screen.blit('tiles/aprovado', (terminal_screen_x, terminal_screen_y - 60))
                except:
                    screen.draw.text(
                        "✓ APROVADO",
                        center=(terminal_screen_x + 50, terminal_screen_y - 40),
                        fontsize=25,
                        color="green",
                        owidth=1,
                        ocolor="black"
                    )
            
            elif terminal.is_near_player(player):
                terminal_screen_x = int(terminal.x - camera_x)
                terminal_screen_y = int(terminal.y - camera_y)
                screen.draw.text(
                    "Aperte F para programar",
                    center=(terminal_screen_x + 50, terminal_screen_y - 40),
                    fontsize=20,
                    color="white",
                    owidth=1,
                    ocolor="black"
                )
        
        
        player.draw(screen, camera_x, camera_y)
        
       
        for i in range(player.max_hp):
            x = 20 + i * 35
            y = 20
            if i < player.hp:
                
                screen.draw.filled_circle((x, y), 8, (255, 50, 50))
                screen.draw.filled_circle((x + 8, y), 8, (255, 50, 50))
                screen.draw.filled_circle((x + 4, y + 10), 6, (255, 50, 50))
            else:
                
                screen.draw.circle((x, y), 8, (100, 100, 100))
                screen.draw.circle((x + 8, y), 8, (100, 100, 100))
        
        
        for enemy in enemies:
            if enemy.hibernating:
                
                enemy_screen_x = int(enemy.x - camera_x)
                enemy_screen_y = int(enemy.y) - 40
                seconds_left = int(enemy.hibernate_timer) + 1
                screen.draw.text(
                    f"{seconds_left}s",
                    center=(enemy_screen_x + enemy.width // 2, enemy_screen_y),
                    fontsize=30,
                    color="yellow",
                    owidth=1,
                    ocolor="black"
                )
    
        
        if showing_senior_dialogue:
            
            if current_senior_type == 29:  
                dialogue_pages = [
                {
                    "title": "👴 SENIOR O ANCIÃO",
                    "subtitle": "",
                    "lines": [
                        "Olá, que bom te rever",
                        "pequena gafanhota!",
                        "decidiu me contratar?",
                        "Vejo que chegou até aqui de novo...",
                        "Impressionante!",
                    ]
                },
                {
                    "title": "👴 SENIOR O ANCIÃO",
                    "subtitle": "",
                    "lines": [
                        "Vou te ensinar como",
                        "resolver esse problema.",
                        "",
                        "Algo ou alguém bagunçou",
                        "a cabeça dos guardiões...",
                    ]
                },
                {
                    "title": " SENIOR O ANCIÃO",
                    "subtitle": "",
                    "lines": [
                        "É seu dever resolver isso!",
                        "",
                        "Mas eu já tô velho,",
                        "corcumido, todo acabado...",
                        "Só o pó da gaita! ",
                    ]
                },
                {
                    "title": "!!! ATENÇÃO IMPORTANTE!",
                    "subtitle": "",
                    "lines": [
                        "O GUARDIÃO DEVE",
                        "PERMANECER VIVO!",
                        "",
                        "Se você matar ele, LITERALMENTE",
                        "destrói tudo que faz parte",
                        "desse elemento!",
                    ]
                },
                {
                    "title": "⚠️ ATENÇÃO IMPORTANTE!",
                    "subtitle": "",
                    "lines": [
                        "Se matar o guardião,",
                        "eu vou te detonar na porrada",
                        "",
                        "com meu poderoso MOUSE GAMER",
                        "com luisinha do Magazine Luiza! CLIK CLICK",
                        "Tá avisado(a)!",
                        "",
                    ]
                },
                {
                    "title": "📚 MOVIMENTAÇÃO",
                    "subtitle": "",
                    "lines": [
                        "A/D ou SETAS - Andar",
                        "W/ESPAÇO - Pular",
                        "SHIFT - Correr e pular mais alto",
                        "(pra fugir dos problemas)",
                        "",
                    ]
                },
                {
                    "title": "COMBATE",
                    "subtitle": "",
                    "lines": [
                        "não tem como derrotalos nem pode",
                        "Q - Dash DIREITA",
                        "E - Dash ESQUERDA",
                        "leve o golem ao terminal e ative ele voltara a hibernar por um tempo ",
                        "temos que chegar ao terminal mãe ADA",
                    ]
                },
                {
                    "title": "💻 TERMINAL",
                    "subtitle": "",
                    "lines": [
                        "Acerte o código:",
                        "→ Inimigos dormem por um tempo ",
                        "",
                        "Erre o código:",
                        "→ Voltam COM DANO x2!",
                    ]
                },
                {
                    "title": "� IMPORTANTE SOBRE ALCANCE!",
                    "subtitle": "",
                    "lines": [
                        "Os guardiões precisam estar",
                        "PERTO do terminal pra hibernar!",
                        "",
                        "É que eles não usam 4G",
                        "de uma boa operadora... 😂",
                        "",
                        "WiFi deles é fraco demais! 📶",
                    ]
                },
                {
                    "title": "�💡 DICA PRO",
                    "subtitle": "",
                    "lines": [
                        "Operador >= é seu amigo!",
                        "",
                        "água >= 50 aceita 50",
                        "água > 50 NÃO aceita 50",
                        "",
                        "Entendeu a diferença? 😉",
                    ]
                },
                {
                    "title": "🎯 BOA SORTE!",
                    "subtitle": "",
                    "lines": [
                        "Agora você sabe tudo!",
                        "",
                        "Vá lá e mostre quem manda!",
                        "",
                        "Lembre-se: Programar é 10% código",
                        "e 90% googlar erros! 😄",
                    ]
                },
            ]
            elif current_senior_type == 2901:  
                dialogue_pages = [
                    {
                        "title": "👴 SENIOR MALANDRO",
                        "subtitle": "",
                        "lines": [
                            "Olá pequena gafanhota!",
                            "",
                            "Se joga do penhasco aí,",
                            "confia na call!",
                            "",
                            "Que é sucesso! 🚀😎",
                        ]
                    },
                ]
            elif current_senior_type == 2902:  
                dialogue_pages = [
                    {
                        "title": "👴 SENIOR TIPO 2",
                        "subtitle": "",
                        "lines": [
                            "E aí, tudo certo?",
                            "",
                            "Este é um diálogo",
                            "do Senior tipo 2.",
                            "",
                            "Textos diferentes por tipo!",
                        ]
                    },
                ]
            elif current_senior_type == 2903:  
                dialogue_pages = [
                    {
                        "title": " SENIOR ",
                        "subtitle": "",
                        "lines": [
                            "Opa, beleza?",
                            "",
                            "Se joga dali de novo ",
                            "se quiser que o jogo continue me contrate :)",
                            "por enquanto vc só vai volta pro lvl1",
                            "",
                        ]
                    },
                ]
            else:  
                dialogue_pages = [
                    {
                        "title": "👴 SENIOR",
                        "subtitle": "",
                        "lines": [
                            "Olá!",
                            "",
                            "Tipo de senior desconhecido.",
                        ]
                    },
                ]
            
           
            if dialogue_page >= len(dialogue_pages):
                showing_senior_dialogue = False
                dialogue_page = 0
                return  
            
           
            page = dialogue_pages[dialogue_page]
            
           
            senior_screen_x = None
            senior_screen_y = None
            for senior in seniors:
                if senior.is_near_player(player):
                    senior_screen_x = int(senior.x - camera_x)
                    senior_screen_y = int(senior.y)
                    break
            
           
            if senior_screen_x is not None:
                balloon_x = senior_screen_x - 200  
                balloon_y = senior_screen_y - 200 + balloon_float_offset  
            else:
                balloon_x = 100
                balloon_y = 100 + balloon_float_offset
            
            
            balloon_width = 450
            balloon_height = 180
            
            
            screen.draw.filled_rect(Rect(balloon_x, balloon_y, balloon_width, balloon_height), (30, 50, 30))
            screen.draw.rect(Rect(balloon_x, balloon_y, balloon_width, balloon_height), (150, 200, 100))
            
            
            screen.draw.text(page["title"], (balloon_x + 20, balloon_y + 15), fontsize=32, color="yellow")
            
            
            if page["subtitle"]:
                screen.draw.text(page["subtitle"], (balloon_x + 20, balloon_y + 55), fontsize=20, color="lightgreen")
            
            
            line_y = balloon_y + 60
            for line in page["lines"]:
                if line:  
                    screen.draw.text(line, (balloon_x + 30, line_y), fontsize=16, color="white")
                line_y += 18
            
            
            hint_text = "aperta Y pra próxima conversa"
            screen.draw.text(hint_text, (balloon_x + balloon_width - 240, balloon_y + balloon_height - 25), fontsize=12, color="gray")
        
        
        if showing_terminal:
            
            screen.draw.filled_rect(Rect(100, 50, 1080, 620), (20, 20, 40))
            
           
            screen.draw.text("DESAFIO DE PROGRAMAÇÃO", center=(WIDTH//2, 100), fontsize=40, color="yellow")
            
            
            screen.draw.text("O fogo está muito forte!", (150, 170), fontsize=25, color="white")
            screen.draw.text("Para apagá-lo, a água precisa ser maior ou igual a 50.", (150, 200), fontsize=25, color="white")
            
           
            screen.draw.text("Código:", (150, 260), fontsize=30, color="cyan")
            screen.draw.text('agua = int(input("Quanto de água?"))', (170, 300), fontsize=22, color="lightgray")
            screen.draw.text('if agua ??? 50:', (170, 330), fontsize=22, color="lightgray")
            screen.draw.text('    print("🔥 O fogo foi apagado!")', (170, 360), fontsize=22, color="lightgray")
            screen.draw.text('else:', (170, 390), fontsize=22, color="lightgray")
            screen.draw.text('    print("🔥 Fogo ainda queimando!")', (170, 420), fontsize=22, color="lightgray")
            
           
            screen.draw.text("Qual operador corrige o código?", (150, 480), fontsize=28, color="yellow")
            
            options = ["A) > 50", "B) >= 50  ✓ CORRETA", "C) < 50"]
            for i, option in enumerate(options):
                color = "green" if i == selected_option else "white"
                screen.draw.text(option, (170, 520 + i*35), fontsize=26, color=color)
            
            screen.draw.text("Use SETAS para escolher, Y para confirmar, X para sair", center=(WIDTH//2, 640), fontsize=20, color="gray")
        
       
        if showing_error_message:
            
            screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (60, 10, 10))
            
           
            screen.draw.text(
                "⚠ ACESSO NEGADO! ⚠",
                center=(WIDTH//2, HEIGHT//2 - 100),
                fontsize=60,
                color="red",
                owidth=2,
                ocolor="black"
            )
            
            screen.draw.text(
                "Apenas um guardião dos códigos",
                center=(WIDTH//2, HEIGHT//2),
                fontsize=40,
                color="white",
                owidth=1,
                ocolor="black"
            )
            
            screen.draw.text(
                "da natureza pode controlar",
                center=(WIDTH//2, HEIGHT//2 + 50),
                fontsize=40,
                color="white",
                owidth=1,
                ocolor="black"
            )
            
            screen.draw.text(
                "o poder da criação!",
                center=(WIDTH//2, HEIGHT//2 + 100),
                fontsize=40,
                color="white",
                owidth=1,
                ocolor="black"
            )
            
            screen.draw.text(
                "Pressione Y para continuar",
                center=(WIDTH//2, HEIGHT - 100),
                fontsize=30,
                color="yellow",
                owidth=1,
                ocolor="black"
            )    
    elif game_state == "game_over":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        screen.draw.text("Press R to restart", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")
    
    elif game_state == "victory":
        screen.draw.text("VICTORY!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="gold")
        screen.draw.text("Press R to restart", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")


def on_key_down(key):
    global game_state
    
    if game_state == "menu":
        if key == keys.SPACE or key == keys.RETURN:
            initialize_game()
        elif key == keys.ESCAPE:
            exit()
    
    elif game_state == "playing":
        if key == keys.ESCAPE:
            game_state = "menu"
    
    elif game_state in ["game_over", "victory"]:
        if key == keys.R:
            initialize_game()
        elif key == keys.ESCAPE:
            game_state = "menu"


def on_mouse_down(button, pos):
    """Detecta clique do mouse"""
    global game_state, player
    
    if game_state == "playing":
        if button == mouse.LEFT:
            player.attack()

def on_mouse_down(pos):
    global game_state, music_enabled, music_playing
    
    if game_state == "menu":
       
        if btn_start.collidepoint(pos):
            initialize_game()
            game_state = "playing"
            if music_enabled:
                music.play("background")
                music_playing = True
        
        elif btn_audio.collidepoint(pos):
            music_enabled = not music_enabled
            if not music_enabled:
                music.stop()
                music_playing = False
            else:
                if game_state == "playing":
                    music.play("background")
                    music_playing = True
        
        elif btn_exit.collidepoint(pos):
            import sys
            sys.exit()

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def on_mouse_down(pos):
    global game_state, music_enabled, music_playing
    
    if game_state == "menu":
        if btn_start.collidepoint(pos):
            initialize_game()
            game_state = "playing"
            if music_enabled:
                music.play("background")
                music_playing = True
        
        elif btn_audio.collidepoint(pos):
            music_enabled = not music_enabled
            if not music_enabled:
                music.stop()
                music_playing = False
            elif game_state == "playing":
                music.play("background")
                music_playing = True
        
        elif btn_exit.collidepoint(pos):
            exit()

pgzrun.go()
