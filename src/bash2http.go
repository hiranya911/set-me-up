// This tool exposes any binary (shell command/script) as an HTTP service.
// A remote client can trigger the execution of the command by sending
// a simple HTTP request. The output of the command execution is sent
// back to the client in plain text format.
package main

import (
	"flag"
	"fmt"
	"net/http"
	"os/exec"
	"strings"
)

func main() {
	binary := flag.String("b", "", "Path to the executable binary")
	port := flag.Int("p", 8080, "HTTP port to listen on")
	flag.Parse()

	if *binary == "" {
		fmt.Println("Path to binary not specified.")
		return
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fields := strings.Fields(*binary)
		output, err := exec.Command(fields[0], fields[1:]...).Output()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "text/plain")
		w.Write(output)
	})

	fmt.Printf("Listening on port %d...\n", *port)
	fmt.Printf("Exposed binary: %s\n", *binary)
	http.ListenAndServe(fmt.Sprintf("127.0.0.1:%d", *port), nil)
}
