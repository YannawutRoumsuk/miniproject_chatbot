# README
## Overview
This project is a LINE Messaging API chatbot that recommends music, movies, or travel destinations based on user input. The bot interacts with users in a step-by-step conversational manner, maintaining user state between messages to guide them through choosing categories, countries, and subcategories (for music and movies) or seasons and countries (for travel).

## Fetures
*Stateful Conversation: Remembers user choices (category, country, season) through each step.
*Multiple Categories: Users can choose between music, movies, or travel recommendations.
*Nested Subcategories:
---*Music: Choose country (Thai/Chinese), then select music genre (e.g., top hits, tpop, etc.).
---*Movie: Choose country (Thai/Chinese), then select movie type (animation, series, movie).
---*Travel: Choose country (Thai/Chinese), then select season (summer, rainy, winter), and get place and menu recommendations.
*Flexible Continuation: After receiving recommendations, users can continue to choose other subcategories without restarting.


