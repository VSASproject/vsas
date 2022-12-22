package main

import (
	"context"
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io"
	"math/big"
	"os"
	"time"

	quic "github.com/lucas-clemente/quic-go"
)

const addr = "192.168.0.125:4242"

const message_example = "loot_vox10_1000.ply"

// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
func main() {
	err := echoServer()
	if err != nil {
		panic(err)
	}
}

func serveOne(sess quic.Session) error {
	stream, err := sess.AcceptStream(context.Background())
	if err != nil {
		panic(err)
	}

	message := make([]byte, len(message_example))
	_, err = io.ReadFull(stream, message)
	if err != nil {
		return err
	}
	fmt.Printf("Server: Got '%s'\n", message)

	dirPath := "D:\\volumetric\\dataset\\8i\\loot\\Ply"
	PthSep := string(os.PathSeparator)
	filepath := dirPath + PthSep + string(message)
	file, err := os.Open(filepath)
	if err != nil {
		panic(err)
	}
	n, err := io.Copy(stream, file)
	if err != nil {
		fmt.Println("1")
		panic(err)
	}
	fmt.Println(n)
	time.Sleep(10)
	sess.CloseWithError(200, "OK")
	return err
}

// Start a server that echos all data on the first stream opened by the client
func echoServer() error {
	listener, err := quic.ListenAddr(addr, generateTLSConfig(), nil)
	if err != nil {
		return err
	}
	for {
		sess, err := listener.Accept(context.Background())
		if err != nil {
			return err
		}
		go serveOne(sess)
	}
	return err
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
