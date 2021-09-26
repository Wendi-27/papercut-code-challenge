#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module test the process and the functions of the cost_calculator module.
Giving valid inputs to check if the function return the correct value and giving
invalid inputs to check if the function return the expected Error.
"""

import os
import csv
import json
import unittest
import costs_calculator
from decimal import Decimal
from job import Job


class TestCostCalculator(unittest.TestCase):
    def setUp(self):
        job_details = ['Total Pages', 'Color Pages', 'Double Sided']
        with open('./invalid_sample.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(job_details[1:])
        with open('./invalid_sample_1.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(job_details[1:] + ["Black and White Pages"])
        with open('./invalid_sample_2.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(job_details)
            csv_writer.writerow(['2.5', '1', 'true'])
        with open('./invalid_sample_3.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(job_details)
            csv_writer.writerow(['2', '1.5', 'true'])
        with open('./invalid_sample_4.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(job_details)
            csv_writer.writerow(['2', '1', '100'])
        with open('./invalid_sample_5.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(job_details)
            csv_writer.writerow(['1', '2', 'true'])

    def test_create_job_list(self):
        job_path = "./sample.csv"
        job_list = costs_calculator.create_job_list(job_path)
        self.assertIsNotNone(job_list)
        for job in job_list:
            self.assertIsInstance(job, Job)
            self.assertIsInstance(job.double_sided, bool)
            self.assertIsInstance(job.total_pages, int)
            self.assertIsInstance(job.color_pages, int)
        with self.assertRaises(ValueError):
            costs_calculator.create_job_list(None)
        with self.assertRaises(ValueError):
            costs_calculator.create_job_list('./invalid_sample.csv')
        with self.assertRaises(ValueError):
            costs_calculator.create_job_list('./invalid_sample_1.csv')
        with self.assertRaises(ValueError):
            costs_calculator.create_job_list('./invalid_sample_2.csv')
        with self.assertRaises(ValueError):
            costs_calculator.create_job_list('./invalid_sample_3.csv')
        with self.assertRaises(ValueError):
            costs_calculator.create_job_list('./invalid_sample_4.csv')
        with self.assertRaises(ValueError):
            costs_calculator.create_job_list('./invalid_sample_5.csv')

    def test_calculate_cost(self):
        with open('./page_charge.json') as p:
            page_charge = json.load(p)
        job_1 = Job(3, 1, 'true')
        job_2 = Job(4, 2, 'false')
        invalid_job = Job(4, 2, 'false', 'A5')
        self.assertEqual(costs_calculator.calculate_cost([job_1], page_charge), Decimal('0.4'))
        self.assertEqual(costs_calculator.calculate_cost([job_1, job_2], page_charge), Decimal('1.0'))
        with self.assertRaises(ValueError):
            costs_calculator.calculate_cost(None, page_charge)
        with self.assertRaises(ValueError):
            costs_calculator.calculate_cost([job_1], None)
        with self.assertRaises(ValueError):
            costs_calculator.calculate_cost([invalid_job], page_charge)

    def test_main(self):
        total_cost = costs_calculator.main(['--csv_path', 'sample.csv', '--page_charge_path', 'page_charge.json'])
        self.assertEqual(total_cost, Decimal('64.1'))
        with self.assertRaises(FileNotFoundError):
            costs_calculator.main(['--csv_path', 'fake_sample.csv', '--page_charge_path', 'page_charge.json'])
        with self.assertRaises(FileNotFoundError):
            costs_calculator.main(['--csv_path', 'sample.csv', '--page_charge_path', 'fake_page_charge.json'])

    def tearDown(self):
        for f in os.listdir("./"):
            if 'invalid_sample' in f:
                os.remove(f)


if __name__ == '__main__':
    unittest.main()
