@echo off
echo "Hello, world!" > C:\Users\vboxuser\Documents\b.txt

type nul > "N:\a.txt"

type "E:\a.txt"
echo "Hello, world!" > F:\a.txt

del G:\a.txt
move H:\a.txt H:\b.txt

type nul > I:\a.txt
copy J:\a.txt J:\b.txt

copy /Y K:\a.txt K:\b.txt
move L:\a.txt L:\dir-a\b.txt
move C:\Users\%USERNAME%\b.txt M:\a.txt