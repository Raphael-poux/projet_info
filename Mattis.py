import pygame as pg
from random import randint
import math
import random



x1 = 100 # coordonnée x1 (colonnes) en pixels
y1 = 100 # coordonnée y1 (lignes) en pixels
x2 = 400 # coordonnée x2 (colonnes) en pixels
y2 = 200 # coordonnée y2 (lignes) en pixels







def main():
    d=0
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((640, 640))    
    
    window_width = 640
    window_height = 640
    radius_c = 20    
    circle_x, circle_y= window_width/2, window_height/2
    # on initialise pygame et on crée une fenêtre de 640x640 pixels

    # On donne un titre à la fenetre
    pg.display.set_caption("agario")

    # La boucle du jeu
    done = False
    while not done:
        
        #la boucle fruit:
        clock.tick(5)
    
        ecart_x=pg.mouse.get_pos()[0]-circle_x
        ecart_y=pg.mouse.get_pos()[1]-circle_y
        norme=1/6
        dx=ecart_x*norme
        dy=ecart_y*norme
        # Mettez à jour les coordonnées du cercle en ajoutant dx à X et dy à Y
        
        circle_x += dx
        circle_y += dy
        # on génère une couleur (Rouge, Vert, Bleu) au hasard
        random_color = (175,20, 125)
        screen.fill(random_color)
        blop=pg.draw.circle(screen,color=(255, 0, 0),center=(circle_x, circle_y),radius=radius_c)
        if d<radius_c:
            rand_pos=(random.randint(0,640),random.randint(0,640))
            radius_c+=2
            
            
        # Couleur du quadrillage
        grid_color = (0, 0, 0)  # Noir
        fruit=pg.draw.circle(screen,color=(0, 0, 255),center=rand_pos,radius=10)
        
        # Dimensions du quadrillage
        num_rows = 20
        num_cols = 20
        line_width = 1  # Épaisseur des lignes
        d=math.sqrt((rand_pos[0]-circle_x)**2+(rand_pos[1]-circle_y)**2)


        # Dessinez les lignes horizontales
        for row in range(num_rows + 1):
            y = row * window_height // num_rows
            pg.draw.line(screen, grid_color, (0, y), (window_width, y), line_width)


        
        # Dessinez les lignes verticales
        for col in range(num_cols + 1):
            x = col * window_width // num_cols
            pg.draw.line(screen, grid_color, (x, 0), (x, window_height), line_width)
            # enfin on met à jour la fenêtre avec tous les changements
        pg.display.update()









        for event in pg.event.get():
            # chaque évênement à un type qui décrit la nature de l'évênement
            # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
            if event.type == pg.QUIT:
                done = True
            # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
            elif event.type == pg.KEYDOWN:
                # si la touche est "Q" on veut quitter le programme
                if event.key == pg.K_q:
                    done = True

    pg.quit()




# if python says run, then we should run
if __name__ == "__main__":
    main()