import os
import argparse
import praw
import csv
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
if not all ([os.getenv('REDDIT_CLIENT_ID'),os.getenv('REDDIT_CLIENT_SECRET'),os.getenv('REDDIT_USER_AGENT')]):
    raise ValueError('Missing required environment variables: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT')

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
class custom_iterators:
    """
    A custom iterator for iterating over posts.

    This iterator allows one by one access to posts while keeping track of the current position.
    
    Attributes:
        posts (list): A list of posts to iterate over.
        index (int): The current position of iteration.
    
    Methods:
        __iter__(): Returns the iterator object itself.
        __next__(): Returns the next post in the sequence or raises StopIteration if no more posts exist.
    
    """
    def __init__(self, posts):
        self.posts = list(posts)
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.posts):
            raise StopIteration
        post = self.posts[self.index]
        self.index += 1
        return post  
    pass                                                                                                                                                                                                                                                                                                                                                                                                               
def post_generator(posts):
    for post in posts:
        yield post

def fetch_posts(subreddits = "all",sort_by= "hot", limit=5, min_score=10):
    subreddit_list = subreddits.split(",")
    all_post = []
    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name.strip())
        if sort_by == "hot":
            post = subreddit.hot(limit=limit)
        elif sort_by == "new":
            post = subreddit.new(limit=limit)
        elif sort_by == "controversial":
            post = subreddit.controversial(limit=limit)
        elif sort_by == "top":
            post = subreddit.top(limit=limit)
        elif sort_by == "gilded":
            post = subreddit.gilded(limit=limit)
        else:
            print("Invalid sort_by option. Please choose from hot, new, controversial, top, or gilded.")
            return
        
        filtered_posts = filter(lambda post: post.score >= min_score, post)
        post_gen = post_generator(filtered_posts)
        post_iter = custom_iterators(post_gen)
        post_data = zip((post.title for post in post_iter),
                        (post.url for post in post_iter),
                        (post.score for post in post_iter))
    print(f"\nFetching posts from {subreddit_name} ({sort_by}):\n" + "-"*40)
    
    for title,url,score in post_data:  
        print(f"Title: {title}")
        print(f"URL: {url}")
        print("---")
        all_post.append((title,url,score))
    return all_post
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
        pdf.cell(col_widths[0], 10, title[:40], border=1) 
        pdf.cell(col_widths[1], 10, url[:40], border=1, link=url)
        pdf.cell(col_widths[2], 10, str(score), border=1, ln=True) 
    # Save PDF
    pdf.output("reddit_posts.pdf")
    print("\nPDF saved to 'reddit_posts.pdf'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrapping Raddit")
    parser.add_argument("--subreddits", default="all", help="Comma-separated subreddit names (default: all)")
    parser.add_argument('--sort_by', default="hot", choices=["hot", "new", "controversial", "top"], help="Sort by (default: hot)")
    parser.add_argument('--limit', type=int, default=5, help="Limit the number of posts (default: 5)")
    parser.add_argument('--min_score', type=int, default=10, help="Minimum score for a post to be included (default: 10)")
    args = parser.parse_args()
    posts = fetch_posts(args.subreddits,args.sort_by, args.limit, args.min_score)
    
    if args.min_score<0:
        print("Invalid minimum score. Please enter a positive integer.")
    if args.limit<0:
        print("Invalid minimum score. Please enter a positive integer.")
    if posts:
        save_to_csv(posts)
        save_to_pdf(posts)
        print(f"\nPosts saved to 'reddit_posts.pdf'.")

    else:
        print("\nNo posts found with the given criteria.")