# Database Schema for PAT
A schema for the database warehousing all financial data used in PAT.  

```mermaid
erDiagram
    Company {
        int cid PK
        str ticker
        str name
        str sector
        str industry
    }
    FinancialStatement{
        int statement_id PK
        int cid FK
        string statement_type   
        string period_type   
        int fiscal_year  
        datetime date
    }
    FinancialMetric{
        int metric_id PK
        int statement_id FK
        int cid FK
        string metric_name
        numeric metric_value
    }
    CorporateAction{
        int action_id PK
        int cid FK
        datetime date
        string type 
        numeric value
        string detail
    }

    Currency{
        int fid PK
        string countryOfIssue 
        string name
    }

    ETFConstituents{
        int const_id PK
        int etf_id FK
        int instr_id FK
        datetime startDate
        datetime endDate
        float weight
    }

    Instrument {
        int iid PK
        int currencyOfIssue FK
        string name
        string ticker
        string type
        datetime startDate
        datetime endDate
    }
    Equity {
        int iid PK
        int cid FK
    }
    FX {
        int iid PK
        int fid FK
    }
    ETF{
        int iid PK
        int eid FK
    }

    PriceAction {
        int price_id PK
        datetime timestamp
        float open
        float high 
        float low
        float close
        bigint volume
    }
    Company||--o{FinancialStatement : reports
    FinancialStatement||--o{ FinancialMetric : contains
    Company||--o{CorporateAction : undergoes
    Company||--o{FinancialMetric : has

    Instrument ||--||Equity : isa
    Instrument ||--||FX : isa
    Instrument ||--||ETF : isa

    Instrument ||--||PriceAction: priceAs

    Instrument }o--o{ ETFConstituents : include
    Instrument }o--o{ Currency : issuedIn
    
    Company ||--|{ Equity : issues
    FX||--|| Currency: issues
    ETF||--|| ETFConstituents : constitute


```
Notes:  
- In FinancialStatement type can only be one of : Income, CashFlow, Balance  
- In FinancialStatement period_type can only be one of : Q1, Q2, Q3, Q4, FY  
- In CorporateAction type can only be one of : Divident, BuyBack, Split  
- In CorporateAction value depends on type, e.g. if there was a 3:1 split, input 3, if there was a 100,000 share buy back, input 100,000, if there was a divident pay out of $1.26 per share, input 1.26. 
- Company should have multiple statements across periods
- Instrument houses all financial instruments which are can be traded on exchanges  
- Instrument tables attribute 'type' can only be on of : 'FX', 'ETF', 'Equity'  
- Note the many to one relationship between Equity and Company, as a company can be listed on many exchanges and trade at different prices (or currency)