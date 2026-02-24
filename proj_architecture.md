# System Overview for Personalized Cold-Email Internship Automation Tool 

Functional requirements: 
1. Must be able to send a personalized email given: 
- - personal information(name, school, year, major, expected graduation date)
- - experience/background info specific to the role 
- - email address 
- - resume file
2. Keep track of emails that are:
- - sent 
- - replied 
- - 
3. Extrapolate company info in the context of how I can contribute as an intern
- - separate into roles(backend, fullstack, data engineer, solutions engineer, ai engineer)
- - store company info as a context resource when sending cold emails
4. Multiple resumes based on their framing
- - backend, fullstack, data engineer, solutions engineer, ai engineer, mobile


Non-Functional requirements: 
1. Personalized emails can be framed based on different categories of roles.
2. Send follow up emails after x amount of days. 
3. Follow up email for normal internship application status updates.
4. Rate limiting for scraping company websites and sending emails(maybe like 20 every hour). 
5. Separate tool for tailoring resumes. 

Workflows required: 
- Company info research to gather useful information 
- Personalized email creator/sender 
--- Separating into two different workflows makes it easier when I need to focus on getting more leads to cold-email, and another one purely for how I want to personalize the email. So they can potentially run in parallel too.

Company-info Research Workflow: 
1. Agent scrapes company info, looks for:
- type of company(startup, mid-size, etc)
- open/past tech roles that match relevant experience 
- potential recruiter emails and/or linkedin profile links 
2. Insert relevant company info into SQL. 

Personalized Automation Email Generation Workflow: 
1. Pings the SQLite database for any emails that have not been sent yet. 
2. Put all emails into a queue and pull up company information tied with the emails. 
3. For each email in the queue, use company and personal info to draft a personalized email. 
4. Find most relevant resume and attach to the email.
5. Email gets sent to the recruiter/company.


Tech Stack: 
- SQLite
- Python
- Claude MCP

