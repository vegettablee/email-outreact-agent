# Requirement: clean_raw_data Command(Process JSON from scraper and insert into database with validation)

Data flow: 
1. Open the data.json file, validate all JSON objects through critical field-checking. 
- - TODO Later when insertions are functional: validate if the company and/or email exists in database first before creating entities
2. Now, repeat the next steps for all individual valid JSON objects. 
3. Create the company entity
4. Create the email entities (uses company as a foreign key, includes recruiter emails AND company emails)
5. Create recruiter entities. 
6. Create the recruiter_email entities.
- - For this, use a the recruiter email that was first inserted into the general email table, and now use this as a foreign key to
- - the recruiter_emails table, and put another foreign key for the recruiter_id. 
- - Not all recruiters.
7. Create the job entities(if needed). 
8. Insert into DB. 

Boundaries:
- Data Layer: knows about JSON structure, parsing
- Validation Layer: guided by business requirements(like recruiter must have an email or linkedin), does not know about DB constraints
- Database Layer: knows about DB operations, not JSON
- Orchestration Layer: coordinates the above, knows the workflow, handles the main loop

Data that crosses boundaries: 
- Data -> Validation, parsed JSON into dicts based on entities. 
- Validation -> Database, validated dicts get sent to the database for insertion 
- Database -> Orchestration, sends the number of fully inserted objects(company, recruiter, emails) 

# Modules/Functions to Implement

Function: validate_fields
Responsibility: Performs simple JSON field checking based on business requirements. 
Dependencies: Needs structured data in data.json file. 

def validate_fields() -> [dict]: 
  Does: [checks if all recruiters have an email AND/OR linkedin, checks that all company fields are filled as well]
  Given: [raw array of JSON objects inside of data.json]
  Returns: [validated raw JSON objects]
  Errors: [failure modes]


Function: normalize_json
Responsibility: Normalizes the raw JSON into SQLAlchemy class models, so every function must follow the same way of manipulating these entities before insertions, updates, and during validation.
Dependencies: Cleaned raw JSON from validate_fields.

def normalize_json([dict]) -> [Class]: 
  Does: [takes the raw structure of the syntactically and business validated entities and normalizes them into]
  Given: [return value from validate_fields]
  Returns: [An array of SQLAlchemy class objects that encompass all entities per object]
  Errors: [failure modes]





