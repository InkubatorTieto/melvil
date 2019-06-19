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
- Fix validator for name and surname 
- Fix test for registration and login
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
### Added
Implement editing book
* change book/magazine forms more modular
* add  "edit_book.html" templates
* add view "edit_book"
* add tests

## [0.1.0] - 2019-06-19
### Added 
- login via ldap
- admin accounts are created automatically while container starts

### Changed
- database schema to allow login via ldap
- cron executes once a day at 4am on production
- asset code accepted in two formats e.g. 123456 and ab123456
- search button not present if user not logged in
- borrow time extended to 30 days
- two books with same title are accepted
- app works on port 8080 in production environment

### Deprecated
- personal data storage in database
- cron

### Removed
- password_hash row in User table inside database
- account creation
- password editing
- account activation via email
- nginx

### Fixed
- view reservations -> borrowed show proper return date
- pagination in search, do not lose query during page changing anymore

### Security
- database credentials, secret_key and salt are stored in .env