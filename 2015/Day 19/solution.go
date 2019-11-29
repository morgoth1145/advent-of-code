package main

import (
	"advent-of-code/aochelpers"
	"strconv"
	"strings"
	"unicode"
)

func main() {
	input := aochelpers.GetInput(2015, 19)
	part1(input)
	part2(input)
}

type replacement struct {
	before string
	after  string
	depth  int
}

func parse(input string) ([]replacement, string) {
	replacements := []replacement{}
	molecule := ""
	for _, line := range strings.Split(input, "\n") {
		molecule = line
		parts := strings.Split(line, " => ")
		if 2 == len(parts) {
			replacements = append(replacements, replacement{before: parts[0], after: parts[1], depth: 1})
		}
	}
	return replacements, molecule
}

func generateMolecules(r replacement, m string) []string {
	out := []string{}
	parts := strings.Split(m, r.before)
	for idx := 0; idx < len(parts)-1; idx++ {
		newMolecule := ""
		newMolecule += strings.Join(parts[:idx+1], r.before)
		newMolecule += r.after
		newMolecule += strings.Join(parts[idx+1:], r.before)
		out = append(out, newMolecule)
	}
	return out
}

func part1(input string) {
	replacements, molecule := parse(input)
	newMolecules := map[string]bool{}
	for _, r := range replacements {
		for _, m := range generateMolecules(r, molecule) {
			newMolecules[m] = true
		}
	}
	println("The answer to part one is " + strconv.Itoa(len(newMolecules)))
}

type stringPair struct {
	first  string
	second string
}

var simpleSequenceMemo map[stringPair][]string = map[stringPair][]string{}

func findSimpleSolution(replacements []replacement, m string, t string) []string {
	if m == t {
		return []string{m}
	}
	key := stringPair{m, t}
	{
		knownValue, present := simpleSequenceMemo[key]
		if present {
			return knownValue
		}
	}
	for _, r := range replacements {
		prefix := ""
		rest := m
		splitIdx := strings.Index(rest, r.after)
		for splitIdx != -1 {
			prefix += rest[:splitIdx]
			rest = rest[splitIdx+len(r.after):]
			subSolution := findSimpleSolution(replacements, prefix+r.before+rest, t)
			if subSolution != nil {
				solution := append([]string{}, subSolution...)
				solution = append(solution, m)
				simpleSequenceMemo[key] = solution
				return solution
			}
			prefix += r.after
			splitIdx = strings.Index(rest, r.after)
		}
	}
	simpleSequenceMemo[key] = nil
	return nil
}

func tokenize(m string) []string {
	out := []string{}
	partial := ""
	for _, c := range m {
		if unicode.IsUpper(c) {
			if len(partial) != 0 {
				out = append(out, partial)
			}
			partial = string(c)
		} else {
			partial += string(c)
		}
	}
	return append(out, partial)
}

func findSolution(replacements []replacement, molecule string, target string) []string {
	parts := []string{}
	suffix := ""
	depth := 0
	for _, a := range tokenize(molecule) {
		if depth == -1 {
			suffix += a
			continue
		}
		switch a {
		case "Rn":
			depth++
			if depth < 1 {
				panic("Invalid parse!")
			}
			if depth == 1 {
				parts = append(parts, suffix)
				suffix = ""
				continue
			}
			suffix += a
		case "Y":
			if depth < 1 {
				panic("Invalid parse!")
			}
			if depth == 1 {
				parts = append(parts, suffix)
				suffix = ""
				continue
			}
			suffix += a
		case "Ar":
			depth--
			if depth < 0 {
				panic("Invalid parse!")
			}
			if depth == 0 {
				parts = append(parts, suffix)
				suffix = ""
				depth = -1 // Poison, we should not see another opening paren now
				continue
			}
			suffix += a
		default:
			suffix += a
		}
	}
	if 0 == len(parts) {
		if len(suffix) == 0 {
			panic("Invalid parse!")
		}
		return findSimpleSolution(replacements, suffix, target)
	}
	if 1 == len(parts) {
		panic("Invalid parse!")
	}
	for _, r := range replacements {
		pieces := strings.Split(r.after, "Rn")
		if 2 != len(pieces) {
			continue
		}
		firstChild := pieces[0]
		otherChildren := strings.Split(pieces[1], "Y")
		if len(otherChildren)+1 != len(parts) {
			continue
		}
		lastChildIdx := len(otherChildren) - 1
		if len(otherChildren[lastChildIdx])-2 != strings.Index(otherChildren[lastChildIdx], "Ar") {
			panic("Unexpected input!")
		}
		otherChildren[lastChildIdx] = otherChildren[lastChildIdx][:len(otherChildren[lastChildIdx])-2]
		childSolutions := [][]string{}
		for idx := 0; idx < len(otherChildren); idx++ {
			childSolution := findSolution(replacements, parts[idx+1], otherChildren[idx])
			if childSolution == nil {
				childSolutions = nil
				break
			}
			childSolutions = append(childSolutions, childSolution)
		}
		if childSolutions == nil {
			continue
		}
		prefix := ""
		rest := parts[0]
		for len(rest) > 0 {
			firstChildSolution := findSolution(replacements, rest, firstChild)
			if firstChildSolution != nil {
				leftover := prefix + r.before + suffix
				leftoverSolution := findSolution(replacements, leftover, target)
				if leftoverSolution != nil {
					// First, do the leftover solution
					solution := append([]string{}, leftoverSolution...)
					// Then do self
					solution = append(solution, prefix+r.after+suffix)
					// Then first child
					assemble := func(first string, others []string) string {
						out := first + "Rn" + others[0]
						for _, c := range others[1:] {
							out += "Y" + c
						}
						return out + "Ar"
					}
					first := firstChildSolution[0]
					others := []string{}
					for _, cs := range childSolutions {
						others = append(others, cs[0])
					}
					for _, step := range firstChildSolution[1:] {
						first = step
						solution = append(solution, prefix+assemble(first, others)+suffix)
					}
					// Then each subsequent child
					for idx, childSolution := range childSolutions {
						for _, step := range childSolution[1:] {
							others[idx] = step
							solution = append(solution, prefix+assemble(first, others)+suffix)
						}
					}
					return solution
				}
			}
			prefix += string(rest[0])
			rest = rest[1:]
		}
	}
	return nil
}

func printSolution(solution []string) {
	for _, step := range solution {
		println(step)
	}
}

func part2(input string) {
	replacements, molecule := parse(input)
	target := "e"

	// All solutions are the same length, so just find one
	solution := findSolution(replacements, molecule, target)
	// printSolution(solution)
	println("The answer to part two is " + strconv.Itoa(len(solution)-1))
}
