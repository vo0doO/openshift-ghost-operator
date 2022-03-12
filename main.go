package main

import (
	"fmt"
	"log"

	exec "golang.org/x/sys/execabs"
)

func Status() {
	status := exec.Command(".\\oc.exe", "status")
	out, err := status.CombinedOutput()
	if err != nil {
		log.Panicln("Error")
	}
	log.Printf("var: %#+v\n", out)
}

func Pods() {
	pods := exec.Command(".\\oc.exe", "get", "pods", "-l", "app=ghostis", "-o", "name")
	pod, err := pods.CombinedOutput()
	if err != nil {
		log.Println(err)
	}
	log.Printf("var: %s", pod)
}

func SyncContent() {

	var pod_content_dir, local_content_dir string = ":/var/lib/content/data/db.sqlite3", "c:\\Users\\vo0\\.ghost\\ghost.db"
	// "oc rsync {local_content_dir} {pod_name}:{pod_content_dir} --exclude=current --include=content.orig --no-perms",
	sync := exec.Command(".\\oc.exe", "cp", "ghostis-1-xct67"+pod_content_dir, local_content_dir)
	fmt.Println(sync)
	out, err := sync.CombinedOutput()
	if err != nil {
		log.Panic(err)
	}
	log.Println(out)
}

func main() {
	sync := exec.Command(".\\oc.exe", "exec", "ghostis-1-xct67", "--", "ls", "-al")
	out, err := sync.CombinedOutput()
	if err != nil {
		log.Panic(err)
	}
	log.Println(out)
	Status()
	SyncContent()
}
