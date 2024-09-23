import pygame
import socket
import json

HOST = 'localhost'  
PORT = 12345        
PLAYER_SIZE = 20  
GRID_SIZE = 50 
WORLD_WIDTH = 10
WORLD_HEIGHT = 10

pygame.mixer.quit()

pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH * GRID_SIZE, WORLD_HEIGHT * GRID_SIZE))
pygame.display.set_caption('Zappy - Client 2D')
clock = pygame.time.Clock()


def draw_world(players, resources):
    screen.fill((255, 255, 255))

    for x in range(0, WORLD_WIDTH * GRID_SIZE, GRID_SIZE):
        for y in range(0, WORLD_HEIGHT * GRID_SIZE, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    for player in players:
        pygame.draw.circle(screen, (0, 0, 255), (player['x'] * GRID_SIZE + GRID_SIZE // 2, player['y'] * GRID_SIZE + GRID_SIZE // 2), PLAYER_SIZE)

    for resource in resources:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(resource['x'] * GRID_SIZE + 10, resource['y'] * GRID_SIZE + 10, 20, 20))

def connect_to_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        return sock
    except ConnectionRefusedError:
        print("Connexion au serveur refusée.")
        return None

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

def main():
    running = True
    sock = connect_to_server()
    
    if not sock:
        return
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        players, resources = receive_game_data(sock)

        draw_world(players, resources)
        
        pygame.display.flip()
        
        clock.tick(50)

    pygame.quit()

if __name__ == "__main__":
    main()
