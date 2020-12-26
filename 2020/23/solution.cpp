#include <iostream>
#include <vector>

using namespace std;

struct Link {
    Link *next = nullptr;
    long long num = 0;
};

constexpr long long seed[] = {<seed>};
constexpr long long NUM_CUPS = 1000000;
constexpr long long TURNS = 10000000;

void do_turn(Link *current, std::vector<Link> &links, long long turn) {
    Link *pulled[3];
    long long taboo[3];
    {
        Link *next_pulled = current->next;
        for (int i = 0; i < 3; i++)
        {
            pulled[i] = next_pulled;
            taboo[i] = next_pulled->num;
            next_pulled = next_pulled->next;
        }
        current->next = next_pulled;
    }
    long long dest = current->num - 1;
    if (dest < 1)
        dest = NUM_CUPS;
    while (dest == taboo[0] || dest == taboo[1] || dest == taboo[2])
    {
        dest--;
        if (dest < 1)
            dest = NUM_CUPS;
    }
    auto dest_link = &links[dest];

    pulled[2]->next = dest_link->next;
    dest_link->next = pulled[0];
}

void debug_sequence(Link *start) {
    Link *cur = start;
    for (;;) {
        std::cout << cur->num << ' ';
        cur = cur->next;
        if (cur == nullptr) {
            std::cout << "nullptr" << std::endl;
            return;
        }
        if (cur == start) {
            std::cout << std::endl;
            return;
        }
    }
}

int main() {
    std::vector<Link> links(NUM_CUPS+1);
    for (long long i = 0; i < NUM_CUPS+1; i++) {
        links[i].num = i;
        links[i].next = &links[(i+1)%(NUM_CUPS+1)];
    }
    for (long long idx = 0; idx < 8; idx++) {
        links[seed[idx]].next = &links[seed[idx+1]];
    }
    links[seed[8]].next = &links[10];
    links[NUM_CUPS].next = &links[seed[0]];
    links[0].next = nullptr;
    links[0].num = -1;

    Link *current = &links[seed[0]];
    for (long long i = 0; i < TURNS; i++) {
        do_turn(current, links, i);
        current = current->next;
    }
    const auto one = &links[1];
    const auto a = one->next;
    const auto b = a->next;

    std::cout << a->num << ", " << b->num << ", " << static_cast<long long>(a->num) * static_cast<long long>(b->num) << '\n';

    return 0;
}
