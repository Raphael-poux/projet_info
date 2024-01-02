import pygame

# Création des différents types de surface sous forme de listes

# On se cogne au sol en descendant
sol1 = [(i, 410) for i in range(101)]
sol2 = [(250 + i, 410) for i in range(471)]
sol3 = [(100 + i, 180) for i in range(151)]
sols = [sol1, sol2, sol3]

# On se cogne au plafond en montant
plafond1 = [(100 + i, 220) for i in range(151)]
plafonds = [plafond1]

# On se cogne aux parois gauches en allant à gauche
paroiG1 = [(100, 410 + i) for i in range(311)]
paroiG2 = [(250, 180 + i) for i in range(41)]
paroisG = [paroiG1, paroiG2]

# On se cogne aux parois droites en allant à droite

paroiD1 = [(250, 410 + i) for i in range(311)]
paroiD2 = [(100, 180 + i) for i in range(41)]
paroisD = [paroiD1, paroiD2]

# Les parois sont renseignées dans une matrice avec un chiffre pour chaque type
# Un niveau correspond à la donnée des surfaces et d'une pos de départ
matsurfaces = [[0 for i in range(721)] for j in range(721)]

for sol in sols:
    for j, i in sol:
        matsurfaces[i][j] = 1

for plafond in plafonds:
    for j, i in plafond:
        matsurfaces[i][j] = 3

for paroi in paroisD:
    for j, i in paroi:
        matsurfaces[i][j] = 2

for paroi in paroisG:
    for j, i in paroi:
        matsurfaces[i][j] = 4

# On définit la fonction collision qui est propre à un disque
        
def collision(point, surface):
    ''' Le fonction prend en entrée une surface et le centre
    du cercle et indique si le cercle touche la surface'''    
    for x, y in surface:
        if (point[0] - x)**2 + (point[1] - y)**2 <= 30**2:
            return True
    return False

White = (255, 255, 255)
Cyan = (0, 255, 255)
Couleurs_portails = [(255, 100, 0), (0, 0, 255)]

def main():
    # on initialise pygame et on crée une fenêtre de 720x720 pixels
    # On donne un titre à la fenetre
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption("Portal")
    clock = pygame.time.Clock()

    # On initialise la position, la vitesse et l'accélération

    x = 360
    y = 360
    vx = 0
    vy = 0
    ay = -0.01
    
    # Les portails sont stockés dans un dictionnaire avec leur couleur
    # Il contient également le type de surface sur lequel il est posé 
    portal = {}
    # On se sert d'un état pour savoir quel portail lancer
    portalstate = 0

    # On utilise un bool qui devient True quand le cercle touche le plafond
    # et devient faux quand il touche le sol
    a_cogne_plafond = False

    # La boucle du jeu
    done = False

    while not done:
        clock.tick(800)

        # On récupère les touches pressées
        touches = pygame.key.get_pressed()

        # On s'assure que le cercle reste dans la fenêtre, à modifier
        if y > 720:
            y = 0
        if x > 720:
            x = 0
        if x < 0:
            x = 720
        
        # Pour actualiser l'écran, on repeint les murs, et le cercle
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, Cyan, (0, 410, 720, 310))
        pygame.draw.rect(screen, Cyan, (100, 180, 150, 40))
        pygame.draw.rect(screen, (0, 0, 0), (100, 410, 150, 310))
        pygame.draw.circle(screen, White, (x, y), 30)

        # On crée le viseur pour les portails à l'aide de q, s, d, z
        # On créer un vecteur direction = [abscisse, ordonnée]
        direction = [0, 0] 
        if touches[pygame.K_d]:
            direction[0] += 1
        if touches[pygame.K_s]:
            direction[1] += 1 
        if touches[pygame.K_q]:
            direction[0] += -1
        if touches[pygame.K_z]:
            direction[1] += -1

        # On se sert de la valeur True d'un nombre non nul
        # On arrête la ligne au premier obstacle ou à la sortie de l'écran
        curseur = direction[0] or direction[1]
        if curseur:
            xc, yc = int(x), int(y)
            while 0 < xc < 720 and 0 < yc < 720 and not matsurfaces[yc][xc]:
                xc += direction[0]
                yc += direction[1]
            pygame.draw.line(screen, (255, 0, 0), (x, y),(xc, yc), 3)

        # On récupère les touches sur lesquelles on a appuyé
        # On envoie un portail si une surface est disponible
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and curseur and matsurfaces[yc][xc]:
                    portal[portalstate] = ((xc, yc), matsurfaces[yc][xc], Couleurs_portails[portalstate])
                    portalstate = 1 - portalstate
        
        # Affiche les portails et les oriente selon la surface
        for portail in portal.values():
            if portail[1] % 2 == 1:
                rect_ovale = pygame.Rect(portail[0][0] - 30, portail[0][1] - 7, 60, 14)
            if portail[1] % 2 == 0:
                rect_ovale = pygame.Rect(portail[0][0] - 7, portail[0][1] - 30, 14, 60)
            pygame.draw.ellipse(screen, portail[2], rect_ovale)

        # Annule la vitesse verticale la première fois qu'on touche le plafond
        if collision((x, y), plafond1) and not a_cogne_plafond:
            vy = 0
            a_cogne_plafond = True
        
        # Annule les vitesse verticale et horizontale quand on touche le sol
        # On sert du fait qu'une somme de booléens vaut True si elle contient True
        vy += ay
        touche_sol = sum(collision((x, y), sol) for sol in sols)
        if touche_sol:
            vy = 0
            a_cogne_plafond = False
            vx = 0

        # Gère les déplacements latéraux
        if touches[pygame.K_RIGHT] and not sum(collision((x, y), paroi) for paroi in paroisD) and vx <= 0.8:
            vx = 0.8
        if touches[pygame.K_LEFT] and not sum(collision((x, y), paroi) for paroi in paroisG) and vx >= - 0.8:
            vx = - 0.8
        if sum(collision((x, y), paroi) for paroi in paroisG):
            vx = 0
            x += 0.3
        if sum(collision((x, y), paroi) for paroi in paroisD):
            vx = 0
            x -= 0.3
        if touches[pygame.K_UP] and touche_sol:
            vy = 2

        # Fait téléporter le cercle d'un portail à l'autre quand il rentre dedans
        for key in portal:
            if (portal[key][0][0] - x)**2 + (portal[key][0][1] - y)**2 <= 32**2 and len(portal) == 2:
                m = matsurfaces[int(portal[1 - key][0][1])][int(portal[1 - key][0][0])]
                if  m % 2 == 1:
                    y = portal[1 - key][0][1] + (m-2)*40
                    x = portal[1 - key][0][0]
                    vy = (2-m)*2
                if m % 2 == 0:
                    y = portal[1 - key][0][1]
                    x = portal[1 - key][0][0] + (m-3)*40
                    vx = (m-3)*1
        y -= vy
        x += vx
        pygame.display.update()
            
    pygame.quit()

# if python says run, then we should run
if __name__ == "__main__":
    main()
