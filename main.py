import re, ass, os
import pandas as pd
from functools import reduce

# All files came from this link:
# https://www.subtitlist.com/subtitles/bleach-2004/english/2206035

# Except the Season 1 episodes 10-20 that came from:
# https://www.subtitlist.com/subtitles/bleach-2004/english/2311978

# Except the Season 17 episodes 1-13 (episodes 367-379) that came from:
# https://www.opensubtitles.org/en/ssearch/sublanguageid-eng/idmovie-1174151

# ----------------------------------------------------------------------------------------------------------------------

# Cleaning the ASS format subtitles

# set the path to the directory containing the files

path = os.getcwd()

library = "/Episode_Subtitles"

file_name = 'CleanedData.csv'


# Function that cleans the text
def clean_sub(sub):
    # Remove text inside brackets
    sub_text = re.sub('{.*?}', '', sub)
    sub_text = re.sub('[.*?]', '', sub_text)
    sub_text = re.sub('<.*?>', '', sub_text)

    # Split by newline and join with commas
    sub_text = ','.join(sub_text.split('\n'))

    # Remove \N, newlines, apostrophes, and quotes
    sub_text = sub_text.replace(r'\N', ' ')
    sub_text = sub_text.replace('\n', ' ')
    sub_text = sub_text.replace('"', '')
    sub_text = sub_text.replace("'", '')

    return sub_text

# Create a Pandas DataFrame
df = pd.DataFrame()

# Get a list of all files in the directory and sort them numerically
files = os.listdir(path+library)
files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Loop over the ASS files and process each one
for i, file in enumerate(files):

# Skip any files that don't contain .ass extention
    if not file.endswith(".ass"):
        continue

    # Open files
    with open(os.path.join(path+library, file), 'r', encoding='utf_8_sig') as f:
        docASS = ass.parse(f)

    # Define an empty string to store processed text
    full_script = ""

    # Reading the events (text) of the files line by line
    for event in docASS.events:
        script = clean_sub(event.text)

        # Making the full script into one single cell
        full_script = full_script + " " + script

    # Assigning full episode script to the first cell of each row
    df.loc[i, ["Scripts"]] = str(full_script)


# Now we add the final season that is in srt format at the end


# Loop over the ASS files and process each one
for i, file in enumerate(files):

    # Skip any files that don't contain .ass extension
    if not file.endswith(".srt"):
        continue

    # Open files
    with open(os.path.join(path + library, file), 'r', encoding='utf_8_sig') as f:
        docSRT = f.readlines()

    # Create string that contains entire script
    full_script_2 = ""

    for line in docSRT:

        if not re.search('[a-zA-Z]', line):
            continue
        else:
            full_script_2 = full_script_2 + " " + clean_sub(line)

    # Assigning full episode script to the first cell of each row
    df.loc[i, ["Scripts"]] = str(full_script_2)

# Now the dataframe has been created, and we have the entire Bleach script.
# The data is in a format where every row of the first column is an entire episode's script.

# ---------------------------------------------------------------------------------------------------------------------

# After the data cleaning, now comes the analysis!

# Creating empty words list
number_words = []

# Creating variable of length of dataframe
n_df = len(df)

# Going through rows of df to count total words, and characters
df["N° of Words"] = df["Scripts"].apply(lambda n: len(n.split(" ")))
df["N° of Characters"] = df["Scripts"].apply(lambda n: len(n))

# Print total amount of words
print("\nTotal amount of words are: " + str(sum(df["N° of Words"])))
print("\nTotal amount of characters are: " + str(sum(df["N° of Characters"])))

# ----------------------------------------------------------------------------------------------------------------------

# Now we will create a list of the main arcs from : https://bleach.fandom.com/wiki/Episodes
arcs = []

for x in df.index:
    if x <= 19:
        arcs.append("1. Agent of the Shinigami")
    elif x <= 40:
        arcs.append("2. Soul Society: The Sneak Entry")
    elif x <= 62:
        arcs.append("3. Soul Society: The Rescue")
    elif x <= 90:
        arcs.append("4. The Bount")
    elif x <= 108:
        arcs.append("5. The Bount: Assault on Soul Society")
    elif x <= 130:
        arcs.append("6. Arrancar: The Arrival")
    elif x <= 150:
        arcs.append("7. Arrancar: The Hueco Mundo Sneak Entry")
    elif x <= 166:
        arcs.append("8. Arrancar: The Fierce Fight")
    elif x <= 188:
        arcs.append("9. The New Captain Shūsuke Amagai")
    elif x <= 204:
        arcs.append("10. Arrancar vs. Shinigami")
    elif x <= 211:
        arcs.append("11. The Past")
    elif x <= 228:
        arcs.append("12. Arrancar: The Arrival")
    elif x <= 264:
        arcs.append("13. Zanpakutō Unknown Tales")
    elif x <= 315:
        arcs.append("14. Arrancar: Downfall")
    elif x <= 341:
        arcs.append("15. Gotei 13 Invading Army")
    elif x <= 365:
        arcs.append("16. The Lost Substitute Shinigami")
    else:
        arcs.append("17. The Thousand-Year Blood War")

# Add this list into the dataframe
df["Arcs"] = arcs

# ----------------------------------------------------------------------------------------------------------------------

# We will now look at the appearances of the main characters names
good_characters = ["Ichigo", "Kurosaki", "Rukia", "Kuchiki", "Orihime", "Inoue", "Chad", "Sado", "Uryu", "Ishida", "Renji", "Abarai", "Kisuke", "Yoruichi", "Zaraki", "Byakuya", "Xcution"]
bad_characters = ["Hollows", "Bounts", "Arrancar", "Espada", "Aizen", "Gin", "Karyia", "Koga",  "Ulquiorra", "Grimmjow", "Yammy", "Yhwach"]

all_characters = good_characters + bad_characters

# Creating an empty dataframes to count characters
all_characters_df = pd.DataFrame(columns=all_characters)

# Looking for the number of times that main characters appear
for i in range(len(df)):
    for char in all_characters:
        all_characters_df.loc[i, char] = df.iloc[i, 0].count(char)

# Define list of DataFrames
dfs = [df, all_characters_df]

# Merge all dataframes into one
df = reduce(lambda left, right: pd.merge(left, right, right_index=True, left_index=True, how='outer'), dfs)

# ----------------------------------------------------------------------------------------------------------------------

