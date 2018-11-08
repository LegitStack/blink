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

As I've researched this idea a bit more I've learned that what I seem to be describing is a framework written on top of the actor model of programming. In this framework actors don't talk to each other through messages, instead they get and send messages to and from a queue or a series of queues (in this estimation 2 or 3 queues) which is a broadcast to everyone subscribing to the queue. I thought of it this way to keep things simple. Also in this framework actors have one or more functions and every argument to every function is a unique function living in some actor. actors come with 'partial maker coroutine' capabilities so that it can build up functions one parameter at a time and be available to do whatever others are asking them to do in the meantime.

This framework should allow us to have only one mapping of functions to arguments and it makes it so the programmer doesn't need to care about that when calling. The point of this framework is to use a communication scheme that adds to overhead in order to allow the programmer to program things more simply. its all about saving the programmer effort. nothing else.

So if the entity gets a message that contains a request for them to run a function that they have they will look to see if they already have all the functions as arguments that this function requires, they probably will not. so they'll make a partial with what they can, add that partial to a coroutine list, and make a request for the network to give them the arguments they don't already have. once they see that a reply has been supplied referencing their request they will open up that partial and add the new argument to it. If all the arguments have been added they will continue to return it. otherwise they'll wait.

So really the coroutine should be a run_function(function_name, request_id) because they need to look up everything for that function and manage it until they finally run it and return the output as a response referencing the original request.

I think I need a solid example to program first. function a requires no arguments, it simply wraps data which is, we'll say 1. function b takes a and does some computation on it; multiplies it by 2, function c takes a and b and returns b * a. That way if you are the entity that has c function but not a or b you'll ask for a and b at the same time. whoever has a will return it to you. whoever has b will ask for a since they don't already have it and once the entity with a gives it to them they'll give it to you.

Lets throw one more complication into the mix. lets say there are only two entities. but 3 functions.

Entity 1 has functions a and c
Entity 2 has function b

So the user will ask the system for the results of function c. then entity 1 will see that message and notice that it has access to function c. It will then look through the inputs for function c and know that it does have a and does not have b. it will join a to c's argument as a partial, then send in a message to the system to get b then entity 2 will see that message, notice it has b but not b's only argument: a. Entity 2 will then send a request for a then entity 1 will see that message and return the answer to a. Then entity 2, upon receiving a will join it to the function b as a partial and having seen that all arguments have been satisfied will, instead of waiting, run the function, extract the answer and encapsulate it in a message to send back to the requester, entity 1, of course referencing the original request id. entity 1 will receive the message, join the answer to the argument list of c as b and run the function, encapsulate it in a message which it will return to the user.

So the user is really just another entity to the system, one that only makes requests.

so the infrastructure I need to code first is keeping track of these tasks they are waiting on and such.
