
MAP_WIDTH = 24   
MAP_HEIGHT = 10  
TILE_SIZE = 240  
TILE_SPACING = 216  
TILE_ROW_HEIGHT = 124  


GROUND_Y_BASE = 596  


EMPTY = 0
GROUND_START = 1          
GROUND_MIDDLE = 2          
GROUND_END = 3             
CAVE_WALL = 4              
CAVE_FLOOR = 5             
CAVE_CEILING_A = 6         
CAVE_CEILING_B = 7         

TILE_Y_OFFSET = {
    1: 0,   
    2: +3,  
    3: 0,   
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: +30,  
    12: 0,
    13: +30,  
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    21: +30,  
    22: +30,  
    23: +30,  
}

CAVE_ENTRANCE_CEILING_L = 8  
CAVE_ENTRANCE_CEILING_R = 9  
CAVE_ENTRANCE_WALL_L = 10    
CAVE_ENTRANCE_WALL_R = 11    
CAVE_ENTRANCE_FLOOR_L = 12   
CAVE_ENTRANCE_FLOOR_R = 13   
TERMINAL = 14              
TERMINAL_BOX = 15          
APPROVED = 16              
SENIOR_ANCIAO = 29        
SENIOR_01 = 2901           
SENIOR_02 = 2902           
SENIOR_03 = 2903           
BARRIER_R = 17             
BARRIER_L = 18            
BARRIER_BROKEN_R = 19      
BARRIER_BROKEN_L = 20     
CAVE_ENTRANCE_FLOOR_LEFT = 21    
CAVE_ENTRANCE_CEILING_LEFT = 22  
CAVE_ENTRANCE_WALL_LEFT = 23     
CAVE_FLOOR_START_A = 26  
CAVE_FLOOR_MIDDLE = 27    
CAVE_FLOOR_START_B = 28   


TILE_COLLISION = {
    EMPTY: False,
    GROUND_START: True,
    GROUND_MIDDLE: True,
    GROUND_END: True,
    CAVE_WALL: False,
    CAVE_FLOOR: True,
    CAVE_CEILING_A: True,
    CAVE_CEILING_B: True,
    CAVE_ENTRANCE_CEILING_L: True,
    CAVE_ENTRANCE_CEILING_R: True,
    CAVE_ENTRANCE_WALL_L: False,
    CAVE_ENTRANCE_WALL_R: False,
    CAVE_ENTRANCE_FLOOR_L: True,
    CAVE_ENTRANCE_FLOOR_R: False,
    TERMINAL: False,
    TERMINAL_BOX: False,
    APPROVED: False,
    BARRIER_R: True,
    BARRIER_L: True,
    BARRIER_BROKEN_R: True,
    BARRIER_BROKEN_L: True,
    CAVE_ENTRANCE_FLOOR_LEFT: False,     
    CAVE_ENTRANCE_CEILING_LEFT: True,    
    CAVE_ENTRANCE_WALL_LEFT: False,      
    CAVE_FLOOR_START_A: True,          
    CAVE_FLOOR_MIDDLE: True,           
    CAVE_FLOOR_START_B: True,          
    SENIOR_ANCIAO: False,               
    2901: False,                         
    2902: False,                         
    2903: False,                
}


TILE_AUTO_DECORATION = {
    26: (23, 60),  
    27: (7, 124),   
    28: (11, 60),   
}


TILE_SPRITES = {
    GROUND_START: 'tiles/chãocomeçodefora',
    GROUND_MIDDLE: 'tiles/chãomeio',
    GROUND_END: 'tiles/chãocomeçofora',
    CAVE_WALL: 'tiles/paredecaverna',
    CAVE_FLOOR: 'tiles/cavernachão',
    CAVE_CEILING_A: 'tiles/cavernatetoa',
    CAVE_CEILING_B: 'tiles/cavernatetob',
    CAVE_ENTRANCE_CEILING_L: 'tiles/entradacavernateto',
    CAVE_ENTRANCE_CEILING_R: 'tiles/entradacavernateto',
    CAVE_ENTRANCE_WALL_L: 'tiles/entradameiocaverna',
    CAVE_ENTRANCE_WALL_R: 'tiles/entradameiocaverna',
    CAVE_ENTRANCE_FLOOR_L: 'tiles/entradacavernachão',
    CAVE_ENTRANCE_FLOOR_R: 'tiles/entradacavernachão',
    TERMINAL: 'tiles/terminal',
    TERMINAL_BOX: 'tiles/caixa_de_codigo_terminal',
    APPROVED: 'tiles/aprovado',
    BARRIER_R: 'tiles/barreira',
    BARRIER_L: 'tiles/barreira',
    BARRIER_BROKEN_R: 'tiles/quebrada',
    BARRIER_BROKEN_L: 'tiles/quebrada',
    CAVE_ENTRANCE_FLOOR_LEFT: 'tiles/entradacavernachãoleft',
    CAVE_ENTRANCE_CEILING_LEFT: 'tiles/entradacavernatetoleft',
    CAVE_ENTRANCE_WALL_LEFT: 'tiles/entradameiocavernaleft',
    CAVE_FLOOR_START_A: 'tiles/chãocomeçodeforacavernaa',
    CAVE_FLOOR_MIDDLE: 'tiles/chãomeiocaverna',
    CAVE_FLOOR_START_B: 'tiles/chãocomeçoforacavernab',
    TERMINAL: 'tiles/terminal',
    SENIOR_ANCIAO: 'tiles/seniorOancião',  
    2901: 'tiles/seniorOancião',  
    2902: 'tiles/seniorOancião', 
    2903: 'tiles/seniorOancião',  
}


LEVEL_01 = [
    # Row 0 (topo)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 1
    [0, 0, 0, 0, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 5
    [0, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 27, 27, 27, 27, 28, 0, 0, 0, 0, 0, 0],
    # Row 6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 4, 4, 4, 4, 11, 0, 0, 25, 0, 0, 0],
    # Row 7
    [0, 0, 29, 0, 27, 27, 0, 0, 0, 0, 0, 0, 23, 4, 25, 4, 4, 11, 0, 0, 0, 0, 0, 0],
    # Row 8 (perto do chão)
    [0, 0, 27, 0, 4, 4, 0, 0, 0, 0, 0, 0, 21, 4, 4, 4, 4, 13, 0, 0, 14, 0, 2901, 0],
    # Row 9 (base)
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
]



# Spawn positions
PLAYER_SPAWN = 24  
ENEMY_SPAWN = 25   

LEVEL_02 = [
    # Row 0 (topo)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 1
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    # Row 2
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 25, 4, 4, 4, 4, 4, 4, 4],
    # Row 3
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 4, 4],
    # Row 4
    [4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 5
    [4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 6
    [4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 7
    [4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0],
    # Row 8 - Plataforma com spawns
    [4, 4, 4, 4, 4, 0, 24, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0,  2903, 0],
    # Row 9 (base)
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
]


