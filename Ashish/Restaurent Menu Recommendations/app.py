import streamlit as st
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="Restaurant Menu & AI Assistant",
    page_icon="🍽️",
    layout="wide"
)

# Sidebar: API key input for Groq
st.sidebar.header("API Settings")
api_key_input = st.sidebar.text_input(
    "GROQ API Key",
    type="password",
    help="Your Groq API key. Stored in memory for this session only."
)
if api_key_input:
    st.session_state.groq_api_key = api_key_input

st.sidebar.subheader("Model")
# A shortlist of available Groq models (including the sample's model)
AVAILABLE_MODELS = [
    "openai/gpt-oss-20b",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]
default_model = st.session_state.get("groq_model") or AVAILABLE_MODELS[0]
selected_model = st.sidebar.selectbox("Groq model", AVAILABLE_MODELS, index=AVAILABLE_MODELS.index(default_model) if default_model in AVAILABLE_MODELS else 0)
st.session_state.groq_model = selected_model

# Restaurant menu data with INR prices
MENU = {
    "Appetizers": [
        {
            "name": "Vegetable Spring Rolls",
            "price": "₹249",
            "spice": "Mild",
            "portion": "4 pieces",
            "description": "Crispy vegetable spring rolls with sweet chili dipping sauce"
        },
        {
            "name": "Paneer Tikka",
            "price": "₹329",
            "spice": "Medium",
            "portion": "6 pieces",
            "description": "Grilled cottage cheese marinated in tandoori spices"
        },
        {
            "name": "Chicken 65",
            "price": "₹399",
            "spice": "Hot",
            "portion": "8 pieces",
            "description": "Spicy deep-fried chicken with curry leaves and green chilies"
        },
        {
            "name": "Garlic Bread",
            "price": "₹199",
            "spice": "None",
            "portion": "6 slices",
            "description": "Toasted baguette with garlic butter and herbs"
        }
    ],
    "Main Courses": [
        {
            "name": "Butter Chicken",
            "price": "₹449",
            "spice": "Mild",
            "portion": "Serves 1-2, comes with 2 naan",
            "description": "Tender chicken in creamy tomato gravy with butter and cream"
        },
        {
            "name": "Paneer Butter Masala",
            "price": "₹399",
            "spice": "Mild",
            "portion": "Serves 1-2, comes with 2 naan",
            "description": "Cottage cheese cubes in rich tomato and cashew gravy"
        },
        {
            "name": "Biryani (Chicken)",
            "price": "₹499",
            "spice": "Medium",
            "portion": "Full plate with raita",
            "description": "Fragrant basmati rice layered with spiced chicken and saffron"
        },
        {
            "name": "Biryani (Vegetable)",
            "price": "₹399",
            "spice": "Medium",
            "portion": "Full plate with raita",
            "description": "Aromatic rice with mixed vegetables, herbs and spices"
        },
        {
            "name": "Dal Makhani",
            "price": "₹349",
            "spice": "Mild",
            "portion": "Large bowl, serves 2",
            "description": "Black lentils slow-cooked with butter, cream and tomatoes"
        },
        {
            "name": "Tandoori Chicken (Half)",
            "price": "₹549",
            "spice": "Medium",
            "portion": "Half chicken with mint chutney",
            "description": "Chicken marinated in yogurt and spices, cooked in tandoor"
        },
        {
            "name": "Chole Bhature",
            "price": "₹299",
            "spice": "Medium",
            "portion": "2 bhature with chickpea curry",
            "description": "Spicy chickpea curry served with fluffy fried bread"
        },
        {
            "name": "Palak Paneer",
            "price": "₹379",
            "spice": "Mild",
            "portion": "Serves 1-2",
            "description": "Cottage cheese in creamy spinach gravy with aromatic spices"
        }
    ],
    "Rice & Breads": [
        {
            "name": "Jeera Rice",
            "price": "₹149",
            "spice": "None",
            "portion": "Single serving",
            "description": "Basmati rice tempered with cumin seeds"
        },
        {
            "name": "Naan (Plain)",
            "price": "₹49",
            "spice": "None",
            "portion": "1 piece",
            "description": "Soft leavened bread baked in tandoor"
        },
        {
            "name": "Garlic Naan",
            "price": "₹69",
            "spice": "None",
            "portion": "1 piece",
            "description": "Naan topped with garlic and coriander"
        },
        {
            "name": "Butter Naan",
            "price": "₹59",
            "spice": "None",
            "portion": "1 piece",
            "description": "Naan brushed with melted butter"
        }
    ],
    "Desserts": [
        {
            "name": "Gulab Jamun",
            "price": "₹129",
            "spice": "None",
            "portion": "2 pieces",
            "description": "Soft milk dumplings soaked in rose-flavored sugar syrup"
        },
        {
            "name": "Ras Malai",
            "price": "₹149",
            "spice": "None",
            "portion": "2 pieces",
            "description": "Cottage cheese dumplings in sweetened, thickened milk"
        },
        {
            "name": "Ice Cream (Kulfi)",
            "price": "₹99",
            "spice": "None",
            "portion": "1 piece",
            "description": "Traditional Indian ice cream with cardamom and pistachios"
        }
    ],
    "Beverages": [
        {
            "name": "Masala Chai",
            "price": "₹49",
            "spice": "Mild (cardamom, ginger)",
            "portion": "1 cup",
            "description": "Indian spiced tea with milk"
        },
        {
            "name": "Mango Lassi",
            "price": "₹129",
            "spice": "None",
            "portion": "300ml",
            "description": "Creamy yogurt drink blended with sweet mango"
        },
        {
            "name": "Fresh Lime Soda",
            "price": "₹79",
            "spice": "None",
            "portion": "300ml",
            "description": "Freshly squeezed lime with soda water"
        },
        {
            "name": "Buttermilk (Chaas)",
            "price": "₹59",
            "spice": "Mild",
            "portion": "300ml",
            "description": "Spiced yogurt drink with cumin and mint"
        }
    ]
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_dish" not in st.session_state:
    st.session_state.selected_dish = None

# Function to create menu context for LLM
def create_menu_context():
    context = "You are a helpful restaurant assistant. Here is our complete menu:\n\n"
    for category, items in MENU.items():
        context += f"\n{category}:\n"
        for item in items:
            context += f"- {item['name']} ({item['price']})\n"
            context += f"  Spice Level: {item['spice']}\n"
            context += f"  Portion: {item['portion']}\n"
            context += f"  Description: {item['description']}\n\n"
    return context

# Function to get combo recommendations
def get_combo_recommendations(dish_name):
    """Generate context about the selected dish for combo recommendations"""
    selected_item = None
    for category, items in MENU.items():
        for item in items:
            if item['name'].lower() == dish_name.lower():
                selected_item = item
                break
        if selected_item:
            break
    
    if selected_item:
        return f"\nThe customer has selected: {selected_item['name']} ({selected_item['price']}, Spice: {selected_item['spice']}, Portion: {selected_item['portion']})\n"
    return ""

# Function to call Groq API
def chat_with_groq(user_message, selected_dish=None, stream=True):
    try:
        api_key = st.session_state.get("groq_api_key") or os.environ.get("GROQ_API_KEY")
        if not api_key:
            return "⚠️ Please enter your GROQ API key in the sidebar (API Settings) or set GROQ_API_KEY in your environment."
        
        client = Groq(api_key=api_key)
        
        # Build system prompt
        system_prompt = create_menu_context()
        if selected_dish:
            system_prompt += get_combo_recommendations(selected_dish)
            system_prompt += f"\nProvide combo recommendations that pair well with {selected_dish}. Consider complementary flavors, spice levels, and complete meal balance. Suggest appetizers, sides, beverages, and desserts that would enhance the dining experience."
        
        system_prompt += "\n\nAnswer questions about spice levels, portion sizes, ingredients, and recommend dish combinations. Be friendly, helpful, and concise. All prices are in Indian Rupees (INR)."
        
        # Create messages for API
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend([{"role": msg["role"], "content": msg["content"]} 
                        for msg in st.session_state.messages])
        messages.append({"role": "user", "content": user_message})
        
        # Call Groq API (streaming by default per provided sample)
        model_name = st.session_state.get("groq_model", AVAILABLE_MODELS[0])
        if stream:
            placeholder = st.empty()
            collected_text = ""
            completion_stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_completion_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            for chunk in completion_stream:
                delta = getattr(chunk.choices[0], "delta", None)
                content_piece = getattr(delta, "content", None) if delta else None
                if content_piece:
                    collected_text += content_piece
                    placeholder.markdown(collected_text)
            return collected_text
        else:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
            )
            return response.choices[0].message.content
    
    except Exception as e:
        # Surface the API's error message directly for clarity
        return f"❌ Error: {str(e)}"

# App Title
st.title("🍽️ Restaurant Menu & AI Assistant")
st.markdown("---")

# Create two columns
col1, col2 = st.columns([1, 1])

# Left column - Menu Display
with col1:
    st.header("📖 Our Menu")
    
    # Display menu by category
    for category, items in MENU.items():
        st.subheader(f"🔸 {category}")
        for item in items:
            with st.expander(f"{item['name']} - {item['price']}"):
                st.write(f"**Description:** {item['description']}")
                st.write(f"**Spice Level:** {item['spice']}")
                st.write(f"**Portion:** {item['portion']}")
                
                # Button to select dish for recommendations
                if st.button(f"Get Combos for {item['name']}", key=f"combo_{item['name']}"):
                    st.session_state.selected_dish = item['name']
                    combo_prompt = f"I'm ordering {item['name']}. What appetizers, sides, beverages, and desserts would you recommend to go with it?"
                    st.session_state.messages.append({"role": "user", "content": combo_prompt})
                    
                    with st.spinner("Getting recommendations..."):
                        response = chat_with_groq(combo_prompt, item['name'])
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    st.rerun()
        st.markdown("---")

# Right column - Chat Interface
with col2:
    st.header("💬 Ask Our AI Assistant")
    
    if st.session_state.selected_dish:
        st.info(f"🎯 Currently selected: **{st.session_state.selected_dish}**")
        if st.button("Clear Selection"):
            st.session_state.selected_dish = None
            st.rerun()
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about menu items, spice levels, portions, or combos..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_groq(prompt, st.session_state.selected_dish)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Quick action buttons
    st.markdown("### Quick Questions")
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("🌶️ Show mild dishes"):
            prompt = "What dishes do you have with mild or no spice?"
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = chat_with_groq(prompt, st.session_state.selected_dish)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col_b:
        if st.button("🥗 Vegetarian options"):
            prompt = "What are all the vegetarian dishes available?"
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = chat_with_groq(prompt, st.session_state.selected_dish)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.selected_dish = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>💡 Tip: Click on any dish to get personalized combo recommendations!</p>
        <p>Ask me about spice levels, portion sizes, or what goes well together.</p>
    </div>
""", unsafe_allow_html=True)