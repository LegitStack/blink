the idea behind this project is to make a software architecture that treats computational units as individual autonomous agents in a network; acting in parallel and independently.

Node A, for instance, wants something.
Node A simply names what she wants.
Node B knows how to get what Node A wants but in order to do so he needs to get something first.
Node B names the thing he wants, so he can get Node A's thing for her.
Node C knows how to get what Node B wants but she needs something else.
Node C names that something else she needs.
Node A has the 'something else' that Node C wants so she presents it.
Node C compiles that thing with her other thing and presents it.
Node B sees that and compiles it with his other thing and presents it.
Node A sees that her original request finally exists so she takes it.

I envision 3 basic message queues:

Requests,
Response (always references requests),
Behaviors (can reference a previous behavior or request or response),

A Requests is essentially a request for behavior or a request for information.
A Response is data that someone has requested.
A Behaviors is a log of a behavior a node has performed outside the system. This one can also be treated as shared state like a score where the last record of a certain type is the current score.

All nodes listen to these three message boards all the time.

Each node knows what it can do, and no other nodes inherently know what other nodes do.

The Oracle Node knows everything that can be done by the system.

Each Node can hold state.

You don't need to know who can do what, or what they need to do it. They know that.

I think I may be able to simulate this with objects and coroutines but it's an obvious network architecture so if I can create a prototype with objects perhaps it can serve as a basis for distributed computing.

In a distributed computing model the message boards can be instantiated by distributed consensus protocols such as hashgraph for an internal cluster, or blockchain for an external permissionless environment.

it seems like programming has to go in this direction to me.

That's the idea anyway.


# idea v2

As I've researched this idea a bit more I've learned that what I seem to be describing is a framework written on top of the actor model of programming. In this framework actors don't talk to each other through messages, instead they get and send messages to and from a queue or a series of queues (in this estimation 2 or 3 queues). Also in this framework actors have one or more functions and every argument to every function is a unique function living in some actor. actors come with a 'partial maker coroutine' capabilities so that it can build up functions one parameter at a time and be available to do whatever others are asking them to do in the meantime.

This framework should allow us to have only one mapping of functions to arguments and it makes it so the programmer doesn't need to care about that when calling. The point of this framework is to use a communication scheme that adds to overhead in order to allow the programmer to program things more simply. its all about saving the programmer effort. nothing else.

So if you need 
