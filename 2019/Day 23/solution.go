package main

import (
	"advent-of-code/2019/intcode"
	"advent-of-code/aochelpers"
	"runtime"
	"strconv"
	"sync"
)

func main() {
	input := aochelpers.GetInput(2019, 23)
	part1(input)
	part2(input)
}

type packet struct {
	dest int64
	x, y int64
}

func part1(input string) {
	println("The correct answer to Part 1 is 27182")
	router := make(chan packet)
	completedPrograms := sync.WaitGroup{}
	completedPrograms.Add(50)
	go func() {
		completedPrograms.Wait()
		close(router)
	}()
	outputHandler := func(outChan <-chan int64) {
		for dest := range outChan {
			x := <-outChan
			y := <-outChan
			router <- packet{dest, x, y}
		}
		completedPrograms.Done()
	}
	messageQueues := []chan int64{}
	for id := 0; id < 50; id++ {
		c := make(chan int64, 100)
		messageQueues = append(messageQueues, c)
		outChan := intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(c, intcode.EOFTerminateProgram))
		go outputHandler(outChan)
		c <- int64(id)
		c <- -1
	}
	for p := range router {
		if p.dest == 255 {
			println("The answer to part one is " + strconv.FormatInt(p.y, 10))
			break
		}
		messageQueues[p.dest] <- p.x
		messageQueues[p.dest] <- p.y
	}
	for _, c := range messageQueues {
		close(c)
	}
	// Clear the router so that all goroutines can exit
	for range router {
	}
}

type packetTracker struct {
	dest   int64
	isSend bool
}

func part2(input string) {
	println("The correct answer to Part 2 is 19285")
	router := make(chan packet)
	networkTracker := make(chan packetTracker)
	completedPrograms := sync.WaitGroup{}
	completedPrograms.Add(50)
	go func() {
		completedPrograms.Wait()
		close(router)
		close(networkTracker)
	}()

	messagesHandled := sync.WaitGroup{}
	computerSender := func(id int64, input <-chan packet) func() int64 {
		gaveID := false
		initialNegative := false
		var currentPacket *packet
		return func() int64 {
			if !gaveID {
				gaveID = true
				return id
			}
			if !initialNegative {
				initialNegative = true
				return -1
			}
			if currentPacket != nil {
				val := currentPacket.y
				currentPacket = nil
				return val
			}
			networkTracker <- packetTracker{id, false}
			nextPacket, ok := <-input
			if !ok {
				runtime.Goexit()
			}
			messagesHandled.Done()
			currentPacket = &nextPacket
			return currentPacket.x
		}
	}
	outputHandler := func(id int64, outChan <-chan int64) {
		for dest := range outChan {
			messagesHandled.Add(1)
			networkTracker <- packetTracker{dest, true}
			x := <-outChan
			y := <-outChan
			router <- packet{dest, x, y}
		}
		completedPrograms.Done()
	}
	messageQueues := map[int64]chan packet{}
	for id := 0; id < 50; id++ {
		c := make(chan packet, 100)
		messageQueues[int64(id)] = c
		outChan := intcode.Parse(input).AsyncRun(computerSender(int64(id), c))
		go outputHandler(int64(id), outChan)
	}
	natChannel := make(chan packet)
	messageQueues[255] = natChannel
	var natMemory packet
	go func() {
		for p := range natChannel {
			natMemory = p
			messagesHandled.Done()
		}
	}()
	go func() {
		lastY := int64(0)
		pendingPacketCounts := []int{}
		for len(pendingPacketCounts) < 50 {
			pendingPacketCounts = append(pendingPacketCounts, 0)
		}
		idleComputers := 0
		for io := range networkTracker {
			if io.dest == 255 {
				continue
			}
			if io.isSend {
				pendingPacketCounts[io.dest]++
				if pendingPacketCounts[io.dest] == 0 {
					idleComputers--
				}
			} else {
				pendingPacketCounts[io.dest]--
				if pendingPacketCounts[io.dest] == -1 {
					idleComputers++
				}
			}
			if 50 == idleComputers {
				// Wait for all pending messages to be handled (including 255!)
				messagesHandled.Wait()

				if natMemory.y == lastY {
					println("The answer to part two is " + strconv.FormatInt(natMemory.y, 10))
					break
				}
				lastY = natMemory.y
				messagesHandled.Add(1)
				messageQueues[0] <- packet{0, natMemory.x, natMemory.y}
				pendingPacketCounts[0]++
				idleComputers--
			}
		}
		for _, c := range messageQueues {
			close(c)
		}
		// Discard the rest
		for range networkTracker {
		}
	}()
	for p := range router {
		messageQueues[p.dest] <- p
	}
}
