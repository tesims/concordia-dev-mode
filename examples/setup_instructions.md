# Getting Started with Concordia and Gemini

## Prerequisites

1. **Python Environment**: Ensure you have Python 3.11+ installed
2. **Concordia Installation**: 
   ```bash
   pip install gdm-concordia
   ```
   Or if working from source:
   ```bash
   pip install --editable .[dev]
   ```
3. **Environment Variables Package**:
   ```bash
   pip install python-dotenv
   ```

## Gemini API Setup

### 1. Get Your API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an account or sign in
3. Generate an API key

### 2. Create .env File (Recommended)
1. **Copy the template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file** and add your API key:
   ```bash
   # Open in your preferred editor
   nano .env
   # or
   code .env
   ```

3. **Replace the placeholder** in .env:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. **Save the file** - The .env file is automatically ignored by git for security

### Alternative: Environment Variable
If you prefer not to use .env files, you can still set environment variables:

**Linux/Mac:**
```bash
export GOOGLE_API_KEY='your_api_key_here'
```

**Windows:**
```cmd
set GOOGLE_API_KEY=your_api_key_here
```

## Running the Test

### Quick Test
```bash
cd examples
python test_gemini_simple.py
```

### Without API (for testing setup)
If you want to test the framework without making API calls:
```python
# In the script, set:
DISABLE_LANGUAGE_MODEL = True
```

## What the Test Does

The test script (`test_gemini_simple.py`) creates a simple simulation with:
- **2 Entities**: Alice and Bob meeting at a coffee shop
- **1 Game Master**: Controls the simulation flow
- **1 Initializer**: Sets up the initial scenario
- **3 Steps**: Short simulation for quick testing

## Expected Output

1. **Console Output**: Shows simulation progress
2. **HTML File**: `test_simulation_results.html` with detailed logs
3. **Success Message**: If everything works correctly

## Troubleshooting

### Common Issues:

1. **API Key Not Set**:
   ```
   Error: GOOGLE_API_KEY environment variable not set!
   ```
   **Solution**: Set your environment variable as shown above

2. **Rate Limiting**:
   ```
   Error running simulation: rate limit exceeded
   ```
   **Solution**: Wait a few minutes and try again, or set `sleep_periodically=True`

3. **Model Not Available**:
   ```
   Error: model not found
   ```
   **Solution**: Check available models at [Google AI Studio](https://aistudio.google.com/)

4. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'concordia'
   ```
   **Solution**: Install concordia: `pip install gdm-concordia`

### Testing Without API
If you want to test the framework setup without using API credits:
1. Edit `test_gemini_simple.py`
2. Set `DISABLE_LANGUAGE_MODEL = True`
3. Run the script - it will use dummy responses

## Next Steps

Once the test works:

1. **Explore Examples**: Check out other notebooks in `/examples/`
2. **Read Documentation**: Review the main README and examples
3. **Create Custom Prefabs**: Build your own entity and game master templates
4. **Scale Up**: Try larger simulations with more agents and steps

## Available Models

Gemini models you can use:
- `gemini-1.5-pro-latest` (default, most capable)
- `gemini-1.5-flash-latest` (faster, cheaper)
- `gemini-1.0-pro` (older version)

Change the model in the script by modifying:
```python
model = google_aistudio_model.GoogleAIStudioLanguageModel(
    model_name='gemini-1.5-flash-latest',  # Change this
    api_key=GOOGLE_API_KEY
)
```