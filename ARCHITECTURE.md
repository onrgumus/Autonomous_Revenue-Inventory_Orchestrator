graph TD
    subgraph "Presentation Layer (Modern Web UI)"
        UI[React/Next.js Strategic Dashboard]
        WS[Real-time WebSocket / REST API]
    end

    subgraph "Intelligence & Orchestration (Agentic Layer)"
        LLM[Claude 3.5 Sonnet / GPT-4o]
        Agent[MCP Orchestrator]
        Reasoning[Strategic Reasoning Engine]
    end

    subgraph "MCP Server Layer (Standardized Protocols)"
        SalesMCP[Sales Data MCP Server]
        MarketMCP[Market Intelligence MCP Server]
        SimMCP[Revenue Simulation MCP Server]
    end

    subgraph "Enterprise Data Infrastructure"
        ERP[(Enterprise ERP: SAP / Oracle)]
        DW[(Cloud Data Warehouse: Snowflake / BigQuery)]
        Scraper[Automated Market Scraper Service]
    end

    %% Data Flow Connections
    ERP -->|CDC / ETL Pipelines| DW
    Scraper -->|Daily Market Sync| DW
    DW --> SalesMCP
    DW --> MarketMCP
    
    UI <--> WS <--> Agent
    Agent <--> LLM
    Agent <--> SalesMCP
    Agent <--> MarketMCP
    Agent <--> SimMCP
    
    %% Styling for Professional Look
    style LLM fill:#6366f1,stroke:#fff,stroke-width:2px,color:#fff
    style Agent fill:#3b82f6,stroke:#fff,stroke-width:2px,color:#fff
    style SalesMCP fill:#10b981,stroke:#fff,color:#fff
    style MarketMCP fill:#10b981,stroke:#fff,color:#fff
    style SimMCP fill:#f43f5e,stroke:#fff,color:#fff
    style DW fill:#1e293b,stroke:#fff,color:#fff