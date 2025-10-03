import os
import openai
from typing import Dict, List, Optional
from dotenv import load_dotenv
import streamlit as st
from .prompts import CUSTOMER_SUMMARY_PROMPT, EMAIL_DRAFT_PROMPT, SENTIMENT_ANALYSIS_PROMPT, SALES_ADVICE_PROMPT

# Load environment variables
load_dotenv()

class OpenAIClient:
    """
    Handles all OpenAI API operations for the AiCRM application.
    """
    
    def __init__(self):
        """Initialize the OpenAI client with API key from environment."""
        self.api_key = os.environ.get("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment variables")
        
        # Set the API key
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_customer_summary(self, customer_data: Dict, interactions: List[Dict], product_interests: List[Dict] = None, available_products: List[Dict] = None, transactions: List[Dict] = None) -> str:
        """
        Generate AI-powered customer summary based on customer data, interactions, and product interests.
        """
        try:
            # Format interactions
            interactions_text = ""
            for interaction in interactions[:5]:  # Last 5 interactions
                interactions_text += f"""
                - {interaction.get('type', 'Unknown')} on {interaction.get('date', 'Unknown date')}
                  Subject: {interaction.get('subject', 'No subject')}
                  Content: {interaction.get('content', 'No content')}
                  Sentiment: {interaction.get('sentiment', 'Unknown')}
                """
            
            # Format product interests
            product_interests_text = "No specific product interests identified yet."
            if product_interests:
                product_interests_text = ""
                for interest in product_interests:
                    product = interest.get('product', {})
                    product_interests_text += f"""
                - {product.get('name', 'Unknown Product')} ({product.get('category', 'Unknown Category')})
                  Price: ${product.get('price', 0):,.2f}
                  Context: {interest.get('context', 'No context')}
                  Sentiment: {interest.get('sentiment', 'Unknown')}
                """
            
            # Format transaction history
            transaction_history_text = "No purchase history available."
            if transactions:
                total_spent = sum(t.get('total_amount', 0) for t in transactions)
                transaction_history_text = f"""
                Purchase Summary:
                - Total Transactions: {len(transactions)}
                - Total Spent: ${total_spent:,.2f}
                - Average Transaction: ${total_spent / len(transactions):,.2f}
                
                Recent Purchases:
                """
                for transaction in transactions[:5]:  # Last 5 transactions
                    product = transaction.get('products', {})
                    transaction_history_text += f"""
                - {product.get('name', 'Unknown Product')} (${transaction.get('total_amount', 0):,.2f}) - {transaction.get('transaction_date', 'Unknown date')}
                """
            
            # Format available products
            available_products_text = "No product information available."
            if available_products:
                available_products_text = ""
                for product in available_products[:10]:  # Top 10 products
                    available_products_text += f"""
                - {product.get('name', 'Unknown Product')} ({product.get('category', 'Unknown Category')})
                  Price: ${product.get('price', 0):,.2f}
                  Description: {product.get('description', 'No description')[:100]}...
                """
            
            # Use the enhanced prompt template
            prompt = CUSTOMER_SUMMARY_PROMPT.format(
                first_name=customer_data.get('first_name', ''),
                last_name=customer_data.get('last_name', ''),
                company=customer_data.get('company', 'N/A'),
                email=customer_data.get('email', 'N/A'),
                phone=customer_data.get('phone', 'N/A'),
                stage=customer_data.get('stage', 'lead'),
                notes=customer_data.get('notes', 'None'),
                interaction_count=len(interactions),
                interactions=interactions_text,
                product_interests=product_interests_text,
                transaction_history=transaction_history_text,
                available_products=available_products_text
            )
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating customer summary: {e}")
            return "Unable to generate AI summary at this time."
    
    def generate_email_draft(self, customer_data: Dict, context: str, email_type: str = "follow_up", product_interests: List[Dict] = None) -> str:
        """
        Generate AI-powered email draft based on customer context and product interests.
        """
        try:
            # Format product interests
            product_interests_text = "No specific product interests identified yet."
            if product_interests:
                product_interests_text = ""
                for interest in product_interests:
                    product = interest.get('product', {})
                    product_interests_text += f"- {product.get('name', 'Unknown Product')} ({product.get('category', 'Unknown Category')})\n"
            
            # Use the enhanced prompt template
            prompt = EMAIL_DRAFT_PROMPT.format(
                first_name=customer_data.get('first_name', ''),
                last_name=customer_data.get('last_name', ''),
                company=customer_data.get('company', 'N/A'),
                stage=customer_data.get('stage', 'lead'),
                context=context,
                email_type=email_type,
                product_interests=product_interests_text
            )
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating email draft: {e}")
            return "Unable to generate email draft at this time."
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of interaction text.
        """
        try:
            prompt = SENTIMENT_ANALYSIS_PROMPT.format(text=text)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.3
            )
            
            sentiment = response.choices[0].message.content.strip().lower()
            
            # Validate sentiment
            if sentiment in ['positive', 'neutral', 'negative']:
                return sentiment
            else:
                return 'neutral'  # Default fallback
                
        except Exception as e:
            st.error(f"Error analyzing sentiment: {e}")
            return 'neutral'
    
    def generate_sales_advice(self, customer_data: Dict, interactions: List[Dict], question: str, product_interests: List[Dict] = None, available_products: List[Dict] = None) -> str:
        """
        Generate AI-powered sales advice based on customer context, interactions, and product interests.
        """
        try:
            # Format interactions
            interactions_text = ""
            for interaction in interactions[:3]:  # Last 3 interactions
                interactions_text += f"- {interaction.get('type', 'Unknown')}: {interaction.get('content', 'No content')[:100]}...\n"
            
            # Format product interests
            product_interests_text = "No specific product interests identified yet."
            if product_interests:
                product_interests_text = ""
                for interest in product_interests:
                    product = interest.get('product', {})
                    product_interests_text += f"- {product.get('name', 'Unknown Product')} ({product.get('category', 'Unknown Category')}) - {interest.get('sentiment', 'Unknown sentiment')}\n"
            
            # Format available products with more detail
            available_products_text = "No product information available."
            if available_products:
                available_products_text = "Our Luxe Couture Collection:\n"
                for product in available_products[:8]:  # Top 8 products with more detail
                    available_products_text += f"""
- {product.get('name', 'Unknown Product')} ({product.get('category', 'Unknown Category')})
  Price: ${product.get('price', 0):,.2f}
  Description: {product.get('description', 'No description')[:150]}...
  Brand: {product.get('brand', 'Luxe Couture')}
"""
            
            # Use the enhanced prompt template
            prompt = SALES_ADVICE_PROMPT.format(
                first_name=customer_data.get('first_name', ''),
                last_name=customer_data.get('last_name', ''),
                company=customer_data.get('company', 'N/A'),
                stage=customer_data.get('stage', 'lead'),
                interactions=interactions_text,
                product_interests=product_interests_text,
                available_products=available_products_text,
                question=question
            )
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating sales advice: {e}")
            return "Unable to generate advice at this time."
    
    def generate_web_social_intelligence(self, customer_data: Dict, interactions: List[Dict], transactions: List[Dict] = None) -> str:
        """
        Generate AI-powered Web & Social Intelligence analysis.
        """
        try:
            # Format customer data
            customer_name = f"{customer_data.get('first_name', '')} {customer_data.get('last_name', '')}"
            company = customer_data.get('company', 'N/A')
            
            # Format recent interactions
            interactions_text = ""
            for interaction in interactions[:3]:
                interactions_text += f"- {interaction.get('type', 'Unknown')}: {interaction.get('content', 'No content')[:100]}...\n"
            
            # Format transaction data
            transactions_text = "No purchase history available."
            if transactions:
                transactions_text = ""
                for transaction in transactions[:5]:
                    product = transaction.get('products', {})
                    transactions_text += f"- {product.get('name', 'Unknown Product')} (${transaction.get('total_amount', 0):,.2f}) - {transaction.get('transaction_date', 'Unknown date')}\n"
            
            prompt = f"""
            Analyze this customer for Web & Social Intelligence insights:
            
            Customer: {customer_name}
            Company: {company}
            Industry: Luxury Fashion/Entertainment
            
            Recent Interactions:
            {interactions_text}
            
            Purchase History:
            {transactions_text}
            
            Provide comprehensive Web & Social Intelligence analysis including:
            1. **Company Intelligence**: Industry analysis, company size, recent news/events
            2. **Social Media Presence**: Public profile analysis, engagement patterns, influence level
            3. **Professional Network**: LinkedIn connections, industry relationships, endorsements
            4. **Recent Mentions**: News coverage, media appearances, public statements
            5. **Market Intelligence**: Industry trends affecting their business, competitive landscape
            6. **Influence Assessment**: Their impact on fashion/entertainment industry
            7. **Opportunity Identification**: Potential collaboration or business opportunities
            
            Focus on actionable insights for luxury fashion sales and relationship building.
            Be specific and reference their industry context.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating web & social intelligence: {e}")
            return "Unable to generate web & social intelligence analysis at this time."
    
    def generate_behavioral_analysis(self, customer_data: Dict, interactions: List[Dict], transactions: List[Dict] = None) -> str:
        """
        Generate AI-powered Behavioral Analysis.
        """
        try:
            # Format customer data
            customer_name = f"{customer_data.get('first_name', '')} {customer_data.get('last_name', '')}"
            stage = customer_data.get('stage', 'lead')
            
            # Format interactions with sentiment analysis
            interactions_text = ""
            sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
            
            for interaction in interactions:
                sentiment = interaction.get('sentiment', 'neutral')
                sentiment_counts[sentiment] += 1
                interactions_text += f"- {interaction.get('type', 'Unknown')} ({sentiment}): {interaction.get('content', 'No content')[:100]}...\n"
            
            # Format transaction behavior
            transactions_text = "No purchase history available."
            if transactions:
                total_spent = sum(t.get('total_amount', 0) for t in transactions)
                avg_transaction = total_spent / len(transactions) if transactions else 0
                categories = [t.get('products', {}).get('category', 'Unknown') for t in transactions]
                
                transactions_text = f"""
                Purchase Behavior:
                - Total Transactions: {len(transactions)}
                - Total Spent: ${total_spent:,.2f}
                - Average Transaction: ${avg_transaction:,.2f}
                - Preferred Categories: {', '.join(set(categories))}
                """
            
            prompt = f"""
            Analyze this customer's behavioral patterns:
            
            Customer: {customer_name}
            Current Stage: {stage}
            
            Interaction History:
            {interactions_text}
            
            Sentiment Analysis:
            - Positive: {sentiment_counts['positive']}
            - Neutral: {sentiment_counts['neutral']}
            - Negative: {sentiment_counts['negative']}
            
            {transactions_text}
            
            Provide comprehensive Behavioral Analysis including:
            1. **Communication Patterns**: Preferred communication methods, response times, engagement style
            2. **Decision-Making Behavior**: How they make purchasing decisions, factors that influence them
            3. **Buying Behavior**: Purchase patterns, price sensitivity, brand loyalty, frequency
            4. **Relationship Dynamics**: How they interact with sales team, trust-building patterns
            5. **Risk Tolerance**: Conservative vs. adventurous purchasing behavior
            6. **Influence Factors**: What motivates their decisions, key stakeholders
            7. **Timing Patterns**: Best times to contact, seasonal preferences, urgency indicators
            8. **Personal Preferences**: Style preferences, quality expectations, service requirements
            9. **Engagement Level**: Active vs. passive customer, responsiveness patterns
            10. **Recommendations**: How to best approach and serve this customer
            
            Focus on actionable insights for sales strategy and customer relationship management.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Error generating behavioral analysis: {e}")
            return "Unable to generate behavioral analysis at this time."

# Singleton instance
_ai_client = None

def get_ai_client() -> OpenAIClient:
    """Get the singleton OpenAI client instance."""
    global _ai_client
    if _ai_client is None:
        _ai_client = OpenAIClient()
    return _ai_client
