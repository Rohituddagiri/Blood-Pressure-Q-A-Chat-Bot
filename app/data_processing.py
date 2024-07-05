from database_operations import create_connection, create_table, execute_sql_statement, load_data_from_csv

import pandas as pd

conn_patient = create_connection('patient.db')

create_vital_table_statement = """CREATE TABLE vital_data(
                PatientID TEXT,
                ComponentID TEXT,
                ObservationDate TEXT,
                ObservationResult TEXT,
                ObservationUnits TEXT
                );"""

create_medication_table_statement = """CREATE TABLE medication_data(
                PatientID TEXT,
                MedInterval TEXT,
                OrderStartDate TEXT,
                Description TEXT,
                Amount REAL,
                Units TEXT,
                DosageForm TEXT,
                ProviderInstructions TEXT      
                );"""


create_table(conn_patient,create_vital_table_statement,'vital_data')
create_table(conn_patient,create_medication_table_statement,'medication_data')

vital_data = load_data_from_csv('data/vital.csv')
medication_data = load_data_from_csv('data/medication.csv')


with conn_patient:
    cur = conn_patient.cursor()
    cur.executemany("INSERT INTO vital_data(PatientID,ComponentID,ObservationDate,ObservationResult,ObservationUnits) VALUES(?,?,?,?,?);",vital_data)
    cur.executemany("INSERT INTO medication_data(PatientID,MedInterval,OrderStartDate,Description,Amount,Units,DosageForm,ProviderInstructions) VALUES(?,?,?,?,?,?,?,?);",medication_data)
    
    
    
vital_details_sql = """SELECT 
                            PatientID,
                            ComponentID, 
                            ObservationDate, 
                            ObservationResult 
                        FROM vital_data WHERE ComponentID = 'BloodPressure';"""
                        
medication_details_sql = """SELECT 
                                PatientID,
                                OrderStartDate, 
                                Description AS MedicationPrescribed
                            FROM medication_data;"""
                            
data_from_vital_table = pd.read_sql_query(vital_details_sql, conn_patient)
data_from_medication_table = pd.read_sql_query(medication_details_sql, conn_patient)


data = [data_from_vital_table, data_from_medication_table]
