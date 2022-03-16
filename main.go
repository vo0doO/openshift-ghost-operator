package main

import (
	"fmt"
	"os"

	exec "golang.org/x/sys/execabs"
)

var (
	pd      int
	logFile = "./logs.log"
)

func System(arg1 string, arg2 string) {
	system := exec.Command(arg1, arg2)
	out, err := system.CombinedOutput()
	if err != nil {
		fmt.Println(err)
		panic(err)
	}
	fmt.Printf("System out: %s", out)
}

func Python(en bool, f *os.File, arg1 string, arg2 string, arg3 string, arg4 string, arg5 string) {

	if en != true {
		python := exec.Command("python", arg1, arg2, arg3, arg4, arg5)
		//
		out, err := python.CombinedOutput()
		if err != nil {
			return
		}
		fmt.Printf("Python out: %s", out)
		fmt.Fprintf(f, "Python out: %s", out)
		pd = (*(*python).Process).Pid
	}
	python := exec.Command(".\\.venv\\Scripts\\python.exe", arg1, arg2, arg3, arg4, arg5)

	out, err := python.CombinedOutput()
	if err != nil {
		panic(err)
	}
	fmt.Printf("Python out: %s", out)
	fmt.Fprintf(f, "Python out: %s", out)
	pd = (*(*python).Process).Pid
}

func main() {
	file, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

	if err != nil {
		errStr := err.Error()
		fmt.Printf("%v", errStr)
	}
	fmt.Fprintf(file, "INFO:[+][+][+][+][+][+][+][+][+]|RUN GHOST BACKUP PROCESS|[+][+][+][+][+][+][+][+][+][+][+]")

	if _, err := os.Stat(".venv"); os.IsNotExist(err) {
		Python(false, file, "-m", "venv", ".venv", "", "")
		fmt.Println("Creaded python virtual enviroment")
		fmt.Fprintf(file, "Creaded python virtual enviroment")
		System(".\\.venv\\Scripts\\activate", "")
		Python(true, file, "-m", "pip", "install", "--upgrade", "pip")
		Python(true, file, "-m", "pip", "install", "-r", "requirements.txt")
	}
	fmt.Println("Python virtual enviroment exists")
	fmt.Fprintf(file, "Python virtual enviroment exists")
	System(".\\.venv\\Scripts\\activate", "")
	Python(true, file, "--version", "", "", "", "")
	Python(true, file, "-m", "pip", "--version", "", "")
	fmt.Printf("Python run main.py in pid: %v", pd)
	fmt.Fprintf(file, "Python run main.py in pid: %v", pd)
	Python(true, file, "src\\main.py", "", "", "", "")

	fmt.Fprintf(file, "INFO:[+][+][+][+][+][+][+][+][+]|STOP GHOST BACKUP PROCESS|[+][+][+][+][+][+][+][+][+][+][+]")
}
