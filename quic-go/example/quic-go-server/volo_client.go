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

	quic "github.com/lucas-clemente/quic-go"
)

const addr = "192.168.0.125:4242"

const message = "loot_vox10_1000.ply"

// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
func main() {
	//go func() { log.Fatal(echoServer()) }()
	err := clientMain(message)
	if err != nil {
		panic(err)
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
	f, err := os.Create(filename)
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
		panic(err)
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
