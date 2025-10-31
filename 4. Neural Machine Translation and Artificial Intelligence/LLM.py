from transformers import pipeline
import torch
import sys

# Define the model to be used from Hugging Face
MODEL_HF = "microsoft/Phi-3-mini-4k-instruct"

def query_hf_llm():
    """
    Loads the Hugging Face model (downloading it if necessary) and queries it.
    """
    print("--- LLM Query with Hugging Face Transformers ---")
    
    # 1. Automatic Check and Load/Download (handled by pipeline)
    print(f"Loading model '{MODEL_HF}'...")
    print("The model will be downloaded automatically if not already in cache.")
    
    try:
        # The pipeline creation handles checking the local cache.
        # If the model is not found, it is downloaded.
        generator = pipeline(
            "text-generation", 
            model=MODEL_HF,
            # Use GPU (0) if available, otherwise use CPU (-1)
            device=0 if torch.cuda.is_available() else -1
        )
        print("✅ Model loaded successfully.")
        
    except Exception as e:
        print(f"\n❌ ERROR during model loading/download: {e}")
        print("Ensure you have sufficient memory and PyTorch/Transformers dependencies installed.")
        sys.exit(1)
        
    print("---------------------------------------")

    # 2. Get user prompt
    
    while 1:
    
        user_prompt = input("Enter your question or X to exit: ")
        
        if user_prompt=="X" or user_prompt=="x":
            sys.exit()
        
        if not user_prompt:
            print("Prompt cannot be empty.")
            return

        print("\nProcessing the response...")

        try:
            # 3. Generate the response
            result = generator(
                user_prompt, 
                max_new_tokens=50, 
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7 
            )

            response_content = result[0]['generated_text']
            
            print("\n--- LLM Response (Hugging Face) ---")
            # Clean the output (model often echoes the input prompt)
            print(response_content.replace(user_prompt, "").strip())
            print("---------------------------------------")

        except Exception as e:
            print(f"\n❌ An error occurred during generation: {e}")

if __name__ == "__main__":
    query_hf_llm()