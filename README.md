# What is Blink?

First of all, Blink is a proof of concept still. Blink is a framework that sits on top of the actor model of programming. Blink treats every behavior of the system, and every thing that triggers the system to behave as event driven. It also treats the whole system as one coherent environment, and pushes the responsibility to acquire arguments for function off onto the functions themselves.

## Blink Concepts:

There are a few concepts in Blink:

Functions - basically everything is a function in Blink. State is encapsulated in functions. In other words, every argument to every function actually corresponds to the name of a different function. In this way an actor can ask for the result of a function without needing to supply it's arguments. (By the way, supplying it's arguments is done through substitution of the function-name-as-argument for some other function name the actor is in control of).

Actors - Higher level than a function is an Actor. If functions are like knowledge about how to do something Actors are like people that know how to do things: they have several functions inside of them that they can perform. Upon request an actor may perform a function and return the results. Every actor must have unique functions.

Message Boards - message boards, prototyped by the object MSGBoard are analogous to message queues. Actors don't talk to each other directly, instead, they post messages on message boards, the boards don't even have a specific recipient, they simply request a function to be ran. If an actor subscribes to that message board that knows how to run the function they will attempt to do so, gathering up all the arguments (requesting other function calls) before they run the function and post a response message containing it's output.

Messages - as described above messages are not addressed to a specific actor. Ideally messages should have a protocol specific the board on which they're placed, but this feature has not been implemented. Messages have a few required fields: `id`, `ref_id`, `request`. Response messages have a `response` field. An optional field that modifies request is `substitutions` which is a dictionary and if an original request has that field all subsequent requests will have the `substitution` field to keep track of what the function should ultimately be substituted as. Here is an example of a few messages that might be sent to the message board in order:

  `{'id': 1, 'ref_id': 1, 'request': 'foo', 'substitutions': {'bar':'baz', 'baz':'bar'}}`

  `{'id': 2, 'ref_id': 1, 'request': 'baz', 'substitution': 'bar'}`

  `{'id': 3, 'ref_id': 1, 'request': 'bar', 'substitution': 'baz'}`

  `{'id': 4, 'ref_id': 2, 'request': 'baz', 'substitution': 'bar', 'response': 3}`

  `{'id': 5, 'ref_id': 2, 'request': 'bar', 'substitution': 'baz', 'response': 7}`

  `{'id': 6, 'ref_id': 1, 'request': 'foo', 'response': 10}`

In this example the `baz` function returns `3` and the `bar` function returns `7`. They are fed into the `foo` function as each other though: `foo(bar=3, baz=7)`. As you can see the `ref_id` is referring to the `id` number of the request that triggered it. The `request` is merely the name of a function, without regard to where that function lives or what it's inputs are, except in the case that we added `substitutions`.

(Originally the plan was that different boards would manage these different 'types' of messages: 'requests' 'responses', 'behaviors', but it was determined, at least for now, that these are protocol-level types because the way actors work require these combinations of fields, and therefore these types shouldn't be coupled to specifically named boards, perhaps that will change in the future, having 3 boards as required but other boards as optional too with their own protocols. Using multiple boards would require referencing `id`s across boards, that would require a `ref_board` field which seems to complicate things, but could also add the ability to make more refined and intricate systems.)

`behavior` and `result` were originally thought to be a record keeping system for things an actor has done that was not triggered by another actor. However, upon closer review we've decided to remove `behavior` and `result` in favor of creating an actor that listens to outside systems and then makes a formal request upon being triggered. that way everything can fit into the framework of `request`->`response`.

## Philosophy

The idea behind this proof of concept is to see what can be done in an environment where we've flipped the responsibility. Typically, in programming in general, if you're going to call a function you have to decide exactly what the function should receive as it's arguments. If we flip the responsibility to the function being called (or the actor overseeing the function being called) to get those arguments then we by necessity turn the whole system in to an environment where any element of that environment can be looked up in real time and used as input.

What implications does this 'flipping' of responsibility have? I don't know. Does it make building actual software that gets stuff done correctly harder? Or is there a way to work in this paradigm that reinforces the truth and which we might find more intuitive? I don't know.

It seems to my intuition that not only is a distributed architecture the future, but also a swarm architecture where each actor is endowed with some level of intelligence and given dominion over understanding certain types of tasks. The pattern we are concepting out here is merely that idea in it's infancy out of micromanagement.

I think that perhaps a major component to this architecture's power is it's ability to (though it involves communication overhead that a simple set of instructions do not) automatically work on many computers as it does on one computer without changing the codebase whatsoever. I mean you need to switch out the communication model for something that communicates over a network instead of this in memory object model but that's nothing once the system is mature. And in order to reduce the amount of communication required you can, (or the program itself can learn to) group common functions together in the same actors.

Functions are just names given for a specific transformation on data. but a function can also be modified. Thus the data that it is transforming can be a representation of a transformation on unknown data. Thus functions can be incrementally mutated over the life of the system.

eventually we want to get to the point where actors are guiding other actors on how to change in a hierarchy and networked fashion. If all functions are just a transformation on data and if the representation for that transformation is itself just data we want to have functions modify other functions so they tranform the data correctly for their context and needs

## integrating with distributed consensus mechanisms

One thing that must be done before this system is mature is to integrate the gossip protocol (Hashgraph) so that actors can re-evaluate past decisions they made in light of new information about the true state of the system at the time that their decision was made and issue an updated response in the event that something substantial they believed or took as input was not true and therefore their response was inaccurate to the requested task.

## to do:

fix triggers to trigger special case shutdown (triggers work for normal case)

node add ability to refer to a different board
node add ability to trigger messages to go to a different board
node add ability to substitute arguments when adding functions to the actor such as when we have a print_someting function that we want to be able to pass any function into it and then have it pass return the original object to pass onto something else

decide what to do - request response at protocol level or message board level? probably protocol

give actors ability to run already owned functions without creating a message (without officially asking yourself to run them (we should record them somewhere incase others have triggers on that function - so maybe a behaviors message board pattern is a good idea, or maybe it's a new message type: like an fyi request that others will automatically ignore unless they're waiting to be triggered by something.), I kind of do want to keep it asking itself officially to do things it knows about because I want to have an accurate history of what happened when...)

integrate gossip about gossip protocol to come to a consensus on the ordering of events and the true state of the system at any given moment

integrate a response mechanism to the gossip protocol so that if a previous response was junk due to a lack of knowledge about the true state of the system we can issue an updated response

explore 'context' pattern

explore default argument={} pattern to automatically remember state
