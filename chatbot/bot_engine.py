"""
Movie Recommendation Chatbot Engine
Provides natural language conversation for movie recommendations
"""

import re
import random
from typing import Dict, List, Optional, Tuple
from difflib import get_close_matches


class MovieChatbot:
    """AI-powered movie recommendation chatbot"""
    
    def __init__(self, recommender=None):
        """Initialize the chatbot with a recommender system"""
        self.recommender = recommender
        self.conversation_state = {}
        
        # Greeting patterns
        self.greetings = [
            "Hello! I'm your movie recommendation assistant. How can I help you today?",
            "Hi there! Looking for some great movies to watch? I'm here to help!",
            "Welcome! I'd love to help you discover your next favorite movie!",
            "Hey! Ready to find some amazing films? Just ask me anything about movies!"
        ]
        
        # Genre categories
        self.genres = {
            'action': ['action', 'adventure', 'thriller'],
            'comedy': ['comedy', 'romantic comedy', 'satire'],
            'drama': ['drama', 'biographical', 'historical'],
            'scifi': ['science fiction', 'sci-fi', 'futuristic', 'space'],
            'horror': ['horror', 'thriller', 'suspense'],
            'romance': ['romance', 'romantic', 'love story'],
            'family': ['family', 'animation', 'children', 'kids'],
            'documentary': ['documentary', 'educational', 'real'],
        }
        
        # Mood-based recommendations
        self.mood_movies = {
            'happy': ['comedy', 'musical', 'feel-good'],
            'sad': ['drama', 'emotional', 'touching'],
            'excited': ['action', 'adventure', 'thriller'],
            'relaxed': ['comedy', 'romance', 'light'],
            'thoughtful': ['drama', 'scifi', 'mystery'],
        }
    
    def process_message(self, message: str, user_id: str = "default") -> Dict:
        """Process user message and return chatbot response"""
        message = message.lower().strip()
        
        # Initialize user state if needed
        if user_id not in self.conversation_state:
            self.conversation_state[user_id] = {
                'stage': 'idle',
                'preferences': {},
                'last_query': None
            }
        
        user_state = self.conversation_state[user_id]
        
        # Check for greetings
        if self._is_greeting(message):
            return {
                'response': random.choice(self.greetings),
                'suggestions': self._get_quick_suggestions(),
                'stage': 'idle'
            }
        
        # Check for genre requests
        genre_match = self._extract_genre(message)
        if genre_match:
            return self._handle_genre_request(genre_match, user_state)
        
        # Check for mood-based requests
        mood_match = self._extract_mood(message)
        if mood_match:
            return self._handle_mood_request(mood_match, user_state)
        
        # Check for specific movie requests
        if self._is_movie_request(message):
            return self._handle_movie_request(message, user_state)
        
        # Check for "like" or "similar to" requests
        if self._is_similarity_request(message):
            return self._handle_similarity_request(message, user_state)
        
        # Check for year/decade requests
        year_match = self._extract_year(message)
        if year_match:
            return self._handle_year_request(year_match, user_state)
        
        # Check for rating requests
        if self._is_rating_request(message):
            return self._handle_rating_request(message, user_state)
        
        # Check for help
        if message in ['help', 'what can you do', 'how does this work']:
            return self._get_help_message()
        
        # Default response
        return {
            'response': "I'm here to help you find great movies! You can ask me for:\n"
                       "• Recommendations by genre (e.g., 'action movies')\n"
                       "• Movies based on your mood (e.g., 'happy movies')\n"
                       "• Suggestions similar to a movie you like\n"
                       "• Movies from a specific year or decade\n"
                       "• Highly rated films\n"
                       "• Or just tell me what you're in the mood for!",
            'suggestions': self._get_quick_suggestions(),
            'stage': 'idle'
        }
    
    def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(message.startswith(g) for g in greetings)
    
    def _extract_genre(self, message: str) -> Optional[str]:
        """Extract genre from message"""
        for genre, keywords in self.genres.items():
            if any(keyword in message for keyword in keywords):
                return genre
        return None
    
    def _extract_mood(self, message: str) -> Optional[str]:
        """Extract mood from message"""
        moods = ['happy', 'sad', 'excited', 'relaxed', 'thoughtful', 'bored', 'lonely']
        for mood in moods:
            if mood in message:
                return mood
        return None
    
    def _is_movie_request(self, message: str) -> bool:
        """Check if message is requesting movie recommendations"""
        patterns = [
            r'(recommend|suggest|show|give|find)\s+(me\s+)?(some\s+)?(good\s+)?movies?',
            r'i\s+(want|need|looking for|in the mood for)\s+(some\s+)?movies?',
            r'what\s+should\s+i\s+watch',
            r'movie\s+(night|time|suggestions|ideas)',
            r'something\s+to\s+watch'
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _is_similarity_request(self, message: str) -> bool:
        """Check if message is asking for similar movies"""
        patterns = [
            r'(similar|like)\s+to\s+(the\s+)?(.+)',
            r'movies?\s+like\s+(the\s+)?(.+)',
            r'if\s+i\s+liked\s+(the\s+)?(.+)',
            r'recommend\s+something\s+like\s+(the\s+)?(.+)'
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _extract_year(self, message: str) -> Optional[Tuple[int, int]]:
        """Extract year or decade from message"""
        # Look for specific years (1900-2099)
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', message)
        if year_match:
            year = int(year_match.group(1))
            return (year, year)
        
        # Look for decades
        decade_match = re.search(r'\b(19\d{2}|20\d{2})s\b', message)
        if decade_match:
            decade = int(decade_match.group(1))
            return (decade, decade + 9)
        
        return None
    
    def _is_rating_request(self, message: str) -> bool:
        """Check if message is asking for highly rated movies"""
        patterns = [
            r'(best|top|greatest|highest\s+rated|oscar|award\s+winning)\s+movies?',
            r'movies?\s+with\s+(high|great|excellent)\s+ratings?',
            r'(9|8)\s*\+\s*(rating|score)',
            r'critically\s+acclaimed'
        ]
        return any(re.search(pattern, message) for pattern in patterns)
    
    def _handle_genre_request(self, genre: str, user_state: Dict) -> Dict:
        """Handle genre-based recommendations"""
        if not self.recommender:
            return self._get_fallback_response()
        
        # Search for movies in this genre
        all_movies = list(self.recommender.title_to_idx.keys())
        genre_movies = [m for m in all_movies if genre in m.lower()]
        
        if genre_movies:
            # Get recommendations for a random movie from this genre
            sample_movie = random.choice(genre_movies[:10])  # Limit search
            result = self.recommender.get_recommendations(sample_movie, n=8)
            
            if 'recommendations' in result:
                response = f"Here are some great {genre.replace('_', ' ')} movies you might enjoy:\n\n"
                for i, movie in enumerate(result['recommendations'][:5], 1):
                    response += f"{i}. **{movie['title']}** ({movie['rating']})\n"
                
                response += "\nWould you like more details about any of these?"
                return {
                    'response': response,
                    'movies': result['recommendations'][:5],
                    'stage': 'genre_results',
                    'genre': genre
                }
        
        return {
            'response': f"I'd love to help you find some {genre.replace('_', ' ')} movies! Let me check what's available...",
            'stage': 'searching'
        }
    
    def _handle_mood_request(self, mood: str, user_state: Dict) -> Dict:
        """Handle mood-based recommendations"""
        if not self.recommender:
            return self._get_fallback_response()
        
        mood_genres = self.mood_movies.get(mood, [])
        
        response = f"Feeling {mood}? I've got some perfect movie suggestions for that mood!\n\n"
        
        # Find movies that match the mood
        all_movies = list(self.recommender.title_to_idx.keys())
        mood_movies = []
        
        for genre in mood_genres:
            matching = [m for m in all_movies if genre in m.lower()][:3]
            mood_movies.extend(matching)
        
        if mood_movies:
            # Get recommendations for a few movies
            sample_movie = random.choice(mood_movies)
            result = self.recommender.get_recommendations(sample_movie, n=6)
            
            if 'recommendations' in result:
                response += f"Based on your {mood} mood, you might enjoy:\n\n"
                for i, movie in enumerate(result['recommendations'][:4], 1):
                    response += f"{i}. **{movie['title']}** - {movie['genres']}\n"
                
                return {
                    'response': response,
                    'movies': result['recommendations'][:4],
                    'stage': 'mood_results',
                    'mood': mood
                }
        
        return {
            'response': f"When you're feeling {mood}, I'd recommend something uplifting and engaging. Let me find the perfect match!",
            'stage': 'searching'
        }
    
    def _handle_movie_request(self, message: str, user_state: Dict) -> Dict:
        """Handle general movie requests"""
        if not self.recommender:
            return self._get_fallback_response()
        
        # Get random recommendations
        all_movies = list(self.recommender.title_to_idx.keys())
        
        # Pick a random starting movie
        random_movie = random.choice(all_movies)
        result = self.recommender.get_recommendations(random_movie, n=8)
        
        if 'recommendations' in result:
            response = "Here are some fantastic movies I think you'll love:\n\n"
            for i, movie in enumerate(result['recommendations'][:6], 1):
                response += f"{i}. **{movie['title']}** ({movie['rating']})\n"
            
            response += "\nWant more details about any of these, or shall I find something different?"
            
            return {
                'response': response,
                'movies': result['recommendations'][:6],
                'stage': 'general_results'
            }
        
        return {
            'response': "Let me find some great movie suggestions for you!",
            'stage': 'searching'
        }
    
    def _handle_similarity_request(self, message: str, user_state: Dict) -> Dict:
        """Handle 'similar to' requests"""
        if not self.recommender:
            return self._get_fallback_response()
        
        # Extract movie name from message
        patterns = [
            r'(similar|like)\s+to\s+(?:the\s+)?(.+?)(?:\s*$|\s+\w+)',
            r'movies?\s+like\s+(?:the\s+)?(.+?)(?:\s*$|\s+\w+)',
            r'if\s+i\s+liked\s+(?:the\s+)?(.+?)(?:\s*$|\s+\w+)',
            r'recommend\s+something\s+like\s+(?:the\s+)?(.+?)(?:\s*$|\s+\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                movie_title = match.group(2) if len(match.groups()) > 1 else match.group(1)
                movie_title = movie_title.strip()
                
                # Try to find the movie
                matched_title = self.recommender.find_movie(movie_title)
                
                if matched_title:
                    result = self.recommender.get_recommendations(matched_title, n=8)
                    
                    if 'recommendations' in result:
                        response = f"If you liked **{matched_title}**, you'll probably enjoy these:\n\n"
                        for i, movie in enumerate(result['recommendations'][:5], 1):
                            response += f"{i}. **{movie['title']}** ({movie['rating']})\n"
                        
                        return {
                            'response': response,
                            'movies': result['recommendations'][:5],
                            'stage': 'similarity_results',
                            'source_movie': matched_title
                        }
                else:
                    # Try fuzzy matching
                    suggestions = self.recommender.search_movies(movie_title, 5)
                    if suggestions:
                        response = f"I couldn't find '{movie_title}' exactly, but here are some similar titles:\n"
                        response += "\n".join(f"• {s}" for s in suggestions)
                        response += "\n\nDid you mean one of these?"
                        
                        return {
                            'response': response,
                            'suggestions': suggestions,
                            'stage': 'clarification'
                        }
        
        return {
            'response': "Tell me a movie you've enjoyed, and I'll find similar ones for you!",
            'stage': 'idle'
        }
    
    def _handle_year_request(self, year_range: Tuple[int, int], user_state: Dict) -> Dict:
        """Handle year/decade-based requests"""
        if not self.recommender:
            return self._get_fallback_response()
        
        start_year, end_year = year_range
        
        if start_year == end_year:
            time_period = f"{start_year}"
        else:
            time_period = f"{start_year}s"
        
        response = f"Looking for great movies from {time_period}? Here are some excellent choices:\n\n"
        
        # For now, provide general recommendations with a note about the era
        all_movies = list(self.recommender.title_to_idx.keys())
        random_movie = random.choice(all_movies)
        result = self.recommender.get_recommendations(random_movie, n=6)
        
        if 'recommendations' in result:
            for i, movie in enumerate(result['recommendations'][:4], 1):
                response += f"{i}. **{movie['title']}**\n"
            
            response += f"\nThese are some fantastic films! While I can't filter by exact year yet, "
            response += f"these are highly recommended movies that might include some from {time_period}."
            
            return {
                'response': response,
                'movies': result['recommendations'][:4],
                'stage': 'year_results',
                'year_range': year_range
            }
        
        return {
            'response': f"Movies from {time_period} can be amazing! Let me find some great recommendations for you.",
            'stage': 'searching'
        }
    
    def _handle_rating_request(self, message: str, user_state: Dict) -> Dict:
        """Handle highly rated movie requests"""
        if not self.recommender:
            return self._get_fallback_response()
        
        response = "Looking for the best of the best? Here are some critically acclaimed movies:\n\n"
        
        # Get recommendations and filter for high ratings
        all_movies = list(self.recommender.title_to_idx.keys())
        random_movie = random.choice(all_movies)
        result = self.recommender.get_recommendations(random_movie, n=10)
        
        if 'recommendations' in result:
            # Filter for highly rated movies (8.0+)
            high_rated = [m for m in result['recommendations'] if float(m['rating'].split('/')[0]) >= 8.0]
            
            if high_rated:
                for i, movie in enumerate(high_rated[:5], 1):
                    response += f"{i}. **{movie['title']}** - {movie['rating']}\n"
                
                response += "\nThese movies have exceptional ratings and are definitely worth watching!"
                
                return {
                    'response': response,
                    'movies': high_rated[:5],
                    'stage': 'rating_results'
                }
        
        return {
            'response': "I'll find you some top-rated masterpieces!",
            'stage': 'searching'
        }
    
    def _get_help_message(self) -> Dict:
        """Return help message"""
        return {
            'response': "🎬 **Movie Chatbot Help**\n\n"
                       "I can help you discover great movies in many ways:\n\n"
                       "📂 **By Genre**: 'action movies', 'comedy films', 'sci-fi recommendations'\n"
                       "😊 **By Mood**: 'happy movies', 'movies for when I'm sad', 'exciting films'\n"
                       "🎯 **Similar Movies**: 'movies like Inception', 'similar to The Matrix'\n"
                       "📅 **By Year**: 'movies from 1990s', 'films from 2020'\n"
                       "⭐ **By Rating**: 'best movies', 'top rated films', 'oscar winners'\n"
                       "🎲 **Random**: 'recommend me something', 'what should I watch'\n\n"
                       "Just type naturally and I'll understand what you're looking for!",
            'suggestions': [
                "Action movies",
                "Movies like The Matrix",
                "Happy movies",
                "Best rated films",
                "90s movies"
            ],
            'stage': 'help'
        }
    
    def _get_quick_suggestions(self) -> List[str]:
        """Get quick suggestion buttons"""
        return [
            "Action movies",
            "Comedy films",
            "Movies like Inception",
            "Happy movies",
            "Best rated films",
            "90s classics"
        ]
    
    def _get_fallback_response(self) -> Dict:
        """Return fallback response when recommender is not available"""
        return {
            'response': "I'd love to help you find movies, but the recommendation system is still loading. "
                       "Please wait a moment and try again!",
            'stage': 'error'
        }
    
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history for a user (for future implementation)"""
        # This would store conversation history in a database
        return []
    
    def clear_conversation(self, user_id: str):
        """Clear conversation state for a user"""
        if user_id in self.conversation_state:
            del self.conversation_state[user_id]