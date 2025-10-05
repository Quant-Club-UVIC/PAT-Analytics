# Main Database ER Diagram  

```mermaid
erDiagram
    Instrument {
        int iid PK 
        string name
        string ticker
        string currency
        string type
    }

    Equity {
        int iid PK, FK
        int cid FK
    }

    ETF {
        int iid PK, FK
    }

    FX {
        int iid PK, FK
    }

    Price {
        int price_id PK
        int iid FK
        datetime timestamp
        float open
        float high 
        float low
        float close
        bigint volume
    }

    Company {
        int cid PK
        string sector
        string industry
    }

    Financial_Statement {
        int statement_id PK
        int company_id FK
        string statement_type   
        string period_type   
        int fiscal_year  
        datetime date
    }

    Financial_Metric {
        int metric_id PK
        int statement_id FK
        string metric_name
        numeric metric_value
    }

    Corporate_Action {
        int action_id PK
        int equity_id FK
        datetime date
        string type 
        numeric value
        string detail
    }

    ETF_Constituent {
        int etf_id FK
        int constituent_id FK
        date effective_date
        numeric weight
        bigint shares
    }

    Instrument ||--|| Equity : isa
    Instrument ||--|| ETF : isa
    Instrument ||--|| FX : isa
    Instrument ||--o{ Price : priced_as

    Company ||--|| Equity : has
    Company ||--o{ Financial_Statement : reports
    Financial_Statement ||--o{ Financial_Metric : contains
    Equity ||--o{ Corporate_Action : undergoes
    ETF ||--o{ ETF_Constituent : holds
    Instrument ||--o{ ETF_Constituent : constituent

```
Notes:  
- In Financial_Statement type can only be one of : Income, CashFlow, Balance  
- In Financial_Statement period_type can only be one of : Q1, Q2, Q3, Q4, FY  
- In Corporate_Action type can only be one of : Divident, BuyBack, Split  
- In Corporate_Action value depends on type, e.g. if there was a 3:1 split, input 3, if there was a 100,000 share buy back, input 100,000, if there was a divident pay out of $1.26 per share, input 1.26. 
- Company should have multiple statements across periods?