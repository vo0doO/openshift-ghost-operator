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

func System(name string, args ...string) {
	system := exec.Command(name, args...)
	out, err := system.CombinedOutput()
	if err != nil {
		fmt.Println(err)
		panic(err)
	}
	fmt.Printf("System out: %s", out)
}

func Python(en string, f *os.File, args ...string) {
	var python *exec.Cmd
	if en == "notEnv" {
		python = exec.Command("python", args...)
	} else {
		System(".\\.venv\\Scripts\\activate")
		python = exec.Command(".\\.venv\\Scripts\\python.exe", args...)
	}

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
	fmt.Println("INFO:[+][+][+][+][+][+][+][+][+]|RUN GHOST BACKUP PROCESS|[+][+][+][+][+][+][+][+][+][+][+]")
	fmt.Fprintf(file, "INFO:[+][+][+][+][+][+][+][+][+]|RUN GHOST BACKUP PROCESS|[+][+][+][+][+][+][+][+][+][+][+]")
	if _, err := os.Stat(".\\src"); os.IsNotExist(err) {
		System("git", "clone", "https://github.com/vo0doo/sync-ghost-openshift")
	}

	if _, err := os.Stat(".\\.venv"); os.IsNotExist(err) {
		fmt.Println("Python virtual enviroment is not exists")
		fmt.Fprintf(file, "Python virtual enviroment is not exists")
		Python("notEnv", file, "-m", "venv", ".\\.venv")
		fmt.Println("Creaded python virtual enviroment")
		fmt.Fprintf(file, "Creaded python virtual enviroment")
		System(".\\.venv\\Scripts\\activate")
		Python("", file, "-m", "pip", "install", "--upgrade", "pip")
		Python("", file, "-m", "pip", "install", "-r", "requirements.txt")
	}

	Python("", file, "--version")
	Python("", file, "-m", "pip", "--version")
	fmt.Printf("Python run main.py in pid: %v", pd)
	fmt.Fprintf(file, "Python run main.py in pid: %v", pd)
	Python("", file, "src\\main.py")
	fmt.Println("INFO:[+][+][+][+][+][+][+][+][+]|RUN GHOST BACKUP PROCESS|[+][+][+][+][+][+][+][+][+][+][+]")
	fmt.Fprintf(file, "INFO:[+][+][+][+][+][+][+][+][+]|STOP GHOST BACKUP PROCESS|[+][+][+][+][+][+][+][+][+][+][+]")
}
