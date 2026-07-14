# desktopet
little pet for people who feel lonely


# Changelog

## 14/07/26
## Added
- A skin class to handle different skins for (different) pets.

### Changed
- Save skins on an array and add a skin index.

## 13/07/26

### Added
- Left clicking while walking reverses direction.
- Right click halts the pet.

### Changed
- Implemented a `StateController` class to control and centralise state changes/transitions.
- `timer_schedule` gate variable now replaced by a `pending_job` system where the action/event can be cancelled to give way to other events.

## 11/07/26
### Added
- A random state change. Every 5-10 seconds (randomised), the `update` function changes the pet's state from IDLE to WAITING and vice versa. 
- A `timer_schedule` gate variable (boolean). This is used to lock down a state change. Without it, the state would change constantly and uncontrollably due to new state changes being scheduled as `update` gets called. This ensures that when a state changes, it actually waits and prevents unintended transitions.
- A `transition` function. This uses the `set_state` function but updates the `timer_schedule` variable so that it is unlocked for the new state. This could be done in the `set_state` function but the idea is that the `transition` function can be expanded later on to include more specific rules.

