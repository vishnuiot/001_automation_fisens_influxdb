ECHO OFF
ECHO SOFTWARE VERSION 2.3 - Beta 
ECHO Authors : Dr Vishnu Prasad ,Dr Kavitha Arunachalam IIT MADRAS
ECHO %DATE%
if %d%==10 (echo "End of trial period") else (echo "unknown")
ECHO CHECKING INTERROGATOR STATUS ..
set /p var1= Enter time in minutes  and press enter : 
set /a var2=%var1% * 60
SET /A a = 5 
SET /A b = 10
SET /A c = %a% + %b% 
if %c%==15 (echo "The value of variable c is 15") else (echo "Unknown value") 
if %c%==10 (echo "The value of variable c is 10") else (echo "Unknown value")
PAUSE
