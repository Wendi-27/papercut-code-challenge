# papercut-code-challenge
This codebase contains the solution for the papercut code challenge. 

### Requirements

The codebase is implemented in Python 3.6.8. All Required packages are built-in in Python

### Running

The solution take two arguments:     

**csv_path**: The path of csv file for the job detail.   
**page_charge_path**: The path of json file for page charge.    

The charge of page is saved as a json file for supporting other paper sizes in the future.


To run the solution, execute the following command:

     cd papercut-code-challenge
     python costs_calculator.py --csv_path sample.csv --page_charge_path page_charge.json
The expected result will be printed on the console like this:
![papercut_image](https://user-images.githubusercontent.com/91405731/134798527-d3cc50ae-ed68-4142-9f54-30a38cd12ffe.png)

### Testing
     
To test the solution, exectue the following command:
    
     cd papercut-code-challenge
     python -m unittest costs_calculator_test




