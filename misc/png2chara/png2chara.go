package main

import (
	"encoding/json"
	"fmt"
	"os"

	gopngchunkschara "github.com/chrisbward/go-png-chunks-chara"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Please provide a PNG file path as an argument")
		return
	}

	filePath := os.Args[1]

	var chara gopngchunkschara.CharacterCardV1V2
	err := chara.PopulateFromPng(filePath)
	if err != nil {
		fmt.Println(err)
		return
	}
	jsonData, err := json.Marshal(chara)
	if err != nil {
		fmt.Println("Error marshaling to JSON:", err)
		return
	}
	fmt.Println(string(jsonData))

}
