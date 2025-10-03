# ai/prompts.py
"""
AI prompt templates for the AiCRM application.
"""

CUSTOMER_SUMMARY_PROMPT = """
Analyze this customer and their interactions to create a comprehensive summary:

Customer Information:
- Name: {first_name} {last_name}
- Company: {company}
- Email: {email}
- Phone: {phone}
- Stage: {stage}
- Notes: {notes}

Recent Interactions ({interaction_count} total):
{interactions}

Product Interests & Preferences:
{product_interests}

Purchase History:
{transaction_history}

Available Products:
{available_products}

Please provide a comprehensive customer summary including:
1. Customer profile and background
2. Key interaction patterns and preferences
3. Product interests and buying behavior analysis
4. Purchase history analysis and spending patterns
5. Current relationship status and stage
6. Product recommendations based on interests, interactions, and purchase history
7. Important insights and recommendations
8. Next steps and opportunities

Focus on how product interests align with customer needs and suggest relevant products from our collection.
Use a friendly, conversational tone while being professional and actionable for sales purposes.
Show enthusiasm about our products and genuine care for the customer's success.
"""

EMAIL_DRAFT_PROMPT = """
Generate a friendly, professional email draft for a sales representative to send to this customer from Luxe Couture:

Customer: {first_name} {last_name}
Company: {company}
Stage: {stage}

Context: {context}
Email Type: {email_type}

Product Interests: {product_interests}

Please generate a warm, semi-casual email draft that the sales rep can send to their customer:
1. Feels personal and genuine, not corporate
2. References their company and specific context naturally
3. Mentions relevant products from our collection with enthusiasm
4. Includes product details, prices, and benefits when appropriate
5. Has a clear but friendly call-to-action
6. Uses a warm, professional but approachable tone
7. Shows knowledge of our luxury fashion products
8. Feels like it's from a real person who cares about their needs

Include subject line and email body. Make it sound like the sales rep is excited to help their customer!
"""

SENTIMENT_ANALYSIS_PROMPT = """
Analyze the sentiment of this interaction text and return only one word: positive, neutral, or negative.

Text: {text}

Consider the overall tone, language, and context.
"""

SALES_ADVICE_PROMPT = """
You are an AI sales assistant helping a sales representative at Luxe Couture, a luxury fashion brand. You provide strategic advice to help the sales rep better serve their customer.

Customer being discussed: {first_name} {last_name}
Company: {company}
Stage: {stage}

Recent Interactions:
{interactions}

Product Interests & Preferences:
{product_interests}

Available Products:
{available_products}

Sales Rep's Question: {question}

Provide strategic sales advice that:
1. Helps the sales rep understand the customer's situation and needs
2. Suggests specific products from our collection that would be relevant
3. Uses a professional, consultative tone
4. Gives actionable recommendations for the sales rep to follow
5. Mentions product details, prices, and benefits for the sales rep to use
6. Suggests next steps and sales strategies
7. Helps with objection handling and closing techniques when relevant

Be professional, strategic, and focused on helping the sales rep succeed with this customer!
"""
