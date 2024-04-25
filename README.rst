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
2. Scriptable output; First to enable the web and interactive terminal
   interface I use, but also to make mangling the data in bulk easier.
3. Works tomorrow; I don’t want to upgrade my system and find my todo list is
   out of reach [again].

``todo.txt`` provides most of this as a base data format.  Let’s make it
happen!

Required features
-----------------

Body text
'''''''''

I realised very early on that I need some degree of multi-line todo items,
which ``todo.txt`` doesn’t provide.  This isn’t a showstopper however, as it is
really easy to implement in a compliant manner.  The format allows for
user-defined key/value pairs, so we can simply add a ``body:<file>`` element to
an entry.

This method has added advantages too:

* We can navigate using ``gf`` from within vim_.
* We aren’t restricted by file type or content, for example
  ``image:<file>`` or ``json:<file>``.  Easy access via ``<C-r><C-f>`` while
  editing.
* Multiple items can reference the same supporting data, which would require
  duplication with simple multi-line items.
* A self-standardised key set makes it easy to support in an external UI.

.. _taskwarrior: https://taskwarrior.org/
.. _changed the backend: https://taskwarrior.org/docs/upgrade-3/
.. _todo.txt: https://todotxt.org/
.. _vim: https://www.vim.org/
