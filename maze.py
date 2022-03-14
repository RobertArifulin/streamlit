import streamlit as st
from random import random, randint
from os.path import exists
from math import sqrt


def get_walls(file_name='maze.txt'):
    walls = []
    with open(file_name, 'r') as file:
        for line in file:
            cell_1 = tuple(map(int, line.split()[0].strip(')').strip('(').split(',')))
            cell_2 = tuple(map(int, line.split()[1].strip(')').strip('(').split(',')))
            walls.append([cell_1, cell_2])

    return walls


def skin_number(skin):
    skins = ['x', 'o', '*', '#', '%', '§', '$']
    return skins.index(skin)


def next_cell(cell):
    return [(cell[0] + 1, cell[1]), (cell[0] - 1, cell[1]), (cell[0], cell[1] + 1), (cell[0], cell[1] - 1)][randint(0, 3)]


def generate_maze_in_file(width, height):
    with open('maze.txt', 'w') as f:
        in_tree = [(0, 0)]
        out_tree = [(i, j) for i in range(width) for j in range(height)]
        out_tree.remove((0, 0))
        stack = []
        while len(out_tree) > 0:
            cell = out_tree[randint(0, len(out_tree) - 1)]
            stack.append(cell)
            while not (cell in in_tree):
                t = next_cell(cell)
                while not ((t in in_tree) | (t in out_tree)):
                    t = next_cell(cell)
                cell = t
                if cell in stack:
                    while stack[-1] != cell:
                        stack.pop()
                elif (cell in out_tree) | (cell in in_tree):
                    stack.append(cell)
            stack.pop()
            while len(stack) > 0:
                new_cell = stack.pop()
                out_tree.remove(new_cell)
                in_tree.append(new_cell)
                if (cell[0] > new_cell[0]) | (cell[1] > new_cell[1]):
                    f.write('(' + str(new_cell[0]) + ',' + str(new_cell[1]) + ') (' + str(cell[0]) + ',' + str(
                        cell[1]) + ')\n')
                else:
                    f.write('(' + str(cell[0]) + ',' + str(cell[1]) + ') (' + str(new_cell[0]) + ',' + str(
                        new_cell[1]) + ')\n')
                cell = new_cell


def create_filled_maze(width, height):
    draw1 = [' ____ ' * (width) for _ in range(height)]
    draw2 = ['|    |' * (width) for _ in range(height)]
    draw3 = ['|____|' * (width) for _ in range(height)]

    maze = []

    for i in range(3 * height):
        if i % 3 == 0:
            maze.append(draw1[i // 3])
        if i % 3 == 1:
            maze.append(draw2[i // 3])
        if i % 3 == 2:
            maze.append(draw3[i // 3])

    for i in range(len(maze)):
        maze[i] = maze[i].replace('||', '|')
        if not i % 3:
            maze[i] = maze[i].replace('  ', ' ')

    return [elem for index, elem in enumerate(maze) if not index or index % 3]


def check_maze(width, height, walls):
    wall_q = int([(width - 2, height - 1), (width - 1, height - 1)] in walls) + int(
        [(width - 1, height - 2), (width - 1, height - 1)] in walls)
    return bool(wall_q % 2)


def create_maze(size, fog_of_war, radius, new_maze=True):
    width, height = list(map(int, size.split('x')))

    if new_maze:
        with open('player_pos.txt', 'w') as f:
            f.write('0 0')
        generate_maze_in_file(width, height)
        walls = get_walls()
        while not check_maze(width, height, walls):
            generate_maze_in_file(width, height)
            walls = get_walls()

    with open('player_pos.txt', 'r') as file:
        player_x, player_y = map(int, file.readlines()[0].split())

    walls = get_walls()

    maze = create_filled_maze(width, height)

    for wall in walls:
        x, y = wall[0]
        if wall[0][0] != wall[1][0]:
            maze[1 + 2 * y] = maze[1 + 2 * y][:5 * x + 5] + ' ' + maze[1 + 2 * y][5 * x + 6:]
            maze[2 + 2 * y] = maze[2 + 2 * y][:5 * x + 5] + ' ' + maze[2 + 2 * y][5 * x + 6:]
        else:
            pass
            maze[2 + 2 * y] = maze[2 + 2 * y][:5 * x + 1] + '    ' + maze[2 + 2 * y][5 * x + 5:]

    for i in range(len(maze)):
        maze[i] = maze[i].replace('_ _', '___')

    maze[0] = '.' + maze[0][1:-1] + '.'

    maze[-2] = maze[-2][:-3] + '✓' + ' |'

    if fog_of_war:
        x = player_x * 5 + 3
        y = player_y * 2 + 1
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if sqrt((x - j)**2 / 4 + (y - i)**2 * 1.9) > radius:
                    maze[i] = maze[i][:j] + '@' + maze[i][j + 1:]

    return maze


def insert_player_at_pos(x, y, skin, maze):
    for i in range(len(maze)):
        maze[i] = maze[i].replace(skin, ' ')
    maze[1 + 2 * y] = maze[1 + 2 * y][:5 * x + 3] + skin + maze[1 + 2 * y][5 * x + 4:]


def run_streamlit_maze():
    global player_x, player_y
    hide_streamlit_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                '''

    st.markdown(
        f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: {1000}px;
        }}
    </style>

    """,
        unsafe_allow_html=True,
    )

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.title('Лабиринт')
    st.write('Цель - дойти в нижний правый угол, перемещая персонажа стрелочками')

    size = st.sidebar.selectbox('Выберите размер',
                                ('5x5', '10x5', '10x10', '15x10', '15x15', '20x15', '20x20', '25x20', '25x25'))
    with open('size.txt', 'r') as file:
        old_size = file.readlines()[0]
    with open('size.txt', 'w') as file:
        file.write(size)
    fog_of_war = st.sidebar.checkbox('Включить туман войны')
    
    radius = 0
    if fog_of_war:
        radius = st.sidebar.slider('Дальность обзора', min_value=1, max_value=max(list(map(int, size.split('x')))), value=max(list(map(int, size.split('x')))) // 2, step=1)

    with open('skins.txt', 'r') as file:
        possible_skins = sorted(file.readlines()[0].split(), key=skin_number)

    skin = st.sidebar.selectbox('Выберите скин', possible_skins)
    
    width, height = list(map(int, size.split('x')))

    button = st.button('Сгенерировать')

    col1, col2, col3, col4 = st.beta_columns([1, 1, 1, 15])
    with col2:
        up = st.button('↑', key=None, help=None)
        down = st.button('↓', key=None, help=None)
    with col3:
        for _ in range(3):
            st.write('')
        right = st.button('→', key=None, help=None)
    with col1:
        for _ in range(3):
            st.write('')
        left = st.button('←', key=None, help=None)

    old_player_x, old_player_y = player_x, player_y

    if up and player_y:
        player_y -= 1
    if down and player_y < height - 1:
        player_y += 1
    if left and player_x:
        player_x -= 1
    if right and player_x < width - 1:
        player_x += 1

    if old_player_x > player_x or old_player_y > player_y:
        check = [(player_x, player_y), (old_player_x, old_player_y)]
    else:
        check = [(old_player_x, old_player_y), (player_x, player_y)]

    walls = get_walls()

    if check not in walls and (old_player_x != player_x or old_player_y != player_y):
        if up:
            player_y += 1
        if down:
            player_y -= 1
        if left:
            player_x += 1
        if right:
            player_x -= 1

    if old_player_x == player_x and old_player_y == player_y and (up or down or left or right):
        with col4:
            for _ in range(3):
                st.write('')
            st.write('СТЕНА!!!')
    if player_x == width - 1 and player_y == height - 1:
        with col4:
            for _ in range(3):
                st.write('')
            st.write('ПОБЕДА!!!')

        new_skin = None
        if size == '5x5' and '*' not in possible_skins:
            new_skin = '*'
        elif size == '10x10' and '#' not in possible_skins:
            new_skin = '#'
        elif size == '15x15' and '%' not in possible_skins:
            new_skin = '%'
        elif size == '20x20' and '§' not in possible_skins:
            new_skin = '§'
        elif size == '25x25' and '$' not in possible_skins:
            new_skin = '$'
        
        if new_skin is not None:
            with open('skins.txt', 'a') as file:
                file.write(new_skin + ' ')
        
        maze = create_maze(size, fog_of_war, radius)
        player_x, player_y = 0, 0
        insert_player_at_pos(player_x, player_y, skin, maze)

    with open('player_pos.txt', 'w') as f:
        f.write(f'{player_x} {player_y}')

    if button:
        maze = create_maze(size, fog_of_war, radius)
        player_x, player_y = 0, 0
    elif size != old_size:
        maze = create_maze(size, fog_of_war, radius)
        player_x, player_y = 0, 0
        

    maze = create_maze(size, fog_of_war, radius, new_maze=False)
    insert_player_at_pos(player_x, player_y, skin, maze)
    st.text('\n'.join(maze))

    
if not exists('maze.txt'):
    generate_maze_in_file(5, 5)

if not exists('player_pos.txt'):
    with open('player_pos.txt', 'w') as file:
        file.write('0 0')

if not exists('size.txt'):
    with open('size.txt', 'w') as file:
        file.write('5x5')

if not exists('skins.txt'):
    with open('skins.txt', 'a') as file:
        file.write('x o ')

with open('player_pos.txt', 'r') as f:
    player_x, player_y = map(int, f.readlines()[0].split())

run_streamlit_maze()
