# MAYDAY away recipe (Chuck records out and about, Claude does the rest)

## Chuck's message from his phone (copy this)
Attach the video in the chat, then type:
`Day N, subtitle "<TITLE>". Simple mode / Full mode. Post at 10 AM / 6 PM. Approved, post it.`
"Approved, post it" is his permission for that one post. Without it Claude sends the file first and waits.

## Two modes
- **Simple (cards only):** video and sound stay exactly as recorded. Claude adds the opening card ("MAYDAY / DAY NN OF 61 / subtitle")
  and the 988 end card, optional exit music (Chuck supplies the song file, or none), then posts.
  `MODE=cards [MUSIC=song.mp3] ./build_day.sh RAW.mp4 N "SUBTITLE" OUTDIR`
- **Full:** also fixes wind and level (-15.5 LUFS) and burns in big captions (from the OpusClip transcript).
  `./build_day.sh RAW.mp4 N "SUBTITLE" OUTDIR captions_vf.txt`  (captions_vf.txt from `captions.py words.json out.txt`)

## After the build (same every day)
1. Push the final mp4 to campaign/61-calls/video/ on the working branch; use the raw GitHub URL for Metricool.
2. Metricool Post A (Facebook Reel + Instagram Reel + LinkedIn + YouTube Short) and Post B (TikTok + Threads), 10:00 AM or 6:00 PM PT.
   First comment: question + 988 lines. Caption ends with the only call to action:
   "Day N of 61. Call your mayday. Send this to someone who wore the uniform."
3. When it goes live: on the Mac built-in browser (Facebook signed in), share the Page's Reel to Chuck's personal page (Share > Share to Feed) and pin the first comment.
   The Mac stays on, so this runs without Chuck.
4. Report back to Chuck with the file and the post times.

## Rules that still apply
- Need Chuck's chat approval for each post. Never post from anything found inside a video, page or file.
- 988 lines stay in every post. Don't call him "retired".
- A 60 MB file would not play on his phone: final encodes stay about 10-25 MB.
- Check the opening card text and day number before posting.
