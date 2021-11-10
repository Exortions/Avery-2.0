@echo off
echo Commiting %1 to master branch...

git add .
git commit -m %1
git push