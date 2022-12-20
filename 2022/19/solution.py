import functools
import typing

import lib.aoc

class Blueprint(typing.NamedTuple):
    num: int
    ore_robot_ore_cost: int
    clay_robot_ore_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int

def parse_blueprints(s):
    for line in s.splitlines():
        parts = line.split()
        yield Blueprint(num=int(parts[1][:-1]),
                        ore_robot_ore_cost=int(parts[6]),
                        clay_robot_ore_cost=int(parts[12]),
                        obsidian_robot_ore_cost=int(parts[18]),
                        obsidian_robot_clay_cost=int(parts[21]),
                        geode_robot_ore_cost=int(parts[27]),
                        geode_robot_obsidian_cost=int(parts[30]))

class State(typing.NamedTuple):
    ore_robots: int
    ore: int
    clay_robots: int
    clay: int
    obsidian_robots: int
    obsidian: int
    geode_robots: int
    geodes: int

    def minutes_to_build_ore_robot(self, bp, remaining_time):
        return max((bp.ore_robot_ore_cost - self.ore + self.ore_robots - 1) // self.ore_robots,
                   0) + 1

    def build_ore_robot(self, bp, harvest_minutes):
        return self._replace(ore_robots=self.ore_robots + 1,
                             ore=self.ore + self.ore_robots * harvest_minutes - bp.ore_robot_ore_cost,
                             clay=self.clay + self.clay_robots * harvest_minutes,
                             obsidian=self.obsidian + self.obsidian_robots * harvest_minutes,
                             geodes=self.geodes + self.geode_robots * harvest_minutes)

    def minutes_to_build_clay_robot(self, bp, remaining_time):
        return max((bp.clay_robot_ore_cost - self.ore + self.ore_robots - 1) // self.ore_robots,
                   0) + 1

    def build_clay_robot(self, bp, harvest_minutes):
        return self._replace(clay_robots=self.clay_robots + 1,
                             ore=self.ore + self.ore_robots * harvest_minutes - bp.clay_robot_ore_cost,
                             clay=self.clay + self.clay_robots * harvest_minutes,
                             obsidian=self.obsidian + self.obsidian_robots * harvest_minutes,
                             geodes=self.geodes + self.geode_robots * harvest_minutes)

    def minutes_to_build_obsidian_robot(self, bp, remaining_time):
        return max((bp.obsidian_robot_ore_cost - self.ore + self.ore_robots - 1) // self.ore_robots,
                   (bp.obsidian_robot_clay_cost - self.clay + self.clay_robots - 1) // self.clay_robots,
                   0) + 1

    def build_obsidian_robot(self, bp, harvest_minutes):
        return self._replace(obsidian_robots=self.obsidian_robots + 1,
                             ore=self.ore + self.ore_robots * harvest_minutes - bp.obsidian_robot_ore_cost,
                             clay=self.clay + self.clay_robots * harvest_minutes - bp.obsidian_robot_clay_cost,
                             obsidian=self.obsidian + self.obsidian_robots * harvest_minutes,
                             geodes=self.geodes + self.geode_robots * harvest_minutes)

    def minutes_to_build_geode_robot(self, bp, remaining_time):
        return max((bp.geode_robot_ore_cost - self.ore + self.ore_robots - 1) // self.ore_robots,
                   (bp.geode_robot_obsidian_cost - self.obsidian + self.obsidian_robots - 1) // self.obsidian_robots,
                   0) + 1

    def build_geode_robot(self, bp, harvest_minutes):
        return self._replace(geode_robots=self.geode_robots + 1,
                             ore=self.ore + self.ore_robots * harvest_minutes - bp.geode_robot_ore_cost,
                             clay=self.clay + self.clay_robots * harvest_minutes,
                             obsidian=self.obsidian + self.obsidian_robots * harvest_minutes - bp.geode_robot_obsidian_cost,
                             geodes=self.geodes + self.geode_robots * harvest_minutes)

    def minimum_guaranteed_geodes(self, remaining_time):
        return self.geodes + self.geode_robots * remaining_time

    def theoretical_maximum_geodes(self, remaining_time):
        if remaining_time <= 1:
            return self.minimum_guaranteed_geodes(remaining_time)

        # If we theoretically built 1 geode robot per minute until time ran
        # out this is how many more geodes we would get
        theoretical_additions = (remaining_time-1) * remaining_time // 2

        return self.minimum_guaranteed_geodes(remaining_time) + theoretical_additions

def max_geodes(bp, minutes):
    max_ore_needed = max(bp.clay_robot_ore_cost,
                         bp.obsidian_robot_ore_cost,
                         bp.geode_robot_ore_cost)

    @functools.cache
    def best_geodes(state, best, remaining_time):
        assert(remaining_time > 0)

        best = max(best, state.minimum_guaranteed_geodes(remaining_time))
        if state.theoretical_maximum_geodes(remaining_time) <= best:
            return best

        # Only try to build robots if:
        # 1) Their prerequisites are being harvested
        # 2) They are needed (as in, there aren't enough for the maximum demand yet)
        # 3) They will be complete early enough to be useful. That is, there is enough
        # time left for a new geode to potentially be harvested thanks to this robot.

        if state.ore_robots < max_ore_needed:
            # Harvest -> geode robot -> harvest
            build_minutes = state.minutes_to_build_ore_robot(bp, remaining_time)
            if build_minutes <= remaining_time-3:
                best = max(best_geodes(state.build_ore_robot(bp, build_minutes),
                                       best, remaining_time-build_minutes),
                           best)

        if state.clay_robots < bp.obsidian_robot_clay_cost:
            # Harvest -> obsidian robot -> harvest -> geode robot -> harvest
            build_minutes = state.minutes_to_build_clay_robot(bp, remaining_time)
            if build_minutes <= remaining_time-5:
                best = max(best_geodes(state.build_clay_robot(bp, build_minutes),
                                       best, remaining_time-build_minutes),
                           best)

        if state.clay_robots > 0 and state.obsidian_robots < bp.geode_robot_obsidian_cost:
            build_minutes = state.minutes_to_build_obsidian_robot(bp, remaining_time)
            # Harvest -> geode robot -> harvest
            if build_minutes <= remaining_time-3:
                best = max(best_geodes(state.build_obsidian_robot(bp, build_minutes),
                                       best, remaining_time-build_minutes),
                           best)

        if state.obsidian_robots > 0:
            build_minutes = state.minutes_to_build_geode_robot(bp, remaining_time)
            # Harvest
            if build_minutes <= remaining_time-1:
                best = max(best_geodes(state.build_geode_robot(bp, build_minutes),
                                       best, remaining_time-build_minutes),
                           best)

        return best

    return best_geodes(State(ore_robots=1,
                             ore=0,
                             clay_robots=0,
                             clay=0,
                             obsidian_robots=0,
                             obsidian=0,
                             geode_robots=0,
                             geodes=0),
                       0, minutes)

def part1(s):
    answer = sum((i+1) * max_geodes(bp, 24)
                 for i, bp in enumerate(parse_blueprints(s)))

    lib.aoc.give_answer(2022, 19, 1, answer)

def part2(s):
    answer = 1

    for bp in list(parse_blueprints(s))[:3]:
        answer *= max_geodes(bp, 32)

    lib.aoc.give_answer(2022, 19, 2, answer)

INPUT = lib.aoc.get_input(2022, 19)
part1(INPUT)
part2(INPUT)
