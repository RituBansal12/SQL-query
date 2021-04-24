'''Q1: Write a query to find the doctors having more ratings than their supervisors.
Employees ratings table
| Employee Id |Employee Name |rating |supervisor employee Id |designation
| 1 |Dr. Max | 9 | 3 |doctor
| 2 |Dr. James | 8 | 4 |doctor
| 3 | Peter | 6 | NULL |supervisor
| 4 | Simon | 9 | NULL |supervisor
For the above table, Dr.Max has more rating than his supervisor.'''

'''Description: I've joined the table with itself & matched employee's with their supervisors based on their employee_id.
Lastly, I select only those employee's who have a rating better than that of their supervisor'''

'''Sample table creation:
create table Employee(E_id int, Name varchar(100), Rating int, S_id int, Designation varchar(100));
insert into Employee(E_id, Name, Rating, S_id, Designation)
values
(1, "Dr.Max", 9, 3, "doctor"),
(2, "Dr. James", 8, 4, "doctor"),
(3, "Peter", 6, NULL, "supervisor"),
(4, "Simon", 9, NULL, "supervisor");'''


Query 1: select E.Name from Employee E, Employee S where E.S_id = S.E_id AND E.Rating > S.Rating;


'''Q2:From the following tables, write a query to get the histogram of specialties of the
unique physicians who have done the procedures but never did prescribe anything.'''


'''Sample table:
create table patient_treatment(P_id int, Event_name varchar(100), Phy_id int);
insert into patient_treatment(P_id, Event_name, Phy_id)
values
(1, "Radiation", 1000),
(2, "Chemotherapy",2000),
(1, "Biopsy", 1000),
(3, "Immunosuppresants", 2000),
(4, "BTKI", 3000),
(5, "Radiation", 4000),
(4, "Chemotherapy", 2000),
(1, "Biopsy", 5000),
(6, "Chemotherapy", 6000);

create table event_category(Event_name varchar(100), Category varchar(100));
insert into event_category(Event_name, Category)
values
("Chemotherapy", "Procedure"),
("Radiation", "Procedure"),
("Immunosuppresants","Prescription"),
("BTKI", "Prescription"),
("Biopsy", "Test");

create table Physician_speciality(Phy_id int, Speciality varchar(100));
insert into Physician_speciality(Phy_id, Speciality)
values
(1000, "Radiologist"),
(2000, "Oncologist"),
(3000, "Hematologist"),
(4000, "Oncologist"),
(5000, "Pathologist"),
(6000, "Oncologist");
'''

'''Description: First, I gather a list of unique physicians who have performed a procedure & subtract any physcians who have prescribed something.
Then I group them based on Speciality & get output.
NOTE: I have created a temp table here so that I can communicate my idea better. This whole thing can be done in one query using triple join as well'''


Query 2:
create table temp(id int);

insert into temp(id)
select DISTINCT A.Phy_id
FROM patient_treatment A
INNER JOIN
event_category B
ON A.Event_name = B.Event_name
Where B.Category= "Procedure"
AND A.Phy_id NOT IN(
select DISTINCT X.Phy_id
FROM patient_treatment X
INNER JOIN
event_category Y
ON X.Event_name = Y.Event_name
Where Y.Category = "Prescription");

select A.Speciality, count(B.id)
FROM
Physician_speciality A
Inner join
temp B
where B.id = A.Phy_id
group by A.Speciality;



'''Q3: Find the top 2 accounts with the maximum number of unique patients on a monthly
basis.'''

'''create table patient_log( Account_Id int, date_var date, P_id int);

insert into patient_log (Account_Id, date_var, P_id)
values
(1,'2020-01-01', 100),
(1,'2020-01-27',200),
(2, '2020-01-01',300),
(2, '2020-01-21',400),
(2,'2020-02-21',300),
(2, '2020-01-01', 500),
(3, '2020-01-20',400),
(1, '2020-03-04',500);'''



'''Description: I've inserted date values directly in yyyy-mm-dd format. If I had more time, I would have converted it into normal format using convert function & 105 style.
Here, I am creating groups based on Months & Patients for a particular account.
Using row ranks, I am getting only the first 2 rows using row ranks which have been created over the partition of months and ordered by the number of unique patients & Account_Id
'''


Query 3:
select Month, Account_Id, Unique_patients from (
select MONTH(date_var) as Month, 
       Account_Id,
       Count(P_id) as Unique_patients,
       row_number() over ( partition by MONTH(date_var) order by Account_Id, count(P_id) desc) as temp_rank
    from patient_log
    group by Account_Id, MONTH(date_var)
    order by Month, Unique_patients desc) ranks
where temp_rank<= 2;




