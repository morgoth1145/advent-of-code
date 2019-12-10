package intcode

import (
	"strconv"
	"strings"
)

// Program holds the state of an Intcode program (obviously)
type Program struct {
	memory             []int
	instructionPointer int
}

// Parse decodes an Intcode program
func Parse(input string) Program {
	memory := []int{}
	for _, line := range strings.Split(input, ",") {
		val, _ := strconv.Atoi(line)
		memory = append(memory, val)
	}
	return Program{memory: memory, instructionPointer: 0}
}

type parameter struct {
	mode int
	val  int
}

func (p *Program) read(param parameter) int {
	switch param.mode {
	case 0:
		if param.val > len(p.memory) {
			return 0
		}
		return p.memory[param.val]
	case 1:
		return param.val
	default:
		panic("Unknown mode")
	}
}

func (p *Program) write(param parameter, val int) {
	p.memory[param.val] = val
}

func (p *Program) params(count int) []parameter {
	params := []parameter{}
	modes := p.memory[p.instructionPointer] / 100
	for paramIdx := 0; paramIdx < count; paramIdx++ {
		params = append(params, parameter{mode: modes % 10, val: p.memory[p.instructionPointer+paramIdx+1]})
		modes /= 10
	}
	return params
}

// AsyncRun executes a copy of an Intcode program asynchronously
func (p Program) AsyncRun(input <-chan int) <-chan int {
	// Copy to avoid messing with the original program
	p = Program{memory: append([]int{}, p.memory...), instructionPointer: p.instructionPointer}
	output := make(chan int)
	impl := func() {
		for {
			switch p.memory[p.instructionPointer] % 100 {
			case 1:
				params := p.params(3)
				p.write(params[2], p.read(params[0])+p.read(params[1]))
				p.instructionPointer += 4
			case 2:
				params := p.params(3)
				p.write(params[2], p.read(params[0])*p.read(params[1]))
				p.instructionPointer += 4
			case 3:
				p.write(p.params(1)[0], <-input)
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
				val := 0
				if p.read(params[0]) < p.read(params[1]) {
					val = 1
				}
				p.write(params[2], val)
				p.instructionPointer += 4
			case 8:
				params := p.params(3)
				val := 0
				if p.read(params[0]) == p.read(params[1]) {
					val = 1
				}
				p.write(params[2], val)
				p.instructionPointer += 4
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
