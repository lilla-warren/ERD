import streamlit as st
import json
import base64

# Page config
st.set_page_config(
    page_title="Comfy Furniture ERD",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Entity Relationship Diagram (ERD)")
st.markdown("### Comfy Furniture LLC - Database Design")
st.markdown("---")

# Load ERD data
@st.cache_data
def load_erd_data():
    with open('erd_data.json', 'r') as f:
        return json.load(f)

erd_data = load_erd_data()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 ERD Diagram", "📋 Entities", "🔗 Relationships", "📝 SQL Schema"])

# Tab 1: ERD Diagram
with tab1:
    st.markdown("### Database Entity Relationship Diagram")
    
    # Create HTML/CSS for visual ERD
    erd_html = f"""
    <style>
    .erd-container {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        padding: 20px;
        background: #f5f5f5;
        border-radius: 10px;
    }}
    .entity {{
        background: white;
        border-radius: 8px;
        width: 260px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    .entity-header {{
        padding: 12px;
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        border-radius: 8px 8px 0 0;
    }}
    .entity-body {{
        padding: 8px;
    }}
    .attribute {{
        padding: 6px 10px;
        border-bottom: 1px solid #eee;
        font-family: monospace;
        font-size: 13px;
    }}
    .attribute-pk {{
        background: #e8f5e9;
        font-weight: bold;
    }}
    .attribute-fk {{
        background: #fff3e0;
    }}
    .key-badge {{
        display: inline-block;
        padding: 2px 6px;
        font-size: 10px;
        border-radius: 4px;
        margin-left: 8px;
    }}
    .pk-badge {{
        background: #4caf50;
        color: white;
    }}
    .fk-badge {{
        background: #ff9800;
        color: white;
    }}
    .relationship-line {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px 0;
    }}
    .arrow {{
        font-size: 20px;
        margin: 0 10px;
    }}
    .cardinality {{
        font-size: 12px;
        font-weight: bold;
        background: #e0e0e0;
        padding: 4px 8px;
        border-radius: 12px;
    }}
    </style>
    
    <div class="erd-container">
        <div class="erd-row" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px;">
    """
    
    # Group entities by row position
    row1_entities = ["CUSTOMER", "SALES_ORDER", "SALE_ORDER_LINE"]
    row2_entities = ["PRODUCT", "INVENTORY", "SUPPLIER"]
    row3_entities = ["PURCHASE_ORDER", "MANUFACTURING_ORDER"]
    
    for entity_name in row1_entities + row2_entities + row3_entities:
        entity = next((e for e in erd_data["entities"] if e["name"] == entity_name), None)
        if entity:
            erd_html += f"""
            <div class="entity">
                <div class="entity-header" style="background: {entity['color']}; border-bottom: 2px solid {entity['border']};">
                    {entity['name']}
                </div>
                <div class="entity-body">
            """
            for attr in entity["attributes"]:
                pk_class = "attribute-pk" if attr["key"] == "PK" else ("attribute-fk" if attr["key"] == "FK" else "")
                erd_html += f"""
                <div class="attribute {pk_class}">
                    {attr['name']} <span style="color:#666;">{attr['type']}</span>
                    {f'<span class="key-badge pk-badge">PK</span>' if attr['key'] == 'PK' else ''}
                    {f'<span class="key-badge fk-badge">FK</span>' if attr['key'] == 'FK' else ''}
                </div>
                """
            erd_html += "</div></div>"
    
    erd_html += "</div>"
    
    # Add relationship arrows
    erd_html += '<div style="text-align: center; margin-top: 20px;"><h4>Relationships</h4><div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 30px;">'
    for rel in erd_data["relationships"]:
        erd_html += f"""
        <div style="background: #e0e0e0; padding: 10px 20px; border-radius: 20px;">
            <strong>{rel['from']}</strong> 
            <span style="font-size: 18px;">→</span> 
            <strong>{rel['to']}</strong>
            <span style="margin-left: 10px; background: {rel['color']}; padding: 4px 8px; border-radius: 12px;">{rel['cardinality']}</span>
        </div>
        """
    erd_html += "</div></div></div>"
    
    st.markdown(erd_html, unsafe_allow_html=True)

# Tab 2: Entities List
with tab2:
    st.markdown("### All Entities")
    
    for entity in erd_data["entities"]:
        with st.expander(f"📦 {entity['name']}"):
            cols = st.columns([1, 2, 1])
            with cols[0]:
                st.markdown(f"**Color:** 🎨 {entity['color']}")
            with cols[1]:
                pk_count = sum(1 for a in entity["attributes"] if a["key"] == "PK")
                fk_count = sum(1 for a in entity["attributes"] if a["key"] == "FK")
                st.markdown(f"**Keys:** {pk_count} PK, {fk_count} FK")
            with cols[2]:
                st.markdown(f"**Attributes:** {len(entity['attributes'])}")
            
            st.markdown("**Attributes:**")
            attr_data = []
            for attr in entity["attributes"]:
                attr_data.append({
                    "Attribute": attr["name"],
                    "Type": attr["type"],
                    "Key": attr["key"] if attr["key"] else "-"
                })
            st.dataframe(attr_data, use_container_width=True)

# Tab 3: Relationships
with tab3:
    st.markdown("### Entity Relationships & Cardinality")
    
    rel_data = []
    for rel in erd_data["relationships"]:
        rel_data.append({
            "From Entity": rel["from"],
            "To Entity": rel["to"],
            "Cardinality": rel["cardinality"],
            "Description": f"One {rel['from']} can have many {rel['to']}, but each {rel['to']} belongs to one {rel['from']}"
        })
    
    st.dataframe(rel_data, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Relationship Diagram")
    
    # Mermaid.js diagram
    mermaid_code = "erDiagram\n"
    for rel in erd_data["relationships"]:
        left = rel["from"].lower().replace("_", "")
        right = rel["to"].lower().replace("_", "")
        if rel["cardinality"] == "1:N":
            mermaid_code += f"    {left} ||--o{{ {right} : has\n"
    mermaid_code += "\n    CUSTOMER ||--o{ SALES_ORDER : places\n"
    mermaid_code += "    SALES_ORDER ||--|{ SALE_ORDER_LINE : contains\n"
    mermaid_code += "    PRODUCT ||--o{ SALE_ORDER_LINE : appears_in\n"
    mermaid_code += "    PRODUCT ||--o{ INVENTORY : tracked_by\n"
    mermaid_code += "    SUPPLIER ||--o{ PURCHASE_ORDER : supplies\n"
    mermaid_code += "    PRODUCT ||--o{ MANUFACTURING_ORDER : produced_as"
    
    st.code(mermaid_code, language="mermaid")

# Tab 4: SQL Schema
with tab4:
    st.markdown("### SQL Database Schema")
    
    sql_statements = []
    
    for entity in erd_data["entities"]:
        sql = f"CREATE TABLE {entity['name']} (\n"
        attrs = []
        pk_attrs = []
        for attr in entity["attributes"]:
            line = f"    {attr['name']} {attr['type']}"
            if attr["key"] == "PK":
                line += " PRIMARY KEY"
                pk_attrs.append(attr["name"])
            attrs.append(line)
        sql += ",\n".join(attrs)
        sql += "\n);"
        sql_statements.append(sql)
    
    # Add foreign key constraints
    sql_statements.append("\n-- Foreign Key Constraints")
    sql_statements.append("ALTER TABLE SALES_ORDER ADD CONSTRAINT fk_sales_order_customer FOREIGN KEY (Customer_ID) REFERENCES CUSTOMER(Customer_ID);")
    sql_statements.append("ALTER TABLE SALE_ORDER_LINE ADD CONSTRAINT fk_sol_sales_order FOREIGN KEY (Sales_Order_ID) REFERENCES SALES_ORDER(Sales_Order_ID);")
    sql_statements.append("ALTER TABLE SALE_ORDER_LINE ADD CONSTRAINT fk_sol_product FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID);")
    sql_statements.append("ALTER TABLE INVENTORY ADD CONSTRAINT fk_inventory_product FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID);")
    sql_statements.append("ALTER TABLE PURCHASE_ORDER ADD CONSTRAINT fk_po_supplier FOREIGN KEY (Supplier_ID) REFERENCES SUPPLIER(Supplier_ID);")
    sql_statements.append("ALTER TABLE MANUFACTURING_ORDER ADD CONSTRAINT fk_mo_product FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID);")
    
    for sql in sql_statements:
        st.code(sql, language="sql")
    
    st.markdown("---")
    st.markdown("### Sample SQL Queries")
    
    st.code("""
    -- Get all sales orders with customer names
    SELECT so.Sales_Order_ID, c.name, so.date_order, so.amount_total, so.state
    FROM SALES_ORDER so
    JOIN CUSTOMER c ON so.Customer_ID = c.Customer_ID;
    
    -- Get inventory status with product names
    SELECT p.name, i.qty_available, i.qty_reserved, i.location
    FROM INVENTORY i
    JOIN PRODUCT p ON i.Product_ID = p.Product_ID;
    
    -- Get low stock alerts (below minimum)
    SELECT p.name, i.qty_available, p.min_stock
    FROM INVENTORY i
    JOIN PRODUCT p ON i.Product_ID = p.Product_ID
    WHERE i.qty_available < p.min_stock;
    """, language="sql")

# Footer
st.markdown("---")
st.markdown("*Comfy Furniture LLC - Odoo ERP Database Design*")
