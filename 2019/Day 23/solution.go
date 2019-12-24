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
	messageBus := make(chan packet)
	receiverWG := sync.WaitGroup{}
	receiverWG.Add(50)
	go func() {
		receiverWG.Wait()
		close(messageBus)
	}()
	computerReciever := func(outChan <-chan int64) {
		for dest := range outChan {
			x := <-outChan
			y := <-outChan
			messageBus <- packet{dest, x, y}
		}
		receiverWG.Done()
	}
	channels := []chan int64{}
	for id := 0; id < 50; id++ {
		c := make(chan int64, 10000)
		channels = append(channels, c)
		outChan := intcode.Parse(input).AsyncRun(intcode.InputChannelFunction(c, intcode.EOFTerminateProgram))
		go computerReciever(outChan)
		c <- int64(id)
		c <- -1
	}
	for p := range messageBus {
		if p.dest == 255 {
			println("The answer to part one is " + strconv.FormatInt(p.y, 10))
			break
		}
		if p.dest > int64(len(channels)) {
			panic("This is bad...")
		}
		channels[p.dest] <- p.x
		channels[p.dest] <- p.y
	}
	for _, c := range channels {
		close(c)
	}
	for range messageBus {
	}
}

type packetTracker struct {
	dest   int64
	isSend bool
}

func part2(input string) {
	println("The correct answer to Part 2 is 19285")
	messageBus := make(chan packet)
	networkTracker := make(chan packetTracker)
	receiverWG := sync.WaitGroup{}
	receiverWG.Add(50)
	go func() {
		receiverWG.Wait()
		close(messageBus)
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
			currentPacket = &nextPacket
			return currentPacket.x
		}
	}
	computerReciever := func(id int64, outChan <-chan int64) {
		for dest := range outChan {
			messagesHandled.Add(1)
			networkTracker <- packetTracker{dest, true}
			x := <-outChan
			y := <-outChan
			messageBus <- packet{dest, x, y}
		}
		receiverWG.Done()
	}
	channels := []chan packet{}
	for id := 0; id < 50; id++ {
		c := make(chan packet, 100)
		channels = append(channels, c)
		outChan := intcode.Parse(input).AsyncRun(computerSender(int64(id), c))
		go computerReciever(int64(id), outChan)
	}
	var natMemory packet
	go func() {
		for p := range messageBus {
			if p.dest == 255 {
				natMemory = p
				messagesHandled.Done()
				continue
			}
			if p.dest > int64(len(channels)) {
				panic("This is bad...")
			}
			channels[p.dest] <- p
			messagesHandled.Done()
		}
	}()
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
			channels[0] <- packet{0, natMemory.x, natMemory.y}
			pendingPacketCounts[0]++
			idleComputers--
		}
	}
	for _, c := range channels {
		close(c)
	}
	// Discard the rest
	for range networkTracker {
	}
}
