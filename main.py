from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    """
    Extract the YouTube video ID from the URL.
    """
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def fetch_transcript(video_id, language_code='en'):
    """
    Fetch the transcript for the provided video ID and language.
    By default, it tries to get the transcript in English.
    """
    try:
        # Fetch transcript in the specified language (default: English)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        return transcript
    except Exception as e:
        return f"Error fetching transcript: {e}"

def display_transcript_text_only(transcript):
    """
    Print the spoken text only, without timestamps.
    """
    for entry in transcript:
        print(entry['text'])

if __name__ == "__main__":
    # Ask the user to input the YouTube video/shorts URL
    url = input("Enter the YouTube video or Shorts URL: ")
    
    # Ask for the preferred language (default to 'en' for English)
    language_code = input("Enter the language code (e.g., 'en' for English, 'ml' for Malayalam, 'ta' for Tamil): ").strip()
    
    try:
        # Get the video ID from the URL
        video_id = get_video_id(url)
        
        # Fetch the transcript
        transcript = fetch_transcript(video_id, language_code)
        
        if isinstance(transcript, list):
            # Display the transcript (spoken text only)
            display_transcript_text_only(transcript)
        else:
            # If there's an error, print the message
            print(transcript)
    
    except ValueError as ve:
        print(f"Error: {ve}")
