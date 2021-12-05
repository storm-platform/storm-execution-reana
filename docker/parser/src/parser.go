package main

import (
	"encoding/json"
	"fmt"
	"os"

	path "path"

	decentcopy "github.com/hugocarreira/go-decent-copy"
)

type FileDefinition struct {
	Source      string `json:"source"`
	Target      string `json:"target"`
	ExecutionId string `json:"executionId"`
	Type        string `json:"type"`
}

type Configuration struct {
	Inputs  []FileDefinition `json:"inputs"`
	Outputs []FileDefinition `json:"outputs"`
}

func LoadConfigurationFile(filename string) (Configuration, error) {

	var config Configuration

	configFile, err := os.Open(filename)
	// defer configFile.Close()

	if err != nil {
		return config, err
	}

	jsonParser := json.NewDecoder(configFile)
	err = jsonParser.Decode(&config)

	return config, err
}

func main() {
	fmt.Println("Reading...")
	argsWithoutProg := os.Args[1:]

	// Extract some arguments
	fileType := argsWithoutProg[2]
	executionId := argsWithoutProg[0]

	// Reading the definition file
	config, _ := LoadConfigurationFile(argsWithoutProg[1])

	// Selecting the file type
	var files []FileDefinition

	if fileType == "input" {
		files = config.Inputs
	} else {
		files = config.Outputs
	}

	// Copying the files
	fmt.Println("Copying the files")
	for i := 0; i < len(files); i++ {
		if files[i].ExecutionId == executionId {
			// Creating the directory
			os.MkdirAll(path.Dir(files[i].Target), 0755)

			// Copy!
			err := decentcopy.Copy(files[i].Source, files[i].Target)

			if err != nil {
				fmt.Printf("Error in copy file : %#v ", err.Error())
			}
		}
	}
}
