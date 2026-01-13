import streamlit as st
from PIL import Image
import ocr_utils
import report_utils
import db_utils
import chatbot_utils
import pandas as pd
import datetime
import os
import concurrent.futures
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder

# Page Config
st.set_page_config(page_title="Customer Review Intelligence", layout="wide")

# Initialize DB (safe to call multiple times as it uses IF NOT EXISTS)
db_utils.init_db()

# Header
st.title("🍵 Southern Frontier Customer Review Intelligence")
st.markdown("**Builder:** [Sophia Chen](https://www.linkedin.com/in/sophia-chen-34794893/) | **Email:** sophiachen2012@gmail.com | **Medium:** https://medium.com/@sophiachen2012")

# Tabs
# Custom CSS for larger tabs
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
    }
    
    /* Move Sidebar to Right using Rerverse Flex */
    /* This overrides the default left positioning by swapping the order */
    
    div[data-testid="stSidebarNav"] {
        display: none;
    }
    
    section[data-testid="stSidebar"] {
        /* Reset positioning */
        left: unset !important;
        right: 0 !important;
    }
    
    /* Target the main container to reverse styling */
    /* This selector targets the flex container holding the sidebar and main content */
    .stApp > header + div {
        flex-direction: row-reverse;
    }
    
    /* Fix for collapse button */
    div[data-testid="stSidebarCollapsedControl"] {
        left: unset !important;
        right: 0 !important; 
    }
    
    /* Ensure resizing handle is on the correct side (visual only) */
    div[data-testid="stSidebarUserContent"] {
        padding-top: 2rem; 
    }
    
</style>
""", unsafe_allow_html=True)

tab_home, tab1, tab2, tab3 = st.tabs(["🏠 Home", "📥 Ingestion", "🗄️ Database", "📈 Analysis"])

with tab_home:
    st.markdown("### Welcome to Southern Frontier Customer Review Intelligence")
    st.markdown("Transforming customer feedback into business growth. Manage reviews, track trends, and unlock AI-powered insights.")
    st.divider()
    
    # Row 1: Space Images
    c1, c2, c3 = st.columns(3)
    with c1: st.image("images/space1.jpg", width='stretch')
    with c2: st.image("images/space2.jpg", width='stretch')
    with c3: st.image("images/space3.JPG", width='stretch')
    
    st.divider()
    
    # Row 2: Drinks & Package
    c4, c5, c6 = st.columns(3)
    with c4: st.image("images/shudrink.png", caption="Shu Pu'er Beverages", width='stretch')
    with c5: st.image("images/shengdrink.png", caption="Sheng Pu'er Beverages", width='stretch')
    with c6: st.image("images/package.png", caption="To-Go Packages", width='stretch')

    # Row 3: Tea Types
    c7, c8, c9 = st.columns(3)
    with c7: st.image("images/shengball.png", caption="Sheng Pu'er Tea Ball", width='stretch')
    with c8: st.image("images/shucake.png", caption="Shu Pu'er Tea Cake (5+yrs)", width='stretch')
    with c9: st.image("images/shengcake.png", caption="Sheng Pu'er Tea Cake (5+yrs)", width='stretch')
    
    st.divider()

    # Row 4: Customer Reviews
    r1, r2, r3, r4, r5, r6 = st.columns(6)
    with r1: st.image("images/1.jpg", caption="Review 1", width='stretch')
    with r2: st.image("images/2.jpg", caption="Review 2", width='stretch')
    with r3: st.image("images/3.jpg", caption="Review 3", width='stretch')
    with r4: st.image("images/4.jpg", caption="Review 4", width='stretch')
    with r5: st.image("images/5.jpg", caption="Review 5", width='stretch')
    with r6: st.image("images/6.jpg", caption="Review 6", width='stretch')
         
    st.info("👈 Navigate to the **Ingestion** tab to start uploading reviews!")

with tab1:
    st.header("Upload Review Screenshot")
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        # If only one file, wrap in list for consistent handling if needed, but uploaded_files is already a list
        st.write(f"Uploaded {len(uploaded_files)} images.")
        
        if st.button("Extract Data from All"):
            # Clear existing session data for fresh upload
            st.session_state['extracted_data_list'] = []
            
            all_extracted_data = []
            progress_bar = st.progress(0)
            
            # 1. Pre-save all images to disk (Fast I/O)
            saved_files = []
            uploads_dir = "uploads"
            os.makedirs(uploads_dir, exist_ok=True)
            
            with st.spinner("Preparing images..."):
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(uploads_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    saved_files.append((uploaded_file.name, file_path))

            # 2. Parallel Extraction
            def process_single_image(file_info):
                fname, fpath = file_info
                try:
                    with Image.open(fpath) as img:
                        # Ensure image is loaded
                        img.load()
                        result = ocr_utils.extract_review_data(img)
                    return result, fname, fpath
                except Exception as e:
                    return {"error": str(e)}, fname, fpath

            with st.spinner(f"Analyzing {len(saved_files)} images in parallel..."):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(process_single_image, f) for f in saved_files]
                    
                    for i, future in enumerate(concurrent.futures.as_completed(futures)):
                        data, fname, fpath = future.result()
                        
                        if "error" in data:
                            st.error(f"Error processing {fname}: {data['error']}")
                        else:
                            # Batch duplicate check logic
                            is_duplicate = False
                            for existing in all_extracted_data:
                                if existing.get('user_name') == data.get('user_name') and existing.get('content') == data.get('content'):
                                    is_duplicate = True
                                    break
                            
                            if not is_duplicate:
                                data['source_filename'] = fname
                                data['image_path'] = fpath
                                all_extracted_data.append(data)
                            else:
                                print(f"Duplicate found in batch: {data.get('user_name')} - {fname}")
                        
                        progress_bar.progress((i + 1) / len(saved_files))
            
            st.session_state['extracted_data_list'] = all_extracted_data
            
        if 'extracted_data_list' in st.session_state and st.session_state['extracted_data_list']:
            st.subheader("Extracted Data Preview")
            
            # Form to save all
            with st.form("bulk_save_form"):
                for i, data in enumerate(st.session_state['extracted_data_list']):
                    with st.expander(f"Review {i+1}: {data.get('user_name', 'Unknown')} ({data.get('source_filename')})", expanded=True):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Taste", data.get('rating_taste', 'N/A'))
                        c2.metric("Env", data.get('rating_env', 'N/A'))
                        c3.metric("Service", data.get('rating_service', 'N/A'))
                        c4.metric("Value", data.get('rating_value', 'N/A'))
                        st.text_area("Content", data.get('content'), height=100, key=f"content_{i}")
                        st.json(data, expanded=False)

                submitted = st.form_submit_button("Save All to Database")
                
            if submitted:
                saved_count = 0
                for data in st.session_state['extracted_data_list']:
                    # Clean date logic (reused)
                    raw_date = data.get('review_date')
                    try:
                        if raw_date and len(raw_date) <= 5:
                            # Handle MM/DD format with custom year logic
                            clean_raw = raw_date.replace('/', '-')
                            parts = clean_raw.split('-')
                            if len(parts) == 2:
                                try:
                                    # month = int(parts[0]) 
                                    # Always 2026 as per user request
                                    raw_date = f"2026-{parts[0]}-{parts[1]}"
                                except ValueError:
                                    pass # Fallback to standard parsing
                        parsed_date = pd.to_datetime(raw_date).strftime('%Y-%m-%d')
                        data['review_date'] = parsed_date
                    except:
                        data['review_date'] = datetime.date.today().strftime('%Y-%m-%d')
                    
                    # Check duplicate
                    if not db_utils.check_duplicate(data.get('user_name'), data.get('content')):
                        if db_utils.insert_review(data):
                            saved_count += 1
                
                st.success(f"✅ Successfully saved {saved_count} new reviews!")
                # Clear cache to reflect new data
                db_utils.get_all_reviews.clear()
                
                # Optional: Clear state or keep for reference? Let's clear to avoid double save confusion
                del st.session_state['extracted_data_list']
                st.rerun()

with tab2:
    
    # Fetch reviews
    df = db_utils.get_all_reviews()
    
    if not df.empty:
        # Reorder columns for better view
        cols = ['id', 'user_name', 'review_date', 'rating_overall', 'rating_taste', 'rating_env', 'rating_service', 'rating_value', 'content', 'source_filename']
        # Ensure columns exist in DF (migration might have just added them, old rows might have NaN)
        existing_cols = [c for c in cols if c in df.columns]
        df_display = df[existing_cols].copy()
        
        # Ensure review_date is string for AgGrid
        if 'review_date' in df_display.columns:
            df_display['review_date'] = pd.to_datetime(df_display['review_date']).dt.strftime('%Y-%m-%d')

        st.markdown("### Manage Reviews")
        
        st.caption("💡 Tip: Click column headers to sort. Use the menu in headers to filter. Select rows to delete.")
        

        
        # Configure AgGrid
        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20) # Add pagination
        gb.configure_side_bar() # Add a sidebar
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        
        # Configure specific columns
        gb.configure_column("id", editable=False)
        gb.configure_column("source_filename", editable=False)
        gb.configure_column("review_date", type=["dateColumnFilter", "customDateTimeFormat"], custom_format_string='yyyy-MM-dd')
        gb.configure_column("rating_overall", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1)
        
        # Selection
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
        gridOptions = gb.build()
        
        grid_response = AgGrid(
            df_display,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=False,
            theme='streamlit', # Add theme color to the table
            enable_enterprise_modules=False,
            height=500, 
            width='100%',
            reload_data=False
        )
        

            
        # CSV Export
        # Use df_display (the filtered view) for export, or grid data if available
        export_df = df_display # Default to what was passed to grid
        if 'grid_response' in locals() and grid_response['data'] is not None and len(grid_response['data']) > 0:
             export_df = pd.DataFrame(grid_response['data'])
            
        csv = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='reviews_export.csv',
            mime='text/csv',
        )
    else:
        st.info("No reviews found in the database.")

with tab3:
    
    
    # AI Assistant Popover
    with st.sidebar:
          # We place it in sidebar or use a floating button concept?
          # User asked for "Pop up or flowing experience on Analysis page"
          # Putting it at the top or bottom of Analysis tab via st.popover
          pass
    
    # To make it "flowing", we can put a persistent popover button at the top/bottom
    st.subheader("📊 Metrics Summary")
    
    # AI Assistant in Sidebar (Floating/Sticky)
    with st.sidebar:
         st.markdown("### 🤖 Canvas")
         with st.popover("💬 AI Assistant", help="Ask questions about your data"):
              st.markdown("### Southern Frontier Asssistant")
              
              # Check validity
              if not chatbot_utils.configure_genai():
                  st.warning("⚠️ Google API Key not found.")
                  st.stop()

              # Initialize Chat History
              if "messages" not in st.session_state:
                  st.session_state.messages = [
                      {"role": "assistant", "content": "Hello! I've analyzed your reviews. Ask me anything!"}
                  ]

              # Display Chat History
              for msg in st.session_state.messages:
                  with st.chat_message(msg["role"]):
                      st.markdown(msg["content"])

              # Handle User Input
              # Note: st.chat_input in popover might close it on submit.
              # If that happens, we need to instruct user or use a form.
              # Recent Streamlit versions support chat_input in containers.
              if prompt := st.chat_input("Ask about the report or data...", key="chat_input_popover"):
                  # Add user message
                  st.session_state.messages.append({"role": "user", "content": prompt})
                  with st.chat_message("user"):
                      st.markdown(prompt)

                  # Generate Response
                  with st.chat_message("assistant"):
                      message_placeholder = st.empty()
                      
                      # Gather Context
                      report_context = st.session_state.get('generated_report', "")
                      analysis_df = st.session_state.get('analysis_df', pd.DataFrame())
                      data_context = chatbot_utils.get_data_context(analysis_df)
                      
                      try:
                          # Stream response
                          full_response = ""
                          response_stream = chatbot_utils.chat_stream(
                              messages=st.session_state.messages,
                              report_context=report_context,
                              data_context=data_context
                          )
                          
                          for chunk in response_stream:
                              if chunk.text:
                                  full_response += chunk.text
                                  message_placeholder.markdown(full_response + "▌")
                          
                          message_placeholder.markdown(full_response)
                          
                          # Append to history
                          st.session_state.messages.append({"role": "assistant", "content": full_response})
                          
                      except Exception as e:
                          st.error(f"Error generating response: {e}")

    # Fetch reviews
    df_analysis = db_utils.get_all_reviews()
    
    if not df_analysis.empty:
        # Ensure date is datetime for calculations
        df_analysis['review_date'] = pd.to_datetime(df_analysis['review_date'])
        
        # Date Filter
        min_date = df_analysis['review_date'].min().date()
        max_date = df_analysis['review_date'].max().date()
        
        col_filter, col_spacer = st.columns([1, 2])
        with col_filter:
            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        # Filter logic
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            mask = (df_analysis['review_date'].dt.date >= start_date) & (df_analysis['review_date'].dt.date <= end_date)
            df_filtered = df_analysis.loc[mask]
        else:
            # If single date selected or invalid range, just show all or handle gracefully
            # Usually streamlit returns a single date if only one is picked so far
            if isinstance(date_range, tuple) and len(date_range) == 1:
                 mask = (df_analysis['review_date'].dt.date == date_range[0])
                 df_filtered = df_analysis.loc[mask]
            else:
                 df_filtered = df_analysis
            
        # --- Pre-calculation for Advanced Charts ---
        # Sort by date for rolling calcs
        df_sorted = df_analysis.sort_values('review_date')
        
        # 1. 7-Day Moving Averages (Weighted by individual reviews)
        # We calculate rolling mean on the raw data
        # Note: This is a simple moving average of the reviews in the window
        df_sorted['mov_avg_overall'] = df_sorted['rating_overall'].rolling(window=7, min_periods=1).mean()
        df_sorted['mov_avg_taste'] = df_sorted['rating_taste'].rolling(window=7, min_periods=1).mean()
        df_sorted['mov_avg_env'] = df_sorted['rating_env'].rolling(window=7, min_periods=1).mean()
        df_sorted['mov_avg_service'] = df_sorted['rating_service'].rolling(window=7, min_periods=1).mean()
        df_sorted['mov_avg_value'] = df_sorted['rating_value'].rolling(window=7, min_periods=1).mean()
        
        # Group by date to get daily stats
        # For daily avg, we just take the mean of that day
        # For moving avg, we take the LAST value of that day (state at end of day)
        daily_stats = df_sorted.groupby(df_sorted['review_date'].dt.date).agg({
            'rating_overall': 'mean',
            'rating_taste': 'mean',
            'rating_env': 'mean',
            'rating_service': 'mean',
            'rating_value': 'mean',
            'mov_avg_overall': 'last',
            'mov_avg_taste': 'last',
            'mov_avg_env': 'last',
            'mov_avg_service': 'last',
            'mov_avg_value': 'last',
            'id': 'count' # Daily review count
        }).rename(columns={'id': 'daily_count'})
        
        # 2. Rolling 7-Day Count
        # We need a complete date index to ensure rolling window accounts for days with 0 reviews
        full_date_range = pd.date_range(start=daily_stats.index.min(), end=daily_stats.index.max(), freq='D').date
        daily_stats = daily_stats.reindex(full_date_range)
        
        # Fill NaNs for daily metrics (0 reviews)
        daily_stats['daily_count'] = daily_stats['daily_count'].fillna(0)
        # For ratings, we forward fill moving avg (state persists) and leave daily as NaN (no data points)
        cols_mov = ['mov_avg_overall', 'mov_avg_taste', 'mov_avg_env', 'mov_avg_service', 'mov_avg_value']
        daily_stats[cols_mov] = daily_stats[cols_mov].ffill()
        
        # Calculate Rolling 7-Day Sum
        daily_stats['rolling_7d_count'] = daily_stats['daily_count'].rolling(window=7, min_periods=1).sum()
        
        # --- Filter for Display ---
        # Now we filter the PRE-CALCULATED daily_stats based on user selection
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            mask_daily = (daily_stats.index >= start_date) & (daily_stats.index <= end_date)
            daily_stats_filtered = daily_stats.loc[mask_daily]
        elif isinstance(date_range, tuple) and len(date_range) == 1:
             mask_daily = (daily_stats.index == date_range[0])
             daily_stats_filtered = daily_stats.loc[mask_daily]
        else:
             daily_stats_filtered = daily_stats

        # Store filtered dataframe for the chatbot to access
        st.session_state['analysis_df'] = df_filtered

        # Topline Metrics Calculation (using df_filtered for raw counts/avgs in range)
        # ... (Metrics calculation remains same as it uses raw filtered df) ...
        # 1. Total Reviews (Selected Range)
        total_reviews = len(df_filtered)
        
        # 2. New Reviews (Last 7 Days)
        today = datetime.date.today()
        seven_days_ago = today - datetime.timedelta(days=7)
        mask_7d = (df_analysis['review_date'].dt.date >= seven_days_ago) & (df_analysis['review_date'].dt.date <= today)
        df_7d = df_analysis.loc[mask_7d]
        new_reviews_7d = len(df_7d)
        
        # 3. Avg Rating (Selected Range)
        avg_rating = df_filtered['rating_overall'].mean() if not df_filtered.empty else 0.0
        
        # 4. Avg Rating (Last 7 Days)
        avg_rating_7d = df_7d['rating_overall'].mean() if not df_7d.empty else 0.0
        
        # Display Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Reviews", total_reviews, help="In selected date range")
        m2.metric("New Reviews (7d)", new_reviews_7d, help="Last 7 days")
        m3.metric("Avg Rating (All)", f"{avg_rating:.1f} ⭐", help="In selected date range")
        m4.metric("Avg Rating (7d)", f"{avg_rating_7d:.1f} ⭐", help="Last 7 days")
        
        st.divider()
        
        # Charts
        c1, c2 = st.columns(2)
        
        with c1:
            st.caption("Number of New Reviews (Selected Range)")
            if not daily_stats_filtered.empty:
                # Plot Daily Count and Rolling 7D
                chart_data = daily_stats_filtered[['daily_count', 'rolling_7d_count']].rename(columns={
                    'daily_count': 'Daily Total',
                    'rolling_7d_count': '7-Day Total'
                })
                st.line_chart(chart_data)
            else:
                st.info("No data for charts.")
            
        with c2:
            st.caption("Average Rating (Selected Range)")
            if not daily_stats_filtered.empty:
                # Plot Daily Avg and Moving Avg
                chart_data = daily_stats_filtered[['rating_overall', 'mov_avg_overall']].rename(columns={
                    'rating_overall': 'Daily Avg',
                    'mov_avg_overall': '7-Day Avg'
                })
                st.line_chart(chart_data)
            else:
                st.info("No data for charts.")
        
        st.divider()
        
        st.subheader("🥣 Category Ratings over Time")
        
        if not daily_stats_filtered.empty:
            c3, c4 = st.columns(2)
            c5, c6 = st.columns(2)
            
            # Helper to plot category
            def plot_category(col, title, col_daily, col_mov):
                with col:
                    st.caption(title)
                    chart_data = daily_stats_filtered[[col_daily, col_mov]].rename(columns={
                        col_daily: 'Daily Avg',
                        col_mov: '7-Day Avg'
                    })
                    st.line_chart(chart_data)

            plot_category(c3, "Taste Rating", "rating_taste", "mov_avg_taste")
            plot_category(c4, "Environment Rating", "rating_env", "mov_avg_env")
            plot_category(c5, "Service Rating", "rating_service", "mov_avg_service")
            plot_category(c6, "Value Rating", "rating_value", "mov_avg_value")
        else:
            st.info("No data for category charts.")

        st.divider()
        
        # --- Section 1.5: Sentiment Breakdown ---
        st.subheader("📊 Daily Sentiment Breakdown")
        
        if not df_filtered.empty:
            # Prepare Data
            df_breakdown = df_filtered.copy()
            
            def classify_sentiment(val):
                if val >= 4.5:
                    return 'Positive'
                elif val > 3.5:
                    return 'Neutral'
                else:
                    return 'Negative'
            
            df_breakdown['sentiment'] = df_breakdown['rating_overall'].apply(classify_sentiment)
            df_breakdown['date'] = df_breakdown['review_date'].dt.date
            
            # Aggregate for Altair (Long Format)
            chart_data = df_breakdown.groupby(['date', 'sentiment']).size().reset_index(name='count')
            
            # Use 'review_date' str for better Altair x-axis or just date object
            # Altair handles date objects well.
            
            # Define Color Scale
            color_scale = alt.Scale(
                domain=['Positive', 'Neutral', 'Negative'],
                range=['green', 'lightblue', 'red']
            )
            
            # Chart 1: Counts
            st.caption("Daily Review Count by Sentiment")
            
            c1 = alt.Chart(chart_data).mark_bar().encode(
                x='date:T',
                y='count:Q',
                color=alt.Color('sentiment:N', scale=color_scale, title="Sentiment"),
                tooltip=['date:T', 'sentiment', 'count']
            ).properties(
                height=300
            ).interactive()
            
            st.altair_chart(c1, use_container_width=True)
            
            # Chart 2: Percentages
            st.caption("Daily Sentiment Distribution (%)")
            
            c2 = alt.Chart(chart_data).mark_bar().encode(
                x='date:T',
                y=alt.Y('count:Q', stack='normalize', axis=alt.Axis(format='%'), title='Percentage'),
                color=alt.Color('sentiment:N', scale=color_scale, title="Sentiment"),
                tooltip=['date:T', 'sentiment', 'count']
            ).properties(
                height=300
            ).interactive()
            
            st.altair_chart(c2, use_container_width=True)

        else:
             st.info("No data for breakdown charts.")

        st.divider()
        
        # --- Section 2: Sentiment Analysis ---
        st.subheader("🤖 AI Sentiment Analysis")
        
        language = st.selectbox("Select Report Language", ["English", "Chinese"])
        
        generate_clicked = st.button("Generate Intelligence Report")
        
        # Area for status messages (spinner)
        status_area = st.empty()
        
        # Always display existing report if available
        if 'generated_report' in st.session_state:
            st.divider()
            # Display metadata if available
            if 'report_metadata' in st.session_state:
                meta = st.session_state['report_metadata']
                st.info(f"""
                **📊 Intelligence Report**
                **Reviews Analyzed:** {meta['count']}
                **Period:** {meta['start_date']} - {meta['end_date']}
                **Report Date:** {meta['generated_on']}
                """)
            
            st.markdown(st.session_state['generated_report'])
            
            c_down1, c_down2 = st.columns(2)
            
            with c_down1:
                # Convert to PDF on the fly
                pdf_io = report_utils.create_pdf_from_markdown(st.session_state['generated_report'])
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_io,
                    file_name=f"intelligence_report_{datetime.date.today()}.pdf",
                    mime="application/pdf"
                )
            
            with c_down2:
                # Convert to DOCX on the fly
                docx_io = report_utils.create_docx_from_markdown(st.session_state['generated_report'])
                st.download_button(
                    label="Download Report as DOCX",
                    data=docx_io,
                    file_name=f"intelligence_report_{datetime.date.today()}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        # Logic for generation
        if generate_clicked:
            with status_area:
                with st.spinner(f"Generating insights from reviews in selected range ({language})..."):
                    if not df_filtered.empty:
                        # Prepare data for AI
                        df_for_ai = df_filtered.copy()
                        df_for_ai['review_date'] = df_for_ai['review_date'].dt.strftime('%Y-%m-%d')
                        reviews_list = df_for_ai[['user_name', 'rating_overall', 'content', 'review_date']].to_dict(orient='records')
                        
                        report_stream = ocr_utils.analyze_sentiment_batch(reviews_list, language=language, stream=True)
                        
                        full_report = ""
                        report_placeholder = st.empty()
                        
                        for chunk in report_stream:
                            if hasattr(chunk, 'text'):
                                full_report += chunk.text
                                report_placeholder.markdown(full_report + "▌")
                                
                        report_placeholder.markdown(full_report)
                        st.session_state['generated_report'] = full_report
                        
                        # Store exact metadata
                        if not df_filtered.empty:
                            actual_min = df_filtered['review_date'].min().strftime('%Y-%m-%d')
                            actual_max = df_filtered['review_date'].max().strftime('%Y-%m-%d')
                            count = len(df_filtered)
                        else:
                            actual_min = actual_max = "N/A"
                            count = 0
                            
                        st.session_state['report_metadata'] = {
                            'start_date': actual_min,
                            'end_date': actual_max,
                            'count': count,
                            'generated_on': datetime.date.today().strftime('%Y-%m-%d')
                        }
                    else:
                        st.warning("No reviews found in the selected date range to analyze.")
            
            # Rerun to update the display with the new report
            st.rerun()
    else:
        st.info("No reviews found to analyze.")

