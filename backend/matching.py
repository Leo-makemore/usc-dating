"""
Matching system: Calculate compatibility scores between users.
Supports basic matching and optional AI-powered matching using OpenAI embeddings.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models import User, Match
from config import settings

# Optional OpenAI for AI matching
openai_client = None
if settings.OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    except ImportError:
        pass


def calculate_basic_match_score(user1: User, user2: User) -> float:
    """
    Calculate basic match score based on shared interests, school, and year.
    
    Args:
        user1: First user
        user2: Second user
        
    Returns:
        Match score between 0.0 and 1.0
    """
    score = 0.0
    
    # School match (40% weight)
    if user1.school == user2.school:
        score += 0.4
    
    # Year match (20% weight)
    if user1.year == user2.year:
        score += 0.2
    
    # Interests match (40% weight)
    if user1.interests and user2.interests:
        user1_interests = set(user1.interests)
        user2_interests = set(user2.interests)
        
        if user1_interests and user2_interests:
            common_interests = user1_interests.intersection(user2_interests)
            total_interests = user1_interests.union(user2_interests)
            
            if total_interests:
                interest_score = len(common_interests) / len(total_interests)
                score += interest_score * 0.4
    
    return min(score, 1.0)  # Cap at 1.0


async def calculate_ai_match_score(user1: User, user2: User) -> Optional[float]:
    """
    Calculate AI-powered match score using OpenAI embeddings.
    Requires OPENAI_API_KEY to be set.
    
    Args:
        user1: First user
        user2: Second user
        
    Returns:
        Match score between 0.0 and 1.0, or None if OpenAI is not configured
    """
    if not openai_client:
        return None
    
    try:
        # Create embeddings for user profiles
        user1_text = f"{user1.name}, {user1.school}, {user1.year}, Interests: {', '.join(user1.interests or [])}"
        user2_text = f"{user2.name}, {user2.school}, {user2.year}, Interests: {', '.join(user2.interests or [])}"
        
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=[user1_text, user2_text]
        )
        
        embedding1 = response.data[0].embedding
        embedding2 = response.data[1].embedding
        
        # Calculate cosine similarity
        import numpy as np
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        similarity = dot_product / (norm1 * norm2)
        
        # Normalize to 0-1 range (cosine similarity is already -1 to 1, but typically 0 to 1)
        return max(0.0, min(1.0, (similarity + 1) / 2))
        
    except Exception as e:
        print(f"[MATCHING] Error calculating AI match score: {e}")
        return None


def get_recommended_matches(db: Session, user_id: int, limit: int = 10, use_ai: bool = False) -> List[dict]:
    """
    Get recommended matches for a user.
    
    Args:
        db: Database session
        user_id: ID of the user to get matches for
        limit: Maximum number of matches to return
        use_ai: Whether to use AI matching (requires OpenAI API key)
        
    Returns:
        List of recommended users with match scores
    """
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        return []
    
    # Get all other verified users
    other_users = db.query(User).filter(
        User.id != user_id,
        User.is_verified == True
    ).all()
    
    matches = []
    
    for other_user in other_users:
        # Calculate match score
        if use_ai:
            # For AI matching, we'd need async support - using basic for now
            score = calculate_basic_match_score(current_user, other_user)
        else:
            score = calculate_basic_match_score(current_user, other_user)
        
        matches.append({
            "user": other_user,
            "score": score
        })
    
    # Sort by score (highest first) and limit results
    matches.sort(key=lambda x: x["score"], reverse=True)
    matches = matches[:limit]
    
    # Format response
    result = []
    for match in matches:
        user = match["user"]
        result.append({
            "id": user.id,
            "name": user.name,
            "school": user.school,
            "year": user.year,
            "interests": user.interests or [],
            "avatar_url": user.avatar_url,
            "match_score": match["score"]
        })
    
    return result

