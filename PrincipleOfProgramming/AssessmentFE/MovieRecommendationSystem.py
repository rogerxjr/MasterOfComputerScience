class Movie:
    """Class representing a movie in the system."""
    def __init__(self, movie_id, title, genre="Unknown", year=0):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.year = year
        self.ratings = []  # List to store all ratings
        self.views = 0     # Counter for total views

    def add_rating(self, score):
        """Adds a rating to the movie (1 to 5)."""
        if 1 <= score <= 5:
            self.ratings.append(score)

    def add_view(self):
        """Increments the view count of the movie."""
        self.views += 1

    def get_average_rating(self):
        """Calculates and returns the average rating of the movie."""
        if not self.ratings:
            return 0.0
        return sum(self.ratings) / len(self.ratings)

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.genre} | Avg Rating: {self.get_average_rating():.1f} | Views: {self.views}"


class User:
    """Class representing a user in the system."""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.watch_history = []  # List of watched Movie objects

    def watch_movie(self, movie):
        """Simulates a user watching a movie and updates the movie's view count."""
        if movie not in self.watch_history:
            self.watch_history.append(movie)
        movie.add_view()

    def rate_movie(self, movie, score):
        """Simulates a user rating a movie."""
        movie.add_rating(score)

    def get_favorite_genre(self):
        """Identifies the user's favorite genre based on their watch history."""
        if not self.watch_history:
            return None
        
        # Count the frequency of each genre in watch history
        genre_counts = {}
        for movie in self.watch_history:
            genre_counts[movie.genre] = genre_counts.get(movie.genre, 0) + 1
            
        # Return the genre with the highest count
        return max(genre_counts, key=genre_counts.get)


class RecommendationSystem:
    """Main system class to manage movies, users, and generate insights."""
    def __init__(self):
        self.movie_database = []
        self.user_database = []

    def add_movie(self, movie):
        self.movie_database.append(movie)

    def remove_movie(self, movie_id):
        """Removes a movie from the database by its ID."""
        self.movie_database = [m for m in self.movie_database if m.movie_id != movie_id]

    def edit_movie(self, movie_id, new_title, new_genre, new_year):
        """Edits an existing movie's details."""
        for movie in self.movie_database:
            if movie.movie_id == movie_id:
                movie.title = new_title
                movie.genre = new_genre
                movie.year = new_year
                return True 
        return False 


    def register_user(self, user):
        self.user_database.append(user)

    # --- Section A (b): Recommendation Logic ---
    def generate_recommendations(self, user, top_n=3):
        """
        Generates movie recommendations based on matching genres (content-based)
        and highest average ratings.
        """
        fav_genre = user.get_favorite_genre()
        if not fav_genre:
            return [] # No history, no recommendation

        # 1. Filter movies by user's favorite genre
        candidates = [m for m in self.movie_database 
                      if m.genre == fav_genre]

        # 2. Sort candidates by highest average rating (Descending order)
        candidates.sort(key=lambda x: x.get_average_rating(), reverse=True)

        return candidates[:top_n]

    # --- Section A (c): Data Insights ---
    def get_most_popular_genre(self):
        """Identifies the most popular genre across the entire platform based on total views."""
        genre_views = {}
        for movie in self.movie_database:
            genre_views[movie.genre] = genre_views.get(movie.genre, 0) + movie.views
            
        if not genre_views:
            return None
        return max(genre_views, key=genre_views.get)

    def get_top_trending_movies(self, top_n=3):
        """Returns the top N trending movies based on total views."""
        # Sort all movies by views in descending order
        sorted_movies = sorted(self.movie_database, key=lambda x: x.views, reverse=True)
        return sorted_movies[:top_n]

    def get_user_watch_counts(self):
        """Returns a dictionary mapping user names to their total watch counts."""
        return {user.name: len(user.watch_history) for user in self.user_database}


# ==========================================
# TEST & DEMONSTRATION (For your report)
# ==========================================
if __name__ == "__main__":
    # 1. Initialize System
    mrs = RecommendationSystem()

    # 2. Create Movies
    m1 = Movie("M1", "Inception", "Sci-Fi", 2010)
    m2 = Movie("M2", "Interstellar", "Sci-Fi", 2014)
    m3 = Movie("M3", "The Matrix", "Sci-Fi", 1999)
    m4 = Movie("M4", "The Dark Knight", "Action", 2008)
    m5 = Movie("M5", "Avengers", "Action", 2008)

    for m in [m1, m2, m3, m4, m5]:
        mrs.add_movie(m)

    # 3. Create User
    u1 = User("U1", "Alice")
    mrs.register_user(u1)

    # --- DEMO: Show how system updates (Section A - c) ---
    print("--- Initial State ---")
    u1.watch_movie(m1)
    u1.rate_movie(m1, 5)
    
    # Give some initial ratings to other movies so they have an average
    m2.add_rating(4)
    m3.add_rating(3)

    print(f"Alice's favorite genre: {u1.get_favorite_genre()}")
    print("Recommendations for Alice:")
    for rec in mrs.generate_recommendations(u1):
        print(f" - {rec}")

    print("\n--- State After New Watch/Rating Event ---")
    # Alice watches and rates another Sci-Fi movie highly, 
    # but let's say a new rating comes in for m3 making it higher than m2
    u1.watch_movie(m4) # Watches an action movie
    m3.add_rating(5)   # Matrix gets a 5-star rating from someone else
    m3.add_rating(5)

    print("New Recommendations for Alice (Updated dynamically):")
    # The Matrix (m3) should now jump ahead of Interstellar (m2) because its average rating increased
    for rec in mrs.generate_recommendations(u1):
        print(f" - {rec}")

    print("\n--- Platform Insights ---")
    print(f"Most Popular Genre: {mrs.get_most_popular_genre()}")
    print("Top 3 Trending Movies:")
    for tm in mrs.get_top_trending_movies():
        print(f" - {tm.title} (Views: {tm.views})")
    print(f"User Watch Counts: {mrs.get_user_watch_counts()}")
