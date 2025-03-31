# Project: Custom Hash Map with Separate Chaining
# Author: Anna Kaza

# This project implements a custom HashMap data structure from scratch using separate chaining
# (singly linked lists) to handle collisions. It supports dynamic resizing, load factor analysis, 
# key/value operations, and includes an efficient find_mode() function for frequency analysis.

# This project demonstrates data structure design, collision resolution techniques, hash function usage,
# dynamic resizing, and time-efficient lookup and insertion.

from data_structures_support import (DynamicArray, LinkedList, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """Initialize new HashMap that uses separate chaining for collision resolution."""
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """Override string method to provide more readable output."""
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """Increment from given number and the find the closest prime number."""
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """Determine if given integer is a prime number and return boolean."""
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """Return size of map."""
        return self._size

    def get_capacity(self) -> int:
        """Return capacity of map."""
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Add or update a key/value pair in the hash map.

        If the key already exists, its value is updated. If not, a new key/value pair is inserted.
        The table is resized (to double its capacity) if the load factor reaches or exceeds 1.0.

        Parameters:
            - key (str): the key to insert or update
            - value (object): the value to associate with the key
        """
        # resize table if load factor >= 1.0
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # compute the key's index using the hash function and find its bucket
        index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[index]

        # search for a matching key in the bucket
        matching_key = bucket.contains(key)

        if matching_key:
            # if matching key exists, update its value
            matching_key.value = value
        else:
            # if key not found, insert a new node and increment size
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to a new capacity.
        
        If the given capacity is not prime, it is increased to the next highest prime.
        All key/value pairs are rehashed and inserted into a new table of the given size.

        Parameters:
            - new_capacity (int): desired new capacity of the hash table
        """
        # ignore invalid capacity requests
        if new_capacity < 1:
            return

        # ensure new capacity is a prime number
        if not self._is_prime(new_capacity):
            # if not, update it to the next highest prime
            new_capacity = self._next_prime(new_capacity)

        # create a new empty hash table with updated capacity
        new_table = DynamicArray()
        for i in range(new_capacity):
            new_table.append(LinkedList())

        # save references to old table
        old_table = self._buckets
        old_capacity = self._capacity

        # replace current table with the new one
        self._buckets = new_table
        self._capacity = new_capacity
        self._size = 0      # will be recalculated during reinsertion

        # rehash and insert all existing key/value pairs into the new table
        for i in range(old_capacity):
            bucket = old_table[i]
            for n in bucket:
                self.put(n.key, n.value)

    def table_load(self) -> float:
        """
        Return the current load factor of the hash table.

        Load factor is defined as (# of elements stored in the table) / (# of buckets).
        A key performance metric used to trigger resizing.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.
        
        Useful for analyzing space usage and hash function distribution.
        """
        empty_buckets = 0

        # iterate through all buckets and count how many are empty
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str):
        """
        Return the value associated with the given key, or None if the key is not found.

        Parameters:
            - key (str): key to look up

        Returns:
            - value associated with the key, or
            - None if not found
        """
        # compute the key's index using the hash function and find its bucket
        index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[index]

        # search for a matching key in the bucket
        matching_key = bucket.contains(key)

        if matching_key:
            # if matching key exists, return its value
            return matching_key.value
        
        # key not found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Check whether the given key exists in the hash map.

        Parameters:
            - key (str): key to look up

        Returns:
            - True if the key exists
            - False otherwise
        """
        # compute the key's index using the hash function and find its bucket
        index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[index]

        # return True if the key is found in the linked list at this bucket
        if bucket.contains(key):
            return True

        # key not found
        return False

    def remove(self, key: str) -> None:
        """
        Remove the key/value pair associated with the given key, if it exists.

        Parameters:
            - key (str): key to remove
        """
        # compute the key's index using the hash function and find its bucket
        index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[index]

        # attempt to remove the key from the linked list in this bucket
        if bucket.remove(key):
            # decrement size if removal was successful
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray containing all key/value pairs in the hash map.
        Each element is a tuple of the form (key, value).

        Returns:
            - DynamicArray of (key, value) tuples
        """
        hash_array = DynamicArray()

        # iterate over each bucket in the table
        for i in range(self._capacity):
            bucket = self._buckets[i]
            # traverse the linked list in the current bucket
            for node in bucket:
                # append each key/value pair as a tuple
                hash_array.append((node.key, node.value))

        return hash_array

    def clear(self) -> None:
        """
        Remove all key/value pairs from the hash map without changing its capacity.
        """
        # replace each bucket with a new, empty linked list
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()

        # reset the size to zero
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find the mode(s) of a given DynamicArray and return a tuple containing:
        - A DynamicArray with the most frequently occurring value(s)
        - The frequency (int) of the value(s)

    Assumes input array has at least one element and all values are strings.
    Time complexity: O(N)
    """
    # hash map to count frequency of each element
    map = HashMap()

    # count occurrences of each element
    for i in range(da.length()):
        key = da[i]
        if map.contains_key(key):
            # if hash map has matching key, increment its frequency
            value = map.get(key)
            map.put(key, value+1)
        else:
            # otherwise, add key to hash map and set frequency to 1
            map.put(key, 1)

    # retrieve a DynamicArray of all (key, frequency) pairs
    keys_and_values = map.get_keys_and_values()

    # initialize the mode and frequency variables
    mode = DynamicArray()
    mode_freq = 0

    # Iterate through value/frequency pairs to find the mode(s)
    for i in range(keys_and_values.length()):
        value, freq = keys_and_values[i]
        
        # if frequency matches current highest frequency, add value to the mode array
        if freq == mode_freq:
            mode.append(value)
        # if a higher frequency is found, reset the mode array and frequency
        elif freq > mode_freq:
            mode = DynamicArray()
            mode.append(value)
            mode_freq = freq

    # return the mode(s) and the frequency
    return mode, mode_freq