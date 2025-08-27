from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api._errors as yt_errors
import re
import os

# --- Customize this ---
SAVE_FOLDER = "/storage/emulated/0/Download"  # Change for non-Android environments
# Optional: supply proxy settings if deployed in cloud environment
PROXIES = {
    # 'http': 'http://username:password@proxy_host:port',
    # 'https': 'http://username:password@proxy_host:port',
} or None

def get_video_id(url: str) -> str:
    """
    Extract YouTube video ID from URLs of various formats.
    """
    match = re.search(r"(?:v=|/|embed/|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    raise ValueError("Invalid or unsupported YouTube URL")

def fetch_transcript(video_id: str, languages=None):
    """
    Try to fetch transcript (with optional proxy support).
    Returns tuple (transcript_list or None, error_message or None).
    """
    if languages is None:
        languages = ['en']
    try:
        # Direct fetch
        api = YouTubeTranscriptApi(proxies=PROXIES) if PROXIES else YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=languages)
        return fetched.to_raw_data(), None

    except yt_errors.TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."

    except yt_errors.NoTranscriptFound:
        return None, f"No transcript found for the specified languages: {languages}"

    except yt_errors.VideoUnavailable:
        return None, "Video is unavailable."

    except yt_errors.RequestBlocked:
        return None, ("Request was blocked by YouTube (likely due to IP issues). "
                      "Consider setting up a proxy or using a residential IP.")

    except Exception as e:
        return None, f"Unexpected error: {type(e).__name__}: {e}"

def display_transcript(transcript):
    """
    Print transcript text (without timestamps).
    """
    if not transcript:
        print("No transcript to display.")
        return
    print("\n--- Transcript ---")
    for entry in transcript:
        print(entry.get('text', ''))
    print("--- End of Transcript ---\n")

def save_transcript(transcript, video_id, folder):
    """
    Save transcript text as .txt in the specified folder.
    """
    try:
        os.makedirs(folder, exist_ok=True)
        filename = f"{video_id}_transcript.txt"
        path = os.path.join(folder, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(entry.get('text', '') for entry in transcript))
        print(f"✅ Transcript saved to: {path}")
    except Exception as e:
        print(f"❌ Failed to save transcript: {e}")

if __name__ == "__main__":
    url = input("Enter YouTube video or Shorts URL: ").strip()
    lang_input = input("Enter language codes (comma-separated) [default: en]: ").strip()
    languages = [c.strip().lower() for c in lang_input.split(',')] if lang_input else ['en']

    try:
        vid = get_video_id(url)
        print(f"Fetching transcript for video ID '{vid}' (languages: {languages})…")
        transcript, error = fetch_transcript(vid, languages)
        if transcript:
            display_transcript(transcript)
            save_transcript(transcript, vid, SAVE_FOLDER)
        else:
            print(f"❌ Error fetching transcript: {error}")

    except ValueError as err:
        print(f"❌ Error: {err}")
