# Buzz Newsletter

## Goal

- Build cost-effective news curation tool with LLM

## What to expect
By signing up for the newsletter:
- Access newsletters from the past up to 7 days. 
- Get daily email featuring today's trending news. 
- Upgrade to the premium version. (Note that there is no difference in content visibility)

## Tech Stack

- **Frontend:** TypeScript, React, TailwindCSS
- **Backend:** Python (FastAPI, LangGraph, SqlAlchemy etc.)
- **Database:** PostgreSQL
- **LLM:** Ollama | OpenRouter ([Link](https://openrouter.ai/))
- **Deployment:** Vercel, Render, Supabase

## Features

### 1. Curation

- Collect trending webz news API ([Link](https://docs.webz.io/reference/news-api-lite))
- Pick top 3 of trending news
- Generate newsletter from those 3 sources

### 2. Billing

- Redirect to Stripe session upon when the Upgrade button is hit
- Update Postgres User table upon successful payment

### 3. Marketing

- For subscribers and non-subscribers, generate marketing email while featuring today's newsletter
- Send email using Gmail SMTP server

### 4. Scheduling

- Curation and Marketing jobs are currently automated with Cron job.

## Design decisions

- LangGraph vs CrewAI: chose LangGraph for flexibility
- Ollama vs OpenRouter: Initially I was using Ollama, but due to hardware limitation, I moved to OpenRouter.
  - Tested model
  1.  Qwen3 8B (Ollama): chosen because of high tool calling performance ([Link](https://www.docker.com/blog/local-llm-tool-calling-a-practical-evaluation/)). Very slow with my hardware.
  2.  Gemma3n E4B (Ollama): good for edge device -> context size was not enough and increasing the size caused crash.
  3.  Gemma3 30B (OpenRouter): faster and better quality output (if data privacy is not important for your app)

## Room for improvement

- Currently the agent curates only top 3 news: 10+ news can be used to add more colors to the newsletter.
- Personalized newsletter generation: Newsletter can be generated for each customer based on their favorite topics.
- Robust retry logic


## Topics learned

- Quantization
- Authorization (JWT token, session management)
- SMTP
