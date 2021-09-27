#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module calculate the cost of the print jobs.
The main function requires two parameters: the path of csv file for job details
and the path of json file for page charge.
The details and cost of each job will be printed to the console. The total cost of
all jobs will be printed to the console when every job's cost is calculated.
"""

import os
import sys
import csv
import json
import argparse
from decimal import Decimal
from job import Job


def create_job_list(job_path):
    """
    This function read the csv file of the job details and return a list of Job which
    will be used for calculating the cost of the print jobs.

    Parameters:
      job_path - the path of csv file which contains the job details

    Returns:
      A list of Job class

    Raises:
      ValueError - Invalid data in the csv file
    """
    if not job_path:
        raise ValueError('The path of csv file is invalid')
    job_details = ['total pages', 'color pages', 'double sided']  # Predefine the columns of job details
    job_list = []
    with open(job_path) as csv_file:
        reader = csv.reader(csv_file)
        line_count = 0
        for row in reader:
            if line_count == 0:
                column_names = list(map(lambda x: x.strip().lower(), row))  # Format the columns
                if len(job_details) != len(column_names):
                    raise ValueError('too much or too little column name of job detail.')
                for column_name in column_names:
                    if column_name not in job_details:
                        raise ValueError('"%s" is an invalid or repetitive job detail column.' % column_name)
                    else:
                        job_details.remove(column_name)
                total_page_index = column_names.index('total pages')  # Find the correct index for each column
                color_page_index = column_names.index('color pages')
                double_side_index = column_names.index('double sided')
            else:
                total_page = row[total_page_index].strip()  # Get data through index to adapt different orders of columns
                color_page = row[color_page_index].strip()
                if not total_page.isnumeric():  # Check if the data is valid
                    raise ValueError('The value of Total Pages must be a Non-negative integer')
                if not color_page.isnumeric():
                    raise ValueError('The value of Color Pages must be a Non-negative integer')
                total_page = int(total_page)
                color_page = int(color_page)
                if color_page > total_page:
                    raise ValueError('The value of Color Pages must less than the value of Total Pages')
                double_sided = row[double_side_index].strip().lower()
                if double_sided not in ['true', 'false']:
                    raise ValueError('The value of Double Sided must be "true" or "false"')
                job = Job(total_page, color_page, True if double_sided == 'true' else False)
                job_list.append(job)
            line_count += 1
    return job_list


def calculate_cost(job_list, price_dict):
    """
    This function calculates the cost of the jobs and prints the
    details and cost of the job to the console.

    Parameters:
      job_list - list of Job
      price_dict - dict of the page charge

    Returns:
      The total cost of all print jobs

    Raises:
      ValueError - Invalid paper size
    """
    if not job_list:
        raise ValueError('The list of Job is invalid')
    if not price_dict:
        raise ValueError('The page charge is invalid')
    total_cost = Decimal(0.)  # Use Decimal for accurate calculation
    for job in job_list:
        if job.paper_size not in price_dict:
            raise ValueError('"%s" is an invalid paper size' % job.paper_size)
        paper_size_price = price_dict[job.paper_size]
        if job.double_sided:
            page_price = paper_size_price['double_sided']
        else:
            page_price = paper_size_price['single_sided']

        job_cost = Decimal(page_price['black_white_page']) * (job.total_pages - job.color_pages) + Decimal(
            page_price['color_page']) * job.color_pages
        print("Current job details: Total Pages: %s, Color Pages: %s, Double Sided: %s, Job Cost: $%s" % (
            job.total_pages, job.color_pages, job.double_sided, job_cost))
        total_cost += job_cost
    return total_cost


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_path', required=True, type=str, help='path of csv file for the print jobs')
    parser.add_argument('--page_charge_path', required=True, type=str, help='path of the json file for the page charge')
    args = parser.parse_args(args)
    page_charge_path = args.page_charge_path
    csv_path = args.csv_path

    if not os.path.isfile(page_charge_path):  # Check if the path is valid
        raise FileNotFoundError(
            '"%s" is an invalid file of the page charge. Please check the input.' % page_charge_path)
    if not os.path.isfile(csv_path):
        raise FileNotFoundError('"%s" is an invalid file of the print jobs. Please check the input.' % csv_path)

    with open(page_charge_path, 'r') as p:
        page_charge_dict = json.load(p)  # load the json file of page charge
    print_job_list = create_job_list(csv_path)
    total_print_cost = calculate_cost(print_job_list, page_charge_dict)
    print("Total cost of all print jobs: $%s" % total_print_cost)
    return total_print_cost


if __name__ == '__main__':
    main(sys.argv[1:])
