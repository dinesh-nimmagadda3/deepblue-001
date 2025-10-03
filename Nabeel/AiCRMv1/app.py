import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import your database and utility functions
from database.supabase_client import get_supabase_client
from utils.helpers import format_customer_name, format_date, get_stage_color, safe_get, get_sentiment_icon, get_customer_overall_sentiment
from ai.openai_client import get_ai_client

# Load environment variables
load_dotenv()

# Get database client
db = get_supabase_client()

# Get AI client
ai_client = get_ai_client()

# Page configuration
st.set_page_config(
    page_title="AiCRM - AI-Powered Customer Relationship Management",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application entry point"""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🤖 AiCRM")
        st.markdown("---")
        
        # Navigation menu
        page = st.selectbox(
            "Navigate to:",
            ["🏠 Home", "👥 Customers", "📊 Analytics"],
            index=0
        )
        
        st.markdown("---")
        
        # Quick stats (placeholder)
        st.subheader("📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Customers", "42", "+3")
        with col2:
            st.metric("This Week", "12", "+2")
            
        st.markdown("---")
        
        # AI Status
        st.subheader("🤖 AI Status")
        st.success("✅ OpenAI Connected")
        st.success("✅ Database Connected")
        st.info("💡 AI Insights Active")
    
    # Main content area
    if page == "🏠 Home":
        show_home_page()
    elif page == "👥 Customers":
        # Check if a customer is selected for detail view
        if st.session_state.get("selected_customer"):
            show_customer_detail_view()
        else:
            show_customer_list_placeholder()
    elif page == "📊 Analytics":
        show_analytics_placeholder()

def show_home_page():
    """Home page with overview and quick access"""
    
    # Welcome header
    st.title("🏠 Welcome to AiCRM")
    st.write("Your AI-powered customer relationship management hub")
    
    st.subheader("📊 Quick Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Get real metrics from database
    stage_counts = db.get_customer_counts_by_stage()
    total_customers = sum(stage_counts.values())

    with col1:
        st.metric("Total Customers", total_customers)
    
    with col2:
        st.metric("Active Leads", stage_counts.get('lead', 0))
    
    with col3:
        st.metric("Prospects", stage_counts.get('prospect', 0))
    
    with col4:
        st.metric("Customers", stage_counts.get('customer', 0))
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("🔄 Recent Activity")
    
    # get recent interactions for last 5 interactions from database
    recent_interactions = db.get_recent_interactions(limit=5)

    if recent_interactions:
        for interaction in recent_interactions:
            customer_name = format_customer_name(interaction['customers'])
            st.write(f"**{customer_name}** - {interaction['type'].title()}: {interaction.get('subject', 'No subject')}")
            st.caption(f"{format_date(interaction['date'])}")
            st.divider()
    else:
        st.info("📝 No recent activity. Start by adding some customers!")
    
    # Quick actions section
    st.subheader("🚀 Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("👥 View All Customers", width="stretch"):
            st.session_state.page = "👥 Customers"
            st.rerun()
    
    with action_col2:
        if st.button("➕ Add New Customer", width="stretch"):
            st.info("📝 Feature coming soon: Add customer form")
    
    with action_col3:
        if st.button("📊 View Analytics", width="stretch"):
            st.session_state.page = "📊 Analytics"
            st.rerun()

def show_customer_list_placeholder():
    """Customer list view with real database data."""
    st.title("👥 Customers")
    
    # Test database connection
    if not db.test_connection():
        st.error("Cannot connect to database. Please check your Supabase configuration.")
        return
    
    # Search and filters
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Search customers...", placeholder="Search by name, company, or email")
    
    with col2:
        stage_filter = st.selectbox("Filter by Stage", ["All", "Lead", "Prospect", "Customer"])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Company", "Last Contact", "Stage"])
    
    # Fetch customers based on filters
    if search:
        customers_data = db.search_customers(search)
    elif stage_filter != "All":
        customers_data = db.filter_customers_by_stage(stage_filter)
    else:
        customers_data = db.get_all_customers()
    
    # Display customers in tabular format with inline buttons
    if not customers_data:
        st.info("No customers found.")
        return
    
    # Create table header
    st.markdown("### Customer List")
    
    # Table header row
    header_cols = st.columns([2, 2, 2, 1.5, 1, 1.5, 1.5, 1])
    with header_cols[0]:
        st.markdown("**👤 Name**")
    with header_cols[1]:
        st.markdown("**🏢 Company**")
    with header_cols[2]:
        st.markdown("**📧 Email**")
    with header_cols[3]:
        st.markdown("**📞 Phone**")
    with header_cols[4]:
        st.markdown("**📊 Stage**")
    with header_cols[5]:
        st.markdown("**📅 Last Contact**")
    with header_cols[6]:
        st.markdown("**😊 Sentiment**")
    with header_cols[7]:
        st.markdown("**⚡ Actions**")
    
    st.divider()
    
    # Display each customer as a table row
    for customer in customers_data:
        # Get customer interactions to calculate sentiment
        customer_interactions = db.get_customer_interactions(customer['id'])
        overall_sentiment = get_customer_overall_sentiment(customer_interactions)
        sentiment_icon = get_sentiment_icon(overall_sentiment)
        
        # Create row columns
        row_cols = st.columns([2, 2, 2, 1.5, 1, 1.5, 1.5, 1])
        
        with row_cols[0]:
            st.write(format_customer_name(customer))
        
        with row_cols[1]:
            st.write(safe_get(customer, 'company'))
        
        with row_cols[2]:
            st.write(safe_get(customer, 'email'))
        
        with row_cols[3]:
            st.write(safe_get(customer, 'phone'))
        
        with row_cols[4]:
            stage = customer.get('stage', 'lead').title()
            if stage == 'Lead':
                st.info(stage)
            elif stage == 'Prospect':
                st.warning(stage)
            else:
                st.success(stage)
        
        with row_cols[5]:
            st.write(format_date(customer.get('last_contact')))
        
        with row_cols[6]:
            sentiment_text = overall_sentiment.title()
            if overall_sentiment == 'positive':
                st.success(f"{sentiment_text} {sentiment_icon}")
            elif overall_sentiment == 'negative':
                st.error(f"{sentiment_text} {sentiment_icon}")
            else:
                st.info(f"{sentiment_text} {sentiment_icon}")
        
        with row_cols[7]:
            if st.button("View", key=f"btn_{customer['id']}", width="stretch"):
                # Clear AI-generated data when selecting a new customer
                st.session_state.pop("web_intelligence", None)
                st.session_state.pop("behavioral_analysis", None)
                st.session_state.pop("chat_history", None)
                st.session_state.pop("show_interaction_detail", None)
                st.session_state.selected_customer = customer
                st.rerun()
        
        # Add subtle separator between rows
        st.markdown("---")

def show_customer_detail_view():
    """Main customer detail view with AI insights and chat assistant"""
    selected_customer_data = st.session_state.get("selected_customer")
    
    if not selected_customer_data:
        st.error("No customer selected. Please go back to the customer list.")
        if st.button("← Back to Customer List"):
            st.session_state.pop("selected_customer", None)
            st.rerun()
        return
    
    # Get fresh customer data from database
    customer = db.get_customer_by_id(selected_customer_data['id'])
    if not customer:
        st.error("Customer not found in database.")
        return
    
    # Get customer interactions and transactions
    interactions = db.get_customer_interactions(customer['id'])
    transactions = db.get_customer_transactions(customer['id'])
    
    customer_name = format_customer_name(customer)
    company_name = safe_get(customer, 'company')
    
    # Header with back button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Customers"):
            # Clear AI-generated data when leaving customer detail view
            st.session_state.pop("selected_customer", None)
            st.session_state.pop("web_intelligence", None)
            st.session_state.pop("behavioral_analysis", None)
            st.session_state.pop("chat_history", None)
            st.session_state.pop("show_interaction_detail", None)
            st.rerun()
    
    with col2:
        st.title(f"👤 {customer_name}")
    
    # Main layout: Customer info (left) + AI Chat (right)
    col_main, col_chat = st.columns([2, 1])
    
    with col_main:
        # Customer header info with sentiment
        overall_sentiment = get_customer_overall_sentiment(interactions)
        sentiment_icon = get_sentiment_icon(overall_sentiment)
        
        st.subheader(f"👤 {customer_name} {sentiment_icon}")
        st.write(f"🏢 **Company:** {company_name}")
        st.write(f"📧 **Email:** {safe_get(customer, 'email')}")
        st.write(f"📞 **Phone:** {safe_get(customer, 'phone')}")
        
        # Customer status row with stage and sentiment
        col_stage, col_sentiment = st.columns([1, 1])
        
        with col_stage:
            stage = customer.get('stage', 'lead').title()
            if stage == 'Lead':
                st.info(f"**Stage:** {stage}")
            elif stage == 'Prospect':
                st.warning(f"**Stage:** {stage}")
            else:
                st.success(f"**Stage:** {stage}")
        
        with col_sentiment:
            sentiment_text = overall_sentiment.title()
            if overall_sentiment == 'positive':
                st.success(f"**Sentiment:** {sentiment_text} {sentiment_icon}")
            elif overall_sentiment == 'negative':
                st.error(f"**Sentiment:** {sentiment_text} {sentiment_icon}")
            else:
                st.info(f"**Sentiment:** {sentiment_text} {sentiment_icon}")
        
        # AI-Powered Quick Insights
        st.subheader("AI-Powered Quick Insights")
        
        # Web & Social Intelligence Dropdown
        with st.expander("🌐 Web & Social Intelligence", expanded=False):
            # Generate AI Web & Social Intelligence
            if st.button("🔄 Generate Web Intelligence", key="generate_web_intel"):
                with st.spinner("Analyzing web and social intelligence..."):
                    try:
                        web_intelligence = ai_client.generate_web_social_intelligence(customer, interactions, transactions)
                        st.session_state.web_intelligence = web_intelligence
                    except Exception as e:
                        st.error(f"Error generating web intelligence: {e}")
            
            if st.session_state.get("web_intelligence"):
                st.write(st.session_state.web_intelligence)
            else:
                st.write("*Click 'Generate Web Intelligence' to get AI-powered analysis*")
        
        # Behavioral Analysis Dropdown
        with st.expander("📊 Behavioral Analysis", expanded=False):
            # Generate AI Behavioral Analysis
            if st.button("🔄 Generate Behavioral Analysis", key="generate_behavioral"):
                with st.spinner("Analyzing behavioral patterns..."):
                    try:
                        behavioral_analysis = ai_client.generate_behavioral_analysis(customer, interactions, transactions)
                        st.session_state.behavioral_analysis = behavioral_analysis
                    except Exception as e:
                        st.error(f"Error generating behavioral analysis: {e}")
            
            if st.session_state.get("behavioral_analysis"):
                st.write(st.session_state.behavioral_analysis)
            else:
                st.write("*Click 'Generate Behavioral Analysis' to get AI-powered insights*")
        
        # Most Recent Interaction Summary
        st.subheader("📝 Most Recent Interaction")
        
        if interactions:
            latest_interaction = interactions[0]
            sentiment = latest_interaction.get('sentiment', 'neutral')
            sentiment_icon = get_sentiment_icon(sentiment)
            interaction_type = latest_interaction.get('type', 'Unknown').title()
            subject = latest_interaction.get('subject', 'No subject')
            date = format_date(latest_interaction.get('date'))
            
            if st.button(f"📧 {interaction_type}: {subject} ({date}) {sentiment_icon}", key="recent_interaction"):
                st.session_state.show_interaction_detail = True
            
            if st.session_state.get("show_interaction_detail", False):
                st.info("**AI Summary**")
                st.write("*📝 Note: This will be generated by OpenAI API*")
                st.write(f"**Interaction Type:** {interaction_type}")
                st.write(f"**Sentiment:** {sentiment.title()} {sentiment_icon}")
                st.write("**Content:**")
                st.write(latest_interaction.get('content', 'No content'))
                st.write("**AI-Generated Next Actions (Placeholder):**")
                st.write("• Follow up within 2 business days")
                st.write("• Prepare relevant materials based on their interests")
                st.write("• Schedule next meeting if appropriate")
                
                if st.button("📚 View Full Interaction History"):
                    st.info("🔄 Navigate to full interaction history view...")
        else:
            st.info("No interactions found for this customer.")
        
        # Additional customer details
        st.subheader("📋 Customer Details")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Basic Info", "Interaction Timeline", "Purchase History", "AI Summary", "Log Interaction"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Stage:** {customer.get('stage', 'lead').title()}")
                st.write(f"**Email:** {safe_get(customer, 'email')}")
                st.write(f"**Phone:** {safe_get(customer, 'phone')}")
                st.write(f"**Created:** {format_date(customer.get('created_at'))}")
            with col2:
                st.write(f"**Company:** {safe_get(customer, 'company')}")
                st.write(f"**Last Contact:** {format_date(customer.get('last_contact'))}")
                st.write(f"**Notes:** {safe_get(customer, 'notes')}")
        
        with tab2:
            if interactions:
                for interaction in interactions:
                    sentiment = interaction.get('sentiment', 'neutral')
                    sentiment_icon = get_sentiment_icon(sentiment)
                    interaction_type = interaction.get('type', 'Unknown').title()
                    subject = interaction.get('subject', 'No subject')
                    date = format_date(interaction.get('date'))
                    
                    st.write(f"📅 **{date}** - {interaction_type}: {subject} {sentiment_icon}")
            else:
                st.info("No interactions recorded yet.")
        
        with tab3:
            st.subheader("💳 Purchase History")
            
            if transactions:
                # Purchase summary
                total_spent = sum(t.get('total_amount', 0) for t in transactions)
                total_transactions = len(transactions)
                avg_transaction = total_spent / total_transactions if total_transactions > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Transactions", total_transactions)
                with col2:
                    st.metric("Total Spent", f"${total_spent:,.2f}")
                with col3:
                    st.metric("Average Transaction", f"${avg_transaction:,.2f}")
                
                st.markdown("---")
                
                # Transaction details
                for transaction in transactions:
                    product = transaction.get('products', {})
                    st.write(f"📅 **{format_date(transaction.get('transaction_date'))}**")
                    st.write(f"🛍️ **{product.get('name', 'Unknown Product')}** ({product.get('category', 'Unknown Category')})")
                    st.write(f"💰 **Amount:** ${transaction.get('total_amount', 0):,.2f}")
                    st.write(f"💳 **Payment:** {transaction.get('payment_method', 'Unknown').title()}")
                    st.write(f"📝 **Notes:** {transaction.get('notes', 'No notes')}")
                    st.divider()
            else:
                st.info("No purchase history found for this customer.")
        
        with tab4:
            ai_summary = safe_get(customer, 'ai_summary')
            
            st.markdown("### AI-Generated Customer Summary")
            st.markdown("*This summary combines CRM data with online sources to provide comprehensive insights about the customer.*")
            
            # AI Summary Section
            col1, col2 = st.columns([3, 1])
            with col1:
                if ai_summary != "N/A" and ai_summary:
                    st.markdown("**📋 Current AI Summary:**")
                    st.info(ai_summary)
                else:
                    st.info("**AI Summary:** Not generated yet")
            with col2:
                if st.button("🔄 Generate AI Summary", key="generate_summary"):
                    with st.spinner("Generating comprehensive AI summary..."):
                        try:
                            # Get customer product interests and available products
                            product_interests = db.get_customer_product_interests(customer['id'])
                            available_products = db.get_all_products()
                            
                            # Generate AI summary based on CRM data, interactions, product interests, and transactions
                            new_summary = ai_client.generate_customer_summary(
                                customer, 
                                interactions, 
                                product_interests, 
                                available_products,
                                transactions
                            )
                            
                            # Update customer record in database
                            db.client.table('customers').update({
                                'ai_summary': new_summary
                            }).eq('id', customer['id']).execute()
                            
                            st.success("✅ AI Summary generated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error generating summary: {e}")
            
            # Summary Details Section
            st.markdown("---")
            st.markdown("### 📊 Summary Components")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🏢 CRM Data Sources:**")
                st.write(f"• **Customer Profile:** {customer_name} from {company_name}")
                st.write(f"• **Stage:** {customer.get('stage', 'lead').title()}")
                st.write(f"• **Total Interactions:** {len(interactions)}")
                st.write(f"• **Last Contact:** {format_date(customer.get('last_contact'))}")
                st.write(f"• **Contact Info:** {safe_get(customer, 'email')}, {safe_get(customer, 'phone')}")
                
            with col2:
                st.markdown("**🌐 Online Sources (Future Integration):**")
                st.write("• **Company Information:** Industry, size, recent news")
                st.write("• **Social Media:** Public profiles and activity")
                st.write("• **Professional Networks:** LinkedIn data and connections")
                st.write("• **News & Media:** Recent mentions and coverage")
                st.write("• **Market Intelligence:** Industry trends and insights")
            
            # Regenerate Button
            st.markdown("---")
            if st.button("🔄 Regenerate Summary", key="regenerate_summary", width="stretch"):
                with st.spinner("Regenerating AI summary with latest data..."):
                    try:
                        # Get customer product interests and available products
                        product_interests = db.get_customer_product_interests(customer['id'])
                        available_products = db.get_all_products()
                        
                        # Generate fresh AI summary with product information and transactions
                        new_summary = ai_client.generate_customer_summary(
                            customer, 
                            interactions, 
                            product_interests, 
                            available_products,
                            transactions
                        )
                        
                        # Update customer record in database
                        db.client.table('customers').update({
                            'ai_summary': new_summary
                        }).eq('id', customer['id']).execute()
                        
                        st.success("✅ AI Summary regenerated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error regenerating summary: {e}")
        
        with tab5:
            st.subheader("📝 Log New Interaction")
            st.write(f"Logging interaction for **{customer_name}** from **{company_name}**")
            
            # Interaction form
            with st.form("interaction_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    interaction_type = st.selectbox(
                        "Interaction Type",
                        ["call", "email", "meeting", "note"],
                        help="Select the type of interaction you had with the customer"
                    )
                    
                    interaction_date = st.date_input(
                        "Date",
                        value=datetime.now().date(),
                        help="When did this interaction take place?"
                    )
                
                with col2:
                    subject = st.text_input(
                        "Subject",
                        placeholder="Brief subject or topic of the interaction",
                        help="What was the main topic or subject of this interaction?"
                    )
                    
                    sentiment = st.selectbox(
                        "Sentiment",
                        ["positive", "neutral", "negative"],
                        help="How did the interaction go overall?"
                    )
                
                # Content text area
                content = st.text_area(
                    "Interaction Details",
                    placeholder="Describe what happened during this interaction. Include key points, outcomes, next steps, etc.",
                    height=150,
                    help="Provide detailed notes about the interaction. This will help with future follow-ups and AI analysis."
                )
                
                # Submit button
                submitted = st.form_submit_button("💾 Log Interaction", width="stretch")
                
                if submitted:
                    if not content.strip():
                        st.error("Please provide interaction details before submitting.")
                    else:
                        # Analyze sentiment using AI
                        with st.spinner("Analyzing sentiment..."):
                            try:
                                analyzed_sentiment = ai_client.analyze_sentiment(content)
                            except Exception as e:
                                st.warning(f"Could not analyze sentiment: {e}")
                                analyzed_sentiment = sentiment  # Use user-selected sentiment
                        
                        # Prepare interaction data
                        interaction_data = {
                            "customer_id": customer['id'],
                            "type": interaction_type,
                            "subject": subject if subject.strip() else f"{interaction_type.title()} with {customer_name}",
                            "content": content,
                            "date": f"{interaction_date} {datetime.now().time()}",
                            "sentiment": analyzed_sentiment
                        }
                        
                        # Save to database
                        result = db.create_interaction(interaction_data)
                        
                        if result:
                            st.success(f"✅ Interaction logged successfully!")
                            if analyzed_sentiment != sentiment:
                                st.info(f"🤖 AI detected sentiment: {analyzed_sentiment}")
                            st.balloons()
                            
                            # Refresh the page to show the new interaction
                            st.rerun()
                        else:
                            st.error("❌ Failed to log interaction. Please try again.")

                        # Quick tips section
                        st.markdown("---")
            st.subheader("💡 Tips for Better Interaction Logging")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("""
                **📞 For Calls:**
                - Note key discussion points
                - Record any objections raised
                - Mention next steps agreed upon
                - Include any commitments made
                """)
            
            with col2:
                st.info("""
                **📧 For Emails:**
                - Summarize the email content
                - Note the customer's response
                - Include any attachments mentioned
                - Record follow-up actions needed
                """)
            
            st.info("""
            **🤖 AI Assistant Help:** 
            While logging interactions, you can ask the AI assistant (on the right) for help with:
            - Suggested follow-up questions
            - Email templates for next steps
            - Objection handling strategies
            - Timeline recommendations
            """)
    
    with col_chat:
        # AI Sales Assistant Chat - Standard scrollable interface
        st.markdown("### 🤖 AI Sales Assistant")
        
        # Initialize chat history
        if "chat_history" not in st.session_state:
            # Get some product context for the initial message
            available_products = db.get_all_products()
            product_preview = ""
            if available_products:
                featured_products = available_products[:3]  # Show 3 featured products
                product_preview = f"\n\n🛍️ **Our Featured Collection:**\n"
                for product in featured_products:
                    product_preview += f"• {product.get('name', 'Unknown Product')} - ${product.get('price', 0):,.2f}\n"
            
            st.session_state.chat_history = [
                {"role": "assistant", "content": f"👋 Hello! I'm your AI sales assistant here to help you with {customer_name} from {company_name}. I can provide strategic advice on how to best serve this customer, suggest relevant products from our luxury collection, and help you with sales strategies.{product_preview}\n\nWhat would you like to know about this customer or how can I help you with your sales approach?"}
            ]
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'**You:** {message["content"]}')
            else:
                st.markdown(f'**🤖 Assistant:** {message["content"]}')
            st.divider()
        
        # Chat input
        user_input = st.text_input("Ask me anything about this customer...", key="chat_input", placeholder="e.g., What's the best approach for closing this deal? How should I handle their objections?")
        
        if st.button("Send", key="send_chat") and user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Generate AI response using OpenAI with product information
            with st.spinner("AI is thinking..."):
                try:
                    # Get customer product interests and available products
                    product_interests = db.get_customer_product_interests(customer['id'])
                    available_products = db.get_all_products()
                    
                    ai_response = ai_client.generate_sales_advice(
                        customer, 
                        interactions, 
                        user_input, 
                        product_interests, 
                        available_products
                    )
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Error getting AI response: {e}")
                    # Fallback to simple response
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": f"I'm having trouble connecting to AI right now. Please try again later."
                    })
            
            st.rerun()
        
        # Quick action buttons
        st.markdown("**🚀 Quick Actions:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Draft Email", key="draft_email"):
                with st.spinner("Crafting a personalized email..."):
                    try:
                        # Get customer product interests for email personalization
                        product_interests = db.get_customer_product_interests(customer['id'])
                        
                        # Generate AI email draft with product information
                        email_draft = ai_client.generate_email_draft(
                            customer, 
                            f"Recent interactions: {len(interactions)} total. Last contact: {format_date(customer.get('last_contact'))}",
                            "follow_up",
                            product_interests
                        )
                        
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": f"📧 **Here's a personalized email draft you can send to {customer_name}:**\n\n{email_draft}\n\n💡 *This email is tailored based on their profile, interests, and our product collection. You can customize it further before sending!*"
                        })
                    except Exception as e:
                        st.error(f"Error generating email: {e}")
                        # Fallback to template
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": f"Here's a follow-up email template you can use for {customer_name}:\n\nSubject: Following up on our conversation\n\nHi {customer_name},\n\nThanks for our recent discussion about {company_name}'s needs. I'd love to continue our conversation.\n\nWould next Tuesday or Wednesday work for a brief call?\n\nBest regards\n\n📝 *Note: This is a template. AI email generation is temporarily unavailable.*"
                        })
                st.rerun()
        
        with col2:
            if st.button("📞 Call Prep", key="call_prep"):
                # Get product context for call prep
                available_products = db.get_all_products()
                product_highlights = ""
                if available_products:
                    featured_products = available_products[:3]
                    product_highlights = f"\n\n🛍️ **Products to highlight:**\n"
                    for product in featured_products:
                        product_highlights += f"• {product.get('name', 'Unknown Product')} - ${product.get('price', 0):,.2f}\n"
                
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f"📞 **Call preparation for {customer_name}:**\n\n✅ **Topics to cover:**\n- Current business challenges and needs\n- Budget and timeline discussion\n- Decision-making process\n- Our luxury fashion solutions\n\n✅ **Questions to ask:**\n- What's your biggest priority right now?\n- Who else is involved in this decision?\n- What's your timeline?\n- Any specific style or quality requirements?{product_highlights}\n\n💡 *I can provide more personalized prep based on their specific interests and our product collection!*"
                })
                st.rerun()
        
        with col3:
            if st.button("📝 Log Help", key="log_help"):
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f"📝 **Here's how to log an interaction with {customer_name}:**\n\n1️⃣ Go to the 'Log Interaction' tab below\n2️⃣ Select interaction type (call, email, meeting, note)\n3️⃣ Add subject and details\n4️⃣ Choose sentiment (positive, neutral, negative)\n5️⃣ Submit to save\n\n💡 **Pro tip:** Include key discussion points, product mentions, outcomes, and next steps for better tracking!\n\n🎯 **What to include:**\n- Products discussed or recommended\n- Customer's reaction to our collection\n- Budget or timeline information\n- Next steps or follow-up needed\n\nThis helps me give you better strategic advice and product recommendations for future interactions! 😊"
                })
                st.rerun()

def show_analytics_placeholder():
    """Placeholder analytics view"""
    st.title("�� Analytics")
    st.info("Analytics dashboard coming soon...")

if __name__ == "__main__":
    main()
