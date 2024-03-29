import traceback
import json
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from src import valorant_manager
from src import image_builder
from src.fetch_data import fetch_images, fetch_matches

def main():
    mgr = valorant_manager.Valorant()
    #content = mgr.content

    fetch_images('agent')
    fetch_images('map')
    #choices = fetch_matches(mgr, content) + [Choice(name="Reload", value="reload"), Choice(name="Exit", value="exit")]
    new_choices = [Choice(name="Use JSON", value="json"), Choice(name="Enter Values", value="values"), Choice(name="Exit", value="exit")]
    previous_choices = {
        "team_a": "DEF",
        "team_b": "ATK",
        "primary": "#b6a46d",
        "secondary": "#000000",
        "tertiary": "#ffffff",
        "logo": "data/misc_assets/logo.png",
        "output": True
    }
    while True:
        match_id = inquirer.select("Pick an option:", new_choices).execute()
        if match_id == "json":
            match_id = inquirer.text("Enter player name with tag").execute()
            overwrite = inquirer.select("Overwrite Team Names from File?:", [Choice(name="Yes", value=True), Choice(name="No", value=False)]).execute()
            with open("colors.json", "r") as data:
                choices = json.load(data)
                team_a = choices['team_a']
                team_b = choices['team_b']
                primary_color = choices['primary']
                secondary_color = choices['secondary']
                tertiary_color = choices['tertiary']
                logo_path = choices['logo']
                path_var = bool(choices['output'])
            
            if overwrite:
                team_a = inquirer.text("Enter Team A (Attackers, Left Side of Lobby)", default=previous_choices['team_a']).execute()
                team_b = inquirer.text("Enter Team B (Defenders, Right Side of Lobby)", default=previous_choices['team_b']).execute()


        elif match_id == "custom":
            match_id = inquirer.text("Enter match id (Found on tracker.gg)").execute()
            team_a = inquirer.text("Enter Team A (Attackers)", default=previous_choices['team_a']).execute()
            previous_choices['team_a'] = team_a
            
            team_b = inquirer.text("Enter Team B (Defenders)", default=previous_choices['team_b']).execute()
            previous_choices['team_b'] = team_b
            
            primary_color = inquirer.text("Enter Primary Color in hex(Winning Banners)", default=previous_choices['primary']).execute()
            previous_choices['primary'] = primary_color
            primary_color = tuple(int(primary_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            
            secondary_color = inquirer.text("Enter Secondary Color (Losing Banners)", default=previous_choices['secondary']).execute()
            previous_choices['secondary'] = secondary_color
            secondary_color = tuple(int(secondary_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            
            tertiary_color = inquirer.text("Enter Third Color (Text)", default=previous_choices['tertiary']).execute()
            previous_choices['tertiary'] = tertiary_color
            tertiary_color = tuple(int(tertiary_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            
            logo_path = inquirer.text("Enter logo path", default=previous_choices['logo']).execute()
            logo_path = logo_path.strip('\"')
            previous_choices['logo'] = logo_path
            path_var = inquirer.select("Output to same file?:", [Choice(name="Yes", value=True), Choice(name="No", value=False)]).execute()

            
        elif match_id == "exit":
            break
        # elif match_id == "reload":
        #     choices[:-2] = fetch_matches(mgr, content)
        #     continue
        if match_id is not None and match_id != "":
            try:
                print("Generating image...")
                data = mgr.load_match_data(match_id)
                # with open("match_reference_2.json", "r") as f:
                #     #f.write(json.dumps(data))
                #     data = json.load(f)                       
                builder = image_builder.Builder(data, team_a, team_b, primary_color, secondary_color, tertiary_color)
                builder.build_image(path_var, logo_path)
            except:
                traceback.print_exc()

if __name__ == "__main__":
    main()

    # builder = image_builder.Builder(data)
    # builder.build_image()
    # print("done")
