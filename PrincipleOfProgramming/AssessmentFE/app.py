import streamlit as st
import pandas as pd
import random
# Ensure this import matches your local filename exactly
from MovieRecommendationSystem import Movie, User, RecommendationSystem

# ==========================================
# 1. System Initialization (Session State & 1000 Movies)
# ==========================================
if 'system' not in st.session_state:
    system = RecommendationSystem()
    
    # Pre-load some classic movies
    classic_movies = [
        Movie("M1", "Inception", "Sci-Fi", 2010),
        Movie("M2", "Interstellar", "Sci-Fi", 2014),
        Movie("M3", "The Dark Knight", "Action", 2008),
        Movie("M4", "Toy Story", "Animation", 1995)
    ]
    for m in classic_movies:
        system.add_movie(m)
        
    #  Batch generate 1000 simulated movies to increase database realism
    adjectives = ["Dark", "Lost", "Hidden", "Secret", "Last", "First", "Golden", "Silent", "Quantum", "Cyber", "Magic"]
    nouns = ["City", "World", "Star", "Knight", "Dream", "Shadow", "Journey", "Hero", "Legend", "Chronicle", "Illusion"]
    genres = ["Action", "Sci-Fi", "Comedy", "Drama", "Horror", "Romance", "Thriller", "Fantasy", "Animation"]
    
    for i in range(5, 1005): # Generate M5 to M1004
        title = f"The {random.choice(adjectives)} {random.choice(nouns)}"
        genre = random.choice(genres)
        year = random.randint(1980, 2024)
        new_movie = Movie(f"M{i}", title, genre, year)
        
        # Randomly add views and ratings to populate the analytics dashboard
        new_movie.views = random.randint(0, 500)
        for _ in range(random.randint(0, 10)):
            new_movie.ratings.append(random.randint(3, 5))
        system.add_movie(new_movie)
        
    # Pre-load basic users
    u1 = User("U1", "Alice")
    u2 = User("U2", "Bob")
    system.register_user(u1)
    system.register_user(u2)
    
    random_names = [
        "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia", 
        "Kevin", "Luna", "Mason", "Nora", "Oliver", "Penelope", "Quinn", "Riley", 
        "Samuel", "Tara", "Ulysses", "Victoria"
    ]
    
    for i, name in enumerate(random_names, start=3): # Start ID from U3
        new_user = User(f"U{i}", name)
        system.register_user(new_user)
        
        # Simulate watch history to populate the Engagement Analytics dashboard
        # Randomly pick 5 to 25 movies for each user to watch and rate
        movies_to_watch = random.sample(system.movie_database, random.randint(5, 25))
        for m in movies_to_watch:
            new_user.watch_movie(m)
            new_user.rate_movie(m, random.randint(1, 5)) # Random rating 1-5
            
    st.session_state.system = system


sys = st.session_state.system

# ==========================================
# 2. Sidebar Navigation & Layout
# ==========================================
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.sidebar.title("Navigation")
view_mode = st.sidebar.radio("Select View:", ["User Dashboard", "Admin Console"])

# ==========================================
# 3. View 1: User Dashboard
# ==========================================
if view_mode == "User Dashboard":
    st.title("🎬 User Dashboard")
    
    # Select User
    user_names = [u.name for u in sys.user_database]
    selected_name = st.selectbox("Login as:", user_names)
    current_user = next(u for u in sys.user_database if u.name == selected_name)
    st.write(f"### Welcome back, {current_user.name}!")
    
    # --- : Flexible Multi-criteria Search (Title, Genre, Year) ---
    st.divider()
    st.subheader("🔍 Advanced Movie Search")
    st.write("Assignment Requirement: Please specify at least two criteria to search.")
    # --- Step 1: Dynamically extract unique genres and years from the database ---
    # Use a Set comprehension to get unique genres, then convert to a sorted List
    unique_genres = sorted(list(set([movie.genre for movie in sys.movie_database])))

    # Use a Set comprehension to get unique years, convert to string, and sort descending
    unique_years = sorted(list(set([str(movie.year) for movie in sys.movie_database])), reverse=True)

    # --- Step 2: Prepend the default "All" options to the lists ---
    genre_options = ["All Genres"] + unique_genres
    year_options = ["All Years"] + unique_years

    # --- Step 3: Render the UI columns ---
    col1, col2, col3 = st.columns(3)

    with col1:
        # Text input for partial title search
        title_query = st.text_input("1. Movie Title (Partial):", key="adv_search_title")
        
    with col2:
        # Selectbox populated with dynamic genre options
        genre_query = st.selectbox("2. Select Genre:", genre_options, key="adv_search_genre")
        
    with col3:
        # Selectbox populated with dynamic year options
        year_query = st.selectbox("3. Select Year:", year_options, key="adv_search_year")

    # === 2. search button and logic ===
    if st.button("Search Movies", key="adv_search_btn"):
        
        # check logic 
        if not title_query and genre_query == "All Genres" and year_query == "All Years":
            st.warning("⚠️ Please provide at least ONE search criterion.")
        else:
            # Dynamic filtration pipeline
            filtered_movies = sys.movie_database  # Obtain basic data
            
            if title_query:
                filtered_movies = [m for m in filtered_movies if title_query.lower() in m.title.lower()]
                
            if genre_query != "All Genres":
                filtered_movies = [m for m in filtered_movies if m.genre == genre_query]
                
            if year_query != "All Years":
                filtered_movies = [m for m in filtered_movies if str(m.year) == year_query]
                
            # display results
            if len(filtered_movies) > 0:
                st.success(f"✅ Found {len(filtered_movies)} movies!")
                for movie in filtered_movies:
                    st.write(f"- **{movie.title}** ({movie.year}) - {movie.genre} | ⭐ rate: {movie.get_average_rating():.1f}")
            else:
                st.info("No movies found matching your criteria.")


    st.divider()
        
    # --- NEW: Comprehensive User Dashboard (Tabs) ---
    st.subheader("📊 Your Personalized Dashboard")
    
    tab_rec, tab_trend, tab_hist, tab_vis = st.tabs([
        "🎯 Recommendations", 
        "🔥 Trending", 
        "📜 Watch History", 
        "📈 Data Insights"
    ])
    
    # Requirement I: Recommendations
    with tab_rec:
        fav_genre = current_user.get_favorite_genre()
        st.info(f"Based on your favorite genre: **{fav_genre if fav_genre else 'Not enough data'}**")
        recs = sys.generate_recommendations(current_user, top_n=5)
        if recs:
            for r in recs:
                st.success(f"**{r.title}** ({r.year}) - {r.genre} | Avg Rating: {r.get_average_rating():.1f}")
        else:
            st.warning("Watch some movies to get personalized recommendations!")

    # Requirement II: Trending & Popular Genres
    with tab_trend:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("**🔥 Top Trending Movies (By Views)**")
            trending_movies = sys.get_top_trending_movies(top_n=5)
            for tm in trending_movies:
                st.write(f"- **{tm.title}** ({tm.views} views)")
        with col_t2:
            st.markdown("**👑 Most Popular Genre Platform-wide**")
            pop_genre = sys.get_most_popular_genre()
            if pop_genre:
                st.success(f"**{pop_genre}**")

    # Requirement III: Watch History in Tabular Format
    with tab_hist:
        if current_user.watch_history:
            # Convert list of Movie objects to Pandas DataFrame
            history_data = [{
                "Movie ID": m.movie_id,
                "Title": m.title, 
                "Genre": m.genre, 
                "Year": m.year,
                "Platform Avg Rating": round(m.get_average_rating(), 1)
            } for m in reversed(current_user.watch_history)] # Show latest first
            
            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, use_container_width=True)
        else:
            st.info("Your watch history is empty. Go watch some movies!")

    # Requirement IV: Data Visualizations
    with tab_vis:
        if current_user.watch_history:
            # Count genres watched by the user
            genre_counts = {}
            for m in current_user.watch_history:
                genre_counts[m.genre] = genre_counts.get(m.genre, 0) + 1
                
            # Create DataFrame and set index for Streamlit bar chart
            df_chart = pd.DataFrame(
                list(genre_counts.items()), 
                columns=["Genre", "Movies Watched"]
            ).set_index("Genre")
            
            st.markdown("**Movies Watched per Genre**")
            st.bar_chart(df_chart)
        else:
            st.info("Watch some movies to see your insights chart!")

    
    # ---  Rating system UI  (Button clicks) ---
    st.subheader("🍿 Watch & Rate a Movie")
    available_movies = [m for m in sys.movie_database]
    
    # Streamlit's selectbox supports keyboard typing
    movie_options = [f"{m.title} ({m.year}) - {m.movie_id}" for m in available_movies]
    selected_option = st.selectbox("Select a movie to watch:", movie_options)
    
    selected_id = selected_option.split(" - ")[-1]
    selected_movie = next(m for m in available_movies if m.movie_id == selected_id)

    
    # Core optimization: Use radio with horizontal=True to simulate clickable buttons
    st.write("**Select your rating:**")
    rating = st.radio(
        "Rate this movie:", 
        options=[1, 2, 3, 4, 5], 
        index=4, # Default selection is 5 stars
        horizontal=True, # Arrange horizontally to look like a row of buttons
        label_visibility="collapsed" # Hide extra label text for a cleaner UI
    )
    
    if st.button("Watch & Submit Rating", type="primary"):
        current_user.watch_movie(selected_movie)
        current_user.rate_movie(selected_movie, rating)
        st.success(f"You watched '{selected_movie.title}' and rated it {rating} stars!")
        st.rerun() 

# ==========================================
# 4. View 2: Admin Console (Protected)
# ==========================================
elif view_mode == "Admin Console":
    st.sidebar.divider()
    st.sidebar.write("🔒 **Admin Authentication**")
    admin_key = st.sidebar.text_input("Enter Admin Key:", type="password")
    
    # --- [Admin Mod 1]: Improved Authentication Feedback ---
    if not admin_key:
        # If empty, just show an info message
        st.info("ℹ️ Please enter the Admin Key in the sidebar to access this console.")
    elif admin_key != "admin123":
        # If wrong, show an explicit error message
        st.error("❌ Incorrect Admin Key! Access Denied.")
    else:
        # If correct, render the admin console
        st.title("⚙️ System Administrator Console")
        tab1, tab2 = st.tabs(["I. Advanced Data Explorer", "II. Engagement Analytics"])
        
        with tab1:
            st.subheader("📊 Advanced Database Management")
            
            # Convert object database to Pandas DataFrame for advanced manipulation
            raw_data = [{
                "ID": m.movie_id, "Title": m.title, "Genre": m.genre, 
                "Year": m.year, "Views": m.views, "Avg Rating": round(m.get_average_rating(), 1)
            } for m in sys.movie_database]
            df_movies = pd.DataFrame(raw_data)
            
            # ---: Custom Dimensions, Sorting, and Ranges ---
            st.write("**⚙️ Customize Data View**")
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            
            with filter_col1:
                # 1. Custom Dimensions (Select Columns)
                all_columns = df_movies.columns.tolist()
                selected_cols = st.multiselect("1. Select Columns to Display:", all_columns, default=all_columns)
                
            with filter_col2:
                # 2. Custom Sorting
                sort_col = st.selectbox("2. Sort By:", all_columns, index=all_columns.index("ID"))
                sort_order = st.radio("Sort Order:", ["Ascending", "Descending"], horizontal=True)
                
            with filter_col3:
                # 3. Custom Data Range (Year and Rating Sliders)
                min_year, max_year = int(df_movies["Year"].min()), int(df_movies["Year"].max())
                year_range = st.slider("3. Filter by Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))
                
                rating_range = st.slider("Filter by Rating Range:", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1)

            # Apply Range Filters
            filtered_df = df_movies[
                (df_movies["Year"] >= year_range[0]) & (df_movies["Year"] <= year_range[1]) &
                (df_movies["Avg Rating"] >= rating_range[0]) & (df_movies["Avg Rating"] <= rating_range[1])
            ]
            
            # Apply Custom Sorting
            is_ascending = True if sort_order == "Ascending" else False
            filtered_df = filtered_df.sort_values(by=sort_col, ascending=is_ascending)
            
            # Apply Custom Dimensions (Column Selection)
            if selected_cols:
                filtered_df = filtered_df[selected_cols]
            else:
                # Prevent error if user deselects all columns
                filtered_df = pd.DataFrame() 

            # Display the highly customized DataFrame
            st.dataframe(filtered_df, use_container_width=True, height=300)
            st.caption(f"Showing {len(filtered_df)} out of {len(df_movies)} movies based on your filters.")
            
            st.divider()
            
            # --- Database CRUD Operations ---
            col_add, col_edit, col_del = st.columns(3)
            with col_add:
                with st.form("add_form"):
                    st.write("**Add New Movie**")
                    new_id = st.text_input("Movie ID (e.g., M2000)")
                    new_title = st.text_input("Title")
                    new_genre = st.text_input("Genre")
                    new_year = st.number_input("Year", min_value=1900, max_value=2030, value=2024)
                    if st.form_submit_button("Add Movie"):
                        if new_id and new_title:
                            sys.add_movie(Movie(new_id, new_title, new_genre, new_year))
                            st.success("Added successfully!")
                            st.rerun()
                            
            with col_edit:
                with st.form("edit_form"):
                    st.write("**Edit Movie**")
                    edit_id = st.selectbox("Select Movie ID to Edit", [m.movie_id for m in sys.movie_database])
                    edit_title = st.text_input("New Title")
                    edit_genre = st.text_input("New Genre")
                    edit_year = st.number_input("New Year", min_value=1900, max_value=2030, value=2024)
                    if st.form_submit_button("Update Movie"):
                        sys.edit_movie(edit_id, edit_title, edit_genre, edit_year)
                        st.success("Updated successfully!")
                        st.rerun()
                        
            with col_del:
                with st.form("delete_form"):
                    st.write("**Remove Movie**")
                    del_id = st.selectbox("Select Movie ID to Remove", [m.movie_id for m in sys.movie_database])
                    if st.form_submit_button("Delete Movie"):
                        sys.remove_movie(del_id)
                        st.error("Deleted successfully!")
                        st.rerun()

        with tab2:
            st.subheader("📈 Platform Engagement Analytics")
            
            # Keep top core metrics (KPIs)
            pop_genre = sys.get_most_popular_genre()
            st.metric(label="🔥 Most Popular Genre (by views)", value=pop_genre if pop_genre else "N/A")
            
            st.divider()
            st.write("**⚙️ Customize Analytics Chart**")
            
            # --- Step 1: Select Analysis Target and Metric ---
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                analysis_target = st.selectbox("1. Select Analysis Target:", ["Movies", "Users"])
            with col_t2:
                if analysis_target == "Movies":
                    metric_choice = st.selectbox("2. Select Metric:", ["Views", "Average Rating"])
                else:
                    metric_choice = st.selectbox("2. Select Metric:", ["Watch Count"])
                    
            # --- Step 2: Extract Base Data ---
            # We must fetch the data first to determine the min and max values for the range slider
            if analysis_target == "Movies":
                movie_data = [{
                    "Movie": m.title, 
                    "Views": m.views, 
                    "Average Rating": round(m.get_average_rating(), 1)
                } for m in sys.movie_database]
                df_base = pd.DataFrame(movie_data)
            else:
                user_counts = sys.get_user_watch_counts()
                if user_counts:
                    df_base = pd.DataFrame(list(user_counts.items()), columns=["User", "Watch Count"])
                else:
                    df_base = pd.DataFrame()

            # --- Step 3: Dynamically Generate Filters (Transform & Visualize) ---
            if not df_base.empty:
                col_f1, col_f2, col_f3 = st.columns(3)
                
                with col_f1:
                    # Dynamically calculate the min and max values of the current metric
                    min_val = float(df_base[metric_choice].min())
                    max_val = float(df_base[metric_choice].max())
                    
                    # Smart step size: 0.1 for ratings, 1.0 for views/counts
                    step_val = 0.1 if metric_choice == "Average Rating" else 1.0
                    
                    if min_val < max_val:
                        filter_range = st.slider(
                            f"3. Filter by {metric_choice}:", 
                            min_value=min_val, max_value=max_val, value=(min_val, max_val), step=step_val
                        )
                    else:
                        # Edge case: All data points have the exact same metric value
                        st.info(f"All {metric_choice} values are {min_val}")
                        filter_range = (min_val, max_val)
                        
                with col_f2:
                    top_n = st.slider("4. Number of Items (Top N):", min_value=1, max_value=20, value=5)
                    
                with col_f3:
                    sort_order_tab2 = st.radio("5. Sort Order:", ["Descending (Highest first)", "Ascending (Lowest first)"])
                    is_desc = True if "Descending" in sort_order_tab2 else False

                # === Core Data Pipeline ===
                # 1. Filter Range
                df_plot = df_base[(df_base[metric_choice] >= filter_range[0]) & (df_base[metric_choice] <= filter_range[1])]
                
                # 2. Sort
                df_plot = df_plot.sort_values(by=metric_choice, ascending=not is_desc)
                
                # 3. Limit to Top N
                df_plot = df_plot.head(top_n)
                
                st.divider()
                
                # --- Step 4: Render Chart ---
                if not df_plot.empty:
                    st.write(f"**📊 Top {len(df_plot)} {analysis_target} ranked by {metric_choice}**")
                    st.caption(f"Filtered Range: {filter_range[0]} to {filter_range[1]}")
                    
                    index_col = "Movie" if analysis_target == "Movies" else "User"
                    st.bar_chart(df_plot.set_index(index_col)[metric_choice])
                else:
                    st.warning("⚠️ No data matches your current filter range. Try widening the slider.")
            else:
                st.info("No data available yet.")




