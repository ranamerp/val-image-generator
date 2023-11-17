import traceback
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from src import valorant_manager
from src import image_builder
from src.fetch_data import fetch_images, fetch_matches

def main():
    mgr = valorant_manager.Valorant()
    content = mgr.content

    fetch_images('agent')
    fetch_images('map')
    choices = fetch_matches(mgr, content) + [Choice(name="Reload", value="reload"), Choice(name="Exit", value="exit")]

    while True:
        match_id = inquirer.select("Pick a match:", choices).execute()
        if match_id == "custom":
            match_id = inquirer.text("Enter match id").execute()
            team_a = inquirer.text("Enter Team A (Defenders)", default="DEF").execute()
            team_b = inquirer.text("Enter Team B (Attackers)", default="ATK").execute()
            primary_color = inquirer.text("Enter Primary Color in hex(Winning Banners)", default='#b6a46d').execute()
            primary_color = tuple(int(primary_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            secondary_color = inquirer.text("Enter Secondary Color (Losing Banners)", default='#000000').execute()
            secondary_color = tuple(int(secondary_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            tertiary_color = inquirer.text("Enter Third Color (Text)", default='#ffffff').execute()
            tertiary_color = tuple(int(tertiary_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            logo_path = inquirer.text("Enter logo path", default="None").execute()
            if logo_path == "None":
                logo_path = None
            path_var = inquirer.select("Output to same file?:", [Choice(name="Yes", value=True), Choice(name="No", value=False)]).execute()
            #See if you can enter team names here. 
            #Also winning color
        elif match_id == "exit":
            break
        elif match_id == "reload":
            choices[:-2] = fetch_matches(mgr, content)
            continue
        if match_id is not None and match_id != "":
            try:
                print("Generating image...")
                data = mgr.load_match_data(match_id)
                builder = image_builder.Builder(data, team_a, team_b, primary_color, secondary_color, tertiary_color)
                builder.build_image(path_var, logo_path)
            except:
                traceback.print_exc()

if __name__ == "__main__":
    main()

    # builder = image_builder.Builder(data)
    # builder.build_image()
    # print("done")
