import { GoogleGenAI, Modality, GenerateContentResponse } from "@google/genai";
import { TransformMode } from "../types";

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  throw new Error("API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey: API_KEY });

const callGemini = async (base64ImageData: string, mimeType: string, prompt: string): Promise<string> => {
    const model = 'gemini-2.5-flash-image';
    const response = await ai.models.generateContent({
        model: model,
        contents: {
            parts: [
                {
                    inlineData: {
                        data: base64ImageData,
                        mimeType: mimeType,
                    },
                },
                {
                    text: prompt,
                },
            ],
        },
        config: {
            responseModalities: [Modality.IMAGE, Modality.TEXT],
        },
    });

    for (const part of response.candidates?.[0]?.content?.parts ?? []) {
        if (part.inlineData && part.inlineData.mimeType.startsWith('image/')) {
            return part.inlineData.data;
        }
    }
    
    throw new Error("AI did not return an image from a call. Please try again.");
}


/**
 * Transforms a food image into a professional photograph using the Gemini API.
 * @param base64ImageData The base64 encoded string of the image.
 * @param mimeType The MIME type of the image (e.g., 'image/jpeg').
 * @param mode The transformation mode ('reimagine' or 'polish').
 * @param foodLabel An optional label for the food item to improve results.
 * @returns A promise that resolves to the base64 encoded string of the generated image.
 */
export const transformFoodImage = async (
  base64ImageData: string,
  mimeType: string,
  mode: TransformMode,
  foodLabel?: string
): Promise<string> => {
  
  let prompt = '';

  if (mode === 'reimagine') {
    const specificFood = foodLabel ? `of ${foodLabel}` : 'of food';
    prompt = `Transform this image ${specificFood} into a professional food photograph. The photo must have a 1:1 aspect ratio and professional food photography lighting. Reimagine the plating and presentation to be highly contextual and authentic to the dish. For example, rustic pasta might be in a warm, ceramic bowl, while delicate sushi could be on a minimalist slate. The setting, utensils, and garnishes must complement the food's origin and style. The final composition should be elegant, making the dish look incredibly delicious and appetizing. Enhance colors and textures to make the dish pop.`;
  } else { // 'polish'
    prompt = `A professional food photography shot of the dish from the reference image. The dish should be artfully arranged on a clean, pristine white ceramic plate. The photo is taken from a 45-degree angle in a bright, minimalist studio environment with soft, diffused lighting. The focus is sharp on the food, with a slightly blurred background. Photorealistic, high detail, appetizing. The final image must have a 1:1 aspect ratio.`;
  }
  
  try {
    const result = await callGemini(base64ImageData, mimeType, prompt);
    
    if (!result) {
        throw new Error("AI failed to generate an image.");
    }

    return result;

  } catch (error) {
    console.error("Error transforming image:", error);
    throw new Error("Failed to generate the image. The AI model might be unavailable or the request failed.");
  }
};