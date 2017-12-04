# homeassistant-reconcile

Reconcile the entities that exist in Home Assistant with those
in the groups.yaml file.

To use, create a file ~/.homeassistant.ini

    [api]
    password = MYAPI-PASSWORD

And then run this script in the configuration dir. It will parse your
group.yaml file.  The last entry in the group.yaml file (after you have
run this the first time) should be changed to:

    untracked: !include untracked.yaml

This script will create an 'untracked.yaml' file

entities:
- entity1
 ...
- entityN
name: untracked
view: 'yes'


When you run it, you will see 3 lines:
    $ python3 ./reconcile.py

    Num Entities: ###

    Untracked entities: ['entity1','entity2', ...]

    Stale entities: ['entity1','entity2', ...]

The first ### is the number that exist within the API.
The second are the entities which exist withn the API,
but are not in any group.
The 3rd are the entities that exist in a group, but
are not known by the API.




