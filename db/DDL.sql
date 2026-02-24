create table companies(
company_id integer primary key autoincrement, 
cname text unique not null,
company_size text, 
category text, 
company_addr text   
);

-- this will be by far the most queried table 
create table emails(
email text unique primary key not null, 
company_id integer,
num_sent integer default 0, 
num_replied integer default 0,
template_id integer, -- numbers correspond to what prompt was used or how it was structured
last_date_sent date null,
foreign key (company_id) references companies(company_id)
  on delete cascade, 
contact_status text default 'N/A' check(contact_status in ('N/A', 'Ghosted', 'Interested'))
);

create table jobs( 
job_id integer primary key autoincrement,
company_id integer,
role_name text not null, 
source_url text unique not null, 
is_open boolean not null,
foreign key (company_id) references companies(company_id)
  on delete cascade
); 

create table recruiters(
recruiter_id integer primary key autoincrement,
fname text not null, 
lname text, 
email text unique, 
linkedin text, 
foreign key (email) references emails(email)
);

-- Workflow Order:
-- Create the company
-- Create the email (linked to the company)
-- Create the recruiter (linked to the email)