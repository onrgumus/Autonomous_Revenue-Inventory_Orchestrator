import os
import pandas as pd
from fastmcp import FastMCP

# Dosyanın olduğu klasörü otomatik bulur
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "database_csv_files")

mcp = FastMCP("FMCG_Insight_Engine")

@mcp.tool()
def get_sales_performance(sku_id: str = None):
    """
    Fetches internal sales data, including units sold, costs, and inventory levels.
    You can filter by SKU_ID to get specific product data.
    """
    file_path = os.path.join(DATA_DIR, "sales_data.csv")
    df = pd.read_csv(file_path)
    
    if sku_id:
        df = df[df['sku_id'] == sku_id]
        
    return df.to_dict(orient="records")

@mcp.tool()
def get_competitor_intelligence():
    """
    Retrieves latest competitor pricing and promotion status from the market.
    Use this to compare our prices with GlobalMart and QuickShop.
    """
    file_path = os.path.join(DATA_DIR, "competitor_prices.csv")
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

@mcp.tool()
def calculate_price_elasticity_simulation(sku_id: str, new_price: float):
    """
    A simulator tool that predicts the impact of a price change on margins.
    Input: sku_id and the proposed new_price.
    """
    file_path = os.path.join(DATA_DIR, "sales_data.csv")
    df = pd.read_csv(file_path)
    product = df[df['sku_id'] == sku_id].iloc[-1] # Get latest record
    
    current_price = product['unit_price']
    cost = product['unit_cost']
    
    old_margin = (current_price - cost) / current_price
    new_margin = (new_price - cost) / new_price
    
    impact = "Positive" if new_margin > old_margin else "Negative"
    
    return {
        "sku_id": sku_id,
        "current_margin": f"{old_margin:.2%}",
        "projected_margin": f"{new_margin:.2%}",
        "margin_impact": impact,
        "note": "Simulation based on static cost analysis."
    }

@mcp.tool()
def save_draft_action(sku_id: str, proposed_price: float, reasoning: str):
    """
    Saves a proposed pricing action to the draft system for manager approval.
    Useful when you find a strategic opportunity.
    """
    plan_file = os.path.join(DATA_DIR, "proposed_actions.csv")
    
    # Dosya yoksa başlıklarla oluştur
    if not os.path.exists(plan_file):
        with open(plan_file, "w") as f:
            f.write("sku_id,proposed_price,reasoning,status\n")
            
    with open(plan_file, "a") as f:
        # CSV formatına uygun yazım
        f.write(f"{sku_id},{proposed_price},\"{reasoning}\",Pending\n")
        
    return f"Success: Strategy for {sku_id} saved as 'Pending' for manager review."

@mcp.tool()
def get_brand_guidelines():
    """
    Retrieves strategic brand guidelines to ensure AI suggestions align with brand values.
    Use this before suggesting aggressive price cuts.
    """
    guideline_path = os.path.join(DATA_DIR, "brand_strategy.txt")
    if os.path.exists(guideline_path):
        with open(guideline_path, "r") as f:
            return f.read()
    return "No specific guidelines found. Optimize for margin and volume balance."

@mcp.prompt()
def morning_briefing():
    """
    A template for the Category Manager's daily check-in.
    Provides a structured way to start the analysis.
    """
    return (
        "1. Check current inventory levels and find items with less than 10 days of stock.\n"
        "2. Compare our prices for these items with competitor intelligence.\n"
        "3. Review brand guidelines to see if we can adjust prices.\n"
        "4. Give me the top 3 urgent actions to protect my margins today."
    )

if __name__ == "__main__":
    mcp.run()