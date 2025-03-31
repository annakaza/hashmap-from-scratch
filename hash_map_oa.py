# Project: Custom Hash Map with Open Addressing
# Author: Anna Kaza

# This project implements a custom HashMap data structure from scratch using open addressing
# with quadratic probing for collision resolution. It supports dynamic resizing, key/value operations,
# load factor analysis, iteration, and deletion using tombstones.

# This project demonstrates algorithmic thinking, probing techniques, prime-based resizing,
# iterator implementation, and in-place memory management in Python.

from data_structures_support import (DynamicArray, DynamicArrayException, HashEntry, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """Initialize new HashMap that uses quadratic probing for collision resolution."""
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """Override string method to provide more readable output."""
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """Increment from given number to find the closest prime number."""
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
        The table is resized (to double its capacity) if the load factor reaches or exceeds 0.5.

        Parameters:
            - key (str): the key to insert or update
            - value (object): the value to associate with the key
        """
        # resize table if load factor >= 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # compute the key's initial index using the hash function
        i_initial = self._hash_function(key) % self.get_capacity()
        # initialize the quadratic probe offset
        quad_prob = 0

        while True:
            # compute the key's index using quadratic probing and find its bucket
            index = (i_initial + quad_prob ** 2) % self.get_capacity()
            bucket = self._buckets[index]

            # Case 1: the bucket is empty or a tombstone -> insert a new entry and increment size
            if bucket is None or bucket.is_tombstone:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return

            # Case 2: the key already exists -> update its value
            if bucket.key == key:
                bucket.value = value
                return

            # Case 3: collision occurs -> continue probing
            quad_prob += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to a new capacity and rehash all valid (non-tombstone) entries.
        
        If the given capacity is not prime, it is increased to the next highest prime.
        All key/value pairs are rehashed and inserted into the new table using quadratic probing.

        Parameters:
            - new_capacity (int): desired new capacity of the hash table
        """
        # prevent downsizing below the current number of elements
        if new_capacity < self._size:
            return

        # ensure new capacity is a prime number
        if not self._is_prime(new_capacity):
            # if not, update it to the next highest prime
            new_capacity = self._next_prime(new_capacity)

        # create a new empty hash table with updated capacity
        new_table = DynamicArray()
        for i in range(new_capacity):
            new_table.append(None)

        # save references to old table
        old_table = self._buckets
        old_capacity = self._capacity

        # replace current table with the new one
        self._buckets = new_table
        self._capacity = new_capacity
        self._size = 0      # will be recalculated during reinsertion

        # rehash and insert all valid (non-tombstone) entries into the new table
        for i in range(old_capacity):
            bucket = old_table[i]
            if bucket is not None and not bucket.is_tombstone:
                self.put(bucket.key, bucket.value)

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

        A bucket is considered empty if it is either:
            - None (never occupied), or
            - A tombstone (was removed "logically")
        """
        empty_buckets = 0

        # iterate through all buckets and count how many are empty or marked as a tombstone
        for i in range(self._capacity):
            bucket = self._buckets[i]
            if bucket is None or bucket.is_tombstone:
                empty_buckets += 1

        return empty_buckets

    def get(self, key: str) -> object:
        """
        Return the value associated with the given key, or None if the key is not found.

        Uses quadratic probing to resolve collisions and locate the desired key.
        Skips over tombstone entries as they represent logically deleted keys.
    
        Parameters:
            - key (str): key to look up

        Returns:
            - value associated with the key, or
            - None if not found
        """
        # compute the key's initial index using the hash function
        i_initial = self._hash_function(key) % self.get_capacity()
        # initialize the quadratic probe offset
        quad_prob = 0

        while True:
            # compute the key's index using quadratic probing and find its bucket
            index = (i_initial + quad_prob ** 2) % self.get_capacity()
            bucket = self._buckets[index]

            # stop probing if hit an empty bucket -> key does not exist
            if bucket is None:
                return
            
            # return the value if the key is found and it's not a tombstone
            if bucket.key == key and not bucket.is_tombstone:
                return bucket.value

            # otherwise, continue probing
            quad_prob += 1

    def contains_key(self, key: str) -> bool:
        """
        Check whether the given key exists in the hash map.

        Uses quadratic probing to resolve collisions while searching.
        Skips over tombstone entries as they represent logically deleted keys.

        Parameters:
            - key (str): key to look up

        Returns:
            - True if the key exists and is active (not deleted)
            - False otherwise
        """
        # compute the key's initial index using the hash function
        i_initial = self._hash_function(key) % self.get_capacity()
        # initialize the quadratic probe offset
        j = 0

        while True:
            # compute the key's index using quadratic probing and find its bucket
            index = (i_initial + j ** 2) % self.get_capacity()
            bucket = self._buckets[index]

            # stop probing if hit an empty bucket -> key does not exist
            if bucket is None:
                return False
            
            # return True if the key is found and it's not a tombstone
            if bucket.key == key and not bucket.is_tombstone:
                return True

            # otherwise, continue probing
            j += 1

    def remove(self, key: str) -> None:
        """
        Remove the key/value pair associated with the given key, if it exists.

        Uses quadratic probing to locate the key. If found, the entry is not physically
        deleted but is instead marked as a tombstone. This allows future probes to continue
        past deleted entries, preserving the integrity of the probe chain.

        Parameters:
            - key (str): key to remove
        """
        # compute the key's initial index using the hash function
        i_initial = self._hash_function(key) % self.get_capacity()
        # initialize the quadratic probe offset
        j = 0

        while True:
            # compute the key's index using quadratic probing and find its bucket
            index = (i_initial + j ** 2) % self.get_capacity()
            bucket = self._buckets[index]

            # stop probing if hit an empty bucket -> key does not exist
            if bucket is None:
                return

            # if the key is found and is active (not deleted), mark as deleted
            if bucket.key == key and not bucket.is_tombstone:
                bucket.is_tombstone = True      # logically delete the entry
                self._size -= 1                 # update size
                return

            # otherwise, continue probing
            j += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray containing all active key/value pairs in the hash map.
        Each element is a tuple of the form (key, value).
        
        Entries marked as tombstones are skipped.

        Returns:
            - DynamicArray of active (key, value) tuples
        """
        hash_array = DynamicArray()

        # iterate over each bucket in the table
        for i in range(self._capacity):
            bucket = self._buckets[i]
            
            # only include entries that are non-empty and not tombstones
            if bucket is not None and not bucket.is_tombstone:
                hash_array.append((bucket.key, bucket.value))

        return hash_array

    def clear(self) -> None:
        """
        Remove all key/value pairs from the hash map without changing its capacity.
        """
        # reset each bucket to None
        for i in range(self._capacity):
            self._buckets[i] = None

        # reset the size
        self._size = 0

    def __iter__(self):
        """
        Initialize the iterator for the hash map.

        This enables iteration over all active key/value pairs (non-tombstone entries)
        using Python's built-in iteration protocol (e.g., for-loops).
    
        Returns:
            - self (iterator object)
        """
        self._index = 0     # start at first index of the hash table
        return self

    def __next__(self):
        """
        Obtain next active key/value pair in the hash map and advance iterator.

        Skips over empty and logically removed (tombstone) entries.
        Raises StopIteration when the end of the table is reached.

        Returns:
            - next active key/value pair
        """
        try:
            bucket = self._buckets[self._index]
            # iterate until a non-empty and non-tombstone bucket is found
            while bucket is None or bucket.is_tombstone:
                bucket = self._buckets[self._index]
                self._index += 1
        except DynamicArrayException:
            # stop iteration when the end of array is reached
            raise StopIteration

        # return a non-empty and non-tombstone bucket
        self._index += 1
        return bucket