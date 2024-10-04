package main

import (
	// "context"
	"encoding/json"
	// "fmt"
	"log"
	"net/http"
	// "os"
	// "strings"
	"time"

	//"github.com/jackc/pgx/v4/pgxpool"

	"github.com/nDmitry/web-benchmarks/golang/common"
)

func main() {

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		users := []common.User{
			{
				ID:       1,
				Username: "erica81",
				Name:     "Donald Walker",
				Sex:      "M",
				Address:  "38908 Debra Neck\nNew Lisatown, OH 45098",
				Mail:     "jasongallagher@gmail.com",
				Birthdate: time.Date(1956, 1, 8, 23, 0, 0, 0, time.UTC),
			},
			{
				ID:       2,
				Username: "amanda61",
				Name:     "Lindsey Roman",
				Sex:      "F",
				Address:  "5931 Jeremy Glens Apt. 316\nNew Michael, GA 35494",
				Mail:     "frances19@yahoo.com",
				Birthdate: time.Date(1977, 1, 3, 23, 0, 0, 0, time.UTC),
			},
			{
				ID:       3,
				Username: "angela50",
				Name:     "James Mayo",
				Sex:      "M",
				Address:  "41395 Victor Tunnel\nDouglasland, NE 98413",
				Mail:     "rachael65@gmail.com",
				Birthdate: time.Date(1923, 2, 21, 0, 0, 0, 0, time.UTC),
			},
			{
				ID:       4,
				Username: "laura69",
				Name:     "Anthony Rodriguez",
				Sex:      "M",
				Address:  "848 Smith Roads\nAmandaburgh, CO 57486",
				Mail:     "smithjennifer@hotmail.com",
				Birthdate: time.Date(1972, 6, 10, 23, 0, 0, 0, time.UTC),
			},
			{
				ID:       5,
				Username: "kromero",
				Name:     "Brian Garrett",
				Sex:      "M",
				Address:  "809 Andrew Viaduct\nDeckerburgh, UT 10823",
				Mail:     "tuckerchad@hotmail.com",
				Birthdate: time.Date(2008, 7, 16, 22, 0, 0, 0, time.UTC),
			},
			{
				ID:       6,
				Username: "catherine38",
				Name:     "Theresa Martin",
				Sex:      "F",
				Address:  "657 Hayes Forge Apt. 098\nEast Chadstad, VA 43810",
				Mail:     "youngelizabeth@gmail.com",
				Birthdate: time.Date(1922, 4, 27, 23, 0, 0, 0, time.UTC),
			},
			{
				ID:       7,
				Username: "richarddavis",
				Name:     "Kenneth Sanchez",
				Sex:      "M",
				Address:  "0106 Mcbride Court\nSouth Donaldville, UT 10381",
				Mail:     "michellepierce@gmail.com",
				Birthdate: time.Date(1977, 11, 19, 23, 0, 0, 0, time.UTC),
			},
			{
				ID:       8,
				Username: "jasonmorales",
				Name:     "Dr. Samuel Martin",
				Sex:      "M",
				Address:  "474 Susan Well\nJenniferland, WI 76415",
				Mail:     "bruce50@gmail.com",
				Birthdate: time.Date(1969, 3, 15, 23, 0, 0, 0, time.UTC),
			},
			{
				ID:       9,
				Username: "lopezbrooke",
				Name:     "Christopher Yu",
				Sex:      "M",
				Address:  "93990 Barnes Passage\nSarahville, ID 52377",
				Mail:     "brewerstephen@hotmail.com",
				Birthdate: time.Date(1914, 3, 10, 0, 0, 0, 0, time.UTC),
			},
			{
				ID:       10,
				Username: "william25",
				Name:     "Kristine Garcia",
				Sex:      "F",
				Address:  "2784 Archer Ports Apt. 841\nTaylorland, NV 36198",
				Mail:     "jasoncooper@hotmail.com",
				Birthdate: time.Date(1940, 3, 28, 23, 0, 0, 0, time.UTC),
			},
		}

		w.Header().Set("Content-Type", "application/json")

		if err := json.NewEncoder(w).Encode(users); err != nil {
			log.Fatal(err)
		}
	})

	log.Fatal(http.ListenAndServe(":8000", nil))
}
