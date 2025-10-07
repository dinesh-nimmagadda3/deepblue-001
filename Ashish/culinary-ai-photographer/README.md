# MenuReady AI Photo Studio

**The ultimate photography tool for hotel and restaurant owners.**

Turn simple phone snapshots of your menu items into stunning, professional-grade photographs that attract more customers and drive sales. No expensive photoshoots, no complicated software. Just beautiful food photography, ready in seconds.

<!-- TODO: Add a new screenshot of the application here. -->

## 🤔 Why Use This Tool for Your Business?

In the digital age, customers eat with their eyes first. High-quality photos on your menu, website, delivery apps (like Uber Eats, DoorDash), and social media are critical for success. However, professional food photography is expensive and time-consuming.

**MenuReady AI solves this problem.**

-   ✅ **Save Thousands on Photography**: Eliminate the need to hire professional photographers and book studio time.
-   ✅ **Increase Customer Engagement**: Mouth-watering photos grab attention and have been proven to increase order rates.
-   ✅ **Maintain Brand Consistency**: Achieve a consistent, high-quality look for all your menu items across all platforms.
-   ✅ **Update Menus Instantly**: Launching a new special? Get a professional photo ready for your menu and social media in under a minute.

## ✨ Features

-   **AI-Powered Image Transformation**: Utilizes Google's cutting-edge AI to intelligently generate beautiful food photos.
-   **Two Powerful Modes for Your Menu**:
    -   **Reimagine**: Perfect for creating a unique, aspirational lifestyle shot. The AI designs a completely new, professional scene with plating and a setting that authentically matches the dish.
    -   **Polish**: Ideal for a clean, consistent menu look. The AI places your dish on a pristine white ceramic plate in a bright studio setting, ensuring every photo is sharp, appetizing, and ready for your menu or delivery app.
-   **Download & Deploy**: Instantly download the high-quality, 1:1 aspect ratio image, perfectly optimized for most delivery apps and social media platforms.
-   **Simple & Fast**: The interface is incredibly easy to use. No training required. Get from a simple phone picture to a professional photo in just a few clicks.
-   **Side-by-Side Comparison**: Instantly see the incredible transformation from your original photo to the AI-generated masterpiece.

## 🚀 Getting Started

This project is ready to run. The only configuration required is setting up your Google Gemini API key.

### 1. Get a Gemini API Key

You need an API key to use the Google Gemini models. You can obtain one for free from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Set the API Key

The application is configured to use an environment variable to securely access your API key.

-   In your project's development environment, find the section for managing "Secrets" or "Environment Variables".
-   Create a new secret with the name `API_KEY`.
-   Set the value of this secret to the API key you obtained from Google AI Studio.

Once the `API_KEY` is set, the application will be fully functional.

## 👩‍🍳 How to Use

1.  **Upload Your Photo**: Click the **Upload Food Photo** button or the card on the left to select an image of your dish.
2.  **Choose Your Style**:
    *   **Reimagine**: Creates a completely new, professional scene with plating and a setting that authentically matches the dish.
    *   **Polish**: Places your dish on a pristine white ceramic plate in a bright studio setting, perfect for a clean and consistent menu look.
3.  **(Optional) Name Your Dish**: For the "Reimagine" mode, entering the menu item's name (e.g., "Signature Angus Burger") helps the AI create a more contextual photo.
4.  **Generate Your Photo**: Click **Make it Professional**. The AI will generate your new image in a few moments.
5.  **View and Download**:
    *   Your new photo will appear on the right. Click it to see a larger preview.
    *   Click the **Download Photo** button to save the high-quality image.
6.  **Start Over**: Use the **Clear** button to reset the app for your next menu item.

## 🛠️ Tech Stack

-   **Frontend**: [React](https://reactjs.org/) & [TypeScript](https://www.typescriptlang.org/)
-   **AI Model**: [Google Gemini API (`gemini-2.5-flash-image`)](https://ai.google.dev/) via `@google/genai` SDK
-   **Styling**: [Tailwind CSS](https://tailwindcss.com/)