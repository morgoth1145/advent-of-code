package intcode

import (
	"strconv"
	"strings"
)

// Program holds the state of an Intcode program (obviously)
type Program struct {
	Memory             []int64
	instructionPointer int64
	relativeBase       int64
}

// Parse decodes an Intcode program
func Parse(input string) Program {
	memory := []int64{}
	for _, line := range strings.Split(input, ",") {
		val, _ := strconv.ParseInt(line, 10, 64)
		memory = append(memory, val)
	}
	return Program{Memory: memory, instructionPointer: 0, relativeBase: 0}
}

// InputChannelFunction returns an input function based on an input channel
func InputChannelFunction(input <-chan int64) func() int64 {
	return func() int64 {
		return <-input
	}
}

type parameter struct {
	mode int64
	val  int64
}

func (p *Program) read(param parameter) int64 {
	switch param.mode {
	case 0:
		if param.val > int64(len(p.Memory)) {
			return int64(0)
		}
		return p.Memory[param.val]
	case 1:
		return param.val
	case 2:
		pos := p.relativeBase + param.val
		if pos > int64(len(p.Memory)) {
			return int64(0)
		}
		return p.Memory[pos]
	default:
		panic("Unknown mode")
	}
}

func (p *Program) write(param parameter, val int64) {
	var pos int64
	switch param.mode {
	case 0, 1:
		pos = param.val
	case 2:
		pos = p.relativeBase + param.val
	default:
		panic("Unknown mode")
	}
	for pos >= int64(len(p.Memory)) {
		p.Memory = append(p.Memory, int64(0))
	}
	p.Memory[pos] = val
}

func (p *Program) params(count int) []parameter {
	params := []parameter{}
	modes := p.Memory[p.instructionPointer] / 100
	for paramIdx := 0; paramIdx < count; paramIdx++ {
		params = append(params, parameter{mode: modes % 10, val: p.Memory[p.instructionPointer+int64(paramIdx+1)]})
		modes /= 10
	}
	return params
}

// AsyncRun executes a copy of an Intcode program asynchronously
func (p Program) AsyncRun(input func() int64) <-chan int64 {
	// Copy to avoid messing with the original program
	p = Program{Memory: append([]int64{}, p.Memory...), instructionPointer: p.instructionPointer, relativeBase: p.relativeBase}
	output := make(chan int64)
	impl := func() {
		for {
			switch p.Memory[p.instructionPointer] % 100 {
			case 1:
				params := p.params(3)
				p.write(params[2], p.read(params[0])+p.read(params[1]))
				p.instructionPointer += 4
			case 2:
				params := p.params(3)
				p.write(params[2], p.read(params[0])*p.read(params[1]))
				p.instructionPointer += 4
			case 3:
				p.write(p.params(1)[0], input())
				p.instructionPointer += 2
			case 4:
				output <- p.read(p.params(1)[0])
				p.instructionPointer += 2
			case 5:
				params := p.params(2)
				if p.read(params[0]) != 0 {
					p.instructionPointer = p.read(params[1])
				} else {
					p.instructionPointer += 3
				}
			case 6:
				params := p.params(2)
				if p.read(params[0]) == 0 {
					p.instructionPointer = p.read(params[1])
				} else {
					p.instructionPointer += 3
				}
			case 7:
				params := p.params(3)
				val := int64(0)
				if p.read(params[0]) < p.read(params[1]) {
					val = 1
				}
				p.write(params[2], val)
				p.instructionPointer += 4
			case 8:
				params := p.params(3)
				val := int64(0)
				if p.read(params[0]) == p.read(params[1]) {
					val = 1
				}
				p.write(params[2], val)
				p.instructionPointer += 4
			case 9:
				params := p.params(1)
				p.relativeBase += p.read(params[0])
				p.instructionPointer += 2
			case 99:
				close(output)
				return
			default:
				panic("Something broke!")
			}
		}
	}
	go impl()
	return output
}
