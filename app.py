import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Vendor Comparison", layout="wide")
st.title("🏭 Vendor Proposal Intelligence System")
st.write("Compare multiple vendor proposals and get AI-powered rankings")

# Initialize session state
if "vendors" not in st.session_state:
    st.session_state.vendors = []

# Sidebar for adding vendors
with st.sidebar:
    st.header("Add Vendor Proposal")
    
    vendor_name = st.text_input("Vendor Name", placeholder="e.g., Acme Corp")
    
    col1, col2 = st.columns(2)
    with col1:
        unit_price = st.number_input("Unit Price ($)", 1000, 50000, 10000, key="price")
        quality_score = st.slider("Quality Score", 1.0, 10.0, 7.0, key="quality")
        delivery_days = st.number_input("Delivery Days", 1, 90, 30, key="delivery")
    
    with col2:
        defect_rate = st.slider("Defect Rate (%)", 0.0, 15.0, 5.0, key="defect")
        experience = st.number_input("Experience (years)", 1, 30, 5, key="exp")
        support_rating = st.slider("Support Rating", 1.0, 5.0, 4.0, key="support")
    
    on_time_rate = st.slider("On-Time Delivery Rate", 0.0, 1.0, 0.9, key="ontime")
    certifications = st.number_input("Certifications Count", 0, 10, 5, key="cert")
    payment_terms = st.number_input("Payment Terms (days)", 0, 120, 30, key="payment")
    warranty_months = st.number_input("Warranty (months)", 0, 60, 12, key="warranty")
    
    vendor_region = st.selectbox("Vendor Region", ["Asia", "Europe", "North America", "Local"], key="region")
    product_category = st.selectbox("Product Category", ["Electronics", "Machinery", "Software"], key="category")
    
    if st.button("➕ Add Vendor", use_container_width=True):
        if vendor_name.strip():
            vendor_data = {
                "name": vendor_name,
                "unit_price": unit_price,
                "quality_score": quality_score,
                "delivery_days": delivery_days,
                "defect_rate_percent": defect_rate,
                "vendor_experience_years": experience,
                "support_rating": support_rating,
                "on_time_delivery_rate": on_time_rate,
                "certifications_count": certifications,
                "payment_terms_days": payment_terms,
                "warranty_months": warranty_months,
                "vendor_region": vendor_region,
                "product_category": product_category
            }
            st.session_state.vendors.append(vendor_data)
            st.success(f"✅ Added {vendor_name}")
            st.rerun()
        else:
            st.error("Please enter a vendor name")
    
    # CSV Upload Section
    st.divider()
    st.subheader("📤 Or Upload CSV")
    st.caption("Upload a CSV file with vendor proposals")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Required columns mapping
            required_columns = {
                'vendor_id': ['vendor_id', 'id', 'name', 'vendor_name'],
                'unit_price': ['unit_price', 'price', 'cost'],
                'delivery_days': ['delivery_days', 'days', 'delivery_time'],
                'quality_score': ['quality_score', 'quality'],
                'vendor_experience_years': ['vendor_experience_years', 'experience', 'experience_years'],
                'defect_rate_percent': ['defect_rate_percent', 'defect_rate', 'defect'],
                'support_rating': ['support_rating', 'support'],
                'on_time_delivery_rate': ['on_time_delivery_rate', 'on_time_rate', 'delivery_rate'],
                'certifications_count': ['certifications_count', 'certifications'],
                'payment_terms_days': ['payment_terms_days', 'payment_terms', 'terms'],
                'warranty_months': ['warranty_months', 'warranty'],
                'vendor_region': ['vendor_region', 'region'],
                'product_category': ['product_category', 'category']
            }
            
            # Find matching columns
            column_mapping = {}
            for target, alternatives in required_columns.items():
                for alt in alternatives:
                    if alt.lower() in df.columns or alt.lower() in [col.lower() for col in df.columns]:
                        for col in df.columns:
                            if col.lower() == alt.lower():
                                column_mapping[target] = col
                                break
                        if target in column_mapping:
                            break
            
            # Validate required columns
            missing = [k for k in ['unit_price', 'delivery_days', 'quality_score', 'vendor_experience_years', 
                                   'defect_rate_percent', 'support_rating', 'on_time_delivery_rate', 
                                   'certifications_count', 'payment_terms_days', 'warranty_months', 
                                   'vendor_region', 'product_category'] if k not in column_mapping]
            
            if missing:
                st.error(f"❌ Missing required columns: {', '.join(missing)}")
                st.write("**Expected columns:**")
                st.write(", ".join(required_columns.keys()))
            else:
                # Display preview
                preview_df = df[[column_mapping[k] for k in column_mapping.keys() if k != 'vendor_id']].head(3)
                st.write("**Preview:**")
                st.dataframe(preview_df, use_container_width=True)
                
                if st.button("✅ Import Vendors from CSV", use_container_width=True):
                    vendors_to_add = []
                    for idx, row in df.iterrows():
                        vendor_id = row[column_mapping['vendor_id']] if 'vendor_id' in column_mapping else f"V{idx+1}"
                        
                        vendor_data = {
                            "name": str(vendor_id),
                            "unit_price": float(row[column_mapping['unit_price']]),
                            "quality_score": float(row[column_mapping['quality_score']]),
                            "delivery_days": int(row[column_mapping['delivery_days']]),
                            "defect_rate_percent": float(row[column_mapping['defect_rate_percent']]),
                            "vendor_experience_years": int(row[column_mapping['vendor_experience_years']]),
                            "support_rating": float(row[column_mapping['support_rating']]),
                            "on_time_delivery_rate": float(row[column_mapping['on_time_delivery_rate']]),
                            "certifications_count": int(row[column_mapping['certifications_count']]),
                            "payment_terms_days": int(row[column_mapping['payment_terms_days']]),
                            "warranty_months": int(row[column_mapping['warranty_months']]),
                            "vendor_region": str(row[column_mapping['vendor_region']]),
                            "product_category": str(row[column_mapping['product_category']])
                        }
                        vendors_to_add.append(vendor_data)
                    
                    st.session_state.vendors.extend(vendors_to_add)
                    st.success(f"✅ Imported {len(vendors_to_add)} vendors from CSV!")
                    st.rerun()
        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
    
    # Clear all button
    st.divider()
    if st.button("🗑️ Clear All Vendors", use_container_width=True):
        st.session_state.vendors = []
        st.info("All vendors cleared!")
        st.rerun()

# Main content area
st.subheader(f"📊 Vendors Added: {len(st.session_state.vendors)}")

if st.session_state.vendors:
    # Display added vendors
    if st.checkbox("Show Added Vendors"):
        for idx, vendor in enumerate(st.session_state.vendors):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{vendor['name']}** - Price: ${vendor['unit_price']}, Quality: {vendor['quality_score']}, Days: {vendor['delivery_days']}")
            with col2:
                if st.button("❌", key=f"del_{idx}", use_container_width=True):
                    st.session_state.vendors.pop(idx)
                    st.rerun()
    
    # Compare button
    if st.button("🚀 Compare All Vendors & Rank", use_container_width=True, type="primary"):
        with st.spinner("Analyzing vendors..."):
            # Convert vendor region and category to one-hot encoding
            vendors_data = []
            for vendor in st.session_state.vendors:
                data = {
                    "unit_price": vendor["unit_price"],
                    "quality_score": vendor["quality_score"],
                    "delivery_days": vendor["delivery_days"],
                    "defect_rate_percent": vendor["defect_rate_percent"],
                    "vendor_experience_years": vendor["vendor_experience_years"],
                    "support_rating": vendor["support_rating"],
                    "on_time_delivery_rate": vendor["on_time_delivery_rate"],
                    "certifications_count": vendor["certifications_count"],
                    "payment_terms_days": vendor["payment_terms_days"],
                    "warranty_months": vendor["warranty_months"],
                    "vendor_region_Europe": 1 if vendor["vendor_region"] == "Europe" else 0,
                    "vendor_region_Asia": 1 if vendor["vendor_region"] == "Asia" else 0,
                    "vendor_region_North America": 1 if vendor["vendor_region"] == "North America" else 0,
                    "vendor_region_Local": 1 if vendor["vendor_region"] == "Local" else 0,
                    "product_category_Electronics": 1 if vendor["product_category"] == "Electronics" else 0,
                    "product_category_Machinery": 1 if vendor["product_category"] == "Machinery" else 0,
                    "product_category_Software": 1 if vendor["product_category"] == "Software" else 0,
                }
                vendors_data.append(data)
            
            # Send to backend for batch prediction
            try:
                response = requests.post("http://localhost:8000/predict_batch", json={"vendors": vendors_data})
                
                if response.status_code == 200:
                    results = response.json()["results"]
                    
                    # Combine vendor names with scores
                    ranked_vendors = []
                    for idx, score in enumerate(results):
                        ranked_vendors.append({
                            "rank": 0,  # Will be set after sorting
                            "name": st.session_state.vendors[idx]["name"],
                            "score": score,
                            "recommendation": ""
                        })
                    
                    # Sort by score descending
                    ranked_vendors.sort(key=lambda x: x["score"], reverse=True)
                    
                    # Add rank and recommendation
                    for idx, vendor in enumerate(ranked_vendors):
                        vendor["rank"] = idx + 1
                        if idx == 0:
                            vendor["recommendation"] = "⭐ HIGHLY RECOMMENDED"
                        elif idx <= len(ranked_vendors) // 2 or (len(ranked_vendors) > 1 and idx == 1):
                            vendor["recommendation"] = "✅ RECOMMENDED"
                        else:
                            vendor["recommendation"] = "⚠️ NOT RECOMMENDED"
                    
                    # Display results
                    st.success("✅ Ranking Complete!")
                    st.divider()
                    
                    for vendor in ranked_vendors:
                        if vendor["rank"] == 1:
                            st.markdown(f"### 🏆 Rank #{vendor['rank']}: {vendor['name']}")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Score", f"{vendor['score']:.2f}")
                            with col2:
                                st.metric("Status", vendor['recommendation'])
                            with col3:
                                st.info("TOP CHOICE")
                        else:
                            with st.container(border=True):
                                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                                with col1:
                                    st.write(f"**Rank #{vendor['rank']}**")
                                with col2:
                                    st.write(f"**{vendor['name']}**")
                                with col3:
                                    st.write(f"Score: `{vendor['score']:.2f}`")
                                with col4:
                                    st.write(vendor['recommendation'])
                    
                    # Summary table
                    st.divider()
                    st.subheader("📈 Detailed Ranking Summary")
                    df = pd.DataFrame([
                        {
                            "Rank": v["rank"],
                            "Vendor": v["name"],
                            "Score": f"{v['score']:.2f}",
                            "Recommendation": v["recommendation"]
                        }
                        for v in ranked_vendors
                    ])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error connecting to API: {str(e)}")
else:
    st.info("👈 Add vendor proposals using the sidebar to get started!")