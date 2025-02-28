/* -----------------------------------------------------------
Course: CSE 251
Lesson Week: 12
File: team1.go

Purpose: Process URLs

Instructions:

Part 1
- Take this program and use goroutines for the function getPerson().

Part 2
- Create a function "getSpecies()" that will receive the following urls
  using that function as a goroutine.
- For a species, display name, average_height and language

"http://swapi.dev/api/species/1/",
"http://swapi.dev/api/species/2/",
"http://swapi.dev/api/species/3/",
"http://swapi.dev/api/species/6/",
"http://swapi.dev/api/species/15/",
"http://swapi.dev/api/species/19/",
"http://swapi.dev/api/species/20/",
"http://swapi.dev/api/species/23/",
"http://swapi.dev/api/species/24/",
"http://swapi.dev/api/species/25/",
"http://swapi.dev/api/species/26/",
"http://swapi.dev/api/species/27/",
"http://swapi.dev/api/species/28/",
"http://swapi.dev/api/species/29/",
"http://swapi.dev/api/species/30/",
"http://swapi.dev/api/species/33/",
"http://swapi.dev/api/species/34/",
"http://swapi.dev/api/species/35/",
"http://swapi.dev/api/species/36/",
"http://swapi.dev/api/species/37/",

----------------------------------------------------------- */
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
	"time"
)

type Person struct {
	Birth_year string
	Created    time.Time
	Edited     time.Time
	Eye_color  string
	Films      []string
	Gender     string
	Hair_color string
	Height     string
	Homeworld  string
	Mass       string
	Name       string
	Skin_color string
	Species    []string
	Starships  []string
	Url        string
	Vehicles   []string
}

type Species struct {
	Name           string
	Classification string
	Average_height string
	Language       string
}

func getSpecies(wg *sync.WaitGroup, url string) {
	// make a sample HTTP GET request
	res, err := http.Get(url)

	// check for response error
	if err != nil {
		log.Fatal(err)
	}

	// read all response body
	data, _ := ioutil.ReadAll(res.Body)

	// close response body
	res.Body.Close()

	// fmt.Println(string(data))

	species := Species{}
	jsonErr := json.Unmarshal(data, &species)
	if jsonErr != nil {
		log.Fatal(jsonErr)
		fmt.Println("ERROR Pasing the JSON")
	}

	fmt.Println("-----------------------------------------------")
	// fmt.Println(person)
	fmt.Println("Name      			: ", species.Name)
	fmt.Println("Average height     : ", species.Average_height)
	fmt.Println("Language 			: ", species.Language)

	wg.Done()
}

func getPerson(wg *sync.WaitGroup, url string) {
	// make a sample HTTP GET request
	res, err := http.Get(url)

	// check for response error
	if err != nil {
		log.Fatal(err)
	}

	// read all response body
	data, _ := ioutil.ReadAll(res.Body)

	// close response body
	res.Body.Close()

	// fmt.Println(string(data))

	person := Person{}
	jsonErr := json.Unmarshal(data, &person)
	if jsonErr != nil {
		log.Fatal(jsonErr)
		fmt.Println("ERROR Pasing the JSON")
	}

	fmt.Println("-----------------------------------------------")
	// fmt.Println(person)
	fmt.Println("Name      : ", person.Name)
	fmt.Println("Birth     : ", person.Birth_year)
	fmt.Println("Eye color : ", person.Eye_color)

	wg.Done()
}

func main() {
	urls := []string{
		"http://swapi.dev/api/people/1/",
		"http://swapi.dev/api/people/2/",
		"http://swapi.dev/api/people/3/",
		"http://swapi.dev/api/people/4/",
		"http://swapi.dev/api/people/5/",
		"http://swapi.dev/api/people/6/",
		"http://swapi.dev/api/people/7/",
		"http://swapi.dev/api/people/8/",
		"http://swapi.dev/api/people/9/",
		"http://swapi.dev/api/people/10/",
		"http://swapi.dev/api/people/12/",
		"http://swapi.dev/api/people/13/",
		"http://swapi.dev/api/people/14/",
		"http://swapi.dev/api/people/15/",
		"http://swapi.dev/api/people/16/",
		"http://swapi.dev/api/people/18/",
		"http://swapi.dev/api/people/19/",
		"http://swapi.dev/api/people/81/",
	}

	var wg sync.WaitGroup

	for _, url := range urls {
		go getPerson(&wg, url)
		wg.Add(1)
	}
	wg.Wait()

	urls2 := []string{
		"http://swapi.dev/api/species/1/",
		"http://swapi.dev/api/species/2/",
		"http://swapi.dev/api/species/3/",
		"http://swapi.dev/api/species/6/",
		"http://swapi.dev/api/species/15/",
		"http://swapi.dev/api/species/19/",
		"http://swapi.dev/api/species/20/",
		"http://swapi.dev/api/species/23/",
		"http://swapi.dev/api/species/24/",
		"http://swapi.dev/api/species/25/",
		"http://swapi.dev/api/species/26/",
		"http://swapi.dev/api/species/27/",
		"http://swapi.dev/api/species/28/",
		"http://swapi.dev/api/species/29/",
		"http://swapi.dev/api/species/30/",
		"http://swapi.dev/api/species/33/",
		"http://swapi.dev/api/species/34/",
		"http://swapi.dev/api/species/35/",
		"http://swapi.dev/api/species/36/",
		"http://swapi.dev/api/species/37/",
	}

	for _, url := range urls2 {
		go getSpecies(&wg, url)
		wg.Add(1)
	}
	wg.Wait()
	fmt.Println("All done!")
}
