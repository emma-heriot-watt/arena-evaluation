@echo off
pushd %~dp0
call npm run build
call npm run start -- -p 81 -w
popd
pause
