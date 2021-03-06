package main

import (
	"fmt"
	"log"
	"net/http"
)

var (
	serverList = []*server{
		newServer("worker-1", "http://127.0.0.1:5001"),
		newServer("worker-2", "http://127.0.0.1:5002"),
		newServer("worker-3", "http://127.0.0.1:5003"),
		newServer("worker-4", "http://127.0.0.1:5004"),
	}
	lastServedIndex = 0
)

func main() {
	http.HandleFunc("/", forwardRequest)
	go startHealthCheck()
	log.Fatal(http.ListenAndServe(":8000", nil))
}

func forwardRequest(res http.ResponseWriter, req *http.Request) {
	server, err := getHealthyServer()
	if err != nil {
		http.Error(res, "Couldn't process request: "+err.Error(), http.StatusServiceUnavailable)
		return
	}
	server.ReverseProxy.ServeHTTP(res, req)
}

func getHealthyServer() (*server, error) {
	for i := 0; i < len(serverList); i++ {
		server := getServer()
		if server.Health {
			return server, nil
		}
	}
	return nil, fmt.Errorf("No healthy hosts")
}

func getServer() *server {
	nextIndex := (lastServedIndex + 1) % len(serverList)
	server := serverList[nextIndex]
	lastServedIndex = nextIndex
	return server
}
