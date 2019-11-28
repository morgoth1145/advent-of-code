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

func unique(items []string) []string {
	seen := map[string]bool{}
	output := []string{}
	for _, i := range items {
		_, present := seen[i]
		if present {
			continue
		}
		seen[i] = true
		output = append(output, i)
	}
	return output
}

func createAtomMapping(replacements []replacement) map[string]rune {
	atoms := map[string]bool{}
	// Handle before atoms
	for _, r := range replacements {
		atoms[r.before] = true
	}
	for _, r := range replacements {
		partialAtom := ""
		for _, c := range r.after {
			if unicode.IsUpper(c) {
				if 0 != len(partialAtom) {
					atoms[partialAtom] = true
				}
				partialAtom = ""
			}
			partialAtom += string(c)
		}
		if 0 != len(partialAtom) {
			atoms[partialAtom] = true
		}
	}

	mapping := map[string]rune{}
	next := 'a'
	for a := range atoms {
		mapping[a] = next
		next++
	}
	return mapping
}

func applyMapping(mapping map[string]rune, s string) string {
	out := ""

	partialAtom := ""
	for _, c := range s {
		if unicode.IsUpper(c) {
			if 0 != len(partialAtom) {
				out += string(mapping[partialAtom])
			}
			partialAtom = ""
		}
		partialAtom += string(c)
	}
	if 0 != len(partialAtom) {
		out += string(mapping[partialAtom])
	}
	return out
}

func applyMappingToReplacements(mapping map[string]rune, replacements []replacement) []replacement {
	out := []replacement{}
	for _, r := range replacements {
		out = append(out, replacement{before: applyMapping(mapping, r.before), after: applyMapping(mapping, r.after), depth: r.depth})
	}
	return out
}

func filterUnusedReplacements(replacements []replacement, molecule string) []replacement {
	usedAtoms := map[rune]bool{}
	for _, c := range molecule {
		usedAtoms[c] = true
	}
	for _, r := range replacements {
		for _, c := range r.before {
			usedAtoms[c] = true
		}
	}

	unusedAtoms := map[rune]bool{}
	for _, r := range replacements {
		for _, c := range r.after {
			_, present := usedAtoms[c]
			if !present {
				unusedAtoms[c] = true
			}
		}
	}

	out := []replacement{}
	for _, r := range replacements {
		used := true
		for _, c := range r.after {
			_, present := unusedAtoms[c]
			if present {
				used = false
				break
			}
		}
		if used {
			out = append(out, r)
		}
	}
	return out
}

func filterRedundantReplacements(replacements []replacement) []replacement {
	out := []replacement{}
	for idx, r := range replacements {
		testReplacements := append(append([]replacement{}, out...), replacements[idx+1:]...)
		if strings.Contains(r.after, r.before) {
			// Recursive
			isRedundant := true
			for _, subR := range testReplacements {
				prefix := ""
				rest := subR.after
				nextIdx := strings.Index(rest, r.before)
				for nextIdx != -1 {
					prefix += rest[:nextIdx]
					rest = rest[nextIdx+1:]
					testSequenceLength := findBestSequence(testReplacements, prefix+r.after+rest, subR.before)
					if testSequenceLength == -1 || testSequenceLength > r.depth+subR.depth {
						isRedundant = false
						break
					}
					prefix += r.before
					nextIdx = strings.Index(rest, r.before)
				}
				if !isRedundant {
					break
				}
			}
			if isRedundant {
				// Do I need to check the recursive expansion itself? So far it hasn't been necessary
				continue
			}
		} else {
			// Not recursive
			testSequenceLength := findBestSequence(testReplacements, r.after, r.before)
			if testSequenceLength != -1 && testSequenceLength <= r.depth {
				// This replacement is redundant
				continue
			}
		}
		out = append(out, r)
	}
	return out
}

func inlineInvisibleReplacements(replacements []replacement, molecule string, source string) []replacement {
	usedAtoms := map[string]bool{}
	for _, c := range molecule + source {
		usedAtoms[string(c)] = true
	}

	for {
		candidates := map[string][]replacement{}
		recursiveFound := map[string]bool{}
		for _, r := range replacements {
			_, present := usedAtoms[r.before]
			if present {
				continue
			}
			candidates[r.before] = append(candidates[r.before], r)
			if strings.Contains(r.after, r.before) {
				recursiveFound[r.before] = true
			}
		}
		for badAtom := range recursiveFound {
			delete(candidates, badAtom)
		}
		if len(candidates) == 0 {
			break
		}
		bestAtom := ""
		bestReplacements := len(replacements) + 1
		for atom, atomReplacements := range candidates {
			if len(atomReplacements) < bestReplacements {
				bestAtom = atom
				bestReplacements = len(atomReplacements)
			}
		}

		var generateReplacements func(string, string, string, int) []replacement
		generateReplacements = func(before string, prefix string, rest string, depth int) []replacement {
			splitIdx := strings.Index(rest, bestAtom)
			if splitIdx == -1 {
				return []replacement{replacement{before: before, after: prefix + rest, depth: depth}}
			}
			prefix += rest[:splitIdx]
			rest = rest[splitIdx+1:]
			out := []replacement{}
			for _, inlineR := range candidates[bestAtom] {
				out = append(out, generateReplacements(before, prefix+inlineR.after, rest, depth+inlineR.depth)...)
			}
			return out
		}

		nextReplacements := []replacement{}
		for _, r := range replacements {
			if r.before == bestAtom {
				// This is being inlined!
				continue
			}
			for _, inlinedR := range generateReplacements(r.before, "", r.after, r.depth) {
				nextReplacements = append(nextReplacements, inlinedR)
			}
		}
		replacements = nextReplacements
	}
	return replacements
}

func inlineNonRecursiveReplacements(replacements []replacement, source string) []replacement {
	for {
		fixedAtoms := map[string]bool{}
		for _, c := range source {
			fixedAtoms[string(c)] = true
		}

		for _, r := range replacements {
			if strings.Contains(r.after, r.before) {
				// Recursive replacements are fixed
				fixedAtoms[r.before] = true
			}
		}

		candidates := map[string][]replacement{}
		for _, r := range replacements {
			if fixedAtoms[r.before] {
				continue
			}
			candidates[r.before] = append(candidates[r.before], r)
		}
		if len(candidates) == 0 {
			break
		}
		atomToInline := ""
		for atom := range candidates {
			atomToInline = atom
			break
		}

		var generateReplacements func(string, string, string, int) []replacement
		generateReplacements = func(before string, prefix string, rest string, depth int) []replacement {
			splitIdx := strings.Index(rest, atomToInline)
			if splitIdx == -1 {
				return []replacement{replacement{before: before, after: prefix + rest, depth: depth}}
			}
			prefix += rest[:splitIdx]
			rest = rest[splitIdx+1:]
			out := []replacement{}
			out = append(out, generateReplacements(before, prefix+atomToInline, rest, depth)...)
			for _, inlineR := range candidates[atomToInline] {
				out = append(out, generateReplacements(before, prefix+inlineR.after, rest, depth+inlineR.depth)...)
			}
			return out
		}

		nextReplacements := []replacement{}
		for _, r := range replacements {
			if r.before == atomToInline {
				// This is being inlined!
				continue
			}
			for _, inlinedR := range generateReplacements(r.before, "", r.after, r.depth) {
				nextReplacements = append(nextReplacements, inlinedR)
			}
		}
		replacements = nextReplacements
	}
	return replacements
}

func printSource(replacements []replacement, molecule string, mapping map[string]rune) {
	reverseMapping := map[rune]string{}
	for a, c := range mapping {
		reverseMapping[c] = a
	}
	reverseMap := func(s string) string {
		out := ""
		for _, c := range s {
			out += reverseMapping[c]
		}
		return out
	}
	for _, r := range replacements {
		prefix := ""
		if r.depth > 1 {
			prefix = strconv.Itoa(r.depth) + " "
		}
		println(prefix + reverseMap(r.before) + " => " + reverseMap(r.after))
	}
	println()
	println(reverseMap(molecule))
	println("---------------------------------------------------------------------------")
}

func findBestSequenceImpl(replacements []replacement, molecule string, target string, report bool) int {
	sourceCharacters := map[rune]bool{}
	for _, r := range replacements {
		for _, c := range r.before {
			sourceCharacters[c] = true
		}
	}
	sortedReplacements := []replacement{}
	for len(replacements) > 0 {
		bestIdx := 0
		bestScore := 0
		for idx, r := range replacements {
			reductionScore := len(r.after) - len(r.before)
			uniqueScore := 0
			for _, c := range r.after {
				_, present := sourceCharacters[c]
				if !present {
					uniqueScore++
				}
			}
			score := 100*reductionScore + uniqueScore
			if score > bestScore {
				bestIdx = idx
				bestScore = score
			}
		}
		sortedReplacements = append(sortedReplacements, replacements[bestIdx])
		replacements = append(append([]replacement{}, replacements[:bestIdx]...), replacements[bestIdx+1:]...)
	}

	var recursiveBestSequence func(string, string, int, int) int
	recursiveBestSequence = func(m string, t string, length int, best int) int {
		if best != -1 && length >= best {
			return -1
		}
		if m == t {
			if report {
				println("The new best sequence length is " + strconv.Itoa(length))
			}
			return length
		}
		if len(m) < len(t) {
			return -1
		}
		newBest := best
		for _, r := range sortedReplacements {
			prefix := ""
			rest := m
			splitIdx := strings.Index(rest, r.after)
			for splitIdx != -1 {
				prefix += m[:splitIdx]
				rest = m[splitIdx+len(r.after):]
				childLength := recursiveBestSequence(prefix+r.before+rest, target, length+r.depth, newBest)
				if childLength != -1 {
					if newBest == -1 || childLength < newBest {
						newBest = childLength
					}
				}
				prefix += r.after
				splitIdx = strings.Index(rest, r.after)
			}
		}
		if newBest == best {
			return -1
		}
		return newBest
	}
	return recursiveBestSequence(molecule, target, 0, -1)
}

func findBestSequence(replacements []replacement, molecule string, target string) int {
	return findBestSequenceImpl(replacements, molecule, target, false)
}

func part2(input string) {
	replacements, molecule := parse(input)
	target := "e"

	// Reduce complexity (one character per atom)
	atomMapping := createAtomMapping(replacements)
	replacements = applyMappingToReplacements(atomMapping, replacements)
	molecule = applyMapping(atomMapping, molecule)
	target = applyMapping(atomMapping, target)

	// println("Initial state")
	// printSource(replacements, molecule, atomMapping)

	// println("Filter unused")
	replacements = filterUnusedReplacements(replacements, molecule)
	// printSource(replacements, molecule, atomMapping)

	// println("Filter redundant 1")
	replacements = filterRedundantReplacements(replacements)
	// printSource(replacements, molecule, atomMapping)

	// println("Inline invisible 1")
	replacements = inlineInvisibleReplacements(replacements, molecule, target)
	// printSource(replacements, molecule, atomMapping)

	// println("Filter redundant 2")
	replacements = filterRedundantReplacements(replacements)
	// printSource(replacements, molecule, atomMapping)

	// println("Inline invisible 2")
	replacements = inlineInvisibleReplacements(replacements, molecule, target)
	// printSource(replacements, molecule, atomMapping)

	// println("Filter redundant 3")
	replacements = filterRedundantReplacements(replacements)
	// printSource(replacements, molecule, atomMapping)

	// println("Inline non-recursive 1")
	replacements = inlineNonRecursiveReplacements(replacements, target)
	// printSource(replacements, molecule, atomMapping)

	// println("Filter redundant 4")
	replacements = filterRedundantReplacements(replacements)
	// printSource(replacements, molecule, atomMapping)

	// SiTh *only* occurs in locations where the Ca->SiTh transform occured
	// Maybe it can only occur from Ca->SiTh transforms period?
	// No. F->SiAl->SiThF

	// How about I try a greedy algorithm that prefers the greatest shortening?
	// On ties, prefer replacements generating output-only atoms

	// What about a build-up approach that is like A* where the heuristic is matching prefix?
	// Or where the heuristic is total matching characters with a dumb check?
	// But I still need to calculate distance...

	sequenceLength := findBestSequenceImpl(replacements, molecule, target, true)
	//sequenceLength := 0
	println("The answer to part two is " + strconv.Itoa(sequenceLength))
}
