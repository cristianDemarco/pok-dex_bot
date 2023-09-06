import logging
import sys
import os
import time
import json

from telegram import __version__ as TG_VER
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from TOKEN import TOKEN
from Classes.pokemonAPI import PokemonAPI
from TEXTS import translate

pokemonAPI = PokemonAPI()

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await search_pokemon(update, context, True)
    #print(update.callback_query.data)

messages_to_delete = []

async def search_pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE, is_Callback : bool = False) -> None:
    print(update)
    start_timestamp = time.time()
    if not is_Callback:
        pokemon_name = update.message.text
        chat_id = update.effective_chat.id
    elif is_Callback:
        query_data = json.loads(update.callback_query.data)

        pokemon_name = query_data["pokemon"]
        chat_id = update.callback_query.message.chat.id

    for id in messages_to_delete:
        await context.bot.deleteMessage(chat_id=chat_id, message_id=id)
        messages_to_delete.remove(id)

    pokemon_name = pokemon_name.replace("/pokemon", "").strip().lower()

    pokemonAPI.get_api_data(pokemon_name, query_data["variety"] if is_Callback else 0)
    pokemon = pokemonAPI.elaborate_api_data(query_data["variety"] if is_Callback else 0)

    keyboard = [
        [
            InlineKeyboardButton(text = f"< N°{int(pokemon.id) - 1}", callback_data=json.dumps(
                    {
                        "pokemon" : f"/pokemon {int(pokemon.id) - 1}",
                        "variety" : f"{int(pokemon.variety)}"
                        
                    }
                )
            ),
            InlineKeyboardButton(text = f"Change Variety", callback_data=json.dumps(            
                    {
                        "pokemon" : f"/pokemon {int(pokemon.id)}",
                        "variety" : f"{int(pokemon.variety) + 1}"
                    }
                )
            ),
            InlineKeyboardButton(text = f"N°{int(pokemon.id) + 1} >", callback_data=json.dumps(
                    {
                        "pokemon" : f"/pokemon {int(pokemon.id) + 1}",
                        "variety" : f"{int(pokemon.variety)}"
                    }
                )
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await context.bot.send_photo(
        chat_id = chat_id,
        caption = translate("POKEDEX_RETURN_MESSAGE", language="IT", data={
            "name": pokemon.name,
            "id" : pokemon.id,
            "generation" : pokemon.generation,
            "is_legendary" : "  [Leggendario]" if pokemon.is_legendary else "",
            "types" : pokemon.types,
            "description" : pokemon.description
        }),
        photo = pokemon.photo,
        reply_markup=reply_markup,
        parse_mode="html"
    )
    end_timestamp = time.time()
    messages_to_delete.append(message.message_id)
    print(f"Time occured: {end_timestamp - start_timestamp}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("pokemon", search_pokemon))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()