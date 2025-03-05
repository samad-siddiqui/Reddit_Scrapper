import os
import argparse
import praw
import csv
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()


def validate(args):
    """
    Validate the command-line arguments.

    This function checks if the minimum score and limit arguments are non-negative.
    If either is negative, it prints an error message and exits the program.

    Parameters:
    args (argparse.Namespace): The parsed command-line arguments.
        - args.min_score (int): The minimum score for posts.
        - args.limit (int): The maximum number of posts to fetch.

    Returns:
    None

    Raises:
    SystemExit: If either min_score or limit is negative.
    """
    if args.min_score < 0:
        print("Invalid minimum score. Please enter a positive integer.")
        exit(1)
    if args.limit < 0:
        print("Invalid minimum score. Please enter a positive integer.")
        exit(1)
    
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)
# .hot
# .new
# .controversial
# .top
# .gilded

def fetch_posts(subreddits,sort_by, limit):
    subreddit_list = subreddits.split(",")
    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name.strip())
        if sort_by == "hot":
            posts = subreddit.hot(limit=limit)
        elif sort_by == "new":
            posts = subreddit.new(limit=limit)
        elif sort_by == "controversial":
            posts = subreddit.controversial(limit=limit)
        elif sort_by == "top":
            posts = subreddit.top(limit=limit)
        for post in  posts:        
            yield post
        
def execute(fetched_posts, min_score):
    
    filtered_posts = filter(lambda post: post.score >= min_score, fetched_posts)
    post_data = list(map(lambda post: (post.title, post.url, post.score), filtered_posts))
                        
    # print(f"\nFetching posts from {subreddit_name} ({sort_by}):\n" + "-"*40)
    
    for title,url,score in post_data:  
        print(f"Title: {title}")
        print(f"URL: {url}")
        print("---")
    return post_data

def save_to_csv(filtered_posts):
    with open('reddit_posts.csv', 'w', newline='') as csvfile:
        fieldnames = ['Title', 'URL', 'Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for title, url, score in filtered_posts:
            writer.writerow({'Title': title, 'URL': url, 'Score': {score}})

def save_to_pdf(all_posts):
    # TODO: Implement PDF generation using the filtered_posts
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    # Title
    pdf.cell(200, 10, "Reddit Posts", ln=True, align="C") 
    pdf.ln(10)

    # Column Widths
    # Adjusted for Title, URL, and Score
    col_widths = [90, 70, 30]  

    # Headers
    pdf.set_font("Arial", style='B', size=10)
    headers = ["Title", "URL", "Score"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1)
    pdf.ln()

    # Data Rows
    pdf.set_font("Arial", size=10)
    for title, url, score in all_posts:
        pdf.cell(col_widths[0], 10, title[:50], border=1) 
        pdf.cell(col_widths[1], 10, url[:40], border=1, link=url)
        pdf.cell(col_widths[2], 10, str(score), border=1, ln=True) 
    # Save PDF
    pdf.output("reddit_posts.pdf")
    print("\nPDF saved to 'reddit_posts.pdf'.")

def main(args):
    validate(args)
    fetched_posts  = fetch_posts(args.subreddits,args.sort_by, args.limit)
    executed_posts = execute(fetched_posts,args.min_score)
    # print(executed_posts)
    if executed_posts:
        save_to_csv(executed_posts)
        save_to_pdf(executed_posts)
        print(f"\nPosts saved to 'reddit_posts.pdf'.")

    else:
        print("\nNo posts found with the given criteria.")
    return executed_posts
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrapping Raddit")
    parser.add_argument("--subreddits", default="all", help="Comma-separated subreddit names (default: all)")
    parser.add_argument('--sort_by', default="hot", choices=["hot", "new", "controversial", "top"], help="Sort by (default: hot)")
    parser.add_argument('--limit', type=int, default=5, help="Limit the number of posts (default: 5)")
    parser.add_argument('--min_score', type=int, default=10, help="Minimum score for a post to be included (default: 10)")
    args = parser.parse_args()
    # Load environment variables
    if not all ([os.getenv('REDDIT_CLIENT_ID'),os.getenv('REDDIT_CLIENT_SECRET'),os.getenv('REDDIT_USER_AGENT')]):
        raise ValueError('Missing required environment variables: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT')
    
    main(args)
    