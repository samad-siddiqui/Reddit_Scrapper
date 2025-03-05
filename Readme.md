# Reddit Scrapper
A python script that scrapes post form Reddit using PRAW (Python Raddit API Wrapper) and saves them in csv and pdf

# Features
    - Fetch posts from multiple subreddits.
    - Sort posts by hot, new, controversial,top.
    - Filter posts based on minimum score.
    - Save posts in CSV and PDF formats.

# Requirements
make sure to install the requirements.txt file first 
    
    - pip install -r requirements.txt

# Environment Variables
To run this python script you have to set the environment variables by creating .env file and then you need a Raddit API client ID, client secret, and user agent.Here's how you can do that:

    - REDDIT_CLIENT_ID=your_client_id
    - REDDIT_CLIENT_SECRET=your_client_secret
    - REDDIT_USER_AGENT=your_user_agent

# Usage
To run this script you need to run the following command

    - python reddit_scraper.py --subreddits "python,programming" --sort_by "top" --limit --min_score

# Arguments

    --subreddits → Comma-separated list of subreddits (default: all).
    --sort_by → Sorting option (hot, new, controversial, top, gilded).
    --limit → Number of posts to fetch per subreddit (default: 5).
    --min_score → Minimum upvotes required for a post (default: 10).

# Output Files

* CSV: *reddit_post.csv*
* PDF: *reddit_post.pdf*


