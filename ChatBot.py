import os
import emoji
import logging
import openai
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)


class ChatBot:

    def __init__(self):
        self.TELEGRAM_CHAT_ID = {5893933948, 287339072}

    def getAnswer(self, update, context):
        text = update.message.text
        update.message.reply_text("Pending...")

        if not text or update.message.chat.id not in self.TELEGRAM_CHAT_ID:
            update.message.reply_text("Error "+emoji.emojize(":thumbs_down:"))
            return

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.8,
            max_tokens=800,
        )

        update.message.reply_text(response.choices[0].text)

    def getAnswerFromVoice(self, update, context):
        audio = update.message.voice

        if not audio or update.message.chat.id not in self.TELEGRAM_CHAT_ID:
            update.message.reply_text("Error "+emoji.emojize(":thumbs_down:"))
            return

        file = context.bot.get_file(audio.file_id)
        file.download('new_file.ogg')

        #Open the audio file
        ogg_audio = AudioSegment.from_ogg("new_file.ogg")

        #Save the audio file as an mp3 file
        ogg_audio.export("new_file.mp3", format="mp3")

        audio_file= open("new_file.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # Remove Files
        os.remove('new_file.ogg')
        os.remove('new_file.mp3')

        text = transcript.text
        update.message.reply_text("Pending...")
        update.message.reply_text(f'Question: {text}')

        if not text or update.message.chat.id not in self.TELEGRAM_CHAT_ID:
            update.message.reply_text("Error "+emoji.emojize(":thumbs_down:"))
            return

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=0.8,
            max_tokens=800,
        )

        update.message.reply_text(response.choices[0].text)



    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)
        if update:
            update.message.reply_text("Please try again")