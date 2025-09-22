# PAT Project Timeline 
This document will list a high level timeline for this project. Our main goal is to have an MVP (minimal viable product) ready before the start of summers hiring season (mid-january). This gives us October, November, Decemeber, January. After a working piece of software is deployed we can look to improve it.  

## Deliverables
End of Month achievements are listed here  
  
**OCTOBER**: A functional BackEnd API (holdings, metrics) and a FrontEnd mock up pages, functional but disconnected 
   
**NOVEMBER**: A staging site with functional auth, portfolio management, charts and metrics  
  
**DECEMBER**: A staging site with secondary features included, and a DB with live-updating data  
  
**JANUARY**: A deployed MVP fulfiling all the requirements in the design document 


## Month to Month Workflow
### September  (setting things up)
- Define requirements & user stories  
- Decide on tech stack  
- Design prototypes / mock ups
- Assign roles

### October (core development)  
- Backend : API endpoints, database schema, authentication, core business logic  
- Core Business Logic : user can add holdings, see their chart, and basic metrics  
- Database : Collect data up to a certain date, keep the financial data static 
- Frontend : Core pages (Landing page, Portfolio Manager, Holdings Manager, Tool Viewer), state management  

### November (Integration)  
- UI integration with the backend  
- Bug fixes, QA testing of the basic features  
- Set up for secondary features  

### December (Expansion)
- Add RDCF, Risk, Benchmarking, and What if  
- Financial information Database is now being updated regularly (once per day min)  


### January (Polish & Launch)
- Bug Fixes  
- QA Automation  
- Deployment Docs  

## Roles  
BackEnd --> APIs, DB Schema  
FrontEnd --> Pages, components, state management  
Model Development  --> Metric computation  
PM --> Keep scope aligned, run bi-weekly meetings