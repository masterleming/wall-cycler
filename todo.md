# Things still to be done in the project
========================================

- [x] add missing unit tests
    - [x] DataStore
    - [x] TimestampStore
    - [x] ExpirationCheck
- [x] prepare 'main' function
- [x] add program logger
    - [x] add logger to main
    - [x] start logging stuff
    - [ ] ~~rotate the log!~~
- [x] prepare scheduling backends
- [x] prepare wallpaper switching backends
    - [x] extend configuration of sway backend
    - [x] possibly allow force-refresh of the same wallpaper (e.g. with 'daily' wallpaper after a reboot it might be necessary to refresh the wallpaper, because it is not 'remembered' between logins)
- [x] prepare package
- [ ] ~~fix Updaters to detect file removal~~
    - [x] add new mode that would check if files are missing (and optionally remove them from collection)
- [ ] static typing
- [ ] add missing tests
    - [ ] ArgumentParser tests
    - [ ] RuntimeConfig tests
