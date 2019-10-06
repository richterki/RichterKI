@ECHO off
:loop

python richter.py

timeout 60

goto loop
