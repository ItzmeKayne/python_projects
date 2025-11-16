from flask import Flask, render_template, request, url_for
import textwrap
from datetime import datetime
import os
import glob
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_gallery_images(tone=None):
    # Get all images from the uploads folder
    upload_path = os.path.join(app.root_path, UPLOAD_FOLDER)
    print(f"Looking for images in: {upload_path}")  # Debug log
    
    # Get all image files (jpg, jpeg, png, gif)
    images = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
        pattern = os.path.join(upload_path, ext)
        print(f"Searching for pattern: {pattern}")  # Debug log
        all_images = glob.glob(pattern)
        print(f"Found {len(all_images)} images for {ext}")  # Debug log
        
        if tone:
            # Filter images by tone prefix (r_ for romantic, p_ for playful)
            prefix = 'r_' if tone == 'romantic' else 'p_'
            all_images = [img for img in all_images if os.path.basename(img).startswith(prefix)]
            print(f"After filtering for {prefix}: {len(all_images)} images")  # Debug log
        
        images.extend(all_images)
    
    result = sorted([os.path.basename(img) for img in images])
    print(f"Final images for tone {tone}: {result}")  # Debug log
    return result

DEFAULT_TEMPLATES = {
    "romantic": [
        "Hii {name}! Can you believe it's already been {months} months? Time flies when I'm with you.",
        "You make my life complete and I am so grateful to have you.",
        "I love you more than words can express. Happy monthsary, {name}! <3",
        "You are my soulmate and my best friend. I love you endlessly!",
    ],
    "playful": [
        """Haiii Babyy! it's been 2 months already? Time flies, nga talaga HAHAHAHA, wow we made growth with each other:3, I, didn't expect that it's already been our monthsary again AHAHAHAHHA, when i made you my first gift, letter you cried:3, and you know what i feel that when i saw you cried because of the letter i made for you, i felt that i made you happy and you appreciate it:3, i almost cried that day also, i was thankful to have you in my life babyy:3, i love you so much babyy, more than anything in this world:3""",
		"""Im so lucky to have you as my partner in crime. Here's to many more months of adventures together, and more silly moments with just the two of us:3, i still remember the day when we first did it together:3, it was so funny and awkward at the same time AHAHAHAHHA, but i enjoyed it so much babyy:3, i can't wait to make more memories with you babyy:3, i love you so much babyy:3""",	
		"""As of now while i was writing this message the date is Nov 9, 2025 3am as of now:3, because you were asleep right now babyy and i can't sleep, i was thinking of what to do, i just wanna start early on our monthsary message:3, i'll continue it till it's our monthsary, i'll put a date and time when i wrote what's our happenings:3. i'll do it every midnight when you were asleep and made it into a diary. maybe next month i'll start again at exactly when our monthsary:3, iloveyouuu mwuahhh""",
		"""Nov 9, 10:17 pm. as i write this i message, the cause why im so drained or i can't understand what Im feeling right now is maybe because i didn't get what i want:), maybe a photo was enough. but i didn't say it:<, it's because i keep hinting that i was sad, nang lood ko ato nga time kay nang unsent ka HAHAHAHA, maybe mali sad nako kay wako kakita:<, it's oaky po don't blame yourself because i didn't saw it:), maybe i'll be lucky next time:). maybe tommorow i won't be sad anymore:3, it's jsut a phase, im sorry for today that i made myself sad:) and made the day not proactive:), i'm sorry po babyy, iloveyousomuchh pangga nako:3""",
		"""Nov 10, 1:36 am. i can't sleep, babyy:3, imissyousomuchh my palangga, i miss you feys, kisses, hugs, at higit sa lahat ang atoang midnight things:3, im really sorry po kanina sa behaviour nako, i didn't mean to make you feel bad po or anything, im sorry pangga nako, mwuahhhh, iloveyouuuu""",
		"""Nov 11, 2:30 am. Woahhhh, my day was so special kaninang umaga po, you made my day happy and brighter:3, that was unexpected to be honest abi nakog imo japun edelete to T^T, nganong naa man gd koy klase ato ba, tsts, daghan kaykog wala naktiaaa HAHAHAHAHAHAH, joking aside po i was genuinely happy po when i saw it:3, ganiha dili jud ko makapakali sigi kog lakaw lakaw while ga ngisi HAHAHAHAHAHAHHA, tas akoang ano kay ga hard na hehe:3, gusto najud ko kaulion ato tong permi na ga send si babyy, ang mali sad nako kay na view nakong isa pero wakoy load lalaaaa HAHAHAHAHAHHAHA, pero bitaw babyy i was really happy, you starting to change for me po, iloveyouu so muchhh my babyyy:3""",
		"""Nov 14, 1:22 pm. Sorry po babyy i skipp a day i havent have much time to play sa computer po AHHAHAHAHAHA, i forget easily of what happend the other day in Nov 12 T^T, but i know what happend yesterday, i was so happy po that i saw you laughing hard and spending time with your friend po despite na dili kaayo ka hilig mo laag po. it was also my best time seeing you smile and laughs with them po babyyy and dugay ka na nakauli gabie:>, i was worried po na basig kasab an ka sa imong mother po and gabie nasad kaayo to na time basig niyag matapilok ka while gauli po, tas wala ka kadala sa imuhang eyeglasses po babyy and today naman ga laag ka:3, i want you to enjoy your day po with them, i assure you po you're always be in my mind always po and will love youuu forever:3, enjoy your day po with them babyy, iloveyouuusomuchhhh po babyyy:3 mwuahhhmmwuahhhh""",
		"""Nov 15, 4:40 pm. you we're asleep at this time, you know naman what happen kanina hehehe:3, i was soooo happyyyyy po babyyy of what happend kanina ug kagahapon po HAHAHAHAHAHAH, gina tease rabiya ko ato nimo na time tong nang lakaw pami awa maka balos rapo ko sunod nimo if mang lakaw mo usab nila trish ug hazel, maka ana jud kag "gusto nako mouli huhu" HAHAHAHAHAHAH, awa lang ka hehe, anhd kagabie ato na time kay nanglood ka kay lagi tungod sa imong dinulaan babyy, pero i assura naman po na okayy ra po na ing ato imong dinulaan babyy gina higitan man sad nimo next game po if mag kamali man po ka gina smilelan rapo nako then "bawi po babyy, okay lang po", wala po ko ga blame sa imong dinulaan po babyy, and if ever na ma feel napud nimo babyy na malainan ka sa dinulaan nimo po, pero para nako wala mas ma enjoy pa noon nako babyy so don't be sadd po na tungod sa dinulaan nimo nga napildi po ta ato nga game, naa pamay next game after ato, okay po?. iloveyouuuu so muchhh po babyy:) mwuahhh""",
        """Nov 16, 9:16 pm. as of now babyy im wathcing you play po, your not in the mood today T^T, sorry po if i keep asking you po and annoyed you of that sound poT^T, what happend today po was i attend a birthday celebration a debut of my friend po it was fun that i got to spend time with my friend also, but i always think of you po and missed you, until it end huhuhu, gusto najud ko mouli ato tong naga send napo ka babyy, namiss jud po taka hantud sa mahuman pati sa pag lakaw nako, tas feel pud nako po ato kay wala ka sa moodT^T, tas sigi rakog pangutana anxious po jud kayko ato huhuT^T, but after naman ato nahuman ang celebration po is i was happy hehe and nag send kaT^T, i tried my best sad po nga mag send daghan man gud og tao lisud mag pic bantug na ngitngit, and after nako makauli kay nag call dayn ta hehe:3, iloveyouuuuu babyyyy, my pahinga as always. and kagabie po kay ning hilak nasad ka kay naktia nimo ang message T^T tas ning paldo kay ka ato kay naka dungog ka sa akoang tingog hehehe pati kaganiha nga nag call po ta, both ta hehehe:3, ilvoeyouuuusomuchhhh po lovelove nako:3 mwuahhhh""",
        ],
}

def build_message(name: str, months: int, tone: str):
    tone = tone if tone in DEFAULT_TEMPLATES else "romantic"
    lines = [t.format(name=name, months=months) for t in DEFAULT_TEMPLATES[tone]]
    header = f"=== {months} months with {name} — {datetime.now().strftime('%Y-%m-%d')} ==="
    return "\n".join([header, ""] + [textwrap.fill(l, width=72) for l in lines])

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    saved_path = None
    current_tone = 'romantic'
    image_path = None

    if request.method == 'POST':
        name = request.form.get('name', 'Babyy').strip() or 'Babyy'
        months_raw = request.form.get('months', '2').strip() or '2'
        try:
            months = int(months_raw)
        except ValueError:
            months = 2
        tone = request.form.get('tone', 'romantic')
        current_tone = tone
        save = request.form.get('save') == 'on'
        
        # Handle image upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add the appropriate prefix based on tone
                prefix = 'r_' if tone == 'romantic' else 'p_'
                filename = f"{prefix}{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = url_for('static', filename=f'uploads/{filename}')

        message = build_message(name, months, tone)

        if save:
            filename = f"monthsary_{name}_{months}.txt"
            filename = secure_filename(filename)
            saved_path = os.path.abspath(filename)
            try:
                with open(saved_path, 'w', encoding='utf-8') as f:
                    f.write(message + "\n")
            except Exception:
                saved_path = None

    # Get images based on selected tone
    tone_images = get_gallery_images(current_tone)

    return render_template('index.html', 
                       message=message, 
                       saved_path=saved_path,
                       templates=list(DEFAULT_TEMPLATES.keys()), 
                       current_tone=current_tone,
                       gallery_images=tone_images,
                       now=datetime.now())

if __name__ == '__main__':
    # Ensure uploads directory exists
    os.makedirs(os.path.join(app.root_path, UPLOAD_FOLDER), exist_ok=True)
    app.run(debug=True)

DEFAULT_TEMPLATES = {
    # Templates copied from the project's monthsary_message.py (sanitized)
    "romantic": [
        "Hii {name}! Can you believe it's already been {months} months? Time flies when I'm with you.",
        "You make my life complete and I am so grateful to have you.",
        "I love you more than words can express. Happy monthsary, {name}! <3",
        "You are my soulmate and my best friend. I love you endlessly!",
    ],
    "playful": [
        "Haiii Babyy! it's been {months} months already? Time flies, nga talaga HAHAHAHA, wow we made growth with each other:3, I didn't expect that it's already been our monthsary again AHAHAHAHHA, when i made you my first gift, letter you cried:3, and you know what i feel that when i saw you cried because of the letter i made for you, i felt that i made you happy and you appreciate it:3, i almost cried that day also, i was thankful to have you in my life babyy:3, i love you so much babyy, more than anything in this world:3",
        "Im so lucky to have you as my partner in crime. Here's to many more months of adventures together, and more silly moments with just the two of us:3, i still remember the day when we first did it together:3, it was so funny and awkward at the same time AHAHAHAHHA, but i enjoyed it so much babyy:3, i can't wait to make more memories with you babyy:3, i love you so much babyy:3",
        "You make my heart skip a beat and my life so much fun. Happy monthsary. As of now while i was writing this message the date is Nov 9, 2025 3am as of now:3, because you were asleep right now babyy and i can't sleep, i was thinking of what to do, i just wanna start early on our monthsary message:3, i'll continue it till it's our monthsary, i'll put a date and time when i wrote what's our happenings:3. i'll do it every midnight when you were asleep and made it into a diary. maybe next month i'll start again at exactly when our monthsary:3, iloveyouuu mwuahhh",
    ],
}


def build_message(name: str, months: int, tone: str):
    tone = tone if tone in DEFAULT_TEMPLATES else "romantic"
    lines = [t.format(name=name, months=months) for t in DEFAULT_TEMPLATES[tone]]
    header = f"=== {months} months with {name} — {datetime.now().strftime('%Y-%m-%d')} ==="
    return "\n".join([header, ""] + [textwrap.fill(l, width=72) for l in lines])


@app.route('/another', methods=['GET', 'POST'])
def index2():
    message = None
    saved_path = None
    current_tone = 'romantic'
    image_path = None

    # Initialize default tone
    if request.method == 'GET':
        current_tone = 'romantic'  # default tone

    if request.method == 'POST':
        name = request.form.get('name', 'Babyy').strip() or 'Babyy'
        months_raw = request.form.get('months', '2').strip() or '2'
        try:
            months = int(months_raw)
        except ValueError:
            months = 2
        tone = request.form.get('tone', 'romantic')
        # Set default image path based on tone
        if tone in DEFAULT_IMAGES:
            default_image_path = os.path.join(app.root_path, UPLOAD_FOLDER, DEFAULT_IMAGES[tone])
            print(f"Looking for default image at: {default_image_path}")  # Debug log
            if os.path.exists(default_image_path):
                image_path = url_for('static', filename=f'uploads/{DEFAULT_IMAGES[tone]}')
                print(f"Found default image: {image_path}")  # Debug log
            else:
                print(f"Default image not found at {default_image_path}")  # Debug log
        current_tone = tone
        save = request.form.get('save') == 'on'
        
        # Handle image upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = url_for('static', filename=f'uploads/{filename}')

        message = build_message(name, months, tone)

        if save:
            filename = f"monthsary_{name}_{months}.txt"
            # ensure safe filename
            filename = filename.replace(' ', '_')
            saved_path = os.path.abspath(filename)
            try:
                with open(saved_path, 'w', encoding='utf-8') as f:
                    f.write(message + "\n")
            except Exception:
                saved_path = None

    # Get images based on selected tone
    tone_images = get_gallery_images(current_tone) if current_tone else []
    
    return render_template('index.html', 
                           message=message, 
                           saved_path=saved_path,
                           templates=list(DEFAULT_TEMPLATES.keys()), 
                           current_tone=current_tone,
                           gallery_images=tone_images,
                           now=datetime.now(),
                           image_path=image_path if 'image_path' in locals() else None)


if __name__ == '__main__':
    app.run(host='192.168.100.14', port=5000, debug=False)