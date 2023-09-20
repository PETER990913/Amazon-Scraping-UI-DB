from tkinter import Canvas, Entry, Text,  Button, PhotoImage,filedialog,END,Variable,messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path

def BuildingGUI():
    # Create a window object
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets/")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Tk()
    window.title("Crawler")
    window.geometry("+500+100")
    window.geometry("1000x800")
    window.configure(bg = "#202020")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 800,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    # Tree Structure
    canvas.pack()

    # Create a Frame widget to hold the Treeview
    tree_frame = tk.Frame(canvas,  bg="#FFFFFF")
    tree_frame.pack()
    vscrollbar = tk.Scrollbar(tree_frame, orient="vertical")
    vscrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.configure("Custom.Treeview",
                    background="#FFFFFF")

    # Create a Treeview widget inside the Frame
    tree = ttk.Treeview(
        tree_frame,
        # columns=("", "", ""),
        height=30,  # Set the number of visible items
        yscrollcommand=vscrollbar.set,  # Link to the scrollbar
        style="Custom.Treeview"
    )

    # tree.place(width=400, height=200)
    tree.pack(fill="both", expand=True)
    # tree.place(x = -300, y = -200, width=500, height=200)

    # Configure the scrollbar to work with the Treeview
    vscrollbar.config(command=tree.yview)
    
    
    # Getting the treeview text when it's selected
    def on_select(event):
        selected_item = tree.selection()[0]
        item_text = tree.item(selected_item)['text']
        item_link = tree.item(selected_item)['tags']
        # return item_text, item_link
        print(item_text)
        print(item_link)    
    
    # Insert data into the Treeview
    parent_item = tree.insert("", "end", text="Amazon Devices & Accessories", tags="https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices/ref=zg_bs_nav_amazon-devices_0")
    child_0 = tree.insert(parent_item, "end", text="All")
    child_1 = tree.insert(parent_item, "end", text="Amazon Device Accessories")
    tree.insert(child_1, "end", text="All")
    tree.insert(child_1, "end", text="Adapters & Connectors")
    tree.insert(child_1, "end", text="Audio")
    tree.insert(child_1, "end", text="Bases & Stands")
    tree.insert(child_1, "end", text="Charging Docks")
    tree.insert(child_1, "end", text="Clocks")
    tree.insert(child_1, "end", text="Covers")
    tree.insert(child_1, "end", text="Gaming Controllers")
    tree.insert(child_1, "end", text="Home Security Decals & Signs")
    tree.insert(child_1, "end", text="Home Security Solar Chargers")
    tree.insert(child_1, "end", text="Keyboards")
    tree.insert(child_1, "end", text="Memory Cards")
    tree.insert(child_1, "end", text="Mounts")
    tree.insert(child_1, "end", text="Power Supplies & Chargers")
    tree.insert(child_1, "end", text="Projection Mats")
    tree.insert(child_1, "end", text="Protection Plans")
    tree.insert(child_1, "end", text="Reading Lights")
    tree.insert(child_1, "end", text="Remote Controls")
    tree.insert(child_1, "end", text="Screen Protectors")
    tree.insert(child_1, "end", text="Skins")
    tree.insert(child_1, "end", text="Sleeves")
    tree.insert(child_1, "end", text="Styluses")
    tree.insert(child_1, "end", text="Tangrams")
    child_2 = tree.insert(parent_item, "end", text="Amazon Devices")
    tree.insert(child_2, "end", text="All")
    tree.insert(child_2, "end", text="Astro Household Robots")
    tree.insert(child_2, "end", text="Car Dash Cameras")
    tree.insert(child_2, "end", text="Device Bundles")
    tree.insert(child_2, "end", text="Echo Smart Speakers & Displays")
    tree.insert(child_2, "end", text="Fire TV")
    tree.insert(child_2, "end", text="Fire Tablets")
    tree.insert(child_2, "end", text="Home Wi-Fi & Networking")
    tree.insert(child_2, "end", text="Kindle E-readers")
    tree.insert(child_2, "end", text="Programmable Devices")
    tree.insert(child_2, "end", text="Sleep Trackers")
    tree.insert(child_2, "end", text="Smart Appliances")
    tree.insert(child_2, "end", text="Smart Home Security & Lighting")
    tree.insert(child_2, "end", text="Wearable Technology")

    parent_item1 = tree.insert("", "end", text="Amazon Renewed")

    parent_item2 = tree.insert("", "end", text="Appliances")
    tree.insert(parent_item2, "end", text="All")
    tree.insert(parent_item2, "end", text="Astro Household Robots")
    tree.insert(parent_item2, "end", text="Cooktops")
    tree.insert(parent_item2, "end", text="Dishwashers")
    tree.insert(parent_item2, "end", text="Freezers")
    tree.insert(parent_item2, "end", text="Ice Makers")
    tree.insert(parent_item2, "end", text="Range Hoods")
    tree.insert(parent_item2, "end", text="Ranges")
    tree.insert(parent_item2, "end", text="Refrigerators")
    tree.insert(parent_item2, "end", text="Wall Ovens")
    tree.insert(parent_item2, "end", text="Warming Drawers")
    tree.insert(parent_item2, "end", text="Washers & Dryers")
    tree.insert(parent_item2, "end", text="Wine Cellars")

    parent_item3 = tree.insert("", "end", text="Apps & Games")
    child3_0 = tree.insert(parent_item3, "end", text="All")
    child3_1 = tree.insert(parent_item3, "end", text="Books & Comics")
    tree.insert(child3_1, "end", text="All")
    tree.insert(child3_1, "end", text="Book Info & Reviews")
    tree.insert(child3_1, "end", text="Readers & Players")
    child3_2 = tree.insert(parent_item3, "end", text="Business")
    tree.insert(child3_2, "end", text="All")
    tree.insert(child3_2, "end", text="Accounting & Expenses")
    tree.insert(child3_2, "end", text="Banking")
    tree.insert(child3_2, "end", text="Currency Converters & Guides")
    tree.insert(child3_2, "end", text="Payments & Money Transfers")
    tree.insert(child3_2, "end", text="Personal Finance")
    tree.insert(child3_2, "end", text="Stocks & Investing")
    tree.insert(child3_2, "end", text="Tax Calculators")
    child3_3 = tree.insert(parent_item3, "end", text="Communication")
    child3_4 = tree.insert(parent_item3, "end", text="Customization")
    tree.insert(child3_4, "end", text="All")
    tree.insert(child3_4, "end", text="Ringtones & Notifications")
    tree.insert(child3_4, "end", text="Themes")
    tree.insert(child3_4, "end", text="Wallpapers & Images")
    tree.insert(child3_4, "end", text="Widgets")
    child3_5 = tree.insert(parent_item3, "end", text="Education")
    child3_6 = tree.insert(parent_item3, "end", text="Finance")
    tree.insert(child3_6, "end", text="All")
    tree.insert(child3_6, "end", text="Accounting & Expenses")
    tree.insert(child3_6, "end", text="Banking")
    tree.insert(child3_6, "end", text="Currency Converters & Guides")
    tree.insert(child3_6, "end", text="Payments & Money Transfers")
    tree.insert(child3_6, "end", text="Personal Finance")
    tree.insert(child3_6, "end", text="Stocks & Investing")
    tree.insert(child3_6, "end", text="Tax Calculators")
    child3_7 = tree.insert(parent_item3, "end", text="Food & Drink")
    tree.insert(child3_7, "end", text="All")
    tree.insert(child3_7, "end", text="Cooking & Recipes")
    tree.insert(child3_7, "end", text="Wine & Beverages")
    child3_8 = tree.insert(parent_item3, "end", text="Games")
    tree.insert(child3_8, "end", text="All")
    tree.insert(child3_8, "end", text="Action")
    tree.insert(child3_8, "end", text="Adventure")
    tree.insert(child3_8, "end", text="Arcade")
    tree.insert(child3_8, "end", text="Board")
    tree.insert(child3_8, "end", text="Brain & Puzzle")
    tree.insert(child3_8, "end", text="Cards")
    tree.insert(child3_8, "end", text="Casino")
    tree.insert(child3_8, "end", text="Dice")
    tree.insert(child3_8, "end", text="Music & Rhythm")
    tree.insert(child3_8, "end", text="Racing")
    tree.insert(child3_8, "end", text="Role Playing")
    tree.insert(child3_8, "end", text="Seek & Find")
    tree.insert(child3_8, "end", text="Simulation")
    tree.insert(child3_8, "end", text="Sports Games")
    tree.insert(child3_8, "end", text="Strategy")
    tree.insert(child3_8, "end", text="Trivia")
    tree.insert(child3_8, "end", text="Words")
    child3_9 = tree.insert(parent_item3, "end", text="Health & Fitness")
    tree.insert(child3_9, "end", text="All")
    tree.insert(child3_9, "end", text="Activity Tracking")
    tree.insert(child3_9, "end", text="Exercise Motivation")
    tree.insert(child3_9, "end", text="Heart Rate Monitors")
    tree.insert(child3_9, "end", text="Massage Guides")
    tree.insert(child3_9, "end", text="Meditation Guides")
    tree.insert(child3_9, "end", text="Menstrual Trackers")
    tree.insert(child3_9, "end", text="Nutrition & Diet")
    tree.insert(child3_9, "end", text="Pregnancy")
    tree.insert(child3_9, "end", text="Sleep Tracking")
    tree.insert(child3_9, "end", text="Sounds & Relaxation")
    tree.insert(child3_9, "end", text="Workout Guides")
    tree.insert(child3_9, "end", text="Yoga Guides")
    child3_10 = tree.insert(parent_item3, "end", text="Kids")
    tree.insert(child3_10, "end", text="All")
    tree.insert(child3_10, "end", text="Book Readers & Players")
    tree.insert(child3_10, "end", text="Education")
    tree.insert(child3_10, "end", text="Games")
    tree.insert(child3_10, "end", text="Movie & TV Streaming")
    tree.insert(child3_10, "end", text="Music & Audio")
    child3_11 = tree.insert(parent_item3, "end", text="Lifestyle")
    tree.insert(child3_11, "end", text="All")
    tree.insert(child3_11, "end", text="Astrology")
    tree.insert(child3_11, "end", text="Beauty & Cosmetics")
    tree.insert(child3_11, "end", text="Celebrities")
    tree.insert(child3_11, "end", text="Cooking & Recipes")
    tree.insert(child3_11, "end", text="Crafts & DIY")
    tree.insert(child3_11, "end", text="Creative Writing")
    tree.insert(child3_11, "end", text="Diaries")
    tree.insert(child3_11, "end", text="Fashion & Style")
    tree.insert(child3_11, "end", text="Game Rules")
    tree.insert(child3_11, "end", text="Health & Fitness")
    tree.insert(child3_11, "end", text="Home & Garden")
    tree.insert(child3_11, "end", text="Meditation Guides")
    tree.insert(child3_11, "end", text="Outdoors & Nature")
    tree.insert(child3_11, "end", text="Parenting")
    tree.insert(child3_11, "end", text="Pets & Animals")
    tree.insert(child3_11, "end", text="Quotes")
    tree.insert(child3_11, "end", text="Relationships")
    tree.insert(child3_11, "end", text="Religion & Spirituality")
    tree.insert(child3_11, "end", text="Self Improvement")
    tree.insert(child3_11, "end", text="Sexuality")
    tree.insert(child3_11, "end", text="Tattoos & Body Piercing")
    tree.insert(child3_11, "end", text="Wedding")
    tree.insert(child3_11, "end", text="Wine & Beverages")
    child3_12 = tree.insert(parent_item3, "end", text="Local")
    tree.insert(child3_12, "end", text="All")
    tree.insert(child3_12, "end", text="Business Locators")
    tree.insert(child3_12, "end", text="Navigation")
    tree.insert(child3_12, "end", text="Offline Maps")
    tree.insert(child3_12, "end", text="Real Estate")
    tree.insert(child3_12, "end", text="Taxi & Ridesharing")
    child3_13 = tree.insert(parent_item3, "end", text="Magazines")
    child3_14 = tree.insert(parent_item3, "end", text="Medical")
    tree.insert(child3_14, "end", text="All")
    tree.insert(child3_14, "end", text="Education")
    tree.insert(child3_14, "end", text="Heart Rate Monitors")
    tree.insert(child3_14, "end", text="Massage Guides")
    tree.insert(child3_14, "end", text="Menstrual Trackers")
    tree.insert(child3_14, "end", text="Pregnancy")
    tree.insert(child3_14, "end", text="Reference")
    tree.insert(child3_14, "end", text="Sleep Tracking")
    child3_15 = tree.insert(parent_item3, "end", text="Movies & TV")
    tree.insert(child3_15, "end", text="All")
    tree.insert(child3_15, "end", text="Movie Info & Reviews")
    tree.insert(child3_15, "end", text="On-Demand Movie Streaming")
    tree.insert(child3_15, "end", text="Video-Sharing")
    child3_16 = tree.insert(parent_item3, "end", text="Music & Audio")
    tree.insert(child3_16, "end", text="All")
    tree.insert(child3_16, "end", text="Audio Recording")
    tree.insert(child3_16, "end", text="Instruments & Music Makers")
    tree.insert(child3_16, "end", text="Music Info & Reviews")
    tree.insert(child3_16, "end", text="Music Players")
    tree.insert(child3_16, "end", text="On-Demand Music Streaming")
    tree.insert(child3_16, "end", text="Podcasts")
    tree.insert(child3_16, "end", text="Radio Webcasts")
    tree.insert(child3_16, "end", text="Readers & Players")
    tree.insert(child3_16, "end", text="Ringtones & Notifications")
    tree.insert(child3_16, "end", text="Songbooks & Sheet Music")
    tree.insert(child3_16, "end", text="Sounds & Relaxation")
    child3_17 = tree.insert(parent_item3, "end", text="News")
    tree.insert(child3_17, "end", text="All")
    tree.insert(child3_17, "end", text="Feed Aggregators")
    tree.insert(child3_17, "end", text="Newspapers")
    tree.insert(child3_17, "end", text="Sports Fan News")
    child3_18 = tree.insert(parent_item3, "end", text="Novelty")
    tree.insert(child3_18, "end", text="All")
    tree.insert(child3_18, "end", text="Funny Pictures")
    tree.insert(child3_18, "end", text="Funny Sounds")
    tree.insert(child3_18, "end", text="Prank Biometric Scanners")
    tree.insert(child3_18, "end", text="Screen Pranks")
    tree.insert(child3_18, "end", text="Talking & Answering")
    child3_19 = tree.insert(parent_item3, "end", text="Photo & Video")
    child3_20 = tree.insert(parent_item3, "end", text="Productivity")
    tree.insert(child3_20, "end", text="All")
    tree.insert(child3_20, "end", text="Alarms & Clocks")
    tree.insert(child3_20, "end", text="Audio Recording")
    tree.insert(child3_20, "end", text="Calculators")
    tree.insert(child3_20, "end", text="Calendars")
    tree.insert(child3_20, "end", text="Cloud Storage")
    tree.insert(child3_20, "end", text="Contact Management")
    tree.insert(child3_20, "end", text="Document Editing")
    tree.insert(child3_20, "end", text="Document Viewers")
    tree.insert(child3_20, "end", text="Email Clients")
    tree.insert(child3_20, "end", text="File Management")
    tree.insert(child3_20, "end", text="Keyboards")
    tree.insert(child3_20, "end", text="Meetings & Conferencing")
    tree.insert(child3_20, "end", text="Notes & Bookmarking")
    tree.insert(child3_20, "end", text="Organizers & Assistants")
    tree.insert(child3_20, "end", text="Personal Finance")
    tree.insert(child3_20, "end", text="Presentations")
    tree.insert(child3_20, "end", text="Remote PC Access")
    tree.insert(child3_20, "end", text="Scanning & Printing")
    tree.insert(child3_20, "end", text="Security")
    tree.insert(child3_20, "end", text="To-Do Lists & Reminders")
    tree.insert(child3_20, "end", text="Translators")
    tree.insert(child3_20, "end", text="Web Browsers")
    child3_21 = tree.insert(parent_item3, "end", text="Reference")
    tree.insert(child3_21, "end", text="All")
    tree.insert(child3_21, "end", text="Dictionaries")
    tree.insert(child3_21, "end", text="Encyclopedias")
    tree.insert(child3_21, "end", text="Guides & How-Tos")
    tree.insert(child3_21, "end", text="History")
    tree.insert(child3_21, "end", text="Language & Grammar")
    tree.insert(child3_21, "end", text="Math")
    tree.insert(child3_21, "end", text="Reference")
    tree.insert(child3_21, "end", text="Religion")
    tree.insert(child3_21, "end", text="Science")
    tree.insert(child3_21, "end", text="Test Preparation")
    child3_22 = tree.insert(parent_item3, "end", text="Shopping")
    child3_23 = tree.insert(parent_item3, "end", text="Social")
    tree.insert(child3_23, "end", text="All")
    tree.insert(child3_23, "end", text="Blogging")
    tree.insert(child3_23, "end", text="Dating")
    tree.insert(child3_23, "end", text="Email Clients")
    tree.insert(child3_23, "end", text="General Social Networking")
    tree.insert(child3_23, "end", text="Photo-Sharing")
    tree.insert(child3_23, "end", text="Professional Networking")
    tree.insert(child3_23, "end", text="Social Network Management")
    tree.insert(child3_23, "end", text="Video-Sharing")
    child3_24 = tree.insert(parent_item3, "end", text="Sports")
    tree.insert(child3_24, "end", text="All")
    tree.insert(child3_24, "end", text="Activity Tracking")
    tree.insert(child3_24, "end", text="Exercise Motivation")
    tree.insert(child3_24, "end", text="Heart Rate Monitors")
    tree.insert(child3_24, "end", text="Sports Fan News")
    tree.insert(child3_24, "end", text="Sports Games")
    tree.insert(child3_24, "end", text="Sports Information")
    tree.insert(child3_24, "end", text="Workout Guides")
    tree.insert(child3_24, "end", text="Yoga Guides")
    child3_25 = tree.insert(parent_item3, "end", text="Transportation")
    tree.insert(child3_25, "end", text="All")
    tree.insert(child3_25, "end", text="Auto Rental")
    tree.insert(child3_25, "end", text="Flight Finders")
    tree.insert(child3_25, "end", text="Navigation")
    tree.insert(child3_25, "end", text="Taxi & Ridesharing")
    child3_26 = tree.insert(parent_item3, "end", text="Travel")
    tree.insert(child3_26, "end", text="All")
    tree.insert(child3_26, "end", text="Auto Rental")
    tree.insert(child3_26, "end", text="Compasses")
    tree.insert(child3_26, "end", text="Currency Converters & Guides")
    tree.insert(child3_26, "end", text="Flight Finders")
    tree.insert(child3_26, "end", text="Hotel Finders")
    tree.insert(child3_26, "end", text="Navigation")
    tree.insert(child3_26, "end", text="Offline Maps")
    tree.insert(child3_26, "end", text="Taxi & Ridesharing")
    tree.insert(child3_26, "end", text="Translators")
    tree.insert(child3_26, "end", text="Travel Guides")
    tree.insert(child3_26, "end", text="Trip Planners")
    tree.insert(child3_26, "end", text="Unit Converters")
    child3_27 = tree.insert(parent_item3, "end", text="Utilities")
    tree.insert(child3_27, "end", text="All")
    tree.insert(child3_27, "end", text="Alarms & Clocks")
    tree.insert(child3_27, "end", text="All-in-One Tools")
    tree.insert(child3_27, "end", text="Audio Recording")
    tree.insert(child3_27, "end", text="Battery Savers")
    tree.insert(child3_27, "end", text="Calculators")
    tree.insert(child3_27, "end", text="Calendars")
    tree.insert(child3_27, "end", text="Cloud Storage")
    tree.insert(child3_27, "end", text="Contact Management")
    tree.insert(child3_27, "end", text="Device Tracking")
    tree.insert(child3_27, "end", text="Document Viewers")
    tree.insert(child3_27, "end", text="Email Clients")
    tree.insert(child3_27, "end", text="File Management")
    tree.insert(child3_27, "end", text="File Transfer")
    tree.insert(child3_27, "end", text="Flashlights")
    tree.insert(child3_27, "end", text="Keyboards")
    tree.insert(child3_27, "end", text="Notes & Bookmarking")
    tree.insert(child3_27, "end", text="QR & Barcode Scanners")
    tree.insert(child3_27, "end", text="Remote PC Access")
    tree.insert(child3_27, "end", text="Scanning & Printing")
    tree.insert(child3_27, "end", text="Security")
    tree.insert(child3_27, "end", text="Speed Testing")
    tree.insert(child3_27, "end", text="Task & App Managers")
    tree.insert(child3_27, "end", text="Translators")
    tree.insert(child3_27, "end", text="Unit Converters")
    tree.insert(child3_27, "end", text="Web Browsers")
    tree.insert(child3_27, "end", text="Wi-Fi Analyzers")
    tree.insert(child3_27, "end", text="Widgets")
    child3_28 = tree.insert(parent_item3, "end", text="Weather")

    parent_item4 = tree.insert("", "end", text="Arts, Crafts & Sewing")
    child4_0 = tree.insert(parent_item4, "end", text="All")

    parent_item5 = tree.insert("", "end", text="Audible Books & Originals")
    child5_0 = tree.insert(parent_item5, "end", text="All")

    parent_item6 = tree.insert("", "end", text="Automotive")
    child6_0 = tree.insert(parent_item6, "end", text="All")

    parent_item7 = tree.insert("", "end", text="Baby")
    child7_0 = tree.insert(parent_item7, "end", text="All")

    parent_item8 = tree.insert("", "end", text="Beauty & Personal Care")
    child8_0 = tree.insert(parent_item8, "end", text="All")

    parent_item9 = tree.insert("", "end", text="Books")
    child9_0 = tree.insert(parent_item9, "end", text="All")

    parent_item3 = tree.insert("", "end", text="Camera & Photo Products")
    child3_0 = tree.insert(parent_item3, "end", text="All")

    parent_item10 = tree.insert("", "end", text="CDs & Vinyl")
    child10_0 = tree.insert(parent_item10, "end", text="All")

    parent_item11 = tree.insert("", "end", text="Cell Phones & Accessories")
    child11_0 = tree.insert(parent_item11, "end", text="All")

    parent_item12 = tree.insert("", "end", text="Climate Pledge Friendly")
    child12_0 = tree.insert(parent_item12, "end", text="All")

    parent_item13 = tree.insert("", "end", text="Clothing, Shoes & Jewelry")
    child13_0 = tree.insert(parent_item13, "end", text="All")

    parent_item14 = tree.insert("", "end", text="Collectible Coins")
    child14_0 = tree.insert(parent_item14, "end", text="All")

    parent_item15 = tree.insert("", "end", text="Computers & Accessories")
    child15_0 = tree.insert(parent_item15, "end", text="All")

    parent_item16 = tree.insert("", "end", text="Digital Educational Resources")
    child16_0 = tree.insert(parent_item16, "end", text="All")

    parent_item17 = tree.insert("", "end", text="Digital Music")
    child17_0 = tree.insert(parent_item17, "end", text="All")

    parent_item18 = tree.insert("", "end", text="Electronics")
    child18_0 = tree.insert(parent_item18, "end", text="All")

    parent_item19 = tree.insert("", "end", text="Entertainment Collectibles")
    child19_0 = tree.insert(parent_item19, "end", text="All")

    parent_item20 = tree.insert("", "end", text="Gift Cards")
    child20_0 = tree.insert(parent_item20, "end", text="All")

    parent_item21 = tree.insert("", "end", text="Grocery & Gourmet Food")
    child21_0 = tree.insert(parent_item21, "end", text="All")

    parent_item22 = tree.insert("", "end", text="Handmade Products")
    child22_0 = tree.insert(parent_item22, "end", text="All")

    parent_item23 = tree.insert("", "end", text="Health & Household")
    child23_0 = tree.insert(parent_item23, "end", text="All")

    parent_item24 = tree.insert("", "end", text="Home & Kitchen")
    child24_0 = tree.insert(parent_item24, "end", text="All")


    parent_item25 = tree.insert("", "end", text="Industrial & Scientific")
    child25_0 = tree.insert(parent_item25, "end", text="All")

    parent_item26 = tree.insert("", "end", text="Kindle Store")
    child26_0 = tree.insert(parent_item26, "end", text="All")

    parent_item27 = tree.insert("", "end", text="Kitchen & Dining")
    child27_0 = tree.insert(parent_item27, "end", text="All")

    parent_item28 = tree.insert("", "end", text="Movies & TV")
    child28_0 = tree.insert(parent_item28, "end", text="All")


    parent_item29 = tree.insert("", "end", text="Musical Instruments")
    child29_0 = tree.insert(parent_item29, "end", text="All")


    parent_item30 = tree.insert("", "end", text="Office Products")
    child30_0 = tree.insert(parent_item30, "end", text="All")


    parent_item31 = tree.insert("", "end", text="Patio, Lawn & Garden")
    child31_0 = tree.insert(parent_item31, "end", text="All")


    parent_item32 = tree.insert("", "end", text="Pet Supplies")
    child32_0 = tree.insert(parent_item32, "end", text="All")


    parent_item33 = tree.insert("", "end", text="Software")
    child33_0 = tree.insert(parent_item33, "end", text="All")


    parent_item34 = tree.insert("", "end", text="Sports & Outdoors")
    child34_0 = tree.insert(parent_item34, "end", text="All")


    parent_item35 = tree.insert("", "end", text="Sports Collectibles")
    child35_0 = tree.insert(parent_item35, "end", text="All")


    parent_item36 = tree.insert("", "end", text="Tools & Home Improvement")
    child36_0 = tree.insert(parent_item36, "end", text="All")


    parent_item37 = tree.insert("", "end", text="Toys & Games")
    child37_0 = tree.insert(parent_item37, "end", text="All")

    parent_item38 = tree.insert("", "end", text="Unique Finds")
    child38_0 = tree.insert(parent_item38, "end", text="All")


    parent_item39 = tree.insert("", "end", text="Video Games")
    child39_0 = tree.insert(parent_item39, "end", text="All")

    tree.bind("<<TreeviewSelect>>", on_select)
    
    
    # tree.tag_bind("link", "<Button-1>", on_select)

    # Update the canvas window to fit the contents
    tree.update_idletasks()
    canvas.create_window((0, 0), window=tree_frame, anchor="nw")

    # Configure the Canvas to scroll
    canvas.config(scrollregion=canvas.bbox("all"))  


    canvas.create_text(
        400.0,
        150.0,
        anchor="nw",
        text="IP address",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )
    canvas.create_text(
        560.0,
        150.0,
        anchor="nw",
        text="PORT",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )
    canvas.create_text(
        690.0,
        150.0,
        anchor="nw",
        text="USERNAME",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )
    canvas.create_text(
        860.0,
        150.0,
        anchor="nw",
        text="PASSWORD",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    IP_address1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    IP_address1_entry.place(
        x=350.0,
        y=200,
        width=170.0,
        height=30.0
    )

    PORT1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PORT1_entry.place(
        x=530.0,
        y=200,
        width=100.0,
        height=30.0
    )

    USERNAME1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    USERNAME1_entry.place(
        x=645.0,
        y=200,
        width=170.0,
        height=30.0
    )

    PASSWORD1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PASSWORD1_entry.place(
        x=820.0,
        y=200,
        width=170.0,
        height=30.0
    )

    canvas.create_text(
        270.0,
        207.0,
        anchor="nw",
        text="Proxy 1",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    IP_address2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    IP_address2_entry.place(
        x=350.0,
        y=255,
        width=170.0,
        height=30.0
    )

    PORT2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PORT2_entry.place(
        x=530.0,
        y=255,
        width=100.0,
        height=30.0
    )

    USERNAME2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    USERNAME2_entry.place(
        x=645.0,
        y=255,
        width=170.0,
        height=30.0
    )

    PASSWORD2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PASSWORD2_entry.place(
        x=820.0,
        y=255,
        width=170.0,
        height=30.0
    )

    canvas.create_text(
        270.0,
        262.0,
        anchor="nw",
        text="Proxy 2",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    IP_address3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    IP_address3_entry.place(
        x=350.0,
        y=310,
        width=170.0,
        height=30.0
    )

    PORT3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PORT3_entry.place(
        x=530.0,
        y=310,
        width=100.0,
        height=30.0
    )

    USERNAME3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    USERNAME3_entry.place(
        x=645.0,
        y=310,
        width=170.0,
        height=30.0
    )

    PASSWORD3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PASSWORD3_entry.place(
        x=820.0,
        y=310,
        width=170.0,
        height=30.0
    )

    canvas.create_text(
        270.0,
        317.0,
        anchor="nw",
        text="Proxy 3",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    canvas.create_text(
        575.0,
        480.0,
        anchor="nw",
        text="Console Log",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    console_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    console_entry.place(
        x=219.0,
        y=525,
        width=781.0,
        height=100.0
    )


    start_img = PhotoImage(file=relative_to_assets("start.png"))
    # start_btn = Button(
    #     image=start_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("start"),activebackground= "#202020")
    start_btn = Button(
        image=start_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
    start_btn.place(x=75, y=720, width=100, height=47)

    stop_img = PhotoImage(file=relative_to_assets("stop.png"))
    # stop_btn = Button(image=stop_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("stop"),activebackground= "#202020", state="disabled")
    stop_btn = Button(image=stop_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
    stop_btn.place(x=325, y=720, width=100, height=47)

    Display_img = PhotoImage(file=relative_to_assets("result.png"))
    # Display_btn = Button(image=Display_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("stop"),activebackground= "#202020", state="disabled")
    Display_btn = Button(image=Display_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
    Display_btn.place(x=575, y=720, width=100, height=47)

    Import_img = PhotoImage(file=relative_to_assets("import.png"))
    # stop_btn = Button(image=Import_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : handle_btn_press("stop"),activebackground= "#202020", state="disabled")
    Import_btn = Button(image=Import_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
    Import_btn.place(x=825, y=720, width=100, height=47)

    # IP_address1_entry.insert(0, "1632 Scholar Dr")
    # PORT1_entry.insert(0, "Lawrenceville")
    # USERNAME1_entry.insert(0, "GA")
    # PASSWORD1_entry.insert(0, "202-337-1412")

    # IP_address2_entry.insert(0, "605 Saint Lawrence Blvd")
    # PORT2_entry.insert(0, "Eastlake")
    # USERNAME2_entry.insert(0, "OH")
    # PASSWORD2_entry.insert(0, "202-337-1412")

    # IP_address3_entry.insert(0, "203 Magnolia St")
    # PORT3_entry.insert(0, "Siloam Springs")
    # USERNAME3_entry.insert(0, "AR")
    # PASSWORD3_entry.insert(0, "202-337-1412")

    window.resizable(False, False)
    # Run the main event loop to display the window
    window.mainloop()
BuildingGUI()