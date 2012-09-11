Jolverine
=========

Language version 1.0

The Jolverine language was devised as a conscious attempt to expand the
genre of turning tarpit by adding the feature of modifying the instruction
wheel during execution.  It is not dissimilar to Wunnel, and was influenced
slightly by Half-Broken Car in Heavy Traffic.

The name is a portmanteau of "jolly wolverine" (where "jolly" is a euphemism
for "drunk",) which is an attempt to capture, in a noun phrase, the language's
vicious, erratic nature.

Program Structure
-----------------

A Jolverine program consists of a two-dimensional grid of symbols.  An
instruction pointer (IP) traverses the grid, starting in the upper-left
corner (x=0, y=0) travelling right (dx=1, dy=0).  dx and dy have only
three possible values, -1, 0, and 1, like values on the tape (see below.)

Execution
---------

On each tick, if the symbol under the IP is a `*`, the current instruction on
the instruction wheel is executed.  The instruction wheel is then advanced to
the next instruction, regardless of what the symbols under the IP contains.
(All symbols that are not `*` have the same meaning, that is to say, no
meaning besides taking up space.)  The IP is then advanced to the next
position in the playfield, and the next tick begins.  Execution halts when
the IP travels beyond the extent of the playfield (i.e. when it can be proved
that, in its direction of travel, it will never again hit a `*`.)

Storage
-------

There is an unbounded tape, with a single head which can be moved left
and right.  Each cell on the tape may contain one of the three values -1, 0,
or 1.  Initially, all tape cells contain 0.  Addition and subtraction of these
values is always "mod 3 - 1": incrementing 1 yields -1 and decrementing -1
yields 1.

Instruction Wheel
-----------------

The instruction wheel contains seven instructions.  Initially, the wheel looks
like this:

    left <--
    right
    rot
    adddx
    adddy
    input
    output

The arrow indicates the current instruction on the wheel.  Each time the
wheel is advanced, the arrow moves down one row, wrapping around back
to the top once it advances past the bottom of the wheel.

Each time an instruction is executed from the wheel, it is removed from the
wheel and re-inserted at a different position.  The first time this happens, it
is re-inserted at the top of the wheel; the second time, it is re-inserted at
the bottom; the third time, at the top again; the fourth time, at the bottom
again; and so forth.

Instructions
------------

*   `left`: moves the tape head left one tape cell.
*   `right`: moves the tape head right one tape cell.
*   `rot`: increments the current tape cell.
*   `adddx`: adds the contents of the current tape cell to the IP's dx.
*   `adddy`: adds the contents of the current tape cell to the IP's dy.
*   `input`: inputs a single bit (I/O is bitwise, and implementation-defined.)
*   `output`: if the current tape cell is 0, output a 0; if the current tape
    cell is 1, output a 1; otherwise RESERVED for future expansion.

Notes
-----

It is entirely possible for `*` to execute `adddx` or `adddy` with the result
of both dx and dy being zero.  In this case, execution does not halt, but
the same `*` will be executed again, and again, until dx or dy changes.

Computational Class
-------------------

Jolverine may or may not be Turing-complete.  If it is not, it is not because
it has insufficient storage, or no way to execute an instruction it has
previously executed; it will be because there is no way to predictably
execute the same series of instructions as was previously executed.

Discussion
----------

I have yet to write a proper loop in Jolverine.  I have only attempted to
write an infinite loop, executing `adddx` and `adddy` alternately after
`rot`ing a cell on the tape.  After a few iterations, you can guarantee
that `adddx` is at the top of the wheel, and `adddy` at the bottom, so you
can choose to execute the next one, as appropriate, and it will not change
the position of these instructions on the wheel (because they're already at
the top and bottom.)  However, I suspect even this technique really requires
some number theory to do effectively -- probably finding the LCM of 7 (the
number of instructions on the wheel) and a couple of other numbers (the
amount you can change the x and y positions on each spin around the
playfield.)

Happy wheel-mangling!  
Chris Pressey  
September 11, 2012  
Montréal, Québec
