<scope>
Use the best_practices.md and the reference files in /.ref to create a Library of Congress Subject Headings suggestion agent called "LCSH Assistant". The agent provides LCSH suggestions based on the bibliographic information provided by users and validate the suggestions with an API. The design is modern, clean, and in both light and dark theme.    
</scope>

<specs>
- The app is a streamlit app.
- The app uses Google Gemini 2.0 Flash as the LLM.
- The app allows users to enter their Gemini API keys.
- The app does not store any user information. 
- The user can enter the bibliographic informaion in text, or upload text files (txt, md, word), images (jpg, png, etc.), pdfs.
- The user can enter a gemini API key. Once a session ends, all data gets clear.
- Any other ideas to get a more accessible and user-friendly user experience are welcome.
</specs>

<refs>
- lcsh_openai_action.json: the OpenAI action json for the LCSH API
- gemini_snippet.py: python snippet from Gemini AI Studio
- system_prompt.md: the system prompt and the logic for the agent
</refs>

<your_task>
Creat the LCSH suggestion agent based on the above specs
</your_task>

<rules>
- use uv for tooling
- use streamlit to build the app
- the app must be secure
- design should be in both light and dark theme, modern and clean
- the app should be minimize the cost for maintainance and hosting.
</rules>