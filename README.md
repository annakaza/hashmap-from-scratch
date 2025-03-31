# Custom Hash Map Implementations

This project includes **two custom-built hash map implementations** in Python, made without relying on built-in dictionaries or external libraries.
It demonstrates advanced data structure design, collision resolution techniques, dynamic resizing, and clean object-oriented programming.

Implemented versions:
- `hash_map_sc.py` — **Separate Chaining** using singly linked lists
- `hash_map_oa.py` — **Open Addressing** using quadratic probing and tombstones

---

## Features

- **Dynamic resizing** based on load factor thresholds
- **Efficient collision handling** using separate chaining or quadratic probing
- **Logical deletions** with tombstone handling (open addressing)
- **Key lookup**, insertion, update, and deletion
- **Load factor analysis** and empty bucket tracking
- **Iterator support** for for-loops (`__iter__`, `__next__`)
- `find_mode()` function (SC version) to identify most frequent elements

This project demonstrates:
- Proficiency with core data structures and algorithms
- Understanding of time and space trade-offs in hash-based systems
- Ability to translate theoretical concepts into efficient, clean code

---

## Project Structure

- `hash_map_sc.py` - hash map using **separate chaining** with linked lists
- `hash_map_oa.py` - hash map using **open addressing** with quadratic probing and tombstones
- `data_structures_support.py` - support file with custom `DynamicArray`, `LinkedList`, and hash functions

Note: The `data_structures_support.py` file was originally provided in Oregon State University's CS261 (Data Structures) course to support student implementations. All `HashMap` functionality and design decisions in this project were implemented independently.

---

## How to Run

Clone the repo and run either file directly:

```bash
python hash_map_sc.py
# or
python hash_map_oa.py
```

Or import the `HashMap` class into your own code for experimentation.

---

## Sample Usage

```python
from hash_map_sc import HashMap

# initialize map
map = HashMap()
map.put("apple", 3)
map.put("banana", 5)
map.put("apple", 7)  # update

# access values
print(map.get("apple"))         # output: 7
print(map.contains_key("pear")) # output: False

# remove and list
map.remove("banana")
print(map.get_keys_and_values())  # output: [('apple', 7)]
```

```python
from hash_map_oa import HashMap

# quadratic probing version
map = HashMap(11, hash_function_1)
map.put("x", 10)
map.put("y", 20)
map.remove("x")
print(map.get("x"))              # output: None
```

---

## Author

Anna Kaza

Connect with me: annakaza06@gmail.com or www.linkedin.com/in/anna-kaza