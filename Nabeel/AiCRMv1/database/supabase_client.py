import os
from typing import List, Dict, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class SupabaseClient:
    """
    Handles all database operations for the AiCRM application.
    
    This class follows the Singleton pattern - only one instance
    should exist to avoid multiple connections.
    """
    
    def __init__(self):
        """Initialize the Supabase client with credentials from environment."""
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and KEY must be set in environment variables")
        
        self.client: Client = create_client(self.url, self.key)
    
    def test_connection(self) -> bool:
        """
        Test if we can connect to Supabase.
        Returns True if successful, False otherwise.
        """
        try:
            # Simple query to test connection
            response = self.client.table('customers').select("id").limit(1).execute()
            return True
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            return False
    
    # CUSTOMER OPERATIONS
    def get_all_customers(self) -> List[Dict]:
        """
        Fetch all customers from the database.
        Returns a list of customer dictionaries.
        """
        try:
            response = self.client.table('customers').select("*").execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to fetch customers: {e}")
            return []
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:
        """
        Fetch a single customer by ID.
        Returns customer dict or None if not found.
        """
        try:
            response = self.client.table('customers').select("*").eq('id', customer_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to fetch customer: {e}")
            return None
    
    def search_customers(self, search_term: str) -> List[Dict]:
        """
        Search customers by name, email, or company.
        Uses Supabase's text search capabilities.
        """
        try:
            # Search in multiple fields using 'or' condition
            response = self.client.table('customers').select("*").or_(
                f"first_name.ilike.%{search_term}%,"
                f"last_name.ilike.%{search_term}%,"
                f"email.ilike.%{search_term}%,"
                f"company.ilike.%{search_term}%"
            ).execute()
            return response.data
        except Exception as e:
            st.error(f"Search failed: {e}")
            return []
    
    def filter_customers_by_stage(self, stage: str) -> List[Dict]:
        """
        Filter customers by pipeline stage.
        """
        try:
            response = self.client.table('customers').select("*").eq('stage', stage.lower()).execute()
            return response.data
        except Exception as e:
            st.error(f"Filter failed: {e}")
            return []
    
    def create_customer(self, customer_data: Dict) -> Optional[Dict]:
        """
        Create a new customer.
        Returns the created customer dict or None if failed.
        """
        try:
            response = self.client.table('customers').insert(customer_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to create customer: {e}")
            return None
    
    def update_customer(self, customer_id: int, updates: Dict) -> Optional[Dict]:
        """
        Update an existing customer.
        Returns the updated customer dict or None if failed.
        """
        try:
            # Add updated_at timestamp
            updates['updated_at'] = 'now()'
            response = self.client.table('customers').update(updates).eq('id', customer_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to update customer: {e}")
            return None
    
    def delete_customer(self, customer_id: int) -> bool:
        """
        Delete a customer and all their interactions.
        Returns True if successful, False otherwise.
        """
        try:
            # First delete all interactions for this customer
            self.client.table('interactions').delete().eq('customer_id', customer_id).execute()
            
            # Then delete the customer
            response = self.client.table('customers').delete().eq('id', customer_id).execute()
            return True
        except Exception as e:
            st.error(f"Failed to delete customer: {e}")
            return False
    
    # INTERACTION OPERATIONS
    def get_customer_interactions(self, customer_id: int) -> List[Dict]:
        """
        Get all interactions for a specific customer.
        Ordered by date (newest first).
        """
        try:
            response = self.client.table('interactions').select("*").eq('customer_id', customer_id).order('date', desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to fetch interactions: {e}")
            return []
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict]:
        """
        Get the most recent interactions across all customers.
        Useful for dashboard activity feed.
        """
        try:
            response = self.client.table('interactions').select(
                "*, customers(first_name, last_name, company)"
            ).order('date', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to fetch recent interactions: {e}")
            return []
    
    def create_interaction(self, interaction_data: Dict) -> Optional[Dict]:
        """
        Create a new interaction.
        Also updates the customer's last_contact timestamp.
        """
        try:
            # Create the interaction
            response = self.client.table('interactions').insert(interaction_data).execute()
            
            # Update customer's last_contact
            if response.data:
                self.client.table('customers').update({
                    'last_contact': interaction_data['date']
                }).eq('id', interaction_data['customer_id']).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to create interaction: {e}")
            return None
    
    # ANALYTICS OPERATIONS
    def get_customer_counts_by_stage(self) -> Dict[str, int]:
        """
        Get count of customers in each pipeline stage.
        Returns dict like {'lead': 5, 'prospect': 3, 'customer': 12}
        """
        try:
            stages = ['lead', 'prospect', 'customer']
            counts = {}
            
            for stage in stages:
                response = self.client.table('customers').select("id", count='exact').eq('stage', stage).execute()
                counts[stage] = response.count or 0
            
            return counts
        except Exception as e:
            st.error(f"Failed to get stage counts: {e}")
            return {'lead': 0, 'prospect': 0, 'customer': 0}
    
    # PRODUCT OPERATIONS
    def get_all_products(self) -> List[Dict]:
        """
        Get all products from the database.
        Returns a list of product dictionaries.
        """
        try:
            response = self.client.table('products').select("*").execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to fetch products: {e}")
            return []
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """
        Get products filtered by category.
        """
        try:
            response = self.client.table('products').select("*").eq('category', category).execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to fetch products by category: {e}")
            return []
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Get a specific product by ID.
        """
        try:
            response = self.client.table('products').select("*").eq('id', product_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to fetch product: {e}")
            return None
    
    def create_product(self, product_data: Dict) -> Optional[Dict]:
        """
        Create a new product.
        """
        try:
            response = self.client.table('products').insert(product_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to create product: {e}")
            return None
    
    def update_product(self, product_id: int, product_data: Dict) -> bool:
        """
        Update an existing product.
        """
        try:
            response = self.client.table('products').update(product_data).eq('id', product_id).execute()
            return True
        except Exception as e:
            st.error(f"Failed to update product: {e}")
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product.
        """
        try:
            self.client.table('products').delete().eq('id', product_id).execute()
            return True
        except Exception as e:
            st.error(f"Failed to delete product: {e}")
            return False
    
    def get_customer_product_interests(self, customer_id: int) -> List[Dict]:
        """
        Extract product interests from customer interactions.
        Returns a list of products mentioned or discussed in interactions.
        """
        try:
            # Get all interactions for the customer
            interactions = self.get_customer_interactions(customer_id)
            
            # Get all products for reference
            all_products = self.get_all_products()
            
            # Extract product interests from interaction content
            product_interests = []
            
            for interaction in interactions:
                content = interaction.get('content', '').lower()
                subject = interaction.get('subject', '').lower()
                
                # Check for product mentions in content and subject
                for product in all_products:
                    product_name = product.get('name', '').lower()
                    product_category = product.get('category', '').lower()
                    
                    # Check if product name or category is mentioned
                    if (product_name in content or product_name in subject or 
                        product_category in content or product_category in subject):
                        
                        # Add product interest with interaction context
                        interest = {
                            'product': product,
                            'interaction_id': interaction.get('id'),
                            'interaction_type': interaction.get('type'),
                            'interaction_date': interaction.get('date'),
                            'sentiment': interaction.get('sentiment'),
                            'context': interaction.get('content', '')[:200] + '...' if len(interaction.get('content', '')) > 200 else interaction.get('content', '')
                        }
                        
                        # Avoid duplicates
                        if not any(pi['product']['id'] == product['id'] for pi in product_interests):
                            product_interests.append(interest)
            
            return product_interests
            
        except Exception as e:
            st.error(f"Failed to get customer product interests: {e}")
            return []
    
    def get_products_by_interest_keywords(self, keywords: List[str]) -> List[Dict]:
        """
        Find products that match interest keywords.
        """
        try:
            all_products = self.get_all_products()
            matching_products = []
            
            for product in all_products:
                product_text = f"{product.get('name', '')} {product.get('description', '')} {product.get('category', '')}".lower()
                
                for keyword in keywords:
                    if keyword.lower() in product_text:
                        matching_products.append(product)
                        break
            
            return matching_products
            
        except Exception as e:
            st.error(f"Failed to get products by keywords: {e}")
            return []
    
    # TRANSACTION OPERATIONS
    def get_customer_transactions(self, customer_id: int) -> List[Dict]:
        """
        Get all transactions for a specific customer.
        """
        try:
            response = self.client.table('transactions').select("""
                *,
                products:product_id(name, category, price, description),
                customers:customer_id(first_name, last_name, company)
            """).eq('customer_id', customer_id).order('transaction_date', desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to fetch customer transactions: {e}")
            return []
    
    def get_all_transactions(self) -> List[Dict]:
        """
        Get all transactions with product and customer details.
        """
        try:
            response = self.client.table('transactions').select("""
                *,
                products:product_id(name, category, price, description),
                customers:customer_id(first_name, last_name, company)
            """).order('transaction_date', desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to fetch transactions: {e}")
            return []
    
    def create_transaction(self, transaction_data: Dict) -> Optional[Dict]:
        """
        Create a new transaction.
        """
        try:
            response = self.client.table('transactions').insert(transaction_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to create transaction: {e}")
            return None
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Dict]:
        """
        Get a specific transaction by ID.
        """
        try:
            response = self.client.table('transactions').select("""
                *,
                products:product_id(name, category, price, description),
                customers:customer_id(first_name, last_name, company)
            """).eq('id', transaction_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Failed to fetch transaction: {e}")
            return None
    
    def get_customer_purchase_history(self, customer_id: int) -> Dict:
        """
        Get comprehensive purchase history for a customer.
        """
        try:
            transactions = self.get_customer_transactions(customer_id)
            
            if not transactions:
                return {
                    'total_transactions': 0,
                    'total_spent': 0,
                    'average_transaction': 0,
                    'favorite_categories': [],
                    'recent_purchases': [],
                    'purchase_timeline': []
                }
            
            # Calculate metrics
            total_spent = sum(t.get('total_amount', 0) for t in transactions)
            total_transactions = len(transactions)
            average_transaction = total_spent / total_transactions if total_transactions > 0 else 0
            
            # Get favorite categories
            categories = {}
            for transaction in transactions:
                product = transaction.get('products', {})
                category = product.get('category', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
            
            favorite_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'total_transactions': total_transactions,
                'total_spent': total_spent,
                'average_transaction': average_transaction,
                'favorite_categories': favorite_categories,
                'recent_purchases': transactions[:5],  # Last 5 purchases
                'purchase_timeline': transactions
            }
            
        except Exception as e:
            st.error(f"Failed to get purchase history: {e}")
            return {}


# Singleton pattern - create one instance to be used throughout the app
@st.cache_resource
def get_supabase_client() -> SupabaseClient:
    """
    Get or create the Supabase client instance.
    Uses Streamlit's cache to ensure only one instance exists.
    """
    return SupabaseClient()
