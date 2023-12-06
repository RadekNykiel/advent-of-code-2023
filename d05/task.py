from functools import reduce


class Mapping:
    def __init__(self, name):
        self.mapping = []
        self.name = name

    def __str__(self):
        return f"Mapping({sorted(self.mapping, key=lambda x: x.src_start)})"

    def __repr__(self):
        return self.__str__()

    def append(self, item):
        self.mapping.append(item)

    def map(self, src):
        correct_range = [x for x in self.mapping if x.has_src(src)]
        dst = src
        if correct_range:
            dst = correct_range[-1].map(src)
        return dst

    def unmap(self, dst):
        correct_range = [x for x in self.mapping if x.has_dst(dst)]
        src = dst
        if correct_range:
            src = correct_range[-1].unmap(dst)
        return src

    def merge(self, other):
        self_starts = set(x.dst_start for x in self.mapping)
        self_ends = set(x.dst_end for x in self.mapping)
        other_starts = set(x.src_start for x in other.mapping)
        other_ends = set(x.src_end for x in other.mapping)
        new_points = self_starts \
            .union(self_ends) \
            .union(other_starts) \
            .union(other_ends)
        if (m := min(self_starts)) != 0:
            new_points.add(m - 1)
        if (m := min(other_starts)) != 0:
            new_points.add(m - 1)
        if (m1 := max(other_ends)) != (m2 := max(self_ends)):
            new_points.add(min(m1, m2) + 1)
        new_points = list(sorted(new_points))
        merged = Mapping(self.name + other.name)
        for x in range(0, len(new_points) - 1):
            b1 = new_points[x]
            b2 = new_points[x + 1]
            merged.append(MappingItem(other.map(b1), self.unmap(b1), b2 - b1))
        return merged


class MappingItem:
    def __init__(self, dst_start, src_start, range_len):
        self.src_start = src_start
        self.src_end = self.src_start + range_len - 1
        self.dst_start = dst_start
        self.dst_end = self.dst_start + range_len - 1

    def __str__(self):
        return f"{self.src_start}..{self.src_end} => {self.dst_start}..{self.dst_end}\n"

    def __repr__(self):
        return self.__str__()

    def has_src(self, src):
        return src in self.src_range()

    def src_range(self):
        return range(self.src_start, self.src_end + 1)

    def has_dst(self, dst):
        return dst in range(self.dst_start, self.dst_end + 1)

    def map(self, src):
        return self.dst_start + (src - self.src_start)

    def unmap(self, dst):
        return self.src_start + (dst - self.dst_start)


class LowestSolver:
    def __init__(self, map_chain):
        self.map_chain = map_chain

    def solve(self, seed):
        return reduce(lambda r, m: m.map(r), self.map_chain, seed)


def solve_for_task(input_file):
    print(f"Solving for {input_file} data")
    with open(input_file, "r") as fh:
        seeds = fh.readline().split(":")[1].split()
        seeds = list(map(int, seeds))
        map_chain = []
        for line in fh:
            if line.find("map:") != -1:
                map_chain.append(Mapping(line))
            elif line.isspace():
                continue
            else:
                dst_start, src_start, range_len = map(int, line.split())
                mi = MappingItem(dst_start, src_start, range_len)
                map_chain[-1].append(mi)

    ls = LowestSolver(map_chain)
    lowest1 = min(map(ls.solve, seeds))
    print(f"TASK 1 SOLUTION: {lowest1}")

    combined_mapping = reduce(lambda x, y: x.merge(y), map_chain)
    combined_mapping_sort = sorted(combined_mapping.mapping, key=lambda x: x.dst_start)
    seeds_ranges = []
    for a in range(0, len(seeds), 2):
        seed_start = seeds[a]
        seed_end = seed_start + seeds[a + 1]
        seeds_ranges.append((seed_start, seed_end))
    for combined_mapping_part in combined_mapping_sort:
        for tested_seed_range in seeds_ranges:
            tested_start, tested_end = tested_seed_range
            if tested_start <= combined_mapping_part.src_end and tested_end >= combined_mapping_part.src_start:
                print(f"TASK 2 SOLUTION: {ls.solve(max(tested_start, combined_mapping_part.src_start))}")
                return


if __name__ == '__main__':
    solve_for_task("example.txt")
    solve_for_task("input.txt")
