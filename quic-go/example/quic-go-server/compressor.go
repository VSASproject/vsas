package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"strings"
	"time"
)

func GetFiles(dirPath string) (files []string, dirs []string, err error) {
	dir, err := ioutil.ReadDir(dirPath)
	if err != nil {
		return nil, nil, err
	}

	PthSep := string(os.PathSeparator)

	for _, fi := range dir {
		if fi.IsDir() {
		} else {
			ok := strings.HasSuffix(fi.Name(), ".obj")
			if ok {
				files = append(files, dirPath+PthSep+fi.Name())
			}
		}
	}
	return files, dirs, nil
}

func main() {
	files, _, _ := GetFiles("D:\\volumetric\\dataset\\8i\\loot\\Ply")
	for _, file := range files {
		fmt.Printf(file + "\n")
		cmd := exec.Command("draco_encoder", "-i", file)
		stdout, err := cmd.Output()
		if err != nil {
			fmt.Println(err.Error())
			break
		}
		fmt.Println(string(stdout))
		time.Sleep(100)
	}
}
