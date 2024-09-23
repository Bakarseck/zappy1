import pygame
import socket
import json

# Paramètres du client
HOST = 'localhost'  # Adresse du serveur
PORT = 12345        # Port du serveur
PLAYER_SIZE = 20    # Taille des joueurs sur la carte
GRID_SIZE = 50      # Taille des cases de la grille
WORLD_WIDTH = 10    # Largeur de la carte (en cases)
WORLD_HEIGHT = 10   # Hauteur de la carte (en cases)

# Désactiver le son de Pygame pour éviter les erreurs ALSA
pygame.mixer.quit()

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH * GRID_SIZE, WORLD_HEIGHT * GRID_SIZE))
pygame.display.set_caption('Zappy - Client 2D')
clock = pygame.time.Clock()

# Fonction pour dessiner la carte du jeu
def draw_world(players, resources):
    screen.fill((255, 255, 255))  # Couleur de fond (blanc)

    # Dessiner la grille
    for x in range(0, WORLD_WIDTH * GRID_SIZE, GRID_SIZE):
        for y in range(0, WORLD_HEIGHT * GRID_SIZE, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    # Dessiner les joueurs
    for player in players:
        pygame.draw.circle(screen, (0, 0, 255), (player['x'] * GRID_SIZE + GRID_SIZE // 2, player['y'] * GRID_SIZE + GRID_SIZE // 2), PLAYER_SIZE)

    # Dessiner les ressources
    for resource in resources:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(resource['x'] * GRID_SIZE + 10, resource['y'] * GRID_SIZE + 10, 20, 20))

# Connexion au serveur
def connect_to_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        return sock
    except ConnectionRefusedError:
        print("Connexion au serveur refusée.")
        return None

# Recevoir les données de jeu du serveur
def receive_game_data(sock):
    try:
        data = sock.recv(1024).decode('utf-8').strip()
        if data:
            game_data = json.loads(data)
            players = game_data['players']
            resources = game_data['resources']
            return players, resources
    except json.JSONDecodeError:
        print("Erreur lors de la décodage JSON")
    return [], []

# Fonction principale du client
def main():
    running = True
    sock = connect_to_server()  # Connexion au serveur
    
    if not sock:
        return  # Si la connexion échoue, on arrête le jeu
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Recevoir des données du serveur
        players, resources = receive_game_data(sock)

        # Dessiner le monde du jeu
        draw_world(players, resources)
        
        # Mise à jour de l'écran
        pygame.display.flip()
        
        # Limiter la vitesse à 30 FPS
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
