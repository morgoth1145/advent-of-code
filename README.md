# Patrick Hogg's Advent of Code solutions, libraries, and tools

This repo houses all of my Advent of Code adventures!

---

The automation tooling in `lib.aoc` follows (barring bugs and oversights) the automation guidelines on the [/r/adventofcode community wiki](https://www.reddit.com/r/adventofcode/wiki/faqs/automation) as of November 23rd, 2023. Specifically:
- Outbound calls are throttled by `_rate_limit`. The limits vary based on the call type:
  - Fetching inputs is throttled to 5 seconds.
  - Answer submission is throttled to 0.5 seconds. (In practice this throttle shouldn't get hit due to human solving time and other limits below.)
    - Submitting answers on alternate accounts is throttled to 10 seconds instead. (Blocked until January of the next year to ensure that the leaderboard isn't accidentally corrupted.)
    - In the case of bad answers, the script attempts to record the timeout and wait until the timeout expires until submitting the next answer, effectively throttling to 1, 5, etc. minutes based on the timeout for bad answers.
  - Downloading the puzzle page is throttled to 1 second. This is used for time trials of past problems when the script doesn't already know the correct answers. In practice other throttles should cause waits and limit this further.
  - Verifying that the script has updated credentials (which checks the support page for login status) is throttled to 1 second. (In practice this is seldom hit.)
  - No tooling exists to gather statistics from Advent of Code like a web scraper so no stronger limits are needed per my reading, but these can be adjusted if issues arise.
- Various data is cached to avoid unnecesary server pings:
  - Once inputs are downloaded, they are cached locally. (`lib.aoc.forget_input(year, day)` and `lib.aoc.clear_input_cache()` can clear the cache in case of issues.)
  - Once an answer is submitted, good or bad, the script records it to avoid submitting duplicate answers to the server. (This helps the server and avoids unnecessary timeouts!)
  - Once a problem is solved the script remembers the good answer and validates computed answers against the known answer instead of pinging the server (which won't validate the answer anymore anyway).
- The User-Agent header is set to point to this repo and my e-mail in case of issues arising.

---

One note on the alternate accounts mentioned above. This is a feature in the library to support validate and timing on a slightly larger set of inputs to check that the solution code is correct and to help check for performance issues. On occasion bugs have crept in that got found with alternate accounts, helping me keep my solutions robust!

However, the purpose of those accounts (3 alts at most, one per login method) is solely that validation and timing. As such (and as stated above) the core functionality of submitting answers is blocked on those accounts until January of the next calendar year. This should help preserve the integrity of Advent of Code during the December season in case of human error somewhere (though extra steps are needed to activate the alternate accounts in the script making this highly unlikely in the first place).
