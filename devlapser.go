package main

import (
	"fmt"
	"github.com/kbinani/screenshot"
	"gocv.io/x/gocv"
	"image/jpeg"
	"os"
	"time"
)

func main() {
	video := os.Args[1]
	generate(video)
}

func generate(video string) {
	camera, _ := gocv.OpenVideoCapture(0)

	for frame := 0; ; frame++ {
		generateCameraFrame(camera, video, frame)
		generateScreenFrame(video, frame)
		time.Sleep(2 * time.Second)
	}
}

func generateCameraFrame(camera *gocv.VideoCapture, video string, frame int) {
	img := gocv.NewMat()
	camera.Read(&img)
	gocv.IMWrite(fmt.Sprintf("%s/%d_cam_image.jpg", video, frame), img)
}

func generateScreenFrame(video string, frame int) {
	screen, _ := screenshot.CaptureRect(screenshot.GetDisplayBounds(0))
	file, _ := os.Create(fmt.Sprintf("%s/%d_screen_image.jpg", video, frame));
	defer file.Close()

	_ = jpeg.Encode(file, screen, &jpeg.Options{Quality: 80})
}
