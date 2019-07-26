package main

import (
	"fmt"
	"math/rand"
	"time"

	"fyne.io/fyne"
	"fyne.io/fyne/app"
	"fyne.io/fyne/widget"
)

func main() {
	textLabel := widget.NewLabel("")
	textLabel.Alignment = fyne.TextAlignCenter

	a := app.New()
	w := a.NewWindow("english speech to japanese text")
	w.Resize(fyne.Size{Width: 200, Height: 100})

	canvasObjects := []fyne.CanvasObject{
		&widget.Label{Text: "text", Alignment: fyne.TextAlignCenter},
		textLabel,
	}

	w.SetContent(&widget.Box{Children: canvasObjects})
	go func() {
		rand.Seed(time.Now().UnixNano())
		for {
			textLabel.SetText(fmt.Sprint(rand.Intn(100)))
			time.Sleep(3 * time.Second)
		}
	}()
	w.ShowAndRun()

	w.ShowAndRun()
}
