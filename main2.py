from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

# --- THIS IS THE PATH FOR YOUR ANDROID PHONE'S DOWNLOAD FOLDER ---
# If you run this script on a computer, you'll need to change this path.
SAVE_FOLDER = "/storage/emulated/0/Download"

def get_video_id(url):
    """
    Extract the YouTube video ID from the URL.
    """
    # This regex is improved to handle various YouTube URL formats
    video_id_match = re.search(r"(?:v=|\/|embed\/|youtu.be\/)([a-zA-Z0-9_-]{11})", url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid or unsupported YouTube URL")

def fetch_transcript(video_id, language_code='en'):
    """
    Fetch the transcript for the provided video ID and language.
    By default, it tries to get the transcript in English.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        return transcript
    except Exception as e:
        # Provide a more user-friendly error message
        return f"Could not fetch transcript. Please check the following:\n1. The video has subtitles in the language '{language_code}'.\n2. The video URL is correct.\n3. Your internet connection is working.\n\nOriginal error: {e}"

def display_transcript_text_only(transcript):
    """
    Print the spoken text only, without timestamps, to the console.
    """
    print("\n--- Transcript ---")
    for entry in transcript:
        print(entry['text'])
    print("--- End of Transcript ---\n")

def save_transcript_to_txt(transcript, video_id, save_path):
    """
    Saves the transcript text to a .txt file in the specified path.
    """
    # Create a unique, clean filename like 'videoID_transcript.txt'
    filename = f"{video_id}_transcript.txt"
    full_path = os.path.join(save_path, filename)

    # Ensure the target directory exists. If not, create it.
    # This is helpful if the script is run on a new system.
    os.makedirs(save_path, exist_ok=True)

    try:
        # Open the file with 'w' (write mode) and 'utf-8' encoding
        # to support all characters and symbols from any language.
        with open(full_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(entry['text'] + '\n') # Write each line and add a newline
        
        print(f"✅ Transcript successfully saved to:\n{full_path}")

    except Exception as e:
        print(f"❌ Error: Could not save the file. Reason: {e}")


if __name__ == "__main__":
    # Ask the user to input the YouTube video/shorts URL
    url = input("Enter the YouTube video or Shorts URL: ")
    
    # Ask for the preferred language (default to 'en' for English)
    language_code = input("Enter language code (e.g., en, ml, ta) [default: en]: ").strip().lower()
    if not language_code:
        language_code = 'en' # Set English as default if input is empty
    
    try:
        # Get the video ID from the URL
        video_id = get_video_id(url)
        
        print(f"\nFetching transcript for video ID: {video_id} in language: '{language_code}'...")
        
        # Fetch the transcript
        transcript = fetch_transcript(video_id, language_code)
        
        if isinstance(transcript, list):
            # 1. Display the transcript in the console
            display_transcript_text_only(transcript)
            
            # 2. Save the transcript to a .txt file
            save_transcript_to_txt(transcript, video_id, SAVE_FOLDER)
        else:
            # If there's an error message string, print it
            print(f"❌ Error: {transcript}")
    
    except ValueError as ve:
        print(f"❌ Error: {ve}")
