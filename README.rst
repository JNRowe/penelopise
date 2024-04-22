``penelopise`` — Minimal todo tracking
======================================

.. note::

   This isn’t a working tool, or even a *moderately* working tool.  I’m just
   playing around with things.

I’ve been using taskwarrior_ for well over a decade, but the recent release has
left me with somewhat of a quandary.  Version 3 has `changed the backend`_ to
use sqlite, but that makes it incompatible with version 2.  I’m left wondering
if it makes more sense to switch tools than try to figure out how to work while
the different systems I use migrate to making version 3 available at their own
pace.  My question is “What is the *least* amount of effort that could get me
to a working system?”

Perhaps it would be possible to just revert to using todo.txt_, and bring the
experience I value from taskwarrior along for the ride.  What this means to me:

1. Local; I don’t want to trust my data to a remote service for both privacy
   and availability reasons.
2. Scriptable output; firstly to enable the web and interactive terminal
   interface I use, but also to make mangling the data in bulk easier.
3. Works tomorrow; I don’t want to upgrade my system and find my todo list is
   out of reach [again].

``todo.txt`` provides most of this as a base data format.  Let’s make it
happen!

.. _taskwarrior: https://taskwarrior.org/
.. _changed the backend: https://taskwarrior.org/docs/upgrade-3/
.. _todo.txt: https://todotxt.org/
