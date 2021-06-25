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
values is modulo 3, with the result considered to be in the range {-1, 0, 1}.
Incrementing 1 yields -1 and decrementing -1 yields 1.

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

Jolverine is a reversible language, although that was not at all on the
author's mind when it was created.

Computational Class
-------------------

Jolverine was shown to be Turing-complete by Ørjan Johansen, shortly after
version 1.0 was released.  You can read the full details of the construction
(which involves some rather large Jolverine programs) in the
[Jolverine Turing-completeness proof][] article on the esolangs wiki.

[Jolverine Turing-completeness proof]: http://esolangs.org/wiki/Jolverine_Turing-completeness_proof

Discussion
----------

While I have yet to write a proper loop in Jolverine, others have succeeded
at this.  Some programming techniques that may come in useful for writing
Jolverine programs include:

*   You can always add seven non-stars between a star and the next star to
    be executed without changing the semantics of the second star.  (The
    wheel just does a full rotation, ending up where it was originally.)
*   If you execute the instruction at the top of the wheel, and it is an
    odd-numbered execution step (e.g. the first instruction executed in
    the program, or the third, etc.), the position of that instruction on
    the wheel will not change (it will be removed, but then re-inserted
    exactly where it was.)  The same goes for executing the instruction at
    the bottom of the wheel on an even-numbered execution step.
*   There are other techniques for executing an arbitrary instruction,
    then getting the wheel back into the configuration it was in before
    you started executing it; perhaps not surprisingly, these require
    measures such as leaving every second cell of the tape free for
    scratch space.  See the [Jolverine article][] on the esolangs wiki, and
    its talk page, for more information.

[Jolverine article]: http://esolangs.org/wiki/Jolverine

About this Distribution
-----------------------

This is the reference distribution for Jolverine, and as such, it contains
the reference implementation of Jolverine, written in Python, in the file
`script/jolverine`.

This implementation also handles a very simplistic variant of Jolverine
which I call "Jolverine Super Wimp Mode".  This variant is not supposed to
be a real language, so much as an aid to writing Jolverine programs -- you
prototype them in Jolverine Super Wimp Mode first, then you figure out how to
convert them to Jolverine.  In Jolverine Super Wimp Mode, there is no
wheel at all, and the characters `<`, `>`, `+`, `x`, `y`, `i`, and `o`
execute the seven above-listed instructions directly.

There are some example program in the `eg` directory; those with the file
extension `.jol` are in Jolverine, while those with the extension `.jolswm`
are in Jolverine Super Wimp Mode.

Happy wheel-mangling!  
Chris Pressey  
September 11, 2012  
Montréal, Québec
