# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add and Edit Copy feature
- Flashing messages support (as Jinja macro)
- Travis CI configuration
- Reservation mechanism design and implement

## [0.0.1] - 2018-06-11
### Added
- Library Item (Book/Magazine) description view with list of copies and buttons to perform actions on them.
- Error handle views for 401, 404 and 500. 
- Adding book view without test
- Add custom validators for every field in add book view
- Fix bug - Eliminate bug with already registered user registration handling
- Creating form for add books in wishlist
- Creating like button in wishlist for users
- Fix for available statu
- Added button that user is logged or not
- Added different options for logged out or logged in user, redirecting to the right page
- Magazine option in add wish view
- Icons of book and magazine in wish list view
- Like button click without reloading page
- Tests for wish list
- Popover with info about wish list
- Creating delete button in wishlist only for admin


## [0.0.1] - 2018-06-20
###Added
Implement editing book
* change book/magazine forms more modular
* add  "edit_book.html" templates
*add view "edit_book"
*add tests