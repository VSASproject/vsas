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
	"encoding/json"
	"strings"
	"bufio"
	"io/ioutil"

	quic "github.com/lucas-clemente/quic-go"
)

const addr = "127.0.0.1:4242"

const message_example = "frames_Ply"

// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.

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

func main() {
    fmt.Println(os.Args[1])
    fmt.Println("--------------------------------------------")
    err := dashServer(os.Args[1])
    if err != nil {
        panic(err)
    }
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
func serveOne(stream quic.Stream, dirPath string, file_name string) error {
	//Send的格式
		PthSep := string(os.PathSeparator)
	        filepath := dirPath + PthSep + file_name
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
		//_, err = io.Copy(stream, file) //文件传输
		n, err := io.Copy(stream, file)
		if err != nil {
			fmt.Println(err)
			panic(err)
		}
		fmt.Println(n)
		fmt.Println("stream closed")
        return err
}

func dashServer(dir_name string) error {
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
		//-------------------------------------------------------------
		message := make([]byte, len(message_example)) //message: directory name.				改动步骤1
		_, err = io.ReadFull(stream, message)
		if err != nil {
			panic(err)
		}
		fmt.Printf("Server: Got '%s'\n", message)
		//-------------------------------------------------------------
		//加生产manifest
        	//PthSep := string(os.PathSeparator)
		files, _ := ioutil.ReadDir("./" + dir_name)
		filePath := "./manifest_nil_ply.json"
		file, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE, 0666)
		if err != nil{
			fmt.Println("Generate False.", err)
		}
		defer file.Close()
		write := bufio.NewWriter(file)
		write.WriteString("[")
		counter := 0
		for _, f := range files {
			if counter > 0{
				write.WriteString(", ")
			}
			filename := f.Name()
			write.WriteString(strings.Join([]string{"{\"nal_no\": ", strconv.Itoa(1000 + counter), ", \"filename\": \"", filename, "\", \"type\": ", strconv.Itoa(-1), "}"}, ""))	
			counter += 1
		}
		write.WriteString("]")
		write.Flush()
	serveOne(stream, ".", filePath)
    	manifest_path_f := "manifest_nil_ply.json"
    	file_chunks := read_json_as_chunks(manifest_path_f)
        for _, file_chunk := range file_chunks {
                file_name := file_chunk.Filename
                serveOne(stream, dir_name, file_name)
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
