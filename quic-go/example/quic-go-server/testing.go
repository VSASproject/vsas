package main
 
import (
    "fmt"
    "io/ioutil"
    "bufio"
    "os"
    "strconv"
    "strings"
)
 
func main() {
	files, _ := ioutil.ReadDir("./i_frame/")
	filePath := "./manifest_nil2.json"
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
		//buffer := "{\"nal_no\": " + strconv.Itoa(1000 + counter) + ", \"filename\": \"" + f.Name + "\", \"type\": " + strconv.Itoa(-1) + "}"
		write.WriteString(strings.Join([]string{"{\"nal_no\": ", strconv.Itoa(1000 + counter), ", \"filename\": \"", filename, "\", \"type\": ", strconv.Itoa(-1), "}"}, ""))	
		counter += 1
	}
	write.WriteString("]")
	write.Flush()
}
