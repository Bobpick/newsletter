import ollama
import schedule
import time
from datetime import datetime
from typing import Dict, List, Optional
import json
import os
from dataclasses import dataclass
import random

@dataclass
class ContentTemplate:
    type: str
    framework: dict
    tone: str
    length: int
    formatting: str = "plain_text"  # Add default formatting parameter
class AIContentEngine:
    def __init__(self, model_name: str = "llama2"):
        self.model = model_name
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, ContentTemplate]:
        # Load predefined templates for different content types
        return {
           "newsletter": ContentTemplate(
                type="newsletter",
                framework={
            "intro": {
                "weight": 0.15,
                "elements": ["hook", "topic_introduction"]
            },
            "body": {
                "weight": 0.75,  # Increased weight since you're not using a footer here.
                "elements": ["main_points", "detailed_explanation", "examples", "benefits_or_challenges"]
            },
            "call_to_action": {
                "weight": 0.1,
                "elements": ["action_prompt", "value_proposition"]
            }
        },
            tone="uplifting",  # Adjust tone as needed (e.g., professional, conversational)
            formatting="plain_text",  # Alternative: "HTML"
                length=1000
            ),
            "tweet": ContentTemplate(
                type="tweet",
                framework={"hook": 0.3, "message": 0.5, "hashtags": 0.2},
                tone="engaging",
                length=140
            )
        }

    def generate_content(self, content_type: str, prompt: str) -> str:
        template = self.templates.get(content_type)
        if not template:
            raise ValueError(f"Unknown content type: {content_type}")

        system_prompt = f"""Generate {content_type} content:
        - Tone: {template.tone}
        - Length: {template.length} chars max
        - Framework: {template.framework}
        Topic: {prompt}"""

        response = ollama.chat(model=self.model, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ])
        
        return response['message']['content']

class NewsletterCopilot:
    def __init__(self, ai_engine: AIContentEngine):
        self.ai_engine = ai_engine
        self.schedule = {}

    def create_newsletter(self, topic: str, schedule_time: Optional[str] = None) -> str:
        content = self.ai_engine.generate_content("newsletter", topic)
        
        filename = f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Newsletter saved to {filename}")
        print(f"Length: {len(content)} characters")
        
        if schedule_time:
            self.schedule[topic] = schedule_time
            schedule.every().day.at(schedule_time).do(
                self._send_newsletter, topic, content
            )
        
        return content

    def _send_newsletter(self, topic: str, content: str):
        # Implement actual sending logic here
        print(f"Sending newsletter about {topic}: {content[:100]}...")

class ContentCopilot:
    def __init__(self, ai_engine: AIContentEngine):
        self.ai_engine = ai_engine

    def generate_short_form(self, topic: str) -> str:
        return self.ai_engine.generate_content("tweet", topic)

    def repurpose_content(self, original_content: str, target_type: str) -> str:
        prompt = f"Repurpose this content into {target_type}: {original_content}"
        return self.ai_engine.generate_content(target_type, prompt)

class TopicManager:
    def __init__(self, topics_file="topics.json"):
        self.topics_file = topics_file
        self.topics = self.load_topics()
        
    def load_topics(self):
        if os.path.exists(self.topics_file):
            with open(self.topics_file, 'r') as f:
                data = json.load(f)
        else:
            data = {
                'pending': [
                    "AI Technology Trends 2024",
                    "Digital Marketing Strategies",
                    "Remote Work Best Practices",
                    "Overcoming Spiritual Doubt",
                    "Finding Peace in God's Plan",
                    "The Power of Prayer in Crisis",
                    "Faith Over Fear: Biblical Perspectives",
                    "Divine Comfort in Times of Loss",
                    "God's Love in Our Darkest Moments",
                    "Stories of Biblical Resilience",
                    "Trusting God When Life Hurts",
                    "The Role of Faith in Healing",
                    "Finding Hope After Despair",
                    "God's Promises for Troubled Times",
                    "Embracing Change with Faith",
                    "Faith and Mental Health",
                    "The Strength Found in Community",
                    "Living Out Your Faith in Hard Times",
                    "Biblical Figures and Their Challenges",
                    "Mastering the Eisenhower Matrix",
                    "The 7 Habits of Highly Effective People",
                    "First Things First: Prioritizing Life",
                    "Begin with the End in Mind",
                    "Sharpen the Saw: Self-Renewal Techniques",
                    "The Time Management Matrix",
                    "Living Out Your Personal Mission Statement",
                    "Synergizing: Effective Collaboration",
                    "Proactivity vs. Reactivity",
                    "Setting and Achieving SMART Goals",
                    "The Four Quadrants of Time Management",
                    "Dealing with the Tyranny of the Urgent",
                    "Win-Win or No Deal: Negotiating Life",
                    "The Importance of Keeping Promises to Yourself",
                    "The Power of Saying No",
                    "Balancing Life's Roles with Covey's Roles and Goals",
                    "12 Rules for Life: An Antidote to Chaos",
                    "Clean Your Room: Starting with Simple Order",
                    "Stand Up Straight with Your Shoulders Back",
                    "Tell the Truth - or, at Least, Don't Lie",
                    "Pet a Cat When You Encounter One on the Street",
                    "Rule Your Life, Not Your Emotions",
                    "The Significance of Routine",
                    "Hierarchy of Responsibility",
                    "Embracing Meaningful Suffering",
                    "The Necessity of Competence",
                    "Confronting the Chaos Within",
                    "Cultivating Patience Through Faith",
                    "Forgiveness: A Path to Inner Peace",
                    "Spiritual Growth Through Suffering",
                    "The Comfort of the Psalms",
                    "God’s Guidance in Life’s Wilderness",
                    "Miracles in Modern Times",
                    "Encouragement from the Beatitudes",
                    "Faith as the Answer to Anxiety",
                    "Rejoicing in Trials: James' Perspective",
                    "God’s Timing vs. Our Timing",
                    "The Role of Faith in Personal Renewal",
                    "Finding Hope in Uncertain Times",
                    "Faith Over Fear: Trusting the Process",
                    "The Power of Prayer in Daily Life",
                    "You Are Not Alone: Overcoming Isolation",
                    "Strength for the Journey: Scriptures for Hard Times",
                    "How Faith Can Restore Your Joy",
                    "God’s Promises: A Light in the Darkness",
                    "Building Resilience Through Faith",
                    "The Beauty of Surrendering Control",
                    "Navigating Grief with Grace and Faith",
                    "Encouragement for the Weary Soul",
                    "Letting Go of Worry: Trusting God's Plan",
                    "The Role of Community in Healing",
                    "Faith and Mental Health: Finding Balance",
                    "Walking Through the Valley: God's Presence in Pain",
                    "Renewing Your Spirit in Times of Struggle",
                    "Small Steps to Strengthen Your Faith Daily",
                    "When God Feels Distant: Finding Him Again",
                    "Stories of Triumph Through Faith",
                    "The Gift of Grace: Embracing God's Love",
                    "Hope for Tomorrow: Trusting in New Beginnings",
                    "Finding Peace Amidst Chaos",
                    "Courage to Keep Moving Forward",
                    "How Gratitude Transforms Hard Times",
                    "Listening to God's Whisper in the Storm",
                    "Faith in Action: Serving Others During Struggles",
                    "Turning Pain Into Purpose",
                    "Scriptures to Anchor Your Soul",
                    "Celebrating Small Victories Through Faith",
                    "Living Victoriously Even When Life Hurts",
                     "Finding Peace in the Storm",
                    "Overcoming Adversity with Faith",
                    "The Power of Prayer: A Daily Practice",
                    "The Comfort of God's Presence",
                    "Hope in the Midst of Despair",
                    "The Strength of the Human Spirit",
                    "The Healing Power of Forgiveness",
                    "Cultivating Gratitude, Even in Difficult Times",
                    "The Importance of Self-Care for the Soul",
                    "The Sovereignty of God: Trusting His Plan",
                    "The Love of God: Unconditional and Everlasting",
                    "The Promises of God: A Source of Strength",
                    "The Power of God's Word: A Daily Dose of Inspiration",
                    "Lessons from Biblical Figures Who Overcame",
                    "The Importance of Community and Fellowship",
                    "The Role of Faith in Overcoming Addiction",
                    "The Power of Positive Confession",
                    "The Beauty of God's Creation: A Source of Wonder",
                    "The Importance of Rest and Sabbath",
                    "Building a Strong Spiritual Foundation",
                    "Coping with Grief and Loss",
                    "Managing Stress and Anxiety",
                    "Overcoming Fear and Doubt",
                    "The Benefits of Meditation and Mindfulness",
                    "The Importance of Setting Boundaries",
                    "The Power of Positive Thinking",
                    "The Art of Letting Go",
                    "The Importance of Seeking Professional Help",
                    "Building Resilience: A Guide to Overcoming Challenges"
                ],
                'completed': []
            }
            self.save_topics(data)
        return data
    
    def get_random_topic(self):
        if not self.topics['pending']:
            # Reset when all topics used
            self.topics['pending'] = self.topics['completed']
            self.topics['completed'] = []
            
        topic = random.choice(self.topics['pending'])
        self.topics['pending'].remove(topic)
        self.topics['completed'].append(topic)
        self.save_topics(self.topics)
        return topic
        
    def save_topics(self, data):
        with open(self.topics_file, 'w') as f:
            json.dump(data, f)

def generate_short_form(self, topic: str) -> str:
    content = self.ai_engine.generate_content("tweet", topic)
    filename = f"tweet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Tweet saved to {filename}")
    return content

def main():
    ai_engine = AIContentEngine()
    newsletter_copilot = NewsletterCopilot(ai_engine)
    content_copilot = ContentCopilot(ai_engine)
    topic_manager = TopicManager()
    
    while True:
        topic = topic_manager.get_random_topic()
        newsletter = newsletter_copilot.create_newsletter(topic, schedule_time="09:50")
        tweet = content_copilot.generate_short_form(topic)
        schedule.run_pending()
        time.sleep(86400)
        
if __name__ == "__main__":
    main()
