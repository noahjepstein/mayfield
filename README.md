### mayfield

An ode to Mayfield. 

#### pack-bot

Does a little bit of suitcase-style bin packing. 

Usage: `python pack_bot.py <suitcase-json-url> <parts-json-url>`

I implemented pack_bot using a bottom-up dynamic programming approach. Then, I wanted to test it, so I used [Google's ortools] https://github.com/google/or-tools to implement an alternate solution. Both solutions give the same answer, so I would have to be pretty lucky for both to be wrong! 

Since pack_bot uses ortools, you might have to pip install them via `pip install ortools`. If you don't want to do that, you can also just use:

`python pack_bot.py --without-ortools <suitcase-json-url> <parts-json-url>`

#### rotate

Rotates an NxN matrix of integers given on the stdin.

Undefined input for anything other than an NxN int matrix.

##### Usage:

- `$ ./rotate/build/rotate rotate/test/<my_NxN_input_file.txt>`

For an example: 

- `$ ./rotate/build/rotate rotate/test/5x5.txt`

##### Building

Output executable is located in mayfield/rotate/build. 

- `$ git clone https://github.com/noahjepstein/mayfield.git`
- `$ cd mayfield/rotate/build`
- `$ cmake -G "Unix Makefiles" ..`
- `$ make`






