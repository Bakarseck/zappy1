package main

import (
	"encoding/json"
	"fmt"
	"net"
	"time"
)

// Structure pour simuler un joueur
type Player struct {
	X int `json:"x"`
	Y int `json:"y"`
}

// Structure pour simuler des ressources
type Resource struct {
	X    int    `json:"x"`
	Y    int    `json:"y"`
	Type string `json:"type"`
}

// Fonction pour gérer un client
func handleConnection(conn net.Conn) {
	defer conn.Close()

	// Simuler quelques joueurs et ressources
	players := []Player{
		{X: 3, Y: 4},
		{X: 6, Y: 2},
		{X: 8, Y: 9},
	}

	resources := []Resource{
		{X: 2, Y: 5, Type: "food"},
		{X: 7, Y: 1, Type: "jade"},
	}

	// Envoyer des données JSON simulées au client toutes les 2 secondes
	for {
		gameData := map[string]interface{}{
			"players":   players,
			"resources": resources,
		}

		jsonData, err := json.Marshal(gameData)
		if err != nil {
			fmt.Println("Erreur lors de la création du JSON :", err)
			return
		}

		// Envoyer les données au client
		conn.Write(jsonData)
		conn.Write([]byte("\n")) // Ajouter une nouvelle ligne pour que le client sache que le message est terminé

		time.Sleep(2 * time.Second) // Attendre 2 secondes avant d'envoyer la prochaine mise à jour
	}
}

func main() {
	// Écouter sur le port 12345
	ln, err := net.Listen("tcp", ":12345")
	if err != nil {
		fmt.Println("Erreur lors de l'écoute du port :", err)
		return
	}
	defer ln.Close()

	fmt.Println("Serveur en attente de connexion sur le port 12345...")

	// Accepter les connexions clients
	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Erreur lors de la connexion client :", err)
			continue
		}

		// Gérer la connexion client
		go handleConnection(conn)
	}
}
