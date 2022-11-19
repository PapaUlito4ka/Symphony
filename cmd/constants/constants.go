package constants

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

var JWT_SECRET string

func InitConstants() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal(err)
		return
	}

	JWT_SECRET = os.Getenv("JWT_SECRET")
}
