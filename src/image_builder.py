import os
import copy

from PIL import Image, ImageDraw, ImageFont


class Builder:

    cur_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    base_image = os.path.join(cur_path,"data/ggsheetreal.png")
    output_folder = os.path.join(cur_path,"output")

    fonts = {
        "ddin": {
            "mvp_agent": ImageFont.truetype(os.path.join(cur_path,"data\\fonts\\DINNextLTPro-Medium.ttf"), 28),
            "player_agent": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 14),
            "map_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 40),
            "map_text": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 45),
            "win_loss_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Medium.ttf"), 35),
            "player_stat_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 12),
            "timestamp": ImageFont.truetype(os.path.join(cur_path,"data/fonts/DINNextLTPro-Regular.ttf"), 22),
        },
        "tungsten": {
            "mvp_player": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 70),
            "mvp_stats": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 65),
            "mvp_label": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 35),
            "header_scores": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 165),
            "header_team_name": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 100),
            "player_name": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 40),
            "player_stats": ImageFont.truetype(os.path.join(cur_path,"data/fonts/Tungsten-Bold.ttf"), 52),
        }
    }

    other_side_offsets = {
        "mvps": {
            "text": 1116,
            "images": 0,
            "overrides": {
                "kd": 0,
                "kills": 0,
                "combat_score": 0,
                "mvp_gradient": 0,
                "mvp_label": 0,
            }
        },
        "players": {
            "text": 124,
            "images": 124,
            "team": 739,
        },
    }

    def __init__(self, game_data, team_a, team_b, prime, second, ter):
        self.game_data = game_data
        self.img = Image.open(Builder.base_image)
        self.draw = ImageDraw.Draw(self.img)

        self.team_red_name = team_a #defenders
        self.team_blue_name = team_b  #attackers
        self.primary_color = prime,
        self.secondary_color = second,
        self.tertiary_color = ter

        self.image_ref_points = {
            "header_footer": {
                "text": {
                    "map_name": {
                        "anchor": (47,953),
                        "dimensions": (298,56),
                        #This can probably be changed to an accent color. For now we keep white 
                        "color": (255,255,255),
                        "font": self.fonts["ddin"]["map_text"],
                        "var_name": lambda *x: game_data["match_map_display_name"],
                        "justify": 'c',
                        "upper": True,
                    }
                }, 
                "images": {
                    "map": {
                    "anchor": (48, 543),
                    "dimensions": (1280,720),
                    "crop": lambda *x: (491, 115, 787, 601),
                    "file_path": "data/maps/map_{map}.png", 
                }   
        }
            },
            "team_details": {
                 "text": {
                    "team_red_banner": {
                        "anchor": (47, 48),
                        "dimensions": (796, 157),
                        "color": self.primary_color,
                        "alt_color": self.secondary_color
                    }, 
                    "team_blue_banner": {
                        "anchor": (1075, 47),
                        "dimensions": (796, 157),
                        "color": self.primary_color,
                        "alt_color": self.secondary_color
                    },
                    "team_red_score": {
                        "anchor": (724,70),
                        "dimensions": (81,106),
                        "color": self.primary_color,
                        "alt_color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["header_scores"],
                        "var_name": lambda *x: game_data["teams"][x[0]]["rounds_won"],
                        "justify": "r"
                    },
                    "team_blue_score": {
                        "anchor": (1114,70),
                        "dimensions": (81,106),
                        "color": self.primary_color,
                        "alt_color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["header_scores"],
                        "var_name": lambda *x: game_data["teams"][x[0]]["rounds_won"],
                        "justify": "l"
                    },
                    "team_red_name": {
                        "anchor": (125, 76),
                        "dimensions": (225,52),
                        "color": self.primary_color,
                        "alt_color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["header_team_name"],
                        "var_name": lambda *x: self.team_red_name if self.team_red_name is not None else game_data["teams"][x[0]]["team_alias"],
                        "upper": True,
                        "justify": "l"
                    },
                    "team_blue_name": {
                        "anchor": (1791 - 225,76),
                        "dimensions": (225,52),
                        "color": self.primary_color,
                        "alt_color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["header_team_name"],
                        "var_name": lambda *x: self.team_blue_name if self.team_blue_name is not None else game_data["teams"][x[0]]["team_alias"],
                        "upper": True,
                        #this takes the X and adds the X of dimensions
                        "justify": "r"
                    },
                    "team_red_wl": {
                        "anchor": (125, 158),
                        "dimensions": (80,20),
                        "color": self.primary_color,
                        "alt_color": self.tertiary_color,
                        "font": self.fonts["ddin"]["win_loss_label"],
                        "var_name": lambda *x: game_data["teams"][x[0]]["won"],
                        "upper": True,
                        "justify": "l"
                    },
                    "team_blue_wl": {
                        "anchor": (1791 - 80 ,158),
                        "dimensions": (80,20),
                        "color": self.primary_color,
                        "alt_color": self.tertiary_color,
                        "font": self.fonts["ddin"]["win_loss_label"],
                        "var_name": lambda *x: game_data["teams"][x[0]]["won"],
                        "upper": True,
                        "justify": "r"
                    },
                }
            },
            "mvps": {
                "text": {
                    "agent_name": {
                        "anchor": (82,398),
                        "dimensions": (181, 62), 
                        "color": self.tertiary_color,
                        "font": self.fonts["ddin"]["mvp_agent"],
                        "var_name": lambda *x: game_data["players"][int(x[0])][int(x[1])]["agent_display_name"],
                        "upper": True,
                        "justify": "l"
                    },
                    "player_name": {
                        "anchor": (82,452),
                        "dimensions": (289,38),
                        "color": (255,255,255),
                        "font": self.fonts["tungsten"]["mvp_player"],
                        "var_name": lambda *x: game_data["players"][int(x[0])][int(x[1])]["display_name"],
                        "upper": True,
                        "justify": "l"
                    },
                    "kills": {
                        "anchor": (800 - 165,294),
                        "dimensions": (165,43),
                        "color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["mvp_stats"],
                        "var_name": lambda *x: f'{game_data["players"][int(x[0])][int(x[1])]["kills"]}/{game_data["players"][int(x[0])][int(x[1])]["deaths"]}',
                        "justify": "r"
                    },
                    "combat_score": {
                        "anchor": (800 - 114,380),
                        "dimensions": (114,33),
                        "color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["mvp_stats"],
                        "var_name": lambda *x: game_data["players"][int(x[0])][int(x[1])]["combat_score"],
                        "justify": "r"
                    }
                },
                "images": {
                    "agent": {
                        "anchor": (840, 219),
                        "dimensions": (687,415), 
                        "target_width": 887,
                        #This is saying that the point I want is the right most point
                        "justify": 'r',
                        "crop": lambda *x: (100,101,x[1][0], x[1][1]) if x[0] else (x[2]-x[1][0],101,x[2] + x[2]-x[1][0] ,x[1][1]),
                        "file_path": "data/agents/full_image/agent_{agent}.png"
                    }
                }
            },
            "players": {
                "text": {
                    "agent_name": {
                        "anchor": (492,600),
                        "dimensions": (156, 17), 
                        "color": self.secondary_color,
                        "font": self.fonts["ddin"]["player_agent"],
                        "var_name": lambda *x: game_data["players"][int(x[0])][int(x[1])]["agent_display_name"],
                        "upper": True,
                        "justify": "l"
                    },
                    "player_name": {
                        "anchor": (492,626),
                        "dimensions": (156, 17), 
                        "color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["player_name"],
                        "var_name": lambda *x: game_data["players"][int(x[0])][int(x[1])]["display_name"] if len(game_data["players"][int(x[0])][int(x[1])]["display_name"]) < 13 else game_data["players"][int(x[0])][int(x[1])]["display_name"][:11]+"...",
                        "upper": True,
                        "justify": "l"
                    },

                    "combat_score": {
                        "anchor": (803 - 130, 605),
                        "dimensions": (130, 40), 
                        "color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["player_stats"],
                        "var_name": lambda *x: game_data["players"][int(x[0])][int(x[1])]["combat_score"],
                        "justify": "r"
                    },
                    "kd": {
                        "anchor": (803-152, 547),
                        "dimensions": (152, 60), 
                        "color": self.tertiary_color,
                        "font": self.fonts["tungsten"]["player_stats"],
                        "var_name": lambda *x: f'{game_data["players"][int(x[0])][int(x[1])]["kills"]}/{game_data["players"][int(x[0])][int(x[1])]["deaths"]}',
                        "justify": "r"
                    },
                },
                "images": {
                    "banner": {
                        "anchor": (466, 544),
                        "dimensions": (377, 114), 
                        "color": self.primary_color,
                        "justify": 'r',
                    },
                    "agent": {
                        "anchor": (415,543),
                        "dimensions": (113,114), 
                        "slot_width": 114,
                        "crop": lambda *x: (abs(57-(x[0]//2)),0,57+(x[1][0]-(x[0]//2)),x[1][1]),
                        "file_path": "data/agents/headshot/agent_{agent}.png",
                        "justify": 'r',
                    },
                    "role": {
                        "anchor": (463, 628),
                        "dimensions": (25, 25), 
                        "slot_width": 114,
                        "color": self.primary_color,
                        "crop": lambda *x: (abs(57-(x[0]//2)),0,57+(x[1][0]-(x[0]//2)),x[1][1]),
                        "file_path": "data/agents/role/agent_{agent}.png",
                        "justify": 'r',
                    },
                },
            }
        }


    def draw_team_details(self):
        refs = self.image_ref_points["team_details"]
        #for img_type, image in refs["images"].items():

        for team_id,team in enumerate(self.game_data["teams"]):
            team_name = team["team_name"].lower()

            #draw banner
            banner = refs["text"][f"team_{team_name}_banner"]
            banner["color"] = banner["alt_color"] if not team["won_bool"] else banner["color"]
            banner_img = Image.new("RGBA", banner["dimensions"], banner["color"])
            self.__draw_prepared_image(banner_img, banner["anchor"])

            # draw scores
            score_label = refs["text"][f"team_{team_name}_score"]
            score_label["color"] = score_label["color"] if not team["won_bool"] else score_label["alt_color"]
            self.__draw_text(score_label,int(team_id))

            team_name_label = refs["text"][f"team_{team_name}_name"]
            team_name_label["color"] = team_name_label["color"] if not team["won_bool"] else team_name_label["alt_color"]
            self.__draw_text(team_name_label,int(team_id))

            team_wl_label = refs["text"][f"team_{team_name}_wl"]
            team_wl_label["color"] = team_wl_label["color"] if not team["won_bool"] else team_wl_label["alt_color"]
            self.__draw_text(team_wl_label,int(team_id))


    def draw_header_footer(self):
        refs = self.image_ref_points["header_footer"]
        for img_type, image in refs["images"].items():
            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(map=self.game_data['match_map_display_name'].lower(),mode=self.game_data['match_mode'].lower()).split("/"))).convert("RGBA")
            self.__draw_image(image,new_img)


        for label_type,label in refs["text"].items():
            self.__draw_text(label)


    def draw_players(self):
        player_refs = self.image_ref_points["players"]
        og_refs = copy.deepcopy(player_refs)
        mvp_refs = self.image_ref_points["mvps"]
        for team_id,team in enumerate(self.game_data["players"]):
            # player panels
            if team_id != 0:
                player_refs = og_refs
                for ref,data in player_refs["text"].items():
                    data["anchor"] = (1920 - data["anchor"][0], data['anchor'][1])
                    if data['justify'] == 'l':
                        data['justify'] = 'r'
                        data['anchor'] = (data["anchor"][0] - data['dimensions'][0], data['anchor'][1])
                    elif data['justify'] == 'r':
                        data['justify'] = 'l'
                        data['anchor'] = (data["anchor"][0] - data['dimensions'][0], data['anchor'][1])
                    else:
                        data['justify'] = 'c'

                    if data['color'] == self.primary_color:
                        data['color'] = self.secondary_color
                    elif data["color"] == self.secondary_color:
                        data['color'] = self.tertiary_color
                    else:
                        data['color'] = self.primary_color

                for ref,data in player_refs["images"].items():
                    data["anchor"] = (1920 - data["anchor"][0]- data['dimensions'][0], data['anchor'][1])
                    if "color" in data:
                        if data['color'] == self.primary_color:
                            data['color'] = self.secondary_color
                        elif data["color"] == self.secondary_color:
                            data['color'] = self.tertiary_color
                        else:
                            data['color'] = self.primary_color
                
                # team offset (mvps)
                for ref,data in mvp_refs["text"].items():
                    data["anchor"] = (1920 - data["anchor"][0], data['anchor'][1])
                    if data['justify'] == 'l':
                        data['justify'] = 'r'
                        data['anchor'] = (data["anchor"][0] - data['dimensions'][0], data['anchor'][1])
                    elif data['justify'] == 'r':
                        data['justify'] = 'l'
                        data['anchor'] = (data["anchor"][0] - data['dimensions'][0], data['anchor'][1])
                    else:
                        data['justify'] = 'c'

                    if data['color'] == self.primary_color:
                        data['color'] = self.secondary_color
                    elif data["color"] == self.secondary_color:
                        data['color'] = self.tertiary_color
                    else:
                        data['color'] = self.primary_color

                    
                for ref,data in mvp_refs["images"].items():
                    data["anchor"] = (1920 - data["anchor"][0], data['anchor'][1])
                    if "color" in data:
                        if data['color'] == self.primary_color:
                            data['color'] = self.secondary_color
                        elif data["color"] == self.secondary_color:
                            data['color'] = self.tertiary_color
                        else:
                            data['color'] = self.primary_color

            for position,player in enumerate(team):
                
                if position == 0:
                    # mvp player

                    # load images
                    for img_type,image in mvp_refs["images"].items():
                        new_img = None
                        if img_type == "agent": 
                            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(agent=player['agent_display_name']).split("/"))).convert("RGBA")
                            #crop_v = (True,image["dimensions"]) if team_id == 0 else (False,image["dimensions"],image["target_width"])
                            crop_v = (True,image["dimensions"])

                            if team_id == 1:
                                image['justify'] = 'l'
                            agent_image, anchor = self.__draw_image(image,new_img,size_axis="x",crop_vars=crop_v,no_draw=True)
                            self.__draw_prepared_image(agent_image,anchor)

                    # load text
                    for label_type,label in mvp_refs["text"].items():
                        self.__draw_text(label,int(team_id),int(position))

                else:
                    # regular player 
                    if position > 1:
                        # player offset
                        text_offset = self.other_side_offsets["players"]["text"]
                        image_offset = self.other_side_offsets["players"]["images"]

                        
                        for ref,data in player_refs["text"].items():
                            data["anchor"] = (data["anchor"][0],data["anchor"][1]+text_offset)
                        for ref,data in player_refs["images"].items():
                            data["anchor"] = (data["anchor"][0],data["anchor"][1]+image_offset)
                    
                    for img_type,image in player_refs["images"].items():
                        new_img = None
                        if team_id == 1:
                            image["justify"] = 'l'
                        
                        if img_type == "agent": 
                            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(agent=player['agent_display_name']).split("/"))).convert("RGBA")
                            self.__draw_image(image,new_img,size_axis="x",crop_vars=(image["slot_width"],image["dimensions"]),anchor_override=(image["anchor"][0]+45,image["anchor"][1]))

                        elif img_type =="role":
                            role_square = Image.new("RGBA", (image["dimensions"][0] + 3, image["dimensions"][1] + 3), image["color"])
                            self.__draw_prepared_image(role_square, image["anchor"])
                            new_img = Image.open(os.path.join(Builder.cur_path,*image["file_path"].format(agent=player['agent_display_name']).split("/"))).convert("RGBA")
                            self.__draw_image(image,new_img,size_axis="x",crop_vars=(image["slot_width"],image["dimensions"]),anchor_override=(image["anchor"][0] + 1,image["anchor"][1] + 1))

                        elif img_type =="banner":
                            label_banner = Image.new("RGBA", image["dimensions"], image["color"])
                            newanchor = image['anchor']
                            if image['justify'] == 'l':
                                newanchor = (image['anchor'][0], image['anchor'][1])
                            self.__draw_prepared_image(label_banner, newanchor)

                    for label_type,label in player_refs["text"].items():
                        self.__draw_text(label,int(team_id),int(position))


    def build_image(self):
        

        self.draw_header_footer()
        self.draw_team_details()
        self.draw_players()


        self.img.save(os.path.join(Builder.cur_path,f"output/{self.game_data['match_id']}.png"))
        print(f"Done, image saved to output/{self.game_data['match_id']}.png \n")

    def __draw_image(self,img_data,new_img,size_axis="y",crop_vars=(),anchor_override=None,no_draw=False):
        width, height = new_img.size
        ratio = width/height if size_axis == "y" else height/width
        new_height = 0
        new_width = 0

        if img_data.get("target_width"):
            new_width = img_data["target_width"]
            new_height = int(ratio * new_width)
        else:
            if size_axis == "y":
                new_height = img_data["dimensions"][1]
                new_width = int(ratio * new_height)
            elif size_axis == "x":
                new_width = img_data["dimensions"][0]
                new_height = int(ratio * new_width)
        
        new_img = new_img.resize((new_width,new_height),Image.LANCZOS)

        crop_bounds = None
        if img_data.get("crop"):
            crop_bounds = img_data["crop"](*crop_vars)
            new_img = new_img.crop(crop_bounds)

        anchor = img_data["anchor"]
        if anchor_override is not None:
            anchor = anchor_override
        if img_data.get("justify"):
            if img_data['justify'] == 'r':
                anchor = (anchor[0] - img_data['dimensions'][0], anchor[1])
        if img_data.get("centered"):
            anchor = (anchor[0]-new_width//2,anchor[1]-new_height//2)
            anchor = ((img_data["dimensions"][0]//2)+anchor[0],(img_data["dimensions"][1]//2)+anchor[1])
                
            
        if not no_draw:
            self.img.paste(new_img, anchor, new_img)
        return new_img, anchor

    def __draw_prepared_image(self,new_img,anchor):
        self.img.paste(new_img,anchor,new_img)


    def __draw_text(self,label,*var):
        if label.get("justify"):
            justify = label["justify"]
        else:
            justify = "l"

        if label.get("var_name"):
            text = str(label["var_name"](*var))
        else:
            text = label["text"]
        text = text.upper() if label.get("upper") else text

        coords = label["anchor"]

        _, _, w, h = label["font"].getbbox(text)
        
        dimens = label["dimensions"]
        anchor = label["anchor"]

        if justify == "c":
            coords = (((dimens[0]-w)/2)+anchor[0],(((dimens[1]-h)/2)+anchor[1]))
        elif justify == "r":
            coords = ((dimens[0]-w)+anchor[0],(((dimens[1]-h)/2)+anchor[1]))
        elif justify == "l":
            coords = (anchor[0],(((dimens[1]-h)/2)+anchor[1]))


        self.draw.text(coords, text, label["color"], font=label["font"])
