package helpers

import "time"

// PrintCurrentTime prints the current time to microsecond accuracy
func PrintCurrentTime() {
	println(time.Now().Format("2006-01-02 15:04:05.000000000"))
}
