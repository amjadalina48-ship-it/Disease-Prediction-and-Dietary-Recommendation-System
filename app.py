import os
import sqlite3
import joblib
from flask import Flask, render_template, request, redirect, session, flash, url_for


# -------------------- BASIC SETUP --------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)

app.secret_key = "your_secret_key"



# -------------------- LOAD ML MODEL --------------------

try:

    model = joblib.load("disease_model.pkl")

    solutions = joblib.load("disease_solution.pkl")

except Exception as e:

    print(f"Warning: Model files not found. Error: {e}")



# -------------------- DIET PLANS (15 Diseases) --------------------

diet_plans = {
    "Flu": [
        ["Monday", "Oatmeal + Honey | Veg soup | Steamed veggies"],
        ["Tuesday", "Banana + Ginger tea | Chicken soup | Khichdi"],
        ["Wednesday", "Fruit salad | Clear broth | Brown rice + Fish"],
        ["Thursday", "Poached eggs | Lentil soup | Mashed potatoes"],
        ["Friday", "Smoothie bowl | Vegetable stew | Boiled chicken"],
        ["Saturday", "Pancakes | Tomato soup | Baked sweet potato"],
        ["Sunday", "Scrambled eggs | Chicken noodle soup | Steamed veggies"]
    ],
    "Cold": [
        ["Monday", "Ginger tea + Toast | Hot soup | Khichdi"],
        ["Tuesday", "Eggs + Lemon tea | Chicken soup | Rice + Veg curry"],
        ["Wednesday", "Warm porridge | Garlic soup | Steamed veggies"],
        ["Thursday", "Honey Toast | Veggie broth | Dal + Rice"],
        ["Friday", "Boiled eggs | Mushroom soup | Turmeric rice"],
        ["Saturday", "Orange juice | Corn soup | Boiled veg + Chicken"],
        ["Sunday", "Herbal tea | Bone broth | Light khichdi"]
    ],
    "Typhoid": [
        ["Monday", "Rice porridge | Boiled moong dal | Coconut water"],
        ["Tuesday", "White bread | Mashed potatoes | Apple sauce"],
        ["Wednesday", "Soft boiled rice | Vegetable broth | Herbal tea"],
        ["Thursday", "Bananas + Honey | Stewed carrots | Steamed papaya"],
        ["Friday", "Light Khichdi | Curd | Fresh fruit juice"],
        ["Saturday", "Honey water | Vegetable puree | Boiled rice"],
        ["Sunday", "Soft oats | Clear lentil soup | Custard"]
    ],
    "Malaria": [
        ["Monday", "Rice water | Steamed carrots | Coconut water"],
        ["Tuesday", "Soft papaya | Moong dal khichdi | Orange juice"],
        ["Wednesday", "Boiled eggs | Vegetable soup | Mashed potato"],
        ["Thursday", "Oatmeal | Dalia | Herbal tea"],
        ["Friday", "Banana | Stewed apple | Boiled rice"],
        ["Saturday", "Toast with honey | Clear broth | Steamed gourd"],
        ["Sunday", "Rice porridge | Moong dal soup | Curd rice"]
    ],
    "Diabetes": [
        ["Monday", "Steel-cut oats | Quinoa salad | Grilled chicken"],
        ["Tuesday", "Moong dal chilla | Sprouts salad | Baked fish"],
        ["Wednesday", "Greek yogurt | Vegetable Dalia | Brown rice + Dal"],
        ["Thursday", "Boiled eggs | Chickpea salad | Roasted tofu"],
        ["Friday", "Chia pudding | Methi Paratha | Grilled paneer"],
        ["Saturday", "Oat bran | Cucumber salad | Brown rice"],
        ["Sunday", "Fruit bowl | Nut salad | Steamed sprouts"]
    ],
    "Hypertension": [
        ["Monday", "Banana + Oats | Beetroot salad | Baked salmon"],
        ["Tuesday", "Walnuts + Skim milk | Quinoa veg pilaf | Low-salt dal"],
        ["Wednesday", "Flaxseed smoothie | Watermelon salad | Garlic chicken"],
        ["Thursday", "Whole grain toast | Steamed broccoli | Boiled pulses"],
        ["Friday", "Low-fat curd | Celery juice | Baked sweet potato"],
        ["Saturday", "Berries bowl | Roasted nuts | Soya chunks curry"],
        ["Sunday", "Apple + Almonds | Pomegranate salad | Steamed fish"]
    ],
    "Dengue": [
        ["Monday", "Papaya leaf juice | Porridge | Coconut water"],
        ["Tuesday", "Pomegranate juice | Vegetable soup | Khichdi"],
        ["Wednesday", "Boiled egg | Clear broth | Mashed apple"],
        ["Thursday", "Oatmeal | Herbal tea | Steamed vegetables"],
        ["Friday", "Kiwi fruit | Lentil soup | Boiled rice"],
        ["Saturday", "Milk + Turmeric | Stewed fruit | Vegetable dahlia"],
        ["Sunday", "Orange juice | Chicken broth | Curd rice"]
    ],
    "Jaundice": [
        ["Monday", "Sugarcane juice | Boiled rice | Radish soup"],
        ["Tuesday", "Coconut water | Steamed papaya | Curd rice"],
        ["Wednesday", "Barley water | Boiled carrots | Moong dal soup"],
        ["Thursday", "Fresh fruit juice | Mashed banana | Soft rice"],
        ["Friday", "Lemon water | Gourd curry | Wheat porridge"],
        ["Saturday", "Watermelon | Vegetable broth | Boiled pulses"],
        ["Sunday", "Apple juice | Steamed gourd | Rice water"]
    ],
    "Anemia": [
        ["Monday", "Spinach smoothie | Beetroot salad | Iron cereals"],
        ["Tuesday", "Pomegranate | Red meat/Lentils | Dates + Walnuts"],
        ["Wednesday", "Eggs | Chickpea curry | Jaggery + Peanuts"],
        ["Thursday", "Sesame seeds | Fish curry | Broccoli + Quinoa"],
        ["Friday", "Oatmeal with raisins | Kidney beans | Soya chunks"],
        ["Saturday", "Dried apricots | Spinach dal | Grilled chicken"],
        ["Sunday", "Peanut butter toast | Tofu salad | Pumpkin seeds"]
    ],
    "Sepsis": [
        ["Monday", "High-protein broth | Steamed carrots | Coconut water"],
        ["Tuesday", "Greek yogurt | Chicken soup | Mashed potatoes"],
        ["Wednesday", "Oatmeal with honey | Pureed lentils | Herbal tea"],
        ["Thursday", "Soft scrambled eggs | Vegetable broth | Apple sauce"],
        ["Friday", "Smoothie (low sugar) | Chicken congee | Steamed squash"],
        ["Saturday", "Protein shake | Tomato soup | Soft rice"],
        ["Sunday", "Bone broth | Mashed banana | Custard"]
    ],
    "Laryngitis": [
        ["Monday", "Warm honey water | Mashed banana | Ginger tea"],
        ["Tuesday", "Warm vegetable broth | Soft boiled eggs | Oatmeal"],
        ["Wednesday", "Herbal tea | Chicken soup | Yogurt"],
        ["Thursday", "Steamed carrots | Pumpkin puree | Warm milk + Turmeric"],
        ["Friday", "Baked sweet potato | Soft rice | Fruit smoothie"],
        ["Saturday", "Scrambled eggs | Pureed lentils | Honey on toast"],
        ["Sunday", "Warm water with lemon | Vegetable stew | Soft pudding"]
    ],
    "Pneumonia": [
        ["Monday", "Warm milk + Turmeric | Garlic soup | Khichdi"],
        ["Tuesday", "Oatmeal | Chicken broth | Boiled egg"],
        ["Wednesday", "Ginger tea | Steamed veggies | Brown rice"],
        ["Thursday", "Honey water | Lentil soup | Mashed potatoes"],
        ["Friday", "Smoothie | Vegetable stew | Herbal tea"],
        ["Saturday", "Fruit salad | Clear broth | Steamed fish"],
        ["Sunday", "Porridge | Tomato soup | Soft rice"]
    ],
    "Asthma": [
        ["Monday", "Apple | Spinach salad | Salmon + Broccoli"],
        ["Tuesday", "Nuts mix | Garlic stir-fry | Turmeric milk"],
        ["Wednesday", "Orange juice | Quinoa + Veggies | Flaxseeds"],
        ["Thursday", "Avocado toast | Ginger tea | Roasted seeds"],
        ["Friday", "Berries | Beans curry | Steamed sprouts"],
        ["Saturday", "Greek yogurt | Vegetable soup | Green tea"],
        ["Sunday", "Banana | Mashed avocado | Grilled veggies"]
    ],
    "Arthritis": [
        ["Monday", "Walnuts + Oats | Ginger tea | Salmon"],
        ["Tuesday", "Berries | Turmeric milk | Spinach + Garlic"],
        ["Wednesday", "Olive oil salad | Broccoli soup | Soybeans"],
        ["Thursday", "Green tea | Tart cherries | Roasted nuts"],
        ["Friday", "Whole grains | Chia seeds | Beans + Lentils"],
        ["Saturday", "Fruit bowl | Pineapple juice | Steamed kale"],
        ["Sunday", "Almonds | Garlic veggies | Pumpkin seeds"]
    ],
    "Obesity": [
        ["Monday", "Lemon water | Green salad | Grilled chicken"],
        ["Tuesday", "Oatmeal | Sprouts | Clear vegetable soup"],
        ["Wednesday", "Green tea | Boiled pulses | Cucumber salad"],
        ["Thursday", "Apple | Quinoa | Steamed fish"],
        ["Friday", "Buttermilk | Papaya | Roasted makhana"],
        ["Saturday", "Detox juice | Dal + Brown rice | Nut mix"],
        ["Sunday", "Grapefruit | Soya chunks | Vegetable broth"]
    ],
    "Cholesterol": [
        ["Monday", "Oat bran | Almonds | Garlic stir-fry"],
        ["Tuesday", "Avocado | Olive oil salad | Fatty fish"],
        ["Wednesday", "Apples | Soy protein | Flaxseeds"],
        ["Thursday", "Walnuts | Barley water | Dark chocolate"],
        ["Friday", "Legumes | Spinach | Green tea"],
        ["Saturday", "Whole grains | Pears | Steamed broccoli"],
        ["Sunday", "Citrus fruits | Tofu curry | Roasted seeds"]
    ],
    "Acidity": [
        ["Monday", "Cold milk | Banana | Watermelon juice"],
        ["Tuesday", "Coconut water | Oatmeal | Ginger water"],
        ["Wednesday", "Cucumber | Fennel tea | Boiled rice"],
        ["Thursday", "Papaya | Aloe vera juice | Soft dahlia"],
        ["Friday", "Curd rice | Almonds | Melon salad"],
        ["Saturday", "Buttermilk | Boiled veg | Herbal tea"],
        ["Sunday", "Apple | Steamed pumpkin | Rice water"]
    ],
    "Bronchitis": [
        ["Monday", "Warm Ginger tea | Garlic-infused soup | Steamed veggies"],
        ["Tuesday", "Honey Lemon water | Chicken soup | Brown rice"],
        ["Wednesday", "Hot Oatmeal | Clear veg broth | Boiled fish"],
        ["Thursday", "Herbal tea | Lentil soup | Baked potato"],
        ["Friday", "Warm milk | Mushroom soup | Turmeric rice"],
        ["Saturday", "Fruit salad | Bone broth | Steamed chicken"],
        ["Sunday", "Warm water | Vegetable stew | Soft dahlia"]
    ],
    "Tuberculosis": [
        ["Monday", "High-protein milk | Egg curry | Brown rice"],
        ["Tuesday", "Peanut butter toast | Chicken stew | Lentils"],
        ["Wednesday", "Greek yogurt | Beef/Soya broth | Steamed veggies"],
        ["Thursday", "Boiled eggs | Fish curry | Quinoa"],
        ["Friday", "Cheese omelet | Mutton soup | Boiled pulses"],
        ["Saturday", "Nut mix | Chicken soup | Paneer curry"],
        ["Sunday", "Oatmeal with nuts | Dal Tadka | Grilled chicken"]
    ],
    "Hypothyroidism": [
        ["Monday", "Brazil nuts | Grilled fish | Spinach (cooked)"],
        ["Tuesday", "Boiled eggs | Seaweed salad | Brown rice"],
        ["Wednesday", "Greek yogurt | Chicken stir-fry | Quinoa"],
        ["Thursday", "Walnuts | Lentil soup | Steamed sprouts"],
        ["Friday", "Chia pudding | Baked salmon | Roasted veggies"],
        ["Saturday", "Berry bowl | Tofu curry | Boiled pulses"],
        ["Sunday", "Almonds | Garlic chicken | Steamed beans"]
    ],
    "Severe Infection": [
        ["Monday", "Turmeric milk | Garlic-infused broth | Scrambled eggs"],
        ["Tuesday", "Orange juice | Chicken stew | Spinach & Lentils"],
        ["Wednesday", "Greek yogurt | Steamed fish | Mashed sweet potato"],
        ["Thursday", "Berry smoothie | Beef or Soya broth | Brown rice"],
        ["Friday", "Honey Ginger tea | Vegetable soup | Grilled chicken"],
        ["Saturday", "Boiled eggs | Bone broth | Steamed broccoli"],
        ["Sunday", "Protein shake | Chicken noodle soup | Curd rice"]
    ],
    "Food Poisoning": [
        ["Monday", "ORS Solution | Clear vegetable broth | Rice water"],
        ["Tuesday", "Banana | White toast (no butter) | Coconut water"],
        ["Wednesday", "Applesauce | Boiled white rice | Curd (probiotics)"],
        ["Thursday", "Soft boiled carrots | Steamed potato | Herbal tea"],
        ["Friday", "Vegetable khichdi | Poached egg | Mashed banana"],
        ["Saturday", "Chicken soup (no fat) | Soft dahlia | Yogurt"],
        ["Sunday", "Baked fish | Steamed squash | Rice porridge"]
    ],
    "Hyperthyroidism": [
        ["Monday", "Berries bowl | Broccoli soup | Grilled tofu"],
        ["Tuesday", "Oatmeal | Cauliflower curry | Lentils"],
        ["Wednesday", "Fruit smoothie | Bamboo shoots | Brown rice"],
        ["Thursday", "Honey toast | Kale salad | Baked chicken"],
        ["Friday", "Strawberry yogurt | Cabbage stir-fry | Fish"],
        ["Saturday", "Apple | Steamed sprouts | Boiled potato"],
        ["Sunday", "Melon salad | Veggie soup | Soya chunks"]
    ],
    "GERD": [
        ["Monday", "Oatmeal | Melon salad | Grilled chicken"],
        ["Tuesday", "Banana | Brown rice | Steamed fish"],
        ["Wednesday", "Ginger tea | Poached eggs | Mashed potato"],
        ["Thursday", "Pear | Fennel soup | Boiled lentils"],
        ["Friday", "Whole grain toast | Aloe juice | Veggie stew"],
        ["Saturday", "Chamomile tea | Steamed gourd | Soft rice"],
        ["Sunday", "Papaya | Baked chicken | Zucchini noodles"]
    ],
    "Constipation": [
        ["Monday", "Prune juice | Flaxseed oats | Spinach dal"],
        ["Tuesday", "Papaya | Brown rice | Broccoli stir-fry"],
        ["Wednesday", "Chia pudding | Lentil soup | Sweet potato"],
        ["Thursday", "Apple with skin | Quinoa | Steamed beans"],
        ["Friday", "Pear | Whole grain pasta | Leafy greens"],
        ["Saturday", "Berries | Vegetable dahlia | Chickpeas"],
        ["Sunday", "Figs | Popcorn (no salt) | Green salad"]
    ],
    "Diarrhea": [
        ["Monday", "Banana | White rice | Dry toast"],
        ["Tuesday", "Applesauce | Boiled potato | Clear broth"],
        ["Wednesday", "Coconut water | Curd rice | Salted crackers"],
        ["Thursday", "Banana | Soft dahlia | Herbal tea"],
        ["Friday", "Steamed carrots | Rice water | White bread"],
        ["Saturday", "Yogurt | Boiled chicken | Soft oats"],
        ["Sunday", "Banana | Apple puree | Clear veg soup"]
    ],
    "Gastritis": [
        ["Monday", "Chamomile tea | Apple slices | Steamed fish"],
        ["Tuesday", "Oatmeal | Carrot puree | Boiled rice"],
        ["Wednesday", "Coconut water | Zucchini soup | Chicken"],
        ["Thursday", "Banana | Soft pasta | Mashed potato"],
        ["Friday", "Yogurt | Veggie broth | Steamed tofu"],
        ["Saturday", "Pear | Boiled dal | Soft toast"],
        ["Sunday", "Honey water | Pumpkin soup | Brown rice"]
    ],
    "Fatty Liver": [
        ["Monday", "Black coffee | Oatmeal | Tofu salad"],
        ["Tuesday", "Green tea | Baked salmon | Broccoli"],
        ["Wednesday", "Walnuts | Garlic chicken | Quinoa"],
        ["Thursday", "Apple | Lentil soup | Spinach stir-fry"],
        ["Friday", "Sunflower seeds | Steamed fish | Soya chunks"],
        ["Saturday", "Avocado toast | Chickpea salad | Veggies"],
        ["Sunday", "Berry bowl | Brown rice | Grilled chicken"]
    ],
    "Kidney Stone": [
        ["Monday", "Lemon water | Watermelon | Brown rice"],
        ["Tuesday", "Basil tea | Cucumber salad | Steamed fish"],
        ["Wednesday", "Coconut water | Celery juice | Quinoa"],
        ["Thursday", "Orange | Kidney bean soup | Veggie stew"],
        ["Friday", "Lemon water | Grapes | Boiled pulses"],
        ["Saturday", "Apple | Bell pepper stir-fry | Rice"],
        ["Sunday", "Watermelon juice | Steamed gourd | Chicken"]
    ],
    "UTI": [
        ["Monday", "Cranberry juice | Blueberry bowl | Yogurt"],
        ["Tuesday", "Water | Spinach salad | Grilled chicken"],
        ["Wednesday", "Vitamin C fruit | Garlic soup | Brown rice"],
        ["Thursday", "Water | Broccoli stir-fry | Baked fish"],
        ["Friday", "Cranberry juice | Quinoa | Steamed veggies"],
        ["Saturday", "Water | Lentil soup | Soya chunks"],
        ["Sunday", "Herbal tea | Curd rice | Grilled turkey"]
    ],
    "Migraine": [
        ["Monday", "Magnesium oats | Almonds | Salmon"],
        ["Tuesday", "Dark chocolate | Spinach salad | Quinoa"],
        ["Wednesday", "Ginger tea | Avocado | Baked chicken"],
        ["Thursday", "Walnuts | Pumpkin seeds | Steamed fish"],
        ["Friday", "Flaxseeds | Banana | Brown rice"],
        ["Saturday", "Yogurt | Chia seeds | Veggie soup"],
        ["Sunday", "Chamomile tea | Cashews | Grilled steak"]
    ],
    "Hepatitis": [
        ["Monday", "Sugarcane juice | Boiled rice | Curd"],
        ["Tuesday", "Papaya | Vegetable broth | Soft dahlia"],
        ["Wednesday", "Coconut water | Mashed banana | Lentils"],
        ["Thursday", "Honey water | Steamed gourd | White rice"],
        ["Friday", "Fresh juice | Soft oats | Boiled potato"],
        ["Saturday", "Watermelon | Veggie puree | Soft toast"],
        ["Sunday", "Apple juice | Rice porridge | Custard"]
    ],
    "Tension Headache": [
        ["Monday", "Magnesium-rich oats | Almonds | Grilled Salmon"],
        ["Tuesday", "Spinach salad | Walnuts | Quinoa with veggies"],
        ["Wednesday", "Ginger tea | Avocado toast | Baked chicken"],
        ["Thursday", "Pumpkin seeds | Bananas | Steamed fish"],
        ["Friday", "Flaxseed smoothie | Yogurt | Brown rice + Dal"],
        ["Saturday", "Chamomile tea | Dark chocolate (70%) | Leafy greens"],
        ["Sunday", "Hydration focus | Watermelon | Roasted seeds"]
    ],

    "Allergic Rhinitis": [
        ["Monday", "Turmeric milk | Pineapple slices | Ginger-garlic soup"],
        ["Tuesday", "Green tea | Citrus fruits | Steamed broccoli"],
        ["Wednesday", "Local honey on toast | Apple | Fatty fish"],
        ["Thursday", "Onion & garlic stir-fry | Berries | Lentil soup"],
        ["Friday", "Walnuts | Flaxseeds | Chicken with rosemary"],
        ["Saturday", "Probiotic yogurt | Bell peppers | Brown rice"],
        ["Sunday", "Warm water with lemon | Kiwi | Roasted veggies"]
    ],

    "Muscle Strain": [
        ["Monday", "High-protein shake | Tart cherry juice | Grilled chicken"],
        ["Tuesday", "Greek yogurt | Blueberries | Steamed Salmon"],
        ["Wednesday", "Cottage cheese | Bananas (potassium) | Quinoa"],
        ["Thursday", "Boiled eggs | Spinach | Sweet potato"],
        ["Friday", "Almonds | Avocado | Lean beef or lentils"],
        ["Saturday", "Turmeric latte | Papaya | Roasted chickpeas"],
        ["Sunday", "Whey or soy protein | Mixed nuts | Steamed broccoli"]
    ],

    "Covid-19": [
        ["Monday", "Warm chicken soup | Orange juice | Soft dahlia"],
        ["Tuesday", "Ginger tea with honey | Boiled eggs | Khichdi"],
        ["Wednesday", "Vitamin C smoothie | Steamed fish | Mashed potato"],
        ["Thursday", "Turmeric milk | Lentil soup | White rice + Curd"],
        ["Friday", "Coconut water | Banana | Stewed apples"],
        ["Saturday", "Herbal broth | Garlic toast | Steamed veggies"],
        ["Sunday", "Protein shake | Mixed fruit bowl | Chicken stew"]
    ],

    "Psoriasis": [
        ["Monday", "Salmon (Omega-3) | Flaxseeds | Spinach salad"],
        ["Tuesday", "Walnuts | Blueberries | Grilled tofu"],
        ["Wednesday", "Olive oil dressing | Chia pudding | Steamed kale"],
        ["Thursday", "Almonds | Turmeric veggies | Baked trout"],
        ["Friday", "Avocado | Pumpkin seeds | Brown rice + Lentils"],
        ["Saturday", "Colorful bell peppers | Garlic chicken | Seaweed"],
        ["Sunday", "Sweet potato | Berry smoothie | Roasted nuts"]
    ],

    "Eczema": [
        ["Monday", "Quinoa | Blueberries (antioxidants) | Steamed fish"],
        ["Tuesday", "Oatmeal | Pear | Baked chicken (no skin)"],
        ["Wednesday", "Probiotic yogurt | Flaxseeds | Stir-fry veggies"],
        ["Thursday", "Papaya | Miso soup | Brown rice"],
        ["Friday", "Almonds | Celery juice | Grilled turkey"],
        ["Saturday", "Apples | Green beans | Lentil stew"],
        ["Sunday", "Cucumber salad | Salmon | Sunflower seeds"]
    ],

    "Insomnia": [
        ["Monday", "Chamomile tea | Warm milk | Tart cherries"],
        ["Tuesday", "Almonds | Bananas (magnesium) | Oatmeal"],
        ["Wednesday", "Walnuts | Kiwi fruit | Boiled eggs"],
        ["Thursday", "Turkey breast (tryptophan) | Sweet potato | Spinach"],
        ["Friday", "Pumpkin seeds | Hummus | Whole grain crackers"],
        ["Saturday", "Herbal tea | Yogurt | Lettuce salad"],
        ["Sunday", "Steamed fish | Brown rice | Warm honey water"]
    ]
}

general_diet = [

    ["General Recommendation", "Balanced nutritional intake"],

    ["Hydration", "Drink 3-4 liters of water daily"],

    ["Avoid", "Oily, spicy, and processed food"],

    ["Consult", "Follow professional medical advice"]

]



# -------------------- DATABASE INIT --------------------

def init_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE, password TEXT, name TEXT, age INTEGER

        )

    """)

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS patients (

            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,

            fever INTEGER, cough INTEGER, headache INTEGER,

            fatigue INTEGER, sore_throat INTEGER, body_pain INTEGER,

            shortness_of_breath INTEGER, nausea INTEGER,

            prediction TEXT, solution TEXT,

            FOREIGN KEY(user_id) REFERENCES users(id)

        )

    """)

    conn.commit()

    conn.close()



init_db()



# -------------------- ROUTES --------------------



@app.route('/')

def index():

    return render_template("index.html")



@app.route('/about')

def about():

    return render_template("about.html")



@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user_id'] = user[0]

            return redirect(url_for('user_info'))

        flash("Invalid login details")

    return render_template("login.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            # Insert the new user
            cursor.execute("INSERT INTO users (username, password, age) VALUES (?, ?, ?)", (username, password, age))
            conn.commit()
            
            # Fetch the new ID to start the session
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if user:
                session['user_id'] = user[0] # Log them in automatically
                return redirect(url_for('predict')) # Direct to Symptom Assessment
            
        except sqlite3.IntegrityError:
            flash("Username already exists")
        finally:
            conn.close()
            
    return render_template("register.html")



@app.route('/user_info', methods=['GET', 'POST'])

def user_info():

    if 'user_id' not in session: return redirect(url_for('login'))

    if request.method == "POST":

        name = request.form.get('name')

        age = request.form.get('age')

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (name, age, session['user_id']))

        conn.commit()

        conn.close()

        return redirect(url_for('predict'))

    return render_template("user_info.html")

@app.route('/predict', methods=['GET', 'POST'])

def predict():

    if 'user_id' not in session:

        return redirect(url_for('login'))



    if request.method == "POST":

        symptoms = [

            'fever', 'cough', 'headache', 'fatigue',

            'sore_throat', 'body_pain',

            'shortness_of_breath', 'nausea'

        ]



        data = [int(request.form[s]) for s in symptoms]



        # Get prediction

        prediction_result = model.predict([data])[0]



        # Convert to clean string format

        prediction_clean = str(prediction_result).strip().title()

        # Get solution safely

        solution = solutions.get(prediction_clean, "Consult a specialist.")



        # --- SMART DIET LOOKUP (FIXED) ---

        prediction_clean = str(prediction_result).strip().title()

        

        # Start with general diet as default

        diet = general_diet 



        # Check if any disease key exists inside the prediction string

        # This matches "Severe Flu" to the "Flu" plan

        for disease_key in diet_plans.keys():

            if disease_key.lower() in prediction_clean.lower():

                diet = diet_plans[disease_key]

                break



        # Save to database

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO patients 

            (user_id, fever, cough, headache, fatigue, sore_throat, body_pain, shortness_of_breath, nausea, prediction, solution)

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (session['user_id'], *data, prediction_clean, solution))



        conn.commit()

        conn.close()



        return render_template(

            "result.html",

            prediction=prediction_clean,

            solution=solution,

            diet=diet

        )
    



    return render_template("predict.html")

@app.route('/history')

def history():

    if 'user_id' not in session: return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT prediction, solution FROM patients WHERE user_id=? ORDER BY id DESC", (session['user_id'],))

    rows = cursor.fetchall()

    conn.close()

   

    history_data = []
    for r in rows:
        p_name = str(r[0]).strip().title()
        
        # Apply the same smart matching logic here
        assigned_diet = general_diet
        for disease_key in diet_plans.keys():
            if disease_key.lower() in p_name.lower():
                assigned_diet = diet_plans[disease_key]
                break

        history_data.append({
            "prediction": r[0],
            "solution": r[1],
            "diet": assigned_diet
        })

    return render_template("history.html", history=history_data)



@app.route('/logout')

def logout():

    session.clear()

    return redirect(url_for('index'))


if __name__ == "__main__":

    app.run(debug=True)