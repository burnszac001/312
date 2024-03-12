#!/usr/bin/python3
from PyQt6.QtCore import QLineF, QPointF


import random
import sys

PYCHARM_DEBUG=True

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

	# This is the method called by the GUI.  _
	# seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
	# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
	# how many base pairs to use in computing the alignment
	def align(self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.max_characters_to_align = align_length

		score = self.get_edit_distance(seq1, seq2, align_length)

		alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
			len(seq1), align_length, ',BANDED' if banded else '')
		alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
			len(seq2), align_length, ',BANDED' if banded else '')

		return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}

	def get_edit_distance(self, seq1, seq2, align_length):
		if len(seq1) > align_length:
			seq1 = seq1[:align_length]
		num_columns = len(seq1)

		if len(seq2) > align_length:
			seq2 = seq2[:align_length]
		num_rows = len(seq2)

		self.table = self.initialize_table(num_columns, num_rows)
		return self._get_edit_distance(num_rows, num_columns, seq1, seq2)

	def _get_edit_distance(self, row, column, seq1, seq2):
		try:
			return self.table[row][column]
		except IndexError:
			north_west = self._get_edit_distance(row - 1, column - 1, seq1, seq2)
			north = self._get_edit_distance(row - 1, column, seq1, seq2)
			west = self._get_edit_distance(row, column - 1, seq1, seq2)

			try:
				if seq1[column - 1] == seq2[row - 1]:
					north_west += MATCH
				else:
					north_west += SUB
			except Exception as e:
				print(seq2[column - 1])
				exit()

			north += INDEL
			west += INDEL

			self.table[row].append(min(north_west, north, west))
			return self.table[row][column]

	@staticmethod
	def initialize_table(num_columns, num_rows):
		table = []
		first_row = [(_ * INDEL) for _ in range(num_columns + 1)]
		table.append(first_row)
		for _ in range(num_rows + 1):
			if _ != 0:
				table.append([(_ * INDEL)])

		return table


if __name__ == "__main__":
	print(GeneSequencing().get_edit_distance('exponential', 'exponential', 1000))
