package main

import (
	"context"
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"fmt"
	quic "github.com/lucas-clemente/quic-go"
	"io"
	"log"
	"math/big"
	"os"
	"strconv"
)

const addr = "172.31.3.254:4242"

const message = "loot_vox10_1002.ply"

//用户
type Chunk struct {
	Filename string `json:"filename"`
}

func read_json_as_chunks(path string) []Chunk {
	var chunks []Chunk
	f, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	decoder := json.NewDecoder(f)
	err = decoder.Decode(&chunks)
	if err != nil {
		fmt.Println("Manifest Deocoding Failed", err.Error())
	} else {
		fmt.Println("Manifest Decoding Suceeded")
	}
	return chunks
}

//logger
func log_init(log_path string) {
	logFile, err := os.OpenFile(log_path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		fmt.Println("open log file failed, err:", err)
		return
	}
	log.SetOutput(logFile)
	log.SetFlags(log.Llongfile | log.Lmicroseconds | log.Ldate)
	log.SetPrefix("[PS]")
}

// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
func main() {
	log_path := "stall_timing.log"
	log_init(log_path)
	//go func() { log.Fatal(echoServer()) }()
	manifest_path := "manifest.json"
	chunks := read_json_as_chunks(manifest_path)
	for index, chunk := range chunks {
		fmt.Println("Fetching" + chunk.Filename)
		err := clientMain(chunk.Filename)
		if err != nil {
			//panic(err)
			fmt.Println(err.Error())
		}
		fmt.Println("Fetched")
		log.Println("Chunk " + strconv.Itoa(index) + " arrived.")
	}
}

func clientMain(filename string) error {
	tlsConf := &tls.Config{
		InsecureSkipVerify: true,
		NextProtos:         []string{"quic-echo-example"},
	}
	session, err := quic.DialAddr(addr, tlsConf, nil)
	if err != nil {
		return err
	}

	stream, err := session.OpenStreamSync(context.Background())
	if err != nil {
		return err
	}

	fmt.Printf("Client: Sending '%s'\n", filename)
	_, err = stream.Write([]byte(filename))
	if err != nil {
		return err
	}
	full_path := filename
	f, err := os.Create(full_path)
	if err != nil {
		fmt.Println("1")
		panic(err)
	}
	defer f.Close()
	fmt.Println("x")
	n, err := io.Copy(f, stream)
	fmt.Println("y")
	if err != nil {
		fmt.Println("1")
		return err
	}
	fmt.Println("Received:" + string(n))
	fmt.Printf("Finished saving...")
	return nil
}

// Setup a bare-bones TLS config for the server
func generateTLSConfig() *tls.Config {
	key, err := rsa.GenerateKey(rand.Reader, 1024)
	if err != nil {
		panic(err)
	}
	template := x509.Certificate{SerialNumber: big.NewInt(1)}
	certDER, err := x509.CreateCertificate(rand.Reader, &template, &template, &key.PublicKey, key)
	if err != nil {
		panic(err)
	}
	keyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})
	certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certDER})

	tlsCert, err := tls.X509KeyPair(certPEM, keyPEM)
	if err != nil {
		panic(err)
	}
	return &tls.Config{
		Certificates: []tls.Certificate{tlsCert},
		NextProtos:   []string{"quic-echo-example"},
	}
}
