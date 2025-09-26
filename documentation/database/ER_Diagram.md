# Main Database ER Diagram  

```mermaid
erDiagram
    COMPANY {
        int company_id PK
        str ticker
        str name
        str sector
        str industry
    }
    ETF {
        int etf_id PK
        str ticker
        str name 

    }
    STOCK {
        int price_id PK
        int company_id FK
        int etf_id FK
        datetime timestamp
        float open
        float high 
        float low
        float close
        bigint volume
    }
    FINANCIAL_STATEMENT{
        int statement_id PK
        int company_id FK
        string statement_type   
        string period_type   
        int fiscal_year  
        datetime date
    }
    FINANCIAL_METRIC{
        int metric_id PK
        int statement_id FK
        int company_id FK
        string metric_name
        numeric metric_value
    }
    CORPORATE_ACTION{
        int action_id PK
        int company_id FK
        datetime date
        string type 
        numeric value
        string detail
    }
    COMPANY}o--o{ETF : constituent   
    ETF||--||STOCK : is_priced
    COMPANY||--||STOCK : is_priced
    COMPANY||--||FINANCIAL_STATEMENT : reports
    FINANCIAL_STATEMENT||--o{ FINANCIAL_METRIC : contains
    COMPANY||--o{CORPORATE_ACTION : undergoes
    COMPANY||--o{FINANCIAL_METRIC : has 
```
Notes:  
- In FINANCIAL_STATEMENT type can only be one of : Income, CashFlow, Balance  
- In FINANCIAL_STATEMENT period_type can only be one of : Q1, Q2, Q3, Q4, FY  
- In CORPORATE_ACTION type can only be one of : Divident, BuyBack, Split  
- In CORPORATE_ACTION value depends on type, e.g. if there was a 3:1 split, input 3, if there was a 100,000 share buy back, input 100,000, if there was a divident pay out of $1.26 per share, input 1.26. 
- Company has multiple statements across periods?