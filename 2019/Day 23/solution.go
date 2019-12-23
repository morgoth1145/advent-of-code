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

type messageQueue struct {
	packets []packet
	mutex   *sync.Mutex
}

func (q *messageQueue) PushIntoQueue(p packet) {
	q.mutex.Lock()
	defer q.mutex.Unlock()
	q.packets = append(q.packets, p)
}

func (q *messageQueue) PopFromQueue() *packet {
	q.mutex.Lock()
	defer q.mutex.Unlock()
	if 0 == len(q.packets) {
		return nil
	}
	p := q.packets[0]
	q.packets = q.packets[1:]
	return &p
}

func makeComputerInputFunc(id int64, q *messageQueue, shutdownFlag *bool) func() int64 {
	gaveID := false
	var currentPacket *packet
	currentPacket = nil
	return func() int64 {
		if !gaveID {
			gaveID = true
			// fmt.Printf("Giving id for %d\n", id)
			return id
		}
		if *shutdownFlag {
			runtime.Goexit()
		}
		if currentPacket != nil {
			val := currentPacket.y
			// fmt.Printf("Packet %d,%d fully processed by %d\n", currentPacket.x, currentPacket.y, id)
			currentPacket = nil
			return val
		}
		currentPacket = q.PopFromQueue()
		if currentPacket == nil {
			// time.Sleep(time.Microsecond) // Don't block, but give other threads time to make progress
			return -1 // No message
		}
		if currentPacket.dest != id {
			panic("Oh no!")
		}
		// fmt.Printf("Packet %d,%d received by %d\n", currentPacket.x, currentPacket.y, id)
		return currentPacket.x
	}
}

func part1(input string) {
	program := intcode.Parse(input)
	computerQueues := []*messageQueue{}
	for id := 0; id < 50; id++ {
		q := &messageQueue{
			[]packet{},
			new(sync.Mutex),
		}
		computerQueues = append(computerQueues, q)
	}
	shutdown := false // Will be true when it should shut down
	messageBus := make(chan packet)
	computerReciever := func(outChan <-chan int64) {
		for !shutdown {
			dest := <-outChan
			x := <-outChan
			y := <-outChan
			messageBus <- packet{dest, x, y}
		}
		// println("Comptuer receiver shut down...")
	}
	for id := 0; id < 50; id++ {
		outChan := program.Clone().AsyncRun(makeComputerInputFunc(int64(id), computerQueues[id], &shutdown))
		go computerReciever(outChan)
	}
	for p := range messageBus {
		if p.dest == 255 {
			shutdown = true
			println("The answer to part one is " + strconv.FormatInt(p.y, 10))
			return
		}
		if p.dest > int64(len(computerQueues)) {
			panic("This is bad...")
		}
		// fmt.Printf("%d, %d => %d\n", p.x, p.y, p.dest)
		computerQueues[p.dest].PushIntoQueue(p)
		// fmt.Printf("Queued\n")
	}
}

func part2(input string) {
}
