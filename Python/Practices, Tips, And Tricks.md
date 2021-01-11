# 30 Python Best Practices, Tips, And Tricks

## Improve your Python knowledge and skills

3. Use IPython
IPython is basically an enhanced shell. It’s worth it just for the autocompletion alone, but there is much more. I like it too for all the magic commands that are built-in. Here are a few :

4. List Comprehensions
A list comprehension can replace ugly for loops used to fill a list. The basic syntax for a list comprehension is:

<pre>[ expression for item in list if conditional ]</pre>

<pre>mylist = [i for i in range(10)]
print(mylist)</pre>

5. Check memory usage of your objects
With sys.getsizeof() you can check the memory usage of an object:

<pre>import sys

mylist = range(0, 10000)
print(sys.getsizeof(mylist))
# 48</pre>

Woah… wait… why is this huge list only 48 bytes?
It’s because the range function returns a class that only behaves like a list. A range is a lot more memory efficient than using an actual list of numbers.
You can see for yourself by using a list comprehension to create an actual list of numbers from the same range:

<pre>import sys

myreallist = [x for x in range(0, 10000)]
print(sys.getsizeof(myreallist))
# 87632</pre>

6. Return multiple values
Functions in Python can return more than one variable without the need for a dictionary, a list or a class. It works like this:

<pre>def get_user(id):
    # fetch user from database
    # ....
    return name, birthdate

name, birthdate = get_user(4)</pre>

This is alright for a limited number of return values. But anything past 3 values should be put into a (data) class.


7. Use data classes
Since version 3.7, Python offers data classes. There are several advantages over regular classes or other alternatives like returning multiple values or dictionaries:

- a data class requires a minimal amount of code
- you can compare data classes because __eq__ is implemented for you
- you can easily print a data class for debugging because __repr__ is implemented as well
- data classes require type hints, reduced the chances of bugs

<pre>from dataclasses import dataclass

@dataclass
class Card:
    rank: str
    suit: str
    
card = Card("Q", "hearts")

print(card == card)
# True

print(card.rank)
# 'Q'

print(card)
Card(rank='Q', suit='hearts')</pre>

https://realpython.com/python-data-classes/

8. In place variable swapping
9. Merging dictionaries (Python 3.5+)
10. String to title case
11. Split a string into a list

https://towardsdatascience.com/30-python-best-practices-tips-and-tricks-caefb9f8c5f5
