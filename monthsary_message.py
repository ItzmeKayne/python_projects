"""Interactive monthsary message generator

Usage:
  - run without args for interactive prompts
  - or pass CLI args: --name NAME --months N --tone {romantic,playful} [--save PATH]

This script was made to replace the previous static-series of print() calls.
"""

import argparse
import textwrap
import sys
from datetime import datetime


DEFAULT_TEMPLATES = {
	"romantic": [
		"Hii Babyyy! Can you believe it's already been {months} months? Time flies when I'm with you.",
		"You make my life complete and I am so grateful to have you.",
		"I love you more than words can express. Happy monthsary, {name}! <3",
		"You are my soulmate and my best friend. I love you endlessly!",
	],
	"playful": [
		"Haiii Babyy! it's been 2 months already? Time flies, nga talaga HAHAHAHA, wow we made growth with each other:3, I, didn't expect that it's already been our monthsary again AHAHAHAHHA, when i made you my first gift, letter you cried:3, and you know what i feel that when i saw you cried because of the letter i made for you, i felt that i made you happy and you appreciate it:3, i almost cried that day also, i was thankful to have you in my life babyy:3, i love you so much babyy, more than anything in this world:3",
		"Im so lucky to have you as my partner in crime. Here's to many more months of adventures together, and more silly moments with just the two of us:3, i still remember the day when we first did it together:3, it was so funny and awkward at the same time AHAHAHAHHA, but i enjoyed it so much babyy:3, i can't wait to make more memories with you babyy:3, i love you so much babyy:3",	
		"As of now while i was writing this message the date is Nov 9, 2025 3am as of now:3, because you were asleep right now babyy and i can't sleep, i was thinking of what to do, i just wanna start early on our monthsary message:3, i'll continue it till it's our monthsary, i'll put a date and time when i wrote what's our happenings:3. i'll do it every midnight when you were asleep and made it into a diary. maybe next month i'll start again at exactly when our monthsary:3, iloveyouuu mwuahhh"
		"Nov 9, 10:17 pm. as i write this i message, the cause why im so drained or i can't understand what Im feeling right now is maybe because i didn't get what i want:), maybe a photo was enough. but i didn't say it:<, it's because i keep hinting that i was sad, nang lood ko ato nga time kay nang unsent ka HAHAHAHA, maybe mali sad nako kay wako kakita:<, it's oaky po don't blame yourself because i didn't saw it:), maybe i'll be lucky next time:). maybe tommorow i won't be sad anymore:3, it's jsut a phase, im sorry for today that i made myself sad:) and made the day not proactive:), i'm sorry po babyy, iloveyousomuchh pangga nako:3"
		"Nov 10, 1:36 am. i can't sleep, babyy:3, imissyousomuchh my palangga, i miss you feys, kisses, hugs, at higit sa lahat ang atoang midnight things:3, im really sorry po kanina sa behaviour nako, i didn't mean to make you feel bad po or anything, im sorry pangga nako, mwuahhhh, iloveyouuuu"
		"Nov 11, 2:30 am. Woahhhh, my day was so special kaninang umaga po, you made my day happy and brighter:3, that was unexpected to be honest abi nakog imo japun edelete to T^T, nganong naa man gd koy klase ato ba, tsts, daghan kaykog wala naktiaaa HAHAHAHAHAHAH, joking aside po i was genuinely happy po when i saw it:3, ganiha dili jud ko makapakali sigi kog lakaw lakaw while ga ngisi HAHAHAHAHAHAHHA, tas akoang ano kay ga hard na hehe:3, gusto najud ko kaulion ato tong permi na ga send si babyy, ang mali sad nako kay na view nakong isa pero wakoy load lalaaaa HAHAHAHAHAHHAHA, pero bitaw babyy i was really happy, you starting to change for me po, iloveyouu so muchhh my babyyy:3"
}


def build_message(name: str, months: int, tone: str):
	tone = tone if tone in DEFAULT_TEMPLATES else "romantic"
	lines = [t.format(name=name, months=months) for t in DEFAULT_TEMPLATES[tone]]
	header = f"=== {months} months with {name} — {datetime.now().strftime('%Y-%m-%d')} ==="
	return "\n".join([header, ""] + [textwrap.fill(l, width=72) for l in lines])


def parse_args(argv):
	p = argparse.ArgumentParser(description="Monthsary message generator")
	p.add_argument("--name", help="Recipient name", default=None)
	p.add_argument("--months", type=int, help="Number of months", default=None)
	p.add_argument("--tone", choices=list(DEFAULT_TEMPLATES.keys()), help="Tone of messages",
				   default="romantic")
	p.add_argument("--save", help="Path to save the message (optional)")
	return p.parse_args(argv)


def interactive_prompt():
	try:
		name = input("Enter recipient name (default: Babyy): ").strip() or "Babyy"
		months_raw = input("How many months? (default: 2): ").strip() or "2"
		months = int(months_raw)
		print("Choose tone:")
		for i, t in enumerate(DEFAULT_TEMPLATES.keys(), start=1):
			print(f"  {i}. {t}")
		tone_choice = input("Tone number (default 1): ").strip() or "1"
		tone_list = list(DEFAULT_TEMPLATES.keys())
		tone = tone_list[int(tone_choice) - 1]
		save = input("Save to file? (y/N): ").strip().lower() == "y"
		save_path = None
		if save:
			save_path = input("Enter path to save (e.g. monthsary.txt): ").strip() or None
		return name, months, tone, save_path
	except (KeyboardInterrupt, EOFError):
		print("\nAborted by user.")
		sys.exit(1)


def main(argv=None):
	args = parse_args(argv or [])
	if args.name is None or args.months is None:
		name, months, tone, save_path = interactive_prompt()
	else:
		name = args.name
		months = args.months
		tone = args.tone
		save_path = args.save

	message = build_message(name, months, tone)
	print(message)

	if save_path:
		try:
			with open(save_path, "w", encoding="utf-8") as f:
				f.write(message + "\n")
			print(f"Message saved to {save_path}")
		except Exception as e:
			print(f"Failed to save file: {e}")


if __name__ == "__main__":
	main(sys.argv[1:])