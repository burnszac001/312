#!/usr/bin/python3
from PyQt6.QtCore import QLineF, QPointF

import sys

import numpy as np
import math

PYCHARM_DEBUG = True

sys.setrecursionlimit(10000)

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1


class GeneSequencing:
	def __init__(self):
		self.banded = False
		self.max_characters_to_align = None
		self.table = None
		self.back_pointers = None
		self.banded_table = None
		self.banded_pointers = None

	@staticmethod
	def initialize_banded(num_rows):
		table = [[(_ * INDEL) for _ in range(MAXINDELS + 1)]]
		for _ in range(MAXINDELS + 1):
			if _ != 0:
				table.append([(_ * INDEL)])

		for _ in range(num_rows - MAXINDELS):
			table.append([])

		return table

	@staticmethod
	def get_banded_pointers(num_rows):
		table = [[-1 for _ in range(MAXINDELS + 1)]]
		for _ in range(MAXINDELS + 1):
			if _ != 0:
				table.append([-1])

		for _ in range(num_rows - MAXINDELS):
			table.append([])

		return table

	def banded_edit_distance(self, seq1, seq2, align_length):
		if len(seq1) > align_length:
			seq1 = seq1[:align_length]
		num_rows = len(seq1)

		if len(seq2) > align_length:
			seq2 = seq2[:align_length]

		if abs(len(seq1) - len(seq2)) > 100:
			return math.inf, 'No Alignment Possible', 'No Alignment Possible'
		else:
			self.banded_table = self.initialize_banded(num_rows)
			self.banded_pointers = self.get_banded_pointers(num_rows)

			score = self._banded_edit_distance(seq1, seq2)

	def _banded_edit_distance(self, seq1, seq2):


		return 0

	# This is the method called by the GUI.  _
	# seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
	# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
	# how many base pairs to use in computing the alignment
	def align(self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.max_characters_to_align = align_length

		if banded:
			score, alignment1, alignment2 = self.banded_edit_distance(seq1, seq2, align_length)
		else:
			score, alignment1, alignment2 = self.get_edit_distance(seq1, seq2, align_length)

		# alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
		# 	len(seq1), align_length, ',BANDED' if banded else '')
		# alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
		# 	len(seq2), align_length, ',BANDED' if banded else '')

		return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}

	@staticmethod
	def initialize_table(num_columns, num_rows):
		table = []
		first_row = [(_ * INDEL) for _ in range(num_columns + 1)]
		table.append(first_row)
		for _ in range(num_rows + 1):
			if _ != 0:
				table.append([(_ * INDEL)])

		return table

	@staticmethod
	def initialize_back_pointers(num_columns, num_rows):
		table = []
		first_row = [-1 for _ in range(num_columns + 1)]
		table.append(first_row)
		for _ in range(num_rows + 1):
			if _ != 0:
				table.append([-1])

		return table

	def get_alignments(self, seq1, seq2, i, j):
		next_val = self.back_pointers[i][j]
		while next_val != -1:
			if next_val == 0:  # came from the west
				j -= 1
				seq2 = seq2[:j] + '-' + seq2[j:]
			elif next_val == 1:  # came from the north
				i -= 1
				seq1 = seq1[:i] + '-' + seq1[i:]
			elif next_val == 2:  # came form the north_west
				i -= 1
				j -= 1

			next_val = self.back_pointers[i][j]
		return seq1[:100], seq2[:100]

	def get_edit_distance(self, seq1, seq2, align_length):
		if len(seq1) > align_length:
			seq1 = seq1[:align_length]
		num_columns = len(seq1)

		if len(seq2) > align_length:
			seq2 = seq2[:align_length]
		num_rows = len(seq2)

		self.table = self.initialize_table(num_columns, num_rows)
		self.back_pointers = self.initialize_back_pointers(num_columns, num_rows)
		score = self._get_edit_distance(num_rows, num_columns, seq1, seq2)
		alignment_1, alignment_2 = self.get_alignments(seq1, seq2, num_rows, num_columns)
		return score, alignment_1, alignment_2

	def _get_edit_distance(self, row, column, seq1, seq2):
		try:
			return self.table[row][column]
		except IndexError:
			north_west = self._get_edit_distance(row - 1, column - 1, seq1, seq2)
			north = self._get_edit_distance(row - 1, column, seq1, seq2)
			west = self._get_edit_distance(row, column - 1, seq1, seq2)

			if seq1[column - 1] == seq2[row - 1]:
				north_west += MATCH
			else:
				north_west += SUB

			north += INDEL
			west += INDEL

			min_value = self.get_minimum(west, north, north_west)
			pointer = self.get_pointer(min_value, west, north, north_west)

			self.table[row].append(min_value)
			self.back_pointers[row].append(pointer)
			return self.table[row][column]

	@staticmethod
	def get_pointer(min_value, west, north, north_west):
		if min_value == west:
			return 0
		elif min_value == north:
			return 1
		elif min_value == north_west:
			return 2

	@staticmethod
	def get_minimum(west, north, north_west):
		valid_variables = []

		if isinstance(north, int):
			valid_variables.append(north)
		if isinstance(west, int):
			valid_variables.append(west)
		if isinstance(north_west, int):
			valid_variables.append(north_west)

		return min(valid_variables)


if __name__ == "__main__":
	print(GeneSequencing().banded_edit_distance('*' * 1000, '*' * 1000, 1000))

