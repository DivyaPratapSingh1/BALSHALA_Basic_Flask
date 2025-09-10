import os, random, datetime
from typing import Optional

YOGIC_QUOTES = [
    "Practice becomes firmly grounded when well attended for a long time, without break, and with earnestness. — Patanjali",
    "Discipline is choosing what you want most over what you want now.",
    "The body benefits from movement, and the mind benefits from stillness.",
    "Small daily improvements are the key to long-term results.",
    "Strength does not come from the physical capacity. It comes from an indomitable will. — Gandhi",
    "Energy flows where attention goes.",
    "You don't have to be extreme, just consistent.",
    "When you feel like quitting, remember why you started.",
    "Excellence is a habit: what you do daily, you become.",
    "Breathe. Focus. One more rep.",
    "The secret of change is to focus all your energy, not on fighting the old, but on building the new.",
    "Your future self is watching. Make them proud.",
    "Sthira sukham asanam — Steady and comfortable effort.",
    "Sweat is just your fat crying.",
    "Motion creates emotion. Move your body to move your mind.",
    "Right effort, right rest, right food — the trifecta of growth.",
    "Today’s consistency beats tomorrow’s intensity.",
    "Slow progress is still progress. Don’t stop.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Train your mind and your body will follow."
]

def get_quote(seed: Optional[int]=None) -> str:
    if seed is None:
        # daily deterministic seed
        today = datetime.date.today().toordinal()
        seed = today
    random.seed(seed)
    return random.choice(YOGIC_QUOTES)

def get_quote_llm(prompt: str) -> str:
    """
    Optional: if OPENAI_API_KEY is set, attempt to generate a custom quote.
    """
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return get_quote()
        client = OpenAI(api_key=api_key)
        msg = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system", "content":"You are a motivational coach who blends gym training with yogic wisdom. Output a single one-line quote."},
                {"role":"user","content": prompt}
            ],
            temperature=0.7,
            max_tokens=50
        )
        text = msg.choices[0].message.content.strip()
        return text or get_quote()
    except Exception:
        return get_quote()
