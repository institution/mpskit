#!/bin/sh
set -e
set -x 
echo 'RUNNING..'
mpskit hag unpack EX.HAG

mpskit dat unpack EX.HAG.dir/MESSAGES.DAT
mpskit dat pack EX.HAG.dir/MESSAGES.DAT
mpskit dat unpack EX.HAG.dir/MESSAGES.DAT

mpskit ss unpack EX.HAG.dir/RM901C1.SS
mpskit ss pack EX.HAG.dir/RM901C1.SS
mpskit ss unpack EX.HAG.dir/RM901C1.SS

mpskit ss unpack EX.HAG.dir/RM505A8.SS
mpskit ss pack EX.HAG.dir/RM505A8.SS
mpskit ss unpack EX.HAG.dir/RM505A8.SS

mpskit ff unpack EX.HAG.dir/FONTCONV.FF
mpskit ff pack EX.HAG.dir/FONTCONV.FF
mpskit ff unpack EX.HAG.dir/FONTCONV.FF

mpskit aa unpack EX.HAG.dir/RM967A.AA
mpskit aa pack EX.HAG.dir/RM967A.AA
mpskit aa unpack EX.HAG.dir/RM967A.AA

mpskit aa unpack EX.HAG.dir/I0.AA
mpskit aa pack EX.HAG.dir/I0.AA
mpskit aa unpack EX.HAG.dir/I0.AA



mpskit hag pack EX.HAG
mpskit hag unpack EX.HAG
echo 'CLEANING..'
rm EX.HAG.dir -r
rm EX.HAG.lst
echo 'OK'



