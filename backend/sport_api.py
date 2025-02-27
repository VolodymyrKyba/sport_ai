import json

def beautify_text(text):
    """
    Enhances the text formatting and readability by adding emojis, bold sections, and structured headlines.
    :param text: The original text as a string.
    :return: The beautified text.
    """
    replacements = {
        "Last games(score)": "🏆 Last Games (Score)",
        "Current standings": "📊 Current Standings",
        "Latest News": "📰 Latest News",
        "Talking Points": "💬 Talking Points",
        "Fun Facts": "🎉 Fun Facts",
        "Celebrity Gossip": "🌟 Celebrity Gossip",
        "Workplace Drama": "🎭 Workplace Drama",
        "Funny Metaphors": "😂 Funny Metaphors"
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

# Example usage
general_text = """
Here's the information about FC Barcelona in the requested format:

- **Last games(score)**: FC Barcelona's recent performance includes a 2-1 win against Valencia, a 1-0 loss to Manchester United, and a 3-0 win against Sevilla.

- **Current standings**: As of now, FC Barcelona is ranked 2nd in La Liga with 47 points, just behind Real Madrid.

- **Latest News**: FC Barcelona recently announced the signing of a new sponsorship deal, and the team is gearing up for the upcoming El Clásico match against Real Madrid.

- **Talking Points**: The team's recent performance has sparked discussions about the effectiveness of their new formation and the role of their star player, Robert Lewandowski.

- **Fun Facts**: FC Barcelona is one of the most successful and popular sports teams in the world, with a massive following and a rich history that dates back to 1899. The team's iconic stadium, Camp Nou, has a seating capacity of over 99,000.

- **Celebrity Gossip**: FC Barcelona's star player, Ansu Fati, has been spotted attending a high-profile fashion event in Barcelona, while teammate Pedri has been linked to a popular Spanish actress.

- **Workplace Drama**: There have been reports of tension between FC Barcelona's coach and the team's management over transfer decisions and player selections.

- **Funny Metaphors**: FC Barcelona's midfield has been described as a "well-oiled machine," while their defense has been likened to a "leaky faucet" that needs fixing. The team's star striker, Robert Lewandowski, has been called a "goal-scoring machine" with a "license to kill" opponents' chances.
"""

beautified_text = beautify_text(general_text)
print(beautified_text)