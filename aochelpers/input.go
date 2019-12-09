package aochelpers

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"strings"
)

func getCacheDirectory() string {
	user, err := user.Current()
	if err != nil {
		panic(err)
	}
	return fmt.Sprintf("%s\\.advent-of-code", user.HomeDir)
}

func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func readFileIntoString(filePath string) string {
	bytes, err := ioutil.ReadFile(filePath)
	if err != nil {
		panic(err)
	}
	return strings.TrimRight(string(bytes), "\n")
}

func getCookieCacheFile() string {
	return fmt.Sprintf("%s\\session-cookie.txt", getCacheDirectory())
}

func forgetSessionCookie() {
	os.Remove(getCookieCacheFile())
}

func getSessionCookie() string {
	cookieCacheFile := getCookieCacheFile()
	if fileExists(cookieCacheFile) {
		return readFileIntoString(cookieCacheFile)
	}
	newCookieQuery := `A new Advent of Code session cookie is needed. Please do the following:
1) Open this in chrome: chrome://settings/cookies/detail?site=adventofcode.com
2) Look at the session cookie and copy the value/content
3) Replace this file with that cookie`
	ioutil.WriteFile(cookieCacheFile, []byte(newCookieQuery), os.ModePerm)
	exec.Command("notepad", cookieCacheFile).Run()
	return readFileIntoString(cookieCacheFile)
}

func downloadFile(url string, filename string, cookies ...http.Cookie) {
	client := new(http.Client)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		panic(err)
	}

	for _, c := range cookies {
		heapCookie := new(http.Cookie)
		*heapCookie = c
		req.AddCookie(heapCookie)
	}

	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// Create the file
	out, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	defer out.Close()

	// Write the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		panic(err)
	}
}

func getInputCacheFile(year int, day int) string {
	return fmt.Sprintf("%s\\%d\\day-%d.txt", getCacheDirectory(), year, day)
}

// GetInput returns the input for a given problem (by year/day)
// It downloads these inputs from the server on-demand, intelligently caching them on disk
// to avoid pinging the server repeatedly. It also has rudimentary handling to detect
// login issues and premature inputs
func GetInput(year int, day int) string {
	notLoggedInFile := "Puzzle inputs differ by user.  Please log in to get your puzzle input."
	tooEarlyFile := "Please don't repeatedly request this endpoint before it unlocks! The calendar countdown is synchronized with the server time; the link will be enabled on the calendar the instant this puzzle becomes available."

	inputFilePath := getInputCacheFile(year, day)
	os.MkdirAll(filepath.Dir(inputFilePath), os.ModePerm)
	if fileExists(inputFilePath) {
		contents := readFileIntoString(inputFilePath)
		if contents != notLoggedInFile && contents != tooEarlyFile {
			// The contents are good! (I think)
			return contents
		}
		os.Remove(inputFilePath)
	}

	url := fmt.Sprintf("https://adventofcode.com/%d/day/%d/input", year, day)
	sessionCookie := http.Cookie{Name: "session", Value: getSessionCookie()}

	downloadFile(url, inputFilePath, sessionCookie)

	contents := readFileIntoString(inputFilePath)
	if contents != notLoggedInFile {
		// The contents are good! (I think)
		return contents
	}

	// The session cookie may be invalid?
	os.Remove(inputFilePath)
	forgetSessionCookie()
	sessionCookie.Value = getSessionCookie()

	// Last try
	downloadFile(url, inputFilePath, sessionCookie)
	return readFileIntoString(inputFilePath)
}

// ForgetInput removes the input from the cache (effectively forcing a re-download on the next attempt)
func ForgetInput(year int, day int) {
	os.Remove(getInputCacheFile(year, day))
}

// ClearInputCache clears the entire input cache (except for the session cookie)
func ClearInputCache() {
	cacheDir := getCacheDirectory()

	// Make sure it exists, it's just easier this way
	os.MkdirAll(cacheDir, os.ModePerm)

	cookieFile := filepath.Base(getCookieCacheFile())

	items, _ := ioutil.ReadDir(cacheDir)
	for _, i := range items {
		if cookieFile == i.Name() {
			continue
		}
		toDelete := filepath.Join(cacheDir, i.Name())
		os.RemoveAll(toDelete)
	}
}
