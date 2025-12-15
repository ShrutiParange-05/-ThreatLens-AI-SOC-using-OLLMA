from langchain_ollama import ChatOllama

print("--- DIAGNOSTIC TEST START ---")

# 1. Setup
print("1. Initializing Model (llama3)...")
try:
    llm = ChatOllama(
        model="llama3", 
        base_url="http://127.0.0.1:11434"
    )
except Exception as e:
    print(f"CRITICAL ERROR initializing: {e}")
    exit()

# 2. Invoke
print("2. Sending Test Message to Ollama...")
try:
    response = llm.invoke("Are you working? Reply with 'YES'.")
    print(f"\n3. SUCCESS! AI Response:\n{response.content}")
except Exception as e:
    print(f"\n3. CONNECTION FAILED: {e}")
    print("   - Is Ollama running? (Check taskbar/terminal)")
    print("   - Did you pull the model? (Run 'ollama pull llama3')")

print("\n--- DIAGNOSTIC TEST END ---")
