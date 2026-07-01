from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Dosya yollarını ayarla
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "database_csv_files")

def get_enhanced_data():
    # CSV dosyalarını oku
    sales_df = pd.read_csv(os.path.join(DATA_DIR, "sales_data.csv"))
    comp_df = pd.read_csv(os.path.join(DATA_DIR, "competitor_prices.csv"))
    
    # Rakip verilerini özetle
    comp_summary = comp_df.groupby('sku_id').agg({
        'competitor_price': ['min', 'max', 'mean'],
        'competitor_name': 'first'
    }).reset_index()
    comp_summary.columns = ['sku_id', 'min_comp_price', 'max_comp_price', 'avg_comp_price', 'main_competitor']
    
    # Verileri birleştir
    merged_df = pd.merge(sales_df, comp_summary, on='sku_id', how='left')
    
    # Metrikleri hesapla
    merged_df['margin_val'] = (merged_df['unit_price'] - merged_df['unit_cost']) / merged_df['unit_price']
    merged_df['doi'] = (merged_df['inventory_level'] / (merged_df['units_sold'] / 14)).round(0)
    merged_df['market_position'] = ((merged_df['unit_price'] - merged_df['avg_comp_price']) / merged_df['avg_comp_price']) * 100
    
    return merged_df

@app.route('/')
def index():
    try:
        merged_df = get_enhanced_data()
        latest_products = merged_df.sort_values('date').groupby('sku_id').last().reset_index()
        products = latest_products.to_dict(orient='records')
        
        total_rev = (latest_products['units_sold'] * latest_products['unit_price']).sum()
        avg_margin = latest_products['margin_val'].mean()
        
        return render_template('index.html', 
                               products=products, 
                               total_sales=f"${total_rev:,.0f}",
                               avg_margin=f"{avg_margin:.1%}")
    except Exception as e:
        return f"Hata oluştu: {e}. Lütfen CSV dosyalarının 'database_csv_files' klasöründe olduğundan emin olun."

@app.route('/ai-insight', methods=['POST'])
def ai_insight():
    data = request.json
    sku = data.get('sku')
    merged_df = get_enhanced_data()
    
    prod = merged_df[merged_df['sku_id'] == sku].iloc[-1]
    
    margin = prod['margin_val']
    price_gap = prod['market_position']
    doi = prod['doi']
    
    # --- STRATEJİK KARAR MOTORU ---
    if doi < 10:
        title = "⚠️ INVENTORY SHORTAGE & PRICE SKIMMING"
        analysis = f"Stock will only last {int(doi)} days. You are currently priced at ${prod['unit_price']}."
        action = "Immediate Action: Increase price by 8-10% to slow down velocity and maximize margin per unit until replenishment."
        impact = "Projected Impact: +12% increase in Gross Profit for the remaining stock."

    elif price_gap > 5:
        title = "📉 COMPETITIVE GAP DETECTED"
        analysis = f"You are {price_gap:.1f}% more expensive than the market average. Competitors are attracting your price-sensitive customers."
        action = "Immediate Action: Implement a 'Bundle Deal' (Buy 2 Get 1) instead of a direct price cut to protect brand value while matching competitor effective pricing."
        impact = "Projected Impact: +20% recovery in weekly sales volume."

    elif price_gap < -5 and margin < 0.25:
        title = "💰 REVENUE LEAKAGE ALERT"
        analysis = f"You are significantly cheaper than the market ({abs(price_gap):.1f}%). You are leaving money on the table."
        action = "Immediate Action: Apply an incremental price increase of 4%. The market gap is wide enough to absorb this without losing volume."
        impact = "Projected Impact: Direct +4% contribution to EBITDA with zero volume loss."

    else:
        title = "✅ OPTIMIZED PERFORMANCE"
        analysis = "Price position and inventory levels are in the 'Sweet Spot'."
        action = "Strategy: Maintain current pricing but initiate a 'Cross-Sell' campaign with high-margin products."
        impact = "Projected Impact: +5% increase in Basket Size (AOV)."

    return jsonify({
        "title": title,
        "analysis": analysis,
        "action": action,
        "impact": impact
    })

if __name__ == '__main__':
    # Port 5001'de çalıştırıyoruz
    app.run(debug=True, port=5001)