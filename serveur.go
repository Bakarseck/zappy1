package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

type Player struct {
	X        int    `json:"x"`
	Y        int    `json:"y"`
	Food     int    `json:"food"`
	Level    int    `json:"level"`
	TeamName string `json:"team"`
}

type Resource struct {
	X    int    `json:"x"`
	Y    int    `json:"y"`
	Type string `json:"type"`
}

var (
	worldWidth  int
	worldHeight int
	teams       string
	timeDivider int = 100
	maxClients  int
	port        string
)

func init() {
	flag.StringVar(&port, "p", "8080", "Numéro du port")
	flag.IntVar(&worldWidth, "x", 10, "Largeur du monde")
	flag.IntVar(&worldHeight, "y", 10, "Hauteur du monde")
	flag.IntVar(&maxClients, "c", 5, "Nombre de clients autorisés")
	flag.IntVar(&timeDivider, "t", 100, "Diviseur d'unité de temps")
	flag.StringVar(&teams, "n", "", "Noms des équipes séparées par un espace (exemple: team1 team2)")
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: ./server -p <port> -x <width> -y <height> -n <team> [<team>] [<team>] ... -c <nb> [-t <t>]\n")
		flag.PrintDefaults()
	}
}

func main() {
	flag.Parse()

	teamList := strings.Fields(teams)

	if len(teamList) == 0 {
		flag.Usage()
		os.Exit(1)
	}

	fmt.Printf("Démarrage du serveur sur le port %s avec une carte %dx%d et %d clients max.\n", port, worldWidth, worldHeight, maxClients)
	fmt.Printf("Équipes : %s\n", strings.Join(teamList, ", "))
	fmt.Printf("Diviseur de temps : %d\n", timeDivider)

	ln, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Println("Erreur lors de l'écoute :", err)
		return
	}
	defer ln.Close()

	fmt.Println("Serveur en attente de connexions...")

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Erreur lors de l'acceptation d'une connexion :", err)
			continue
		}

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	conn.Write([]byte("WELCOME\n"))

	for {
		buffer := make([]byte, 1024)
		n, err := conn.Read(buffer)
		if err != nil {
			fmt.Println("Erreur de lecture :", err)
			return
		}

		command := strings.TrimSpace(string(buffer[:n]))
		fmt.Printf("Commande reçue : %s\n", command)

		if command == "advance" {
			time.Sleep(time.Duration(7*timeDivider) * time.Millisecond)
			conn.Write([]byte("ok\n"))
		}
	}
}
