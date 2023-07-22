#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict:
        """ return all data"""

	dataset = self.dataset()
        total_items = len(dataset)

        # If index is not provided or out of range, set it to 0
        if index is None or index >= total_items:
            index = 0

        # Calculate the next index to query
        next_index = index + page_size

        # Make sure the index is in a valid range
        assert 0 <= index < total_items, "Index out of range"

        # Create the response dictionary with the current page data
        response = {
            "index": index,
            "next_index": next_index,
            "page_size": page_size,
            "data": []
        }

        # Get the data for the current page, considering any deleted rows
        deleted_indexes = set()
        for i in range(index, min(next_index, total_items)):
            while i in deleted_indexes:
                i += 1
            if i < total_items:
                response["data"].append(dataset[i])

        return response
