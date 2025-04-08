import asyncio
import os
from celery import Celery
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy import select
from db.database import async_session
from db.models import Task

app = Celery(
    "celery_worker",
    broker="redis://redis_broker:6379/0",
    backend="redis://redis_broker:6379/0",
)


load_dotenv("../.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.task
def recognize_category(description: str, task_id: int) -> bool:
    categories = "education, sport, hobby, entertainment, travel, job"
    help_prompt = f"You are assistant of advanced to do list service which based on ai models. The users will send to you some descriptions of task, and your target is to send the category of this task there categories {categories}, in format category: category"

    openai = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {
                    "role": "system",
                    "content": help_prompt
                },
                {
                    "role": "user",
                    "content": description
                }
            ]
        )

        reply = response.choices[0].message.content

        if not "category" in reply:
            return False

        category = reply[len("category: "):]
        return asyncio.run(update_query(task_id=task_id, category=category))

    except Exception as e:
        print(str(e))


async def update_query(task_id, category) -> bool:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()

            if task:
                task.category = category
                await session.commit()
                return True

            return False