#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module define the class of the print job which will be used in the cost
calculating of the print job.
This class requires at least three parameter: the total pages of print job,
the color pages of print job and the job type.

"""


class Job:
    """
    This class can be used in calculating the cost of the print job.
    The argument paper_size is used for future supporting.
    """
    def __init__(self, total_pages, color_pages, double_sided, paper_size="A4"):
        self.total_pages = total_pages
        self.color_pages = color_pages
        self.double_sided = double_sided
        self.paper_size = paper_size
