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
	"strconv"
	"time"

	quic "github.com/lucas-clemente/quic-go"
)

const addr = "172.31.3.254:4242"

const message_example = "loot_vox10_1286.ply"

// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
func main() {
	
    	ch := make(chan string)
    	go func() {
                err := dashServer()
                if err != nil {
                        panic(err)
                }
        	ch <- "result"
    	}()
    	select {
    	case res := <-ch:
		fmt.Println(res)
    	case <-time.After(time.Second * 25):
		fmt.Println("|WARNING: Server Timeout|")
    	}
//	err := dashServer()
//	if err != nil {
//		panic(err)
//	}
}

func get_content_length(path string) int64{
	fi,err:=os.Stat(path)
	if err ==nil {
		fmt.Println("file size is ",fi.Size(),err)
	}
	return fi.Size()
}
//This function is to 'fill'
func fillString(retunString string, toLength int) string {
	for {
		lengthString := len(retunString)
		if lengthString < toLength {
			retunString = retunString + ":"
			continue
		}
		break
	}
	return retunString
}
//server one session
func serveOne(stream quic.Stream) error {
	message := make([]byte, len(message_example))
	//message := make([]byte, 50)

	_, err := io.ReadFull(stream, message)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Server: Got '%s'\n", message)

	//dirPath := "./lox_h264"
	dirPath := "./TrackedMeshes"
	PthSep := string(os.PathSeparator)
	filepath := dirPath + PthSep + string(message)
	file, err := os.Open(filepath)
	if err != nil {
		panic(err)
	}
	content_length := get_content_length(filepath)
	content_length_str := fillString(strconv.FormatInt(content_length,10),10)
	_, err = stream.Write([]byte(content_length_str))
	if err != nil {
		panic(err)
	}
	n, err := io.Copy(stream, file)
	if err != nil {
		fmt.Println(err)
		panic(err)
	}
	fmt.Println(n)
	fmt.Println("stream closed")
	//time.Sleep(10)
	//sess.CloseWithError(200, "OK")
	return err
}

func dashServer() error {
	listener, err := quic.ListenAddr(addr, generateTLSConfig(), nil)
	if err != nil {
		return err
	}
	sess, err := listener.Accept(context.Background())
	if err != nil {
		return err
	}
	stream, err := sess.AcceptStream(context.Background())
	if err != nil {
		panic(err)
	}
	
	for{
		serveOne(stream)
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
